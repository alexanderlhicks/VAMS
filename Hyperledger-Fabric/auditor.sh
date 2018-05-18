CORE_PEER_ENDORSER_ENABLED=true \
CORE_PEER_PROFILE_ENABLED=true \
CORE_PEER_ADDRESS=auditor:7051 \
CORE_PEER_CHAINCODELISTENADDRESS=0.0.0.0:7052 \
CORE_PEER_ID=auditor \
CORE_PEER_LOCALMSPID=AuditorsMSP \
CORE_PEER_GOSSIP_EXTERNALENDPOINT=auditor:7051 \
CORE_PEER_GOSSIP_USELEADERELECTION=true \
CORE_PEER_GOSSIP_ORGLEADER=false \
CORE_PEER_TLS_ENABLED=false \
CORE_PEER_TLS_KEY_FILE=/home/ubuntu/verifiable-access-code/hlf-11preview/crypto-config/peerOrganizations/Auditors/users/Admin@Auditors/tls/server.key \
CORE_PEER_TLS_CERT_FILE=/home/ubuntu/verifiable-access-code/hlf-11preview/crypto-config/peerOrganizations/Auditors/users/Admin@Auditors/tls/server.crt \
CORE_PEER_TLS_ROOTCERT_FILE=/home/ubuntu/verifiable-access-code/hlf-11preview/crypto-config/peerOrganizations/Auditors/users/Admin@Auditors/tls/ca.crt \
CORE_PEER_TLS_SERVERHOSTOVERRIDE=auditor \
CORE_VM_DOCKER_ATTACHSTDOUT=true \
CORE_PEER_MSPCONFIGPATH=/home/ubuntu/verifiable-access-code/hlf-11preview/crypto-config/peerOrganizations/Auditors/users/Admin@Auditors/msp \
CORE_LOGGING_GRPC=debug \
peer node start --peer-defaultchain=false


