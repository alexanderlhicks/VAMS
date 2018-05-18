script screen.log
for ((j=1; j<11; j++)); do bash requests${j}.sh & done
wait
exit
