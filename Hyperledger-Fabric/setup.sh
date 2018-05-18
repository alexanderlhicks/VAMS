echo "#############################################"
echo "# Create main channel on orderer with agent #"
echo "#############################################"

CORE_PEER_LOCALMSPID="AgentsMSP" \
CORE_PEER_TLS_ROOTCERT_FILE=/home/ubuntu/verifiable-access-code/hlf-11preview/crypto-config/peerOrganizations/Agents/users/Admin@Agents/tls/ca.crt \
CORE_PEER_MSPCONFIGPATH=/home/ubuntu/verifiable-access-code/hlf-11preview/crypto-config/peerOrganizations/Agents/users/Admin@Agents/msp \
CORE_PEER_ADDRESS=agent:7051 \
peer channel create -o orderer:7050 -c main -f /home/ubuntu/verifiable-access-code/hlf-11preview/main.tx

sleep 2

echo "#################################################################"
echo "# Join main channel with agent, data provider, user and auditor #"
echo "#################################################################"

PEER_ID=agent \
ORG_ID=Agents \
CORE_PEER_LOCALMSPID="AgentsMSP" \
CORE_PEER_MSPCONFIGPATH=/home/ubuntu/verifiable-access-code/hlf-11preview/crypto-config/peerOrganizations/Agents/users/Admin@Agents/msp \
CORE_PEER_ADDRESS=agent:7051 \
peer channel join -b main.block

sleep 2

echo ""

PEER_ID=dataprovider \
ORG_ID=DataProviders \
CORE_PEER_LOCALMSPID="DataProvidersMSP" \
CORE_PEER_MSPCONFIGPATH=/home/ubuntu/verifiable-access-code/hlf-11preview/crypto-config/peerOrganizations/DataProviders/users/Admin@DataProviders/msp \
CORE_PEER_ADDRESS=dataprovider:7051 \
peer channel join -b main.block

sleep 2

echo ""

PEER_ID=user \
ORG_ID=Users \
CORE_PEER_LOCALMSPID="UsersMSP" \
CORE_PEER_MSPCONFIGPATH=/home/ubuntu/verifiable-access-code/hlf-11preview/crypto-config/peerOrganizations/Users/users/Admin@Users/msp \
CORE_PEER_ADDRESS=user:7051 \
peer channel join -b main.block

sleep 2

echo ""

PEER_ID=auditor \
ORG_ID=Auditors \
CORE_PEER_LOCALMSPID="AuditorsMSP" \
CORE_PEER_MSPCONFIGPATH=/home/ubuntu/verifiable-access-code/hlf-11preview/crypto-config/peerOrganizations/Auditors/users/Admin@Auditors/msp \
CORE_PEER_ADDRESS=auditor:7051 \
peer channel join -b main.block

sleep 2

echo "#####################################"
echo "# Set anchor peers for main channel #"
echo "#####################################"

PEER_ID=agent \
ORG_ID=Agents \
CORE_PEER_LOCALMSPID="AgentsMSP" \
CORE_PEER_MSPCONFIGPATH=/home/ubuntu/verifiable-access-code/hlf-11preview/crypto-config/peerOrganizations/Agents/users/Admin@Agents/msp \
CORE_PEER_ADDRESS=agent:7051 \
peer channel create -o orderer:7050 -c main -f /home/ubuntu/verifiable-access-code/hlf-11preview/Agentsanchors-main.tx

sleep 2

echo ""

PEER_ID=dataprovider \
ORG_ID=DataProviders \
CORE_PEER_LOCALMSPID="DataProvidersMSP" \
CORE_PEER_MSPCONFIGPATH=/home/ubuntu/verifiable-access-code/hlf-11preview/crypto-config/peerOrganizations/DataProviders/users/Admin@DataProviders/msp \
CORE_PEER_ADDRESS=dataprovider:7051 \
peer channel create -o orderer:7050 -c main -f /home/ubuntu/verifiable-access-code/hlf-11preview/DataProvidersanchors-main.tx

sleep 2

echo ""

PEER_ID=user \
ORG_ID=Users \
CORE_PEER_LOCALMSPID="UsersMSP" \
CORE_PEER_MSPCONFIGPATH=/home/ubuntu/verifiable-access-code/hlf-11preview/crypto-config/peerOrganizations/Users/users/Admin@Users/msp \
CORE_PEER_ADDRESS=user:7051 \
peer channel create -o orderer:7050 -c main -f /home/ubuntu/verifiable-access-code/hlf-11preview/Usersanchors-main.tx

sleep 2

echo ""

PEER_ID=auditor \
ORG_ID=Auditors \
CORE_PEER_LOCALMSPID="AuditorsMSP" \
CORE_PEER_MSPCONFIGPATH=/home/ubuntu/verifiable-access-code/hlf-11preview/crypto-config/peerOrganizations/Auditors/users/Admin@Auditors/msp \
CORE_PEER_ADDRESS=auditor:7051 \
peer channel create -o orderer:7050 -c main -f /home/ubuntu/verifiable-access-code/hlf-11preview/Auditorsanchors-main.tx

echo "###############################################################"
echo "# install and instantiate chaincode for each channel on peers #"
echo "###############################################################"

PEER_ID=agent \
ORG_ID=Agents \
CORE_PEER_LOCALMSPID="AgentsMSP" \
CORE_PEER_MSPCONFIGPATH=/home/ubuntu/verifiable-access-code/hlf-11preview/crypto-config/peerOrganizations/Agents/users/Admin@Agents/msp \
CORE_PEER_ADDRESS=agent:7051 \
peer chaincode install -n maincc -v 0 -p chaincode/Main

sleep 2

echo ""

PEER_ID=agent \
ORG_ID=Agents \
CORE_PEER_LOCALMSPID="AgentsMSP" \
CORE_PEER_MSPCONFIGPATH=/home/ubuntu/verifiable-access-code/hlf-11preview/crypto-config/peerOrganizations/Agents/users/Admin@Agents/msp \
CORE_PEER_ADDRESS=agent:7051 \
peer chaincode instantiate -o orderer:7050 -C main -n maincc -v 0 -c '{"Args":[]}' 

sleep 2

echo ""

PEER_ID=auditor \
ORG_ID=Auditors \
CORE_PEER_LOCALMSPID="AuditorsMSP" \
CORE_PEER_MSPCONFIGPATH=/home/ubuntu/verifiable-access-code/hlf-11preview/crypto-config/peerOrganizations/Auditors/users/Admin@Auditors/msp \
CORE_PEER_ADDRESS=auditor:7051 \
peer chaincode install -n maincc -v 0 -p chaincode/Main

sleep 2

echo ""

PEER_ID=user \
ORG_ID=Users \
CORE_PEER_LOCALMSPID="UsersMSP" \
CORE_PEER_MSPCONFIGPATH=/home/ubuntu/verifiable-access-code/hlf-11preview/crypto-config/peerOrganizations/Users/users/Admin@Users/msp \
CORE_PEER_ADDRESS=user:7051 \
peer chaincode install -n maincc -v 0 -p chaincode/Main

sleep 2

echo ""

PEER_ID=dataprovider \
ORG_ID=DataProviders \
CORE_PEER_LOCALMSPID="DataProvidersMSP" \
CORE_PEER_MSPCONFIGPATH=/home/ubuntu/verifiable-access-code/hlf-11preview/crypto-config/peerOrganizations/DataProviders/users/Admin@DataProviders/msp \
CORE_PEER_ADDRESS=dataprovider:7051 \
peer chaincode install -n maincc -v 0 -p chaincode/Main

sleep 2

echo "##################"
echo "# Setup finished #"
echo "##################"