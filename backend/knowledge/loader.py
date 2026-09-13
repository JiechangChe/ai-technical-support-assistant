import pandas as pd

from langchain_core.documents import Document
from langchain_text_splitters import CharacterTextSplitter

def load_knowledge_documents(file_path: str)->list[Document]:
    #read the excel file
    df = pd.read_excel(file_path)

    documents = []

    #iteratively read the df, extract question, solution, 
    #keywords and category
    for _, row in df.iterrows():
        question = row.get("问题描述", "")
        solution = row.get("解决方案", "")
        keywords = row.get("关键词", "")
        category = row.get("场景标签", "general")

        #combine the information into content easy for llm to understand
        content = f"""【问题】{question}
【关键词】{keywords}
【场景】{category}
【答案】{solution}
"""
        #add the content to document
        documents.append(
            Document(
                page_content=content,
                metadata={
                    "category": category,
                    "question": question,
                    "keywords": keywords,
                },
            )
        )
    return documents

def split_documents(
    documents: list[Document],
) -> list[Document]:
    text_splitter = CharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    return text_splitter.split_documents(documents)