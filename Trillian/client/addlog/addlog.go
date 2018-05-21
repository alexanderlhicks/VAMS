package main

import (
	"context"
	"flag"
	"fmt"
	"time"

	"github.com/golang/glog"
	//"github.com/golang/protobuf/ptypes"
	//"github.com/golang/protobuf/ptypes/any"
	//"github.com/google/certificate-transparency-go/x509"
	"github.com/google/trillian"
	//"github.com/google/trillian/examples/ct/ctmapper"
	//"github.com/google/trillian/examples/ct/ctmapper/ctmapperpb"
	"google.golang.org/grpc"
	"../../client"
    "strconv"

	//pb "github.com/golang/protobuf/proto"
	//ct "github.com/google/certificate-transparency-go"
)

var logServer = flag.String("log_server", "", "host:port for the log server")
var logID = flag.Int("log_id", -1, "Log ID")
var key = flag.String("key", "", "key for IDC")
var SID = flag.Int("sid", 0, "SID")
var agent = flag.Int("agent", 0, "agent")
var DP = flag.Int("dp", 0, "DP")
var request = flag.String("request", "test_data", "Request data")

func main() {
	flag.Parse()
	logconn, err := grpc.Dial(*logServer, grpc.WithInsecure())
	if err != nil {
		glog.Fatal(err)
	}
	defer logconn.Close()

    logClient := trillian.NewTrillianLogClient(logconn)
    ctx := context.Background()

	idc, err := client.Compute_idc([]byte(*key), strconv.Itoa(*SID), strconv.Itoa(*DP), strconv.Itoa(*agent))
	if (err != nil) {
		panic(err)
	}

    leaf1 := &trillian.LogLeaf{
        LeafValue: []byte("{\"requests\": [\"" + *request + "\"], \"idc\": \"" + idc + "\"}"),
    }

    start := time.Now()
    glog.Info("Start ", start)
    resp, err2 := logClient.QueueLeaves(ctx, &trillian.QueueLeavesRequest{
		LogId:  int64(*logID),
		Leaves: []*trillian.LogLeaf{leaf1},
	})

	fmt.Printf("%+v\n", resp)

	if err2 != nil {
		glog.Warningf("failed: %v", err2)
	}
}
