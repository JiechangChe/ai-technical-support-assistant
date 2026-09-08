from openai import OpenAI

from core.config import settings

class LLMClient:
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.siliconflow_api_key,
            base_url=settings.llm_base_url,
        )

    def generate(
        self, 
        messages: list[dict[str, str]],
    ) -> str:
        response = self.client.chat.completions.create(
            model=settings.llm_model,
            messages=messages,
            stream=False,
            temperature=0.2, #more stable output
            max_tokens=300, #specific range of output
        )

        print(response)
        
        return response.choices[0].message.content

llm_client = LLMClient()