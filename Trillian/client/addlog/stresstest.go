package main

import (
	"context"
	"flag"
	"fmt"
	//"time"

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
var startSID = flag.Int("start_sid", 0, "starting SID")
var endSID = flag.Int("end_sid", 0, "end SID")
var agent = flag.Int("agent", 0, "agent")
var DP = flag.Int("dp", 0, "DP")
var request = flag.String("request", "test_data", "Request data")
var workers = flag.Int("workers", 1, "number of workers")

func worker(id int, jobs <-chan int, results chan<- int) {
    logconn, err := grpc.Dial(*logServer, grpc.WithInsecure())
    if err != nil {
        glog.Fatal(err)
    }
    defer logconn.Close()

    logClient := trillian.NewTrillianLogClient(logconn)
    ctx := context.Background()

    for SID := range jobs {
        //fmt.Println("worker", id, "started  job", SID)

    	idc, err := client.Compute_idc([]byte(*key), strconv.Itoa(SID), strconv.Itoa(*DP), strconv.Itoa(*agent))
    	if (err != nil) {
            fmt.Printf("err");
    		panic(err)
    	}

        leaf1 := &trillian.LogLeaf{
            LeafValue: []byte("{\"requests\": [\"" + *request + "\"], \"idc\": \"" + idc + "\"}"),
        }

        resp, err2 := logClient.QueueLeaves(ctx, &trillian.QueueLeavesRequest{
    		LogId:  int64(*logID),
    		Leaves: []*trillian.LogLeaf{leaf1},
    	})

    	fmt.Printf("resp: %+v\n", resp)

    	if err2 != nil {
    		glog.Warningf("failed: %v", err2)
            results <- 0
    	}

        //fmt.Println("worker", id, "finished job", SID)
        results <- 1
    }
}


func main() {
	flag.Parse()

    jobs := make(chan int, *endSID - *startSID)
    results := make(chan int, *endSID - *startSID)
    for w := 1; w <= *workers; w++ {
        go worker(w, jobs, results)
    }
    for SID := *startSID; SID < *endSID; SID++ {
        jobs <- SID
    }
    close(jobs)
    for SID := *startSID; SID < *endSID; SID++ {
        <-results
    }
}

