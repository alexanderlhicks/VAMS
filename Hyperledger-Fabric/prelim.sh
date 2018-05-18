echo "##############################"
echo "# Generating crypto material #"
echo "##############################"

cryptogen generate --config=./crypto-config.yaml 

sleep 1

echo "##########################"
echo "# Creating genesis block #"
echo "##########################"

configtxgen -profile OrdererGenesis -outputBlock genesis.block 

sleep 1

echo "##########################################"
echo "# Creating channel creation transactions #"
echo "##########################################"

configtxgen -profile MainChannel -outputCreateChannelTx main.tx -channelID main 

sleep 1

echo "#######################################################"
echo "# Creating anchor peer transactions for both channels #"
echo "#######################################################"

configtxgen -profile MainChannel -outputAnchorPeersUpdate Agentsanchors-main.tx -channelID main -asOrg Agents 

sleep 1

configtxgen -profile MainChannel -outputAnchorPeersUpdate DataProvidersanchors-main.tx -channelID main -asOrg DataProviders 

sleep 1

configtxgen -profile MainChannel -outputAnchorPeersUpdate Usersanchors-main.tx -channelID main -asOrg Users 

sleep 1

configtxgen -profile MainChannel -outputAnchorPeersUpdate Auditorsanchors-main.tx -channelID main -asOrg Auditors

sleep 1

echo "########"
echo "# Done #"
echo "########"