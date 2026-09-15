from services.ai import generate_response


messages = [
    {
        "role": "user",
        "content": "ERP系统登录不了怎么办",
    }
]


response = generate_response(messages)

print("=" * 60)
print("RAG Test")
print("=" * 60)

print("\nUser:")
print(messages[-1]["content"])

print("\nAssistant:")
print(response)