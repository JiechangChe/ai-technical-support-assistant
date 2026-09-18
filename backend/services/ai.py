from ai.llm import llm_client
from ai.prompts import (
    SYSTEM_PROMPT,
    QUERY_REWRITE_PROMPT,
)
from ai.judge import judge_answerability
from knowledge.retrieval import retrieve_documents


FALLBACK_RESPONSE = (
    "我目前没有在知识库中找到能够直接解决这个问题的相关信息。"
    "请提供更具体的报错信息或问题场景，我可以进一步帮你排查。"
)

def rewrite_query(messages):
    """
    Rewrite the latest user question into a
    self-contained query using conversation history.
    """

    if not messages:
        return ""

    latest_user_message = next(
        (
            message["content"]
            for message in reversed(messages)
            if message["role"] == "user"
        ),
        "",
    )

    previous_messages = messages[:-1]

    if not previous_messages:
        return latest_user_message

    history_text = "\n".join(
        f"{message['role']}: {message['content']}"
        for message in previous_messages
    )

    prompt = (
        QUERY_REWRITE_PROMPT
        + "\n\n对话历史：\n"
        + history_text
        + "\n\n当前用户问题：\n"
        + latest_user_message
    )

    response = llm_client.generate(
        [
            {
                "role": "user",
                "content": prompt,
            }
        ]
    )

    return response.strip()

def generate_response(messages):
# Rewrite the latest user question using
    # the conversation history.
    search_query = rewrite_query(messages)

    # Retrieve relevant knowledge using
    # the rewritten query.
    documents = retrieve_documents(
        search_query,
        k=30,
        top_k=3,
    )

    # Check whether the retrieved knowledge
    # can actually answer the question.
    judge_result = judge_answerability(
        search_query,
        documents,
    )

    if judge_result["answerable"] is not True:
        return FALLBACK_RESPONSE

    # Generate the final answer using the conversation
    # history together with the retrieved knowledge.
    knowledge_context = "\n\n".join(
        document["document"]
        for document in documents
    )

    llm_messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "system",
            "content": (
                "以下是从技术支持知识库中检索到的相关信息。"
                "请优先根据这些信息回答用户问题，"
                "不要编造知识库中不存在的解决方案。\n\n"
                f"{knowledge_context}"
            ),
        },
        *messages,
    ]

    return llm_client.generate(llm_messages)