// Copyright 2016 Google Inc. All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

// The mapper binary performs log->map mapping.
package main

import (
	"context"
	"flag"
	"fmt"
	"time"
	"encoding/json"

	"github.com/golang/glog"
	"github.com/golang/protobuf/ptypes"
	"github.com/golang/protobuf/ptypes/any"
	//"github.com/google/certificate-transparency-go/x509"
	"github.com/google/trillian"
	"github.com/google/trillian/examples/ct/ctmapper"
	"github.com/google/trillian/examples/ct/ctmapper/ctmapperpb"
	"google.golang.org/grpc"

	//pb "github.com/golang/protobuf/proto"
	//ct "github.com/google/certificate-transparency-go"
)

var sourceLog = flag.String("source_log", "", "host:port for the log server")
var mapServer = flag.String("map_server", "", "host:port for the map server")
var mapID = flag.Int("map_id", -1, "Map ID to write to")
var logBatchSize = flag.Int("log_batch_size", 1, "Max number of entries to process at a time from the Log")
var logID = flag.Int("log_id", -1, "Log ID to read from")

// VLDMMapper converts between a Trillian Log and a Trillian Map.
type VLDMMapper struct {
	mapID int64
	vlog  trillian.TrillianLogClient
	vmap  trillian.TrillianMapClient
}

type LeafValue struct {
	IDC string `json:"idc"`
	Requests []string `json:"requests"`
}

func makeGetLeavesByIndexRequest(logID int64, startLeaf, numLeaves int64) *trillian.GetLeavesByIndexRequest {
	leafIndices := make([]int64, 0, numLeaves)

	for l := int64(0); l < numLeaves; l++ {
		leafIndices = append(leafIndices, l+startLeaf)
	}

	return &trillian.GetLeavesByIndexRequest{LogId: logID, LeafIndex: leafIndices}
}

func (m *VLDMMapper) oneMapperRun(ctx context.Context) (bool, error) {
	start := time.Now()
	glog.Info("starting mapping batch")
	getRootReq := &trillian.GetSignedMapRootRequest{MapId: m.mapID}
	getRootResp, err := m.vmap.GetSignedMapRoot(context.Background(), getRootReq)
	if err != nil {
		return false, err
	}

	mapperMetadata := &ctmapperpb.MapperMetadata{}
	if getRootResp.GetMapRoot().Metadata != nil {
		var metadataProto ptypes.DynamicAny
		if err := ptypes.UnmarshalAny(getRootResp.MapRoot.Metadata, &metadataProto); err != nil {
			return false, fmt.Errorf("failed to unmarshal MapRoot.Metadata: %v", err)
		}
		mapperMetadata = metadataProto.Message.(*ctmapperpb.MapperMetadata)
	}

	startEntry := mapperMetadata.HighestFullyCompletedSeq + 1
	endEntry := startEntry + int64(*logBatchSize)

	glog.Infof("Fetching entries [%d, %d] from log", startEntry, endEntry)

	// Get the entries from the log:
	req := makeGetLeavesByIndexRequest(int64(*logID), startEntry, int64(*logBatchSize))
	response, err := m.vlog.GetLeavesByIndex(ctx, req)
	if err != nil {
		return false, err
	}
	if len(response.Leaves) == 0 {
		glog.Info("No entries from log")
		return false, nil
	}

	dat := LeafValue{}
	idcs := make(map[string]*LeafValue)
	for _, entry := range response.Leaves {
		if err := json.Unmarshal(entry.LeafValue, &dat); err != nil {
        	panic(err)
    	}

		if entry.LeafIndex > mapperMetadata.HighestFullyCompletedSeq {
			mapperMetadata.HighestFullyCompletedSeq = entry.LeafIndex
		}

		idc := dat.IDC
		idcs[idc] = &dat
	}

	glog.Infof("Found %d unique IDCs", len(idcs))
	glog.Info("Fetching current map values for IDCs...")

	idchashes := make(map[string]string)

	// Fetch the current map values for those IDCs:
	getReq := &trillian.GetMapLeavesRequest{
		MapId:    m.mapID,
		Index:    make([][]byte, 0, len(idcs)),
		Revision: -1,
	}
	for d := range idcs {
		getReq.Index = append(getReq.Index, ctmapper.HashDomain(d))
		idchashes[string(ctmapper.HashDomain(d))] = d
	}

	getResp, err := m.vmap.GetLeaves(context.Background(), getReq)
	if err != nil {
		return false, err
	}
	//glog.Info("Get resp: %v", getResp)

	proofs := 0
	for _, v := range getResp.MapLeafInclusion {
		if err := json.Unmarshal(v.Leaf.LeafValue, &dat); err != nil {
			if v.Leaf.LeafValue != nil {
        		panic(err)
			}
    	}
		if len(v.Inclusion) > 0 {
			proofs++
		}
		mapidc := idchashes[string(v.Leaf.Index)]
		glog.Infof("Got %#v", mapidc)
		if (v.Leaf.LeafValue != nil) {
			idcs[mapidc].Requests = append(idcs[mapidc].Requests, dat.Requests...)
		}
		glog.Infof("will update for %s", mapidc)
	}
	glog.Infof("Got %d values, and %d proofs", len(getResp.MapLeafInclusion), proofs)

	glog.Info("Storing updated map values for domains...")
	// Store updated map values:
	setReq := &trillian.SetMapLeavesRequest{
		MapId:  m.mapID,
		Leaves: make([]*trillian.MapLeaf, 0, len(idcs)),
	}
	for k, b := range idcs {
		index := ctmapper.HashDomain(k)
		b, err := json.Marshal(b)
		if err != nil {
			return false, err
		}
		setReq.Leaves = append(setReq.Leaves, &trillian.MapLeaf{
			Index:     index,
			LeafValue: b,
		})
	}

	var metaAny *any.Any
	if metaAny, err = ptypes.MarshalAny(mapperMetadata); err != nil {
		return false, fmt.Errorf("failed to marshal mapper metadata as 'any': err %v", err)
	}

	setReq.Metadata = metaAny

	setResp, err := m.vmap.SetLeaves(context.Background(), setReq)
	if err != nil {
		return false, err
	}
	glog.Infof("Set resp: %v", setResp)
	d := time.Since(start)
	glog.Infof("Map run complete, took %.1f secs to update %d values (%0.2f/s)", d.Seconds(), len(setReq.Leaves), float64(len(setReq.Leaves))/d.Seconds())
	return true, nil
}

func main() {
	flag.Parse()
	mapconn, err := grpc.Dial(*mapServer, grpc.WithInsecure())
	if err != nil {
		glog.Fatal(err)
	}
	defer mapconn.Close()

	logconn, err := grpc.Dial(*sourceLog, grpc.WithInsecure())
	if err != nil {
		glog.Fatal(err)
	}
	mapper := VLDMMapper{
		mapID: int64(*mapID),
		vlog:  trillian.NewTrillianLogClient(logconn),
		vmap:  trillian.NewTrillianMapClient(mapconn),
	}
	ctx := context.Background()

	for {
		moreToDo, err := mapper.oneMapperRun(ctx)
		if err != nil {
			glog.Warningf("mapper run failed: %v", err)
		}
		if !moreToDo {
			time.Sleep(100)
		}

	}
}
