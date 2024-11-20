import json
import rdflib

def parse_openai(response_json, namespaces):
    if '```' in response_json and len(response_json.split('```')) > 1:
        print(response_json.split('```'))
        response_json = response_json.split('```')[1]
    triples = json.loads(response_json)

    g = rdflib.Graph()
    for triple in triples:
        subject = triple["subject"]
        predicate = triple["predicate"]
        obj = triple["object"]

        if ":" in subject:
            subject_prefix = subject.split(":")[0].strip()
            subject_name = subject.split(":")[1]
            subject_triplet = rdflib.URIRef(namespaces[subject_prefix] + subject_name)
        else:
            subject_triplet = rdflib.Literal(subject)

        if ":" in predicate:
            predicate_prefix = predicate.split(":")[0].strip()
            predicate_name = predicate.split(":")[1]
            predicate_triplet = rdflib.URIRef(namespaces[predicate_prefix] + predicate_name)
        else:
            predicate_triplet = rdflib.Literal(predicate)

        if ":" in obj:
            obj_prefix = obj.split(":")[0].strip()
            obj_name = obj.split(":")[1]
            obj_triplet = rdflib.URIRef(namespaces[obj_prefix] + obj_name)
        else:
            obj_triplet = rdflib.Literal(obj)

        g.add((subject_triplet, predicate_triplet, obj_triplet))
        
    return g
