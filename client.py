import os
from openai import AzureOpenAI
from dotenv import load_dotenv

def get_knowledge_graph(ontology, main_prefix, text, v4 = False):
    client, deployment_name = get_client_and_deployment(v4)
    print(f"Using deployment: {deployment_name}")

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
        model=deployment_name,
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

def get_subjects(classess_ontology, text):
    client, deployment_name = get_client_and_deployment(False)
    subjects = []
    system_prompt = f"""
        You are a professional Knowledge Graph Expert. You have been hired to extract the subjects from
        the given text while using the provided ontology. The returned format should be ONLY a JSON list of subjects.
        Extract entities who are instances of the classes in the ontology.
        Don't repeat the ontology, give real representations of the classes.
        Provide just the names that represent the subjects in PascalCase.
        Don't return anything else besides the JSON list.
        You must only use the following ontology:
        {classess_ontology}
        """
    
    completion = client.chat.completions.create(
        model=deployment_name,
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

def get_properties(properties_ontology, subjects, text, main_prefix):
    client, deployment_name = get_client_and_deployment(False)
    properties = []

    system_prompt = f"""
        You are a professional Knowledge Graph Expert. You have been hired to extract information from
        a text document and sample it into format that can be used to create a knowledge graph. The returned format
        should be ONLY a JSON list of dictionaries, where each dictionary represents a node in the knowledge graph.
        Don't return anything else besides the JSON list.
        Each dictionary should have `subject`, `predicate`, and `object` keys.
        You must only use the following ontology for properties:
        {properties_ontology}
        Extract only properties that are related to those subjects:
        {subjects}
        You cannot add any additional information that is not present in the text document.
        Do not repeat ontology, return only new triples.
        USE the namespaces for the properties.
        If the object is not a literal use main prefix {main_prefix} for the subject from provided subjects.
    """

    completion = client.chat.completions.create(
        model=deployment_name,
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

def get_subject_classess(subjects, classess_ontology, text):
    client, deployment_name = get_client_and_deployment(False)
    properties = []

    system_prompt = f"""
        You are a professional Knowledge Graph Expert. You have been hired to annonate the subjects from text
        with appropriate classes from the ontology. The returned format should be ONLY a JSON list of dictionaries,
        each dictionary should have `subject` and `class` keys.
        Don't return ANYTHING ELSE BESIDES the JSON list.
        You must only use the following ontology for classes:
        {classess_ontology}
        Annotate the subjects with the appropriate classes:
        {subjects}
        You cannot add any additional information that is not present in the text document.
        Do not make annotations that don't make logical sense.
        Ignore the subjects that don't have a class in the ontology.
        Maintatin the classess namespaces.
    """

    completion = client.chat.completions.create(
        model=deployment_name,
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


def get_client_and_deployment(v4):
    load_dotenv()
    if v4:
        client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY_V4"),  
            api_version=os.getenv("AZURE_OPENAI_VERSION_V4"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT_V4")
        )
        deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME_V4")
    else:
        client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
            api_version=os.getenv("AZURE_OPENAI_VERSION"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
        deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

    return client, deployment
