VAMS - Hyperledger Fabric based implementation

Included here are the files required to run the test network used for our evaluation of the Hyperledger Fabric based implementation.
The implementation was tested on seven aws t2.medium machines (2 vCPUs, 4GB memory), running Linux 16.04 LTS with Go 1.7, docker-ce 17.06, docker-compose 1.18 and Fabric 1.06.
For Hyperledger Fabric specific documentation, see https://hyperledger-fabric.readthedocs.io and https://github.com/hyperledger/fabric.

There is one folder, src, that contains the chaincode written in Go, and 10 files (excluding this readme):
Peer and ordering service: agent.sh, dp.sh, user.sh, auditor.sh, kafka-zookeeper.yaml, orderer.sh
Config files: configtx.yaml, crypto-config.yaml
Scripts: prelim.sh, setup.sh

After you've installed Hyperledger Fabric (see HLF documentation), it's recommended that you edit your /etc/hosts file to include a mapping between the ip address of the machines in your network and the use of the machine e.g., a.g.e.n.t.ip agent. This will allow you to use the provided scripts without having to replace the ip addresses. It is also recommended to set up a git repo (cloning this one should be fine) so that you can easily push/pull across machines easily. Once that is done, running the network is as follows:

On the client machine, run prelim.sh, which will generate required cryptographic files (certificates, ...) in the crypto-config folder, as well as generate the genesis block and channel transaction files.

On the four peer machines, run agent.sh, dp.sh, user.sh and auditor.sh to start a peer instance for each organization. To start the ordering service, run docker-compose -f kafka-compose.yaml to start the Kafka Zookeeper service, then run orderer.sh to start the kafka broker.

Once everything peer and the ordering service is up and running, run setup.sh to connect the peers to the channel, install and instantiate the chaincode. The network is now setup, and you are free to start making transactions.

Transactions can be sent from the client, the following is an example request that invokes the "req" function in the chaincode:
PEER_ID=agent \
ORG_ID=Agents \
CORE_PEER_LOCALMSPID="AgentsMSP" \
CORE_PEER_MSPCONFIGPATH=FILEPATH/crypto-config/peerOrganizations/Agents/users/Admin@Agents/msp \
CORE_PEER_ADDRESS=agent:7051 \
peer chaincode invoke -n maincc -c '{"Args":["req", "idc", "ioccoencrypt", "userencrypt"]}' -C main



	



