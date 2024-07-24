from termcolor import colored
from models.openai_models import get_open_ai, get_open_ai_json
from prompts.prompts import (
    normalizer_prompt_template
)
from states.state import AgentGraphState

# Base class for all agents
class Agent:
    def __init__(self, state: AgentGraphState, model=None, server=None, temperature=0, model_endpoint=None, stop=None, guided_json=None):
        """
        Initializes the agent with the graph state and configuration parameters for the language model.

        Args:
            state (AgentGraphState): The current state of the agent graph.
            model (str): The language model to be used.
            server (str): The server where the model is hosted.
            temperature (float): The temperature parameter for the language model.
            model_endpoint (str): The endpoint of the model.
            stop (list): Tokens or phrases to stop text generation.
            guided_json (dict): JSON schema guiding the structure of the responses.
        """
        self.state = state
        self.model = model
        self.server = server
        self.temperature = temperature
        self.model_endpoint = model_endpoint
        self.stop = stop
        self.guided_json = guided_json

    def get_llm(self, json_model=True):
        """
        Gets an instance of the language model from the specified server.

        Args:
            json_model (bool): Indicates if the model returns JSON responses.

        Returns:
            A configured language model object.
        """
        if self.server == 'openai':
            return get_open_ai_json(model=self.model, temperature=self.temperature) if json_model else get_open_ai(model=self.model, temperature=self.temperature)     

    def update_state(self, key, value):
        """
        Updates the graph state with a new value for a specific key.

        Args:
            key (str): The state key to update.
            value (Any): The new value for the key.
        """
        self.state = {**self.state, key: value}

# Agent for routing research questions
class NormalizerAgent(Agent):
    def invoke(self, todo_file, prompt=normalizer_prompt_template):
        """
        Invokes the language model to determine the classification of the research question.

        Args:
            research_question (str): The research question to classify.
            prompt (str): The prompt template to use.

        Returns:
            The updated state of the graph.
        """
        normalizer_prompt = prompt.format(
        )
        messages = [
            {"role": "system", "content": normalizer_prompt},
            {"role": "user", "content": f"todo_file: {todo_file}"}
        ]

        llm = self.get_llm()
        ai_msg = llm.invoke(messages)
        response = ai_msg.content

        self.update_state("normalizer_response", response)
        print(colored(f"Normalizer 🧭: {response}", 'cyan'))
        return self.state


# Agent to mark the end of the processing chain
class EndNodeAgent(Agent):
    def invoke(self):
        """
        Marks the end of the processing chain by updating the graph state.

        Returns:
            The updated state of the graph.
        """
        self.update_state("end_chain", "end_chain")
        return self.state
