import json
from langchain_core.runnables import RunnableLambda
from langgraph.graph import StateGraph, END
from agents.agents import (
    NormalizerAgent,
    EndNodeAgent
)
from prompts.prompts import (
    normalizer_prompt_template,
    normalizer_guided_json,

)

from states.state import AgentGraphState, get_agent_graph_state, state
from tools.update_tasks_number import update_tasks_number
def create_graph(server=None, model=None, stop=None, model_endpoint=None, temperature=0):
    """
    Creates and configures the state graph for processing research questions.

    Args:
        server (str): The server where the model is hosted.
        model (str): The language model to be used.
        stop (list): Tokens or phrases to stop text generation.
        model_endpoint (str): The endpoint of the model.
        temperature (float): The temperature parameter for the language model.

    Returns:
        StateGraph: The configured state graph.
    """
    # Initialize the state graph with the AgentGraphState
    graph = StateGraph(AgentGraphState)

    # Add the NormalizerAgent node
    graph.add_node(
        "normalizer", 
        lambda state: NormalizerAgent(
            state=state,
            model=model,
            server=server,
            guided_json=normalizer_guided_json,
            stop=stop,
            model_endpoint=model_endpoint,
            temperature=temperature
        ).invoke(
            todo_file=state["todo_file"],
            prompt=normalizer_prompt_template
        )
    )
    # Add the cluster context retriever tool node
    graph.add_node(
        "update_tasks_number_tool",
        lambda state: update_tasks_number(state, get_agent_graph_state(state, "normalizer_all"))
    )

    # Add the EndNodeAgent node
    graph.add_node("end", lambda state: EndNodeAgent(state).invoke())

    # Configure the edges of the graph to define the workflow
    graph.set_entry_point("normalizer")
    graph.set_finish_point("end")


    ## general branch
    graph.add_edge("normalizer", "update_tasks_number_tool")
    graph.add_edge("update_tasks_number_tool", "end")

    return graph
    
def compile_workflow(graph):
    """
    Compiles the state graph into a workflow.

    Args:
        graph (StateGraph): The state graph to be compiled.

    Returns:
        Workflow: The compiled workflow.
    """
    workflow = graph.compile()
    return workflow
