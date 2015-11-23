#!/usr/bin/python


import RDF
import yaml
import time
import csv

storage=RDF.Storage(storage_name="hashes",
                    name="test",
                    options_string="new='yes',hash-type='memory',dir='.'")
if storage is None:
  raise Exception("new RDF.Storage failed")



model=RDF.Model(storage)
if model is None:
  raise Exception("new RDF.model failed")

with open("../trainbenchmark/config.yml", 'r') as stream:
        config = yaml.load(stream)

with open('Redland_result.csv', 'w') as csvfile:
    resultWriter = csv.writer(csvfile, delimiter='\t')
    resultWriter.writerow(['CaseName', 'Iteration', 'MetricName', 'MetricValue', 'PhaseName', 'RundIndex', 'Scenario', 'Sequence', 'Size', 'Tool'])

    for scenario in config["scenarios"]:
        scenario=scenario.lower()
        size=config["minsize"]

        while (size<=1):
            test_file='../trainbenchmark/models/railway-'+scenario+'-'+str(size)+'-inferred.ttl'

            uri=RDF.Uri(string="file:"+test_file)

            parser=RDF.Parser('turtle')
            if parser is None:
              raise Exception("Failed to create RDF.Parser raptor")

            count=0
            start_time=time.time()
            for s in parser.parse_as_stream(uri,uri):
              model.add_statement(s)
              count=count+1
            read_time=int(round((time.time()-start_time)*1000000000))
            #print "Parsing added",count,"statements"



            for query in config["queries"]:
              queryPath="../trainbenchmark/queries/"+query+".sparql"
              f = open(queryPath, 'r')
              q = RDF.Query(f.read())

              print "Query for", query, "in", test_file

              start_time=time.time()
              result = q.execute(model)
              check_time=int(round((time.time()-start_time)*1000000000))
              print "Duration for this query: ",check_time,"nanoseconds\n"

              count=0
              for results in result:
                  count=count+1

              #   print "{"
              #   for k in results:
              #     print "  "+k+" = "+str(results[k])
              #   print "}"
              # print "Query for",query,"ended\n"
              # print "Duration for this query: ",end_time,"seconds\n"

              resultWriter.writerow([query, str(1), 'Time', str(read_time), 'Read', str(1), scenario, str(1), str(size), 'Redland'])
              resultWriter.writerow([query, str(1), 'Time', str(check_time), 'Check', str(1), scenario, str(1), str(size), 'Redland'])
              resultWriter.writerow([query, str(1), 'Matches', str(count), 'Check', str(1), scenario, str(1), str(size), 'Redland'])

            size=size*2

            # Use any rdf/xml parser that is available
            #serializer=RDF.Serializer()
            #serializer.set_namespace("dc", RDF.Uri("http://purl.org/dc/elements/1.1/"))
            #serializer.serialize_model_to_file("test-out.rdf", model)

            #print "Serialized to ntriples as a string size",len(model.to_string(name="ntriples", base_uri="http://example.org/base#")),"bytes"

            #print "Done"
