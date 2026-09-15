from ai.llm import llm_client
from ai.prompts import SYSTEM_PROMPT
from ai.judge import judge_answerability
from knowledge.retrieval import retrieve_documents


FALLBACK_RESPONSE = (
    "我目前没有在知识库中找到能够直接解决这个问题的相关信息。"
    "请提供更具体的报错信息或问题场景，我可以进一步帮你排查。"
)


def generate_response(messages):
    # Get the latest user question.
    user_message = next(
        (
            message["content"]
            for message in reversed(messages)
            if message["role"] == "user"
        ),
        "",
    )

    # Retrieve the most relevant knowledge.
    documents = retrieve_documents(
        user_message,
        k=30,
        top_k=3,
    )

    # Verify whether the retrieved knowledge is
    # actually sufficient to answer the question.
    judge_result = judge_answerability(
        user_message,
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