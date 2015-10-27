#!/usr/bin/python


import RDF
import yaml
import time

storage=RDF.Storage(storage_name="hashes",
                    name="test",
                    options_string="new='yes',hash-type='memory',dir='.'")
if storage is None:
  raise Exception("new RDF.Storage failed")



model=RDF.Model(storage)
if model is None:
  raise Exception("new RDF.model failed")

with open("config.yml", 'r') as stream:
        config = yaml.load(stream)

size=config["minsize"]
while (size<=config["maxsize"]):
    test_file='../models/railway-repair-'+str(size)+'-inferred.ttl'

    print "Parsing URI (file)", test_file
    uri=RDF.Uri(string="file:"+test_file)

    parser=RDF.Parser('turtle')
    if parser is None:
      raise Exception("Failed to create RDF.Parser raptor")

    count=0
    for s in parser.parse_as_stream(uri,uri):
      model.add_statement(s)
      count=count+1

    #print "Parsing added",count,"statements"



    for query in config["queries"]:
      queryPath="../queries/"+query+".sparql"
      f = open(queryPath, 'r')
      q = RDF.Query(f.read())

      print "Query for", query, "in", test_file

      start_time=time.time()
      result = q.execute(model)
      end_time=time.time()-start_time
      print "Duration for this query: ",end_time,"seconds\n"

      #for results in result:
      #  print "{"
      #  for k in results:
      #    print "  "+k+" = "+str(results[k])
      #  print "}"
      #print "Query for",query,"ended\n"
      #print "Duration for this query: ",end_time,"seconds\n"
    size=size*2

    # Use any rdf/xml parser that is available
    #serializer=RDF.Serializer()
    #serializer.set_namespace("dc", RDF.Uri("http://purl.org/dc/elements/1.1/"))
    #serializer.serialize_model_to_file("test-out.rdf", model)

    #print "Serialized to ntriples as a string size",len(model.to_string(name="ntriples", base_uri="http://example.org/base#")),"bytes"

    #print "Done"
