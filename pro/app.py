from flask import Flask, request, jsonify, send_file
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

import build_utils

# 测试
# openai.api_base = "http://region-9.seetacloud.com:19656/v1"
base_url = 'http://183.62.118.51:9999'
# 生产
#openai.api_base = "http://region-9.seetacloud.com:25540/v1"
#base_url = 'https://mail.danaai.net'

app = Flask(__name__)
llm = ChatOpenAI(openai_api_base="http://region-9.seetacloud.com:25540/v1",openai_api_key="none",temperature=0.8)
agent = build_utils.build_agent(llm)
infos = [
    {
        "name": "mail",
        "description": "擅长处理发送邮件和保存邮件草稿",
        "chain":build_utils.build_mail_chain("http://localhost:18889/v1/chat")
    },
    {
        "name": "query_mail",
        "description": "擅长查询邮箱地址和将邮箱地址保存到通讯录",
        "chain": agent
    }
]
condition_chains ,router_chain =build_utils.build_router_chain(llm,infos)

default_router_key = ['query_mail']



@app.route('/v1/chat', methods=['POST'])
def chat():
    params = request.json
    messages = params['messages']

    chain_messages = build_utils.build_chain_messages(messages)
    if len(chain_messages) > 1:
        router_history_message = chain_messages[0:-1]
    else:
        router_history_message = ""
    current_message = messages[-1]
    router_result = router_chain.invoke(
        {"input": current_message['content'], "history": ChatPromptTemplate.from_messages(router_history_message).format()},
        return_only_outputs=True)
    router = router_result['destination']

    if router and router not in default_router_key:
        chain = condition_chains.get(router)
        if chain is not None:
           return jsonify(chain.invoke(params, return_only_outputs=True)['result'])
    else:
        return jsonify({'role': 'assistant', 'content': agent.invoke({'input':chain_messages},return_only_outputs=True)['output']})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=18888)