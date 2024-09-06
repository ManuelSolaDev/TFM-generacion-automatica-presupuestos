from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages


class AgentGraphState(TypedDict):
    user_input: str
    audio_transcription: str
    cleaned_audio_transcription: str
    functional_requirements: str
    budget: str
    end_chain: Annotated[list, add_messages]

# Define the nodes in the agent graph
def get_agent_graph_state(state:AgentGraphState, state_key:str):

    
    if state_key == "user_input":
        return state["user_input"]
    
    elif state_key == "audio_transcription":
        return state["audio_transcription"]
    
    elif state_key == "cleaned_audio_transcription":
        return state["cleaned_audio_transcription"]
    
    elif state_key == "functional_requirements":
        return state["functional_requirements"]
    
    elif state_key == "budget":
        return state["budget"]
        
    else:
        return None
    
state = {
    "user_input":"",
    "audio_transcription":"",
    "cleaned_audio_transcription":"",
    "functional_requirements":"",
    "budget":"",
    "end_chain": []
}