__author__ = 'szilard'
import yaml
import time
import signal
from subprocess import call
import csv

def handler(signum, frame):
    print "Forever is over!"
    raise Exception("end of time")

signal.signal(signal.SIGALRM, handler)



with open("../trainbenchmark/config.yml", 'r') as stream:
        config = yaml.load(stream)

with open('result.csv', 'w') as csvfile:
    resultWriter = csv.writer(csvfile, delimiter=',')
    resultWriter.writerow(['Case', 'Iteration', 'Metric', 'Value', 'Phase', 'Run', 'Scenario', 'Artifact', 'Tool'])

    for scenario in config["scenarios"]:
	scenarioOut=scenario
        scenario=scenario.lower()
        size=config["minsize"]

        while (size<=config["maxsize"]):
            for query in config["queries"]:
                queryPath="../trainbenchmark/queries/"+query+".sparql"
                start_time=time.time()
                signal.alarm(100)
                call(["/home/szilard/Szakdolgozat/instans/bin/./instans", "--select-output=railway-"+scenario+"-"+str(size)+"-inferred-"+query+".ttl", "-r", queryPath,
                      "--input-ttl=../trainbenchmark/models/railway-"+scenario+"-"+str(size)+"-inferred.ttl", "--noexecute"])
                signal.alarm(0)
                read_time=int(round((time.time()-start_time)*1000000000))

                start_time=time.time()
                signal.alarm(100)
                call(["/home/szilard/Szakdolgozat/instans/bin/./instans", "--rdf-input-unit=Single", "--execute"])
                signal.alarm(0)
                check_time=int(round((time.time()-start_time)*1000000000))
                Matches=0;
                resultfile = open("railway-"+scenario+"-"+str(size)+"-inferred-"+query+".ttl", 'r')
                matchlist = resultfile.readlines()
                resultfile.close()
                for line in matchlist:
                    solution=str(line)
                    if solution.find("solution")!=-1:
                        Matches=Matches+1
                print (str(query) + " " + str(size)+ " " + str(Matches))


                resultWriter.writerow([query, str(1), 'Time', str(read_time), 'Read', str(1), scenarioOut, str(size), 'INSTANS'])
                resultWriter.writerow([query, str(1), 'Time', str(check_time), 'Check', str(1), scenarioOut, str(size), 'INSTANS'])
                resultWriter.writerow([query, str(1), 'Matches', str(Matches), 'Check', str(1), scenarioOut, str(size), 'INSTANS'])

            size=size*2


#CaseName Iteration MetricName MetricValue PhaseName RundIndex Scenario Sequence Size Tool




