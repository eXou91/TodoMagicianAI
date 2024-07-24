import json
from states.state import AgentGraphState
from langchain_core.messages import HumanMessage

# Function to update the number of tasks in the state
def update_tasks_number(state: AgentGraphState, normalizer_responses: dict) -> dict:
    """
    Update the tasks_number in the agent graph state based on the normalizer response.

    Args:
        normalizer_response (dict): The latest normalizer response containing the tasks.
        state (AgentGraphState): The current state of the agent graph.

    Returns:
        dict: The updated state with the tasks_number.
    """
    tasks_count = 0
    if normalizer_responses:
        for response in normalizer_responses:
            if isinstance(response, HumanMessage):
                # Décoder le contenu JSON de la réponse HumanMessage
                try:
                    response_content = json.loads(response.content)
                    if "tasks" in response_content:
                        tasks_count += len(response_content["tasks"])
                except json.JSONDecodeError:
                    print(f"Error decoding JSON from response: {response.content}")
        state["tasks_number"] = tasks_count
        print("Tasks number updated:", state["tasks_number"])
    else:
        print("No tasks found in normalizer responses.")
    
    # Return the updated state
    return {"tasks_number": state["tasks_number"]}
