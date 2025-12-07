from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings


model_names = ["gpt-4o", "gpt-4o-mini", "o1-preview", "o3-mini"]
costmap_in = {
    "gpt-4o": 2.50 / 1000000,
    "gpt-4o-mini": 0.150 / 1000000,
    "o1-preview": 15.00 / 1000000,
    "o3-mini": 3.00 / 1000000
}

costmap_out = {
    "gpt-4o": 10.00/ 1000000,
    "gpt-4o-mini": 0.6 / 1000000,
    "o1-preview": 60.00 / 1000000,
    "o1-mini": 12.00 / 1000000,
}

def get_model(model_name):
    if model_name not in model_names:
        raise ValueError(f"Model {model_name} is not supported")
    
    llm = ChatOpenAI(
        model_name=model_name,
        temperature=0
    )
    return llm
