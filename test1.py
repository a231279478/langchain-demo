from MyCustomChain import MyCustomChain
from langchain.prompts import ChatPromptTemplate
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

messages = [
        HumanMessage(content="给张三写一封中秋节日快乐的邮件"),
        AIMessage(content="亲爱的张三，中秋节到了，祝你节日快乐！希望你能和家人一起度过一个美好的夜晚，吃月饼、赏月、聊天，享受这个团圆的日子。祝你家庭幸福美满，事业蒸蒸日上！"),
    ]

template = ChatPromptTemplate.from_messages(messages)
print(template.format())