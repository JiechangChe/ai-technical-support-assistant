from ai.judge import judge_answerability


documents = [
    {
        "document": """
【问题】新创建的仓库为什么看不到库存
【关键词】新仓库 看不到库存 显示库存 ERP仓库
【场景】仓储管理
【答案】查看-系统管理--ERP仓库设置-ERP仓库列表--查看该仓库是否未勾选显示库存
""",
        "metadata": {
            "question": "新创建的仓库为什么看不到库存"
        },
        "score": 0.998863,
    }
]


query = "新创建的仓库为什么看不到库存"

result = judge_answerability(
    query,
    documents,
)

print("=" * 60)
print("LLM Judge Test")
print("=" * 60)

print("Query:", query)
print("Answerable:", result["answerable"])
print("Reason:", result["reason"])