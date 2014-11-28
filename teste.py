from rdflib import *
from rdflib.namespace import RDF, FOAF

g = Graph()
result = g.parse("nova_ontologia_rdf.owl", format='xml')

print ("a ontologia tem %s statements" % len(g))

professor = URIRef("&renata;FOAF-modified#Professor")
#fulano = BNode()
#g.add ((fulano, RDF.type, FOAF.Person))
for triple in g.triples((None, RDF.type, FOAF.Person)):
    print (triple)
#print (g.serialize("teste.owl", format='xml'))
