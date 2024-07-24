from typing import TypedDict, Annotated, List, Union
from langgraph.graph.message import add_messages

# Define the state object for the agent graph
class AgentGraphState(TypedDict):
    todo_file: str
    normalizer_response: Annotated[List[dict], add_messages]
    tasks_number: int
    end_chain: Annotated[List[dict], add_messages]

# Function to get the agent graph state based on a state key
def get_agent_graph_state(state: AgentGraphState, state_key: str) -> Union[dict, List[dict], None]:
    """
    Retrieve a specific part of the agent graph state based on the provided state_key.

    Args:
        state (AgentGraphState): The current state of the agent graph.
        state_key (str): The key indicating which part of the state to retrieve.

    Returns:
        Union[dict, List[dict], None]: The requested part of the state, or None if the key is invalid.
    """
    state_mapping = {
        "normalizer_all": state["normalizer_response"],
        "normalizer_latest": state["normalizer_response"][-1] if state["normalizer_response"] else None,
        "tasks_number": state["tasks_number"]
    }
    return state_mapping.get(state_key, None)

# Initialize the state with default values
state: AgentGraphState = {
    "todo_file": "",
    "normalizer_response": [],
    "tasks_number": 0,
    "end_chain": []
}