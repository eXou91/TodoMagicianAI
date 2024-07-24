from graph import create_graph, compile_workflow

server = 'openai'
model = 'gpt-3.5-turbo'
model_endpoint = None

### VLLM CONFIG
# server = 'vllm'
# model = 'meta-llama/Meta-Llama-3-70B-Instruct' # full HF path
# model_endpoint = 'https://kcpqoqtjz0ufjw-8000.proxy.runpod.net/' 
# #model_endpoint = runpod_endpoint + 'v1/chat/completions'
# stop = "<|end_of_text|>"


def read_todo_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def main(todo_file_path, verbose=False):
    print("Creating graph and compiling workflow...")
    graph = create_graph(server=server, model=model, model_endpoint=model_endpoint)
    workflow = compile_workflow(graph)
    print("Graph and workflow created.")

    # Lire le fichier TODO
    todo_content = read_todo_file(todo_file_path)

    # Passer le contenu du fichier TODO au workflow
    dict_inputs = {"todo_file": todo_content}

    for event in workflow.stream(dict_inputs):
        if verbose:
            print("\nState Dictionary:", event)
        else:
            print("\n")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_todo_file>")
    else:
        todo_file_path = sys.argv[1]
        main(todo_file_path)