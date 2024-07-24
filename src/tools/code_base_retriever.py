from states.state import AgentGraphState
import os
def code_base_retriever(directory_path: str, state: AgentGraphState) -> dict:
    """
    Read all files in the given directory and store their content in the state.

    Args:
        directory_path (str): The path to the code base directory.
        state (AgentGraphState): The current state of the agent graph.

    Returns:
        dict: The updated state with the codebase content.
    """
    codebase_content = {"files": []}
    for root, _, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    codebase_content["files"].append({
                        "path": file_path,
                        "content": content
                    })
                    print(f"Read file: {file_path}")  # Debugging statement
            except UnicodeDecodeError:
                print(f"Skipping binary or non-UTF-8 file: {file_path}")

    state["codebase_content"] = codebase_content
    print("Codebase content updated.")
    print(codebase_content)
    # Return the updated state
    return {"codebase_content": state["codebase_content"]}