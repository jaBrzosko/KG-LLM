from client import get_knowledge_graph
import ontology_parser as op
import ontology_formatter as of
import openai_parser as oap
import datetime

def main():
    # buildings()
    curie()

def buildings():
    text_to_extract = "Smith's apartment is in a Osiedle Majdańska building. They live in South Praga"
    
    cnc, pnc = op.parse('ontologies/bot.ttl', "https://w3id.org/bot")
    formatted_ontology = of.format(cnc, pnc, "https://w3id.org/bot", "bot")

    graph = get_knowledge_graph(formatted_ontology, "bot", text_to_extract)
    print(graph)

    rdf_graph = op.parse_openai(graph)
    print(rdf_graph)

def curie():
    namespace = "http://www.semanticweb.org/ontologies/2024/11/curie"
    prefix = "cur"
    text_to_extract = """
        Marie Curie, 7 November 1867 - 4 July 1934, was a Polish and naturalised-French physicist and chemist who conducted pioneering research on radioactivity.
        She was the first woman to win a Nobel Prize, the first person to win a Nobel Prize twice, and the only person to win a Nobel Prize in two scientific fields.
        Her husband, Pierre Curie, was a co-winner of her first Nobel Prize, making them the first-ever married couple to win the Nobel Prize and launching the Curie family legacy of five Nobel Prizes.
        She was, in 1906, the first woman to become a professor at the University of Paris.
        """
    
    namespaces = {
        prefix: f"{namespace}#",
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#"
    }
    
    cnc, pnc = op.parse('ontologies/curie.ttl', namespace)
    formatted_ontology = of.format(cnc, pnc, namespace, prefix)

    graph = get_knowledge_graph(formatted_ontology, prefix, text_to_extract, v4=False)
    print(graph)
    
    rdf_graph = oap.parse_openai(graph, namespaces)
    print(rdf_graph)

    file_path = f'output/curie_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.ttl'
    rdf_graph.serialize(destination=file_path, format='turtle')

if __name__ == '__main__':
    main()
