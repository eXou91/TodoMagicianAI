normalizer_prompt_template = """
You are a task reformatter agent. Your task is to reformat a user given TODO list into a consistent JSON format. Each task should include a title, description, and priority.

Your response should be in the following JSON format:
    "title": "Task title",
    "description": "Detailed task description",
    "priority": "High" or "Medium" or "Low" or "Future"

"""


normalizer_guided_json = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "description": "A concise title for the task"
            },
            "description": {
                "type": "string",
                "description": "A detailed description of the task"
            },
            "priority": {
                "type": "string",
                "description": "The priority of the task",
                "enum": ["High", "Medium", "Low", "Future"]
            }
        },
        "required": ["title", "description", "priority"]
    }
}