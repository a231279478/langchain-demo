from flask import Flask, request, jsonify, send_file
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

import build_utils

app = Flask(__name__)
llm = ChatOpenAI(openai_api_base="http://region-9.seetacloud.com:25540/v1",openai_api_key="none")

infos = [
    {
        "name": "mail",
        "description": "擅长处理邮件问题",
        "chain":build_utils.build_mail_chain("http://localhost:18889/v1/chat")
    }
]
condition_chains ,router_chain =build_utils.build_router_chain(llm,infos)

agent = build_utils.build_agent(llm,serpapi_api_key="9333902da63642ef782fd41fb732587cbb22abf913554dbc7f4f2273345a50f9")



@app.route('/v1/chat', methods=['POST'])
def chat():
    params = request.json
    messages = params['messages']

    chain_messages = build_utils.build_chain_messages(messages)
    chain_messages.pop()

    current_message = messages[-1]

    router_result = router_chain.invoke(
        {"input": current_message['content'], "history": ChatPromptTemplate.from_messages(chain_messages).format()},
        return_only_outputs=True)
    router = router_result['destination']

    if router:
        chain = condition_chains.get(router)
        if chain is not None:
           return jsonify(chain.invoke(params, return_only_outputs=True)['result'])
    else:
        return jsonify({'role': 'assistant', 'content': agent.run(router_result['next_inputs'])})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=18888)