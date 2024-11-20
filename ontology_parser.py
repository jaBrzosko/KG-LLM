import rdflib

CLASS_TYPES = [rdflib.OWL.Class]
PROPERTY_TYPES = [rdflib.OWL.ObjectProperty]
RDF_TYPE = rdflib.RDF.type
RDF_COMMENT = rdflib.RDFS.comment

def parse(turtle_file_path, base_namespace, base_lang="en"):
    g = rdflib.Graph()
    g.parse(turtle_file_path, format='turtle')

    cnc = _get_classess_with_comments(g, base_namespace, base_lang)
    pnc = _get_properties_with_comments(g, base_namespace, base_lang)

    return cnc, pnc

def _get_classess_with_comments(graph, base_namespace, base_lang):
    return _extract_types_with_comments(graph, CLASS_TYPES, base_namespace, base_lang)

def _get_properties_with_comments(graph, base_namespace, base_lang):
    return _extract_types_with_comments(graph, PROPERTY_TYPES, base_namespace, base_lang)

def _extract_types_with_comments(graph, types, base_namespace, base_lang):
    objects = []
    for object_type in types:
        for s, _, _ in graph.triples((None, RDF_TYPE, object_type)):
            if str(s).startswith(base_namespace):
                objects.append(s)

    comments = []
    for c in objects:
        best_match = None
        for _, _, comment in graph.triples((c, RDF_COMMENT, None)):
            lang = comment.language
            if best_match is None or lang == base_lang:
                best_match = comment

        comments.append((c, best_match))

    return comments
