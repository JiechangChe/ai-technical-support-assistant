from ai.llm import llm_client
from ai.prompts import SYSTEM_PROMPT

def generate_response(
    messages: list[dict[str, str]],
) -> str:
    llm_messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        #add conversation history after system prompt
        *messages,
    ]
    return llm_client.generate(llm_messages)