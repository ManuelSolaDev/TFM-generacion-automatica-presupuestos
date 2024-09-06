from langchain_openai import ChatOpenAI
from utils.helper_functions import load_config
import os
from openai import OpenAI

config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
load_config(config_path)


def get_open_ai(temperature=0, model='gpt-4o-mini'):

    llm = ChatOpenAI(
    model=model,
    temperature = temperature,
)
    return llm

def get_open_ai_json(temperature=0, model='gpt-4o-mini'):
    # Cambiar esto por with_structured_output
    llm = ChatOpenAI(
    model=model,
    temperature = temperature,
    model_kwargs={"response_format": {"type": "json_object"}},
)
    return llm

def get_open_ai_with_structured_output(temperature=0, model='gpt-4o-mini', pydantic_model=None):
    llm = ChatOpenAI(
        model=model,
        temperature = temperature,
    )
    return llm.with_structured_output(pydantic_model)

def get_open_ai_audio():

    llm = OpenAI()
    return llm
