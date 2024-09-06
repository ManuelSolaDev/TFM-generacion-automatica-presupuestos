from langgraph.graph import StateGraph
from agents.agents import (
    TranscriberAgent,
    CleanerAgent,
    FunctionalRequirementsDefinerAgent,
    BudgeterAgent,
    EndNodeAgent
)
from prompts.prompts import (
    cleaner_prompt_template, 
    functional_requirements_definer_prompt_template,
    budgeter_prompt_template,

)
from states.state import AgentGraphState, get_agent_graph_state, state

def create_graph(server=None, model=None, temperature=0):
    graph = StateGraph(AgentGraphState)

    graph.add_node(
        "transcriber", 
        lambda state: TranscriberAgent(
            state=state,
            model=model,
            server=server,
            temperature=temperature
        ).invoke(
            user_input=state["user_input"]
        )
    )

    graph.add_node(
        "cleaner",
        lambda state: CleanerAgent(
            state=state,
            model=model,
            server=server,
            temperature=temperature
        ).invoke(
            user_input=state["user_input"],
            audio_transcription=lambda: get_agent_graph_state(state=state, state_key="audio_transcription"),
            feedback=lambda: get_agent_graph_state(state=state, state_key="reviewer_latest"),
            prompt=cleaner_prompt_template,
        )
    )

    graph.add_node(
        "functional_requirements_definer",
        lambda state: FunctionalRequirementsDefinerAgent(
            state=state,
            model=model,
            server=server,
            temperature=temperature
        ).invoke(
            user_input=state["user_input"],
            cleaned_audio_transcription=lambda: get_agent_graph_state(state=state, state_key="cleaned_audio_transcription"),
            feedback=lambda: get_agent_graph_state(state=state, state_key="reviewer_latest"),
            prompt=functional_requirements_definer_prompt_template,
        )
    )

    graph.add_node(
        "budgeter",
        lambda state: BudgeterAgent(
            state=state,
            model=model,
            server=server,
            temperature=temperature
        ).invoke(
            user_input=state["user_input"],
            functional_requirements=lambda: get_agent_graph_state(state=state, state_key="functional_requirements"),
            feedback=lambda: get_agent_graph_state(state=state, state_key="reviewer_latest"),
            prompt=budgeter_prompt_template,
        )
    )

    graph.add_node("end", lambda state: EndNodeAgent(state).invoke())


    # Add edges to the graph
    graph.set_entry_point("transcriber")
    graph.set_finish_point("end")
    graph.add_edge("transcriber", "cleaner")
    graph.add_edge("cleaner", "functional_requirements_definer")
    graph.add_edge("functional_requirements_definer", "budgeter")
    graph.add_edge("budgeter", "end")

    return graph

def compile_workflow(graph):
    workflow = graph.compile()

    return workflow
