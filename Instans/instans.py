__author__ = 'szilard'
import yaml
import time
from subprocess import call
import csv

with open("config.yml", 'r') as stream:
        config = yaml.load(stream)

with open('result.csv', 'w') as csvfile:
    resultWriter = csv.writer(csvfile, delimiter='\t')
    resultWriter.writerow(['CaseName', 'Iteration', 'MetricName', 'MetricValue', 'PhaseName', 'RundIndex', 'Scenario', 'Sequence', 'Size', 'Tool'])
    size=config["minsize"]
    while (size<=config["maxsize"]):
        for query in config["queries"]:
            queryPath="queries/"+query+".sparql"
            start_time=time.time()
            call(["/home/szilard/Szakdolgozat/instans/bin/./instans", "--select-output=railway-repair-"+str(size)+"-inferred-"+query+".ttl", "-r", queryPath,
                  "--input-ttl=models/railway-repair-"+str(size)+"-inferred.ttl"])

            Matches=0;
            resultfile = open("railway-repair-"+str(size)+"-inferred-"+query+".ttl", 'r')
            matchlist = resultfile.readlines()
            resultfile.close()
            for line in matchlist:
                solution=str(line)
                if solution.find("solution")!=-1:
                    Matches=Matches+1
            print (str(query) + " " + str(size)+ " " + str(Matches))


            end_time=(time.time()-start_time)*1000000000
            result="Read + Check time in nanoseconds in model railway-repair-"+str(size)+"-inferred.ttl in query "+query+": " + str(end_time)
            resultWriter.writerow([query, str(1), 'Time', str(end_time), 'Read + Check', str(1), 'Repair', str(1), str(size), 'INSTANS'])

        size=size*2


#CaseName Iteration MetricName MetricValue PhaseName RundIndex Scenario Sequence Size Tool




