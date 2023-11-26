
from langchain.schema.messages import HumanMessage, SystemMessage
from langchain.prompts import ChatPromptTemplate , PromptTemplate
from langchain.chains import LLMChain,ConversationChain,MultiPromptChain
from langchain.chat_models import ChatOpenAI
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from Tool.mail_tool import SendMailTool,EmailAddressTool

import os
os.environ["SERPAPI_API_KEY"] = '9333902da63642ef782fd41fb732587cbb22abf913554dbc7f4f2273345a50f9'
os.environ["OPENAI_API_KEY"] = 'none'
os.environ["OPENAI_API_BASE"] = 'http://region-9.seetacloud.com:25540/v1'
lawyer_template = """ 你是一个法律顾问，你需要根据用户提出的问题给出专业的法律意见，如果你不知道，请说"我不知道"，请不要提供超出文本范围外的内容，也不要自创内容。


用户提问：
{input}
"""


sales_template = """ 你是一个销售顾问，你需要为用户输入的商品进行介绍，你需要提供商品基本信息，以及其使用方式和保修条款。


用户输入的商品：
{input}
"""


english_teacher_template ="""你是一个英语老师，用户输入的中文词汇，你需要提供对应的英文单词，包括单词词性，对应的词组和造句。


用户输入的中文词汇：
{input}
"""


poet_template=""" 你是一个诗人，你需要根据用户输入的主题作诗。


用户输入的主题:
{input}
"""


mail_template=""" {input}"""


prompt_infos = [
    {
        "name": "lawyer",
        "description": "咨询法律相关问题时很专业",
        "prompt_template": lawyer_template,
    },
    {
        "name": "english teacher",
        "description": "能够很好地解答英语问题",
        "prompt_template": english_teacher_template,
    },
    {
        "name": "poet",
        "description": "作诗很专业",
        "prompt_template": poet_template,
    }
]

destinations = [f"{p['name']}: {p['description']}" for p in prompt_infos]


destinations_str = "\n".join(destinations)
print(destinations_str)

from langchain.chains.router.multi_prompt_prompt import MULTI_PROMPT_ROUTER_TEMPLATE


router_template = MULTI_PROMPT_ROUTER_TEMPLATE.format(destinations=destinations_str)

print(router_template)

from langchain.chains.router.llm_router import RouterOutputParser

router_prompt = PromptTemplate(
    template=router_template,
    input_variables=["input"],
    output_parser=RouterOutputParser(),
)


# 首先，创建一个候选链，包含所有的下游子链
candadite_chains = {}


llm = ChatOpenAI()

# 遍历路由目录，生成各子链并放入候选链字典
for p_info in prompt_infos:
    name = p_info["name"]
    prompt_template = p_info["prompt_template"]
    prompt = PromptTemplate(template=prompt_template, input_variables=["input"])
    chain = LLMChain(llm=llm, prompt=prompt)
    candadite_chains[name] = chain
tools = load_tools(["serpapi", "llm-math"], llm=llm)
tools.append(EmailAddressTool())
tools.append(SendMailTool())
# 工具加载后都需要初始化，verbose 参数为 True，会打印全部的执行详情
agent = initialize_agent(tools, llm, agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=True)


# 生成默认链
default_chain = agent


from langchain.chains.router.llm_router import LLMRouterChain
router_chain = LLMRouterChain.from_llm(llm, router_prompt)


chain = MultiPromptChain(
    router_chain=router_chain,
    destination_chains=candadite_chains,
    default_chain=default_chain,
    verbose=True,
    silent_errors=True
)
a = input()
print(chain.run(a))


