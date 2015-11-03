#!/bin/bash
maxSize=16
minSize=1
for (( i=minSize;i<=maxSize;i=i*2)); do
	T="$(date +%s)"
	../bin/./instans --select-output=result$i.ttl -r queries/RouteSensor.sparql --input-ttl=models/railway-repair-$i-inferred.ttl  
	S="$(($(date +%s)-T))"
	echo "Elapsed time during query in seconds: ${S} in railway-repair-$i-inferred.ttl " >> result.txt
done 


