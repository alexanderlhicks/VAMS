ORDERER_GENERAL_LOGLEVEL=debug \
ORDERER_GENERAL_LISTENADDRESS=0.0.0.0 \
ORDERER_GENERAL_GENESISMETHOD=file \
ORDERER_GENERAL_GENESISFILE=/home/ubuntu/verifiable-access-code/hlf-11preview/genesis.block \
ORDERER_GENERAL_LOCALMSPID=OrdererMSP \
ORDERER_GENERAL_LOCALMSPDIR=/home/ubuntu/verifiable-access-code/hlf-11preview/crypto-config/ordererOrganizations/Orderer/users/Admin@Orderer/msp \
ORDERER_GENERAL_TLS_ENABLED=false \
ORDERER_GENERAL_TLS_PRIVATEKEY=/home/ubuntu/verifiable-access-code/hlf-11preview/crypto-config/ordererOrganizations/Orderer/orderers/Orderer.Orderer/tls/server.key \
ORDERER_GENERAL_TLS_CERTIFICATE=/home/ubuntu/verifiable-access-code/hlf-11preview/crypto-config/ordererOrganizations/Orderer/orderers/Orderer.Orderer/tls/server.crt \
ORDERER_GENERAL_TLS_ROOTCAS=[/home/ubuntu/verifiable-access-code/hlf-11preview/crypto-config/ordererOrganizations/Orderer/orderers/Orderer.Orderer/tls/ca.crt,/home/ubuntu/verifiable-access-code/hlf-11preview/crypto-config/peerOrganizations/Agents/users/Admin@Agents/tls/ca.crt,/home/ubuntu/verifiable-access-code/hlf-11preview/crypto-config/peerOrganizations/DataProviders/users/Admin@DataProviders/tls/ca.crt,/home/ubuntu/verifiable-access-code/hlf-11preview/crypto-config/peerOrganizations/Users/users/Admin@Users/tls/ca.crt,/home/ubuntu/verifiable-access-code/hlf-11preview/crypto-config/peerOrganizations/Auditors/users/Admin@Auditors/tls/ca.crt] \
CONFIGTX_ORDERER_BATCHTIMEOUT=1s \
CONFIGTX_ORDERER_ORDERERTYPE=kafka \
CONFIGTX_ORDERER_KAFKA_BROKERS=[kafka:9092] \
ORDERER_LOGGING_GRPC=debug \
orderer

