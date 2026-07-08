from datetime import datetime
from openai import OpenAI

from config import settings
from typing import Callable

def get_current_time() -> str:
    """
    Returns the current date and time.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

TOOLS: dict[str, Callable] = {
    "get_current_time": get_current_time,
}


client = OpenAI(
    api_key=settings.OPENAI_API_KEY
)

tools = [
    {
        "type": "function",
        "name": "get_current_time",
        "description": "Returns the current date and time.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    }
]

response = client.responses.create(
    model=settings.MODEL_NAME,
    input="What time is it right now?",
    tools=tools,
)

print(response.output)

tool_call = response.output[0]

tool_function = TOOLS.get(tool_call.name)

if tool_function is None:
    raise ValueError(
        f"Unknown tool: {tool_call.name}"
    )

result = tool_function()

follow_up = client.responses.create(
    model=settings.MODEL_NAME,
    previous_response_id=response.id,
    input=[
        {
            "type": "function_call_output",
            "call_id": tool_call.call_id,
            "output": result,
        }
    ],
)

print("\nFinal Response:\n")
print(follow_up.output_text)