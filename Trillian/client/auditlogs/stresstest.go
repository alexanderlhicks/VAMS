package main

import (
	"context"
	"flag"
	"time"
	"fmt"

	"github.com/golang/glog"
	//"github.com/golang/protobuf/ptypes"
	//"github.com/golang/protobuf/ptypes/any"
	//"github.com/google/certificate-transparency-go/x509"
	"github.com/google/trillian"
	//"github.com/google/trillian/examples/ct/ctmapper"
	//"github.com/google/trillian/examples/ct/ctmapper/ctmapperpb"
	"google.golang.org/grpc"
	"../../client"
	"github.com/google/trillian/examples/ct/ctmapper"
    "strconv"

	//pb "github.com/golang/protobuf/proto"
	//ct "github.com/google/certificate-transparency-go"
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
var jobsno = flag.Int("jobs", 0, "number of jobs")
var workers = flag.Int("workers", 100, "number of workers")

func worker(id int, jobs <-chan int, results chan<- int) {
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

    for  range jobs {
        //fmt.Println("worker", id, "started  job", i)

		// Fetch the current map values for those IDCs:
		getReq := &trillian.GetMapLeavesRequest{
			MapId:    int64(*mapID),
			Index:    indexes,
			Revision: -1,
		}

		_, err := vmap.GetLeaves(context.Background(), getReq)
		if err != nil {
			panic(err)
		}
		//glog.Info("Get resp: %v", getResp)

        //fmt.Println("worker", id, "finished job", i)
		now := time.Now()
		secs := now.UnixNano()

		fmt.Println(secs)
        results <- 1
    }
}


func main() {
	flag.Parse()

    jobs := make(chan int, *jobsno)
    results := make(chan int, *endSID - *startSID)
    for w := 1; w <= *workers; w++ {
        go worker(w, jobs, results)
    }
    for i := 0; i < *jobsno; i++ {
        jobs <- i
    }
    close(jobs)
    for i := 0; i < *jobsno; i++ {
        <-results
    }
}
