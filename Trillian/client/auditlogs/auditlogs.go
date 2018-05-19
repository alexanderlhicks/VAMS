package main

import (
    "../../client"
    "flag"
	"github.com/google/trillian/examples/ct/ctmapper"
    "strconv"
	"google.golang.org/grpc"
    "github.com/golang/glog"
	"context"
	"github.com/google/trillian"
    "time"
)

var mapServer = flag.String("map_server", "", "host:port for the map server")
var mapID = flag.Int("map_id", -1, "Map ID")
var key = flag.String("key", "", "key for IDC")
var startSID = flag.Int("start_sid", 0, "starting SID")
var endSID = flag.Int("end_sid", 0, "end SID")
var startAgent = flag.Int("start_agent", 0, "starting agent")
var endAgent = flag.Int("end_agent", 0, "end agent")
var startDP = flag.Int("start_dp", 0, "starting DP")
var endDP = flag.Int("end_dp", 0, "end DP")

func main() {
    flag.Parse()
    key := []byte(*key)
    indexes := [][]byte{}

    for x := *startAgent; x < *endAgent; x++ {
        for y := *startDP; y < *endDP; y++ {
            for z := *startSID; z < *endSID; z++ {
                idc, err := client.Compute_idc(key, strconv.Itoa(z), strconv.Itoa(y), strconv.Itoa(x))
                if (err != nil) {
                    panic(err)
                }
                indexes = append(indexes, ctmapper.HashDomain(idc))
            }
        }
    }

    mapconn, err := grpc.Dial(*mapServer, grpc.WithInsecure())
    if err != nil {
        glog.Fatal(err)
    }
    vmap := trillian.NewTrillianMapClient(mapconn)

	// Fetch the current map values for those IDCs:
	getReq := &trillian.GetMapLeavesRequest{
		MapId:    int64(*mapID),
		Index:    indexes,
		Revision: -1,
	}

    start := time.Now()
	getResp, err := vmap.GetLeaves(context.Background(), getReq)
	if err != nil {
		panic(err)
	}
    elapsed := time.Since(start)
	glog.Info("Get resp: %v", getResp)
    glog.Info("Took ", elapsed)

	proofs := 0
	for _, v := range getResp.MapLeafInclusion {
		if len(v.Inclusion) > 0 {
			proofs++
		}
		glog.Infof("Got %#v", v.Leaf.LeafValue)
	}
	glog.Infof("Got %d values, and %d proofs", len(getResp.MapLeafInclusion), proofs)
}
