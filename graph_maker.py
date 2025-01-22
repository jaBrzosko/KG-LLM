import rdflib

def make_graph(namespace, subjects_with_classes, subject_properties, output_file):
    graph = rdflib.Graph()

    rdf_subjects = {}

    # Process classes
    for dictionary in subjects_with_classes:
        rdf_subject = dictionary["subject"]
        rdf_class = dictionary["class"]
            
        if rdf_subject not in rdf_subjects:
            if rdf_subject.startswith("http"):
                rdf_subjects[rdf_subject] = rdflib.URIRef(rdf_subject)
            else:
                rdf_subjects[rdf_subject] = rdflib.URIRef(f"{namespace}#{rdf_subject.replace(' ', '')}")
            graph.add((rdf_subjects[rdf_subject], rdflib.RDF.type, rdflib.URIRef(rdf_class)))

    # Process properties
    for prop in subject_properties:
        subject = prop["subject"]
        predicate = prop["predicate"]
        obj = prop["object"]

        if subject not in rdf_subjects:
            rdf_subjects[subject] = rdflib.URIRef(f"{namespace}#{subject.replace(' ', '')}")

        if obj in rdf_subjects:
            graph.add((rdf_subjects[subject], rdflib.URIRef(predicate), rdf_subjects[obj]))
        elif obj.startswith("http"):
            obj_rdflib = rdflib.URIRef(f"{namespace}#{obj.replace(' ', '')}")
            rdf_subjects[obj] = obj_rdflib
            graph.add((rdf_subjects[subject], rdflib.URIRef(predicate), obj_rdflib))
        else:
            graph.add((rdf_subjects[subject], rdflib.URIRef(predicate), rdflib.Literal(obj)))

    graph.serialize(destination=output_file, format='turtle')
