package main

import (
	"encoding/json"
	"fmt"
	proto "github.com/golang/protobuf/proto"
	"github.com/hyperledger/fabric/core/chaincode/shim"
	pb "github.com/hyperledger/fabric/protos/peer"
)

type Chaincode struct {
}

type request struct {
	Idc     string `json:"common identifier"`
	Auditor string `json:"auditor encryption"`
	User    string `json:"user encryption"`
}

func (t *Chaincode) Init(stub shim.ChaincodeStubInterface) pb.Response {
	var err error
	args := stub.GetStringArgs()
	if len(args) != 0 {
		return shim.Error("Erroneous number of arguments, should be 0")
	}
	if err != nil {
		return shim.Error("Error initialising chaincode: " + err.Error())
	}
	return shim.Success(nil)
}

func (t *Chaincode) Invoke(stub shim.ChaincodeStubInterface) pb.Response {
	function, args := stub.GetFunctionAndParameters()
	fmt.Println("Invoking " + function)
	switch function {
	case "req":
		return t.agentRequest(stub, args)
	case "log":
		return t.logAudit(stub, args)
	case "user":
		return t.userAudit(stub, args)
	case "history":
		return t.keyAudit(stub, args)
	default:
		return shim.Error("Error invoking chaincode function")
	}
}

func (t *Chaincode) agentRequest(stub shim.ChaincodeStubInterface, args []string) pb.Response {
	var err error
	fmt.Println("Creating request")
	if len(args) != 3 {
		return shim.Error("Erroneous number of arguments, should be 3")
	}
	if len(args[0]) <= 0 {
		return shim.Error("Erroneous common identifier length, should not be 0")
	}
	if len(args[1]) <= 0 {
		return shim.Error("Encrypted request for the auditor should not be of length 0")
	}
	if len(args[2]) <= 0 {
		return shim.Error("Encrypted request for the user should not be of length 0")
	}
	_request, err := stub.GetState(args[0])
	if err != nil {
		return shim.Error("Error getting request from state: " + err.Error())
	} else if _request != nil {
		return shim.Error("Common identifer already exists in the state")
	}
	request := &request{args[0], args[1], args[2]}
	requestjson, err := json.Marshal(request)
	if err != nil {
		return shim.Error("Error marshaling request to json: " + err.Error())
	}
	err = stub.PutState(args[0], requestjson)
	if err != nil {
		return shim.Error("Error updating the state with the request: " + err.Error())
	}
	return shim.Success([]byte("State updated with request"))
}

func (t *Chaincode) logAudit(stub shim.ChaincodeStubInterface, args []string) pb.Response {
	var err error
	var requests []string
	if len(args) != 2 {
		return shim.Error("Erroneous number of arguments, should be 2")
	}
	startkey := args[0]
	endkey := args[1]
	log, err := stub.GetStateByRange(startkey, endkey) // empty string as start and endkey iterates over all possible keys in lexical order
	if err != nil {
		return shim.Error("Error obtaining state for the given key range: " + err.Error())
	}
	defer log.Close()
	for log.HasNext() {
		request, err := log.Next()
		if err != nil {
			return shim.Error("Error itterating over keys: " + err.Error())
		}
		requests = append(requests, proto.CompactTextString(request))
	}
	jsonrequests, err := json.Marshal(requests)
	if err != nil {
		return shim.Error("Error marshaling to json: " + err.Error())
	}
	return shim.Success(jsonrequests)
}

// Allows a user to retrieve all requests from the state using the precomputed common identifiers as keys
func (t *Chaincode) userAudit(stub shim.ChaincodeStubInterface, args []string) pb.Response {
	var err error
	var requests []string
	if len(args) <= 0 {
		return shim.Error("submit commin identifiers you wish to retrieve queries for")
	}
	for i := 0; i < len(args); i++ {
		request, err := stub.GetState(args[i])
		if err != nil {
			return shim.Error("Failed to get request: " + err.Error())
		}
		requests = append(requests, string(request))
	}
	jsonrequests, err := json.Marshal(requests)
	if err != nil {
		return shim.Error("Marshaling JSON error: " + err.Error())
	}
	return shim.Success(jsonrequests)
}

func (t *Chaincode) keyAudit(stub shim.ChaincodeStubInterface, args []string) pb.Response {
	var err error
	var changes []string
	if len(args) != 1 {
		return shim.Error("Erroneous number of arguments, should be 1")
	}
	history, err := stub.GetHistoryForKey(args[0])
	if err != nil {
		return shim.Error("Error retrieving history for idc: " + err.Error())
	}
	for history.HasNext() {
		change, err := history.Next()
		if err != nil {
			return shim.Error("Error iterating: " + err.Error())
		}
		changes = append(changes, proto.CompactTextString(change))
	}
	jsonchanges, err := json.Marshal(changes)
	if err != nil {
		return shim.Error("Error marshaling to json: " + err.Error())
	}
	return shim.Success(jsonchanges)
}

func main() {
	err := shim.Start(new(Chaincode))
	if err != nil {
		fmt.Printf("Error starting chaincode: " + err.Error())
	}
}
