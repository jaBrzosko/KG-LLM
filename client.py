import os
from openai import AzureOpenAI
from dotenv import load_dotenv

def get_knowledge_graph(ontology, main_prefix, text):
    load_dotenv()    
    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
        api_version=os.getenv("AZURE_OPENAI_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
    )

    system_prompt = f"""
        You are a professional Knowledge Graph Expert. You have been hired to extract information from
        a text document and sample it into format that can be used to create a knowledge graph. The returned format
        should be ONLY a JSON list of dictionaries, where each dictionary represents a node in the knowledge graph.
        Don't return anything else besides the JSON list.
        Each dictionary should have `subject`, `predicate`, and `object` keys.
        You must only use the following ontology:
        {ontology}
        You must use `{main_prefix}` as the main prefix for the subject and object fields.
        You can use `rdf:type` as the predicate for the type of the subject.
        You cannot add any additional information that is not present in the text document.
        Do not repeat ontology, return only new triples.
    """

    completion = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": f"Please extract the information from the following text: {text}",
            },
        ],
    )

    return completion.choices[0].message.content
