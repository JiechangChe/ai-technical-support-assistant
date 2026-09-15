import json

from ai.llm import llm_client


JUDGE_PROMPT = """
你是一个技术支持知识库匹配判断器。

你的任务是判断：
“提供的知识库内容，是否与用户的问题匹配，并且能够作为回答该问题的可靠依据？”

判断标准：

1. 如果知识库内容直接解决了用户的问题，回答 YES。
2. 如果知识库内容虽然没有提供完整的操作步骤，但与用户询问的是同一个具体业务问题，并且能够作为回答依据，回答 YES。
3. 不要求知识库必须逐字回答用户的问题，也不要求知识库必须包含完整的操作路径。
4. 如果知识库只是与用户问题存在表面上的关键词或主题相似，但实际上解决的是不同的问题，回答 NO。
5. 如果知识库只涉及用户问题的一个不同原因、不同场景或不同功能，且不足以支持回答用户的问题，回答 NO。
6. 如果用户的问题明显超出知识库内容能够支持的范围，回答 NO。
7. 只能根据提供的知识库内容进行判断，不要使用外部知识。
8. 不要因为关键词相似就直接判断 YES，要考虑用户实际想解决的问题是否与知识库内容一致。

例如：

用户：
“第一次登录系统的时候，在哪里改密码？”

知识库：
“系统能不能设置首次登录账号的时候强制需要更改密码呢”

判断：
YES

原因：
两者都涉及首次登录时的密码修改/密码策略，属于同一个具体业务问题。虽然知识库没有完整的操作路径，但可以作为回答该问题的相关依据。

另一个例子：

用户：
“ERP系统登录不了怎么办”

知识库：
“系统提示登录失败，客户端登录地点错误”

判断：
NO

原因：
知识库只描述了一种特定的登录地点错误，并不能支持回答一般性的 ERP 登录失败问题。

请严格输出 JSON，不要输出 Markdown，不要使用 ```json 或其他代码块：

{
  "answerable": true,
  "reason": "简短说明为什么这些知识能够或不能作为回答该问题的可靠依据"
}
"""


def build_judge_prompt(
    query: str,
    documents: list,
) -> str:
    knowledge_text = []

    for index, document in enumerate(
        documents,
        start=1,
    ):
        question = document["metadata"].get(
            "question",
            "",
        )

        answer = document["document"]

        knowledge_text.append(
            f"""
知识 {index}：
问题：{question}
内容：
{answer}
"""
        )

    return (
        JUDGE_PROMPT
        + "\n\n用户问题：\n"
        + query
        + "\n\n候选知识库内容：\n"
        + "\n".join(knowledge_text)
    )


def judge_answerability(
    query: str,
    documents: list,
) -> dict:
    prompt = build_judge_prompt(
        query,
        documents,
    )

    messages = [
        {
            "role": "user",
            "content": prompt,
        }
    ]

    response = llm_client.generate(messages)

    cleaned_response = response.strip()

    # Handle Markdown code fences even if the model
    # ignores the JSON-only instruction.
    if cleaned_response.startswith("```"):
        lines = cleaned_response.splitlines()

        if lines and lines[0].startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        cleaned_response = "\n".join(lines).strip()

    try:
        result = json.loads(cleaned_response)

        return {
            "answerable": bool(
                result["answerable"]
            ),
            "reason": result.get(
                "reason",
                "",
            ),
        }

    except (
        json.JSONDecodeError,
        KeyError,
        TypeError,
    ):
        return {
            "answerable": None,
            "reason": response,
        }