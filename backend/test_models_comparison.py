from openai import OpenAI

from core.config import settings


client = OpenAI(
    api_key=settings.siliconflow_api_key,
    base_url=settings.llm_base_url,
)


MODELS = [
    "deepseek-ai/DeepSeek-V3.2",
    "Qwen/Qwen3-32B",
    "zai-org/GLM-5.2",
    "deepseek-ai/DeepSeek-V4-Flash",
]


SYSTEM_PROMPT = """
你是一名专业的技术支持助手。

你的任务是直接回答用户的问题，并提供清晰、实用的故障排查步骤。

要求：
- 只回答用户当前的问题。
- 不要模拟用户或其他角色。
- 不要输出“用户：”或“助手：”等角色标签。
- 不要编造不存在的信息。
- 如果缺少解决问题所需要的信息，可以向用户提出简短的问题。
- 回答应该清晰、简洁、专业。
"""


USER_MESSAGE = """
安装公司内部软件后，启动时出现“Database connection failed”错误，我应该如何排查？
"""


for model in MODELS:
    print("\n" + "=" * 80)
    print(f"MODEL: {model}")
    print("=" * 80)

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": USER_MESSAGE,
                },
            ],
            temperature=0.2,
            max_tokens=300,
            stream=False,
        )

        message = response.choices[0].message.content
        finish_reason = response.choices[0].finish_reason

        print(f"finish_reason: {finish_reason}")
        print("\nANSWER:")
        print(message)

    except Exception as e:
        print(f"ERROR: {e}")