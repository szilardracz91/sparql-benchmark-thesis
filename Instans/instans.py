__author__ = 'szilard'
import yaml
import time
from subprocess import call
import csv

with open("../trainbenchmark/config.yml", 'r') as stream:
        config = yaml.load(stream)

with open('result.csv', 'w') as csvfile:
    resultWriter = csv.writer(csvfile, delimiter='\t')
    resultWriter.writerow(['CaseName', 'Iteration', 'MetricName', 'MetricValue', 'PhaseName', 'RundIndex', 'Scenario', 'Sequence', 'Size', 'Tool'])

    for scenario in config["scenarios"]:
        scenario=scenario.lower()
        size=config["minsize"]

        while (size<=config["maxsize"]):
            for query in config["queries"]:
                queryPath="../trainbenchmark/queries/"+query+".sparql"
                start_time=time.time()
                call(["/home/szilard/Szakdolgozat/instans/bin/./instans", "--select-output=railway-"+scenario+"-"+str(size)+"-inferred-"+query+".ttl", "-r", queryPath,
                      "--input-ttl=../trainbenchmark/models/railway-"+scenario+"-"+str(size)+"-inferred.ttl", "--noexecute"])

                read_time=int(round((time.time()-start_time)*1000000000))
                start_time=time.time()
                call(["/home/szilard/Szakdolgozat/instans/bin/./instans", "--execute"])
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


                resultWriter.writerow([query, str(1), 'Time', str(read_time), 'Read', str(1), scenario, str(1), str(size), 'INSTANS'])
                resultWriter.writerow([query, str(1), 'Time', str(check_time), 'Check', str(1), scenario, str(1), str(size), 'INSTANS'])
                resultWriter.writerow([query, str(1), 'Matches', str(Matches), 'Check', str(1), scenario, str(1), str(size), 'INSTANS'])

            size=size*2


#CaseName Iteration MetricName MetricValue PhaseName RundIndex Scenario Sequence Size Tool




