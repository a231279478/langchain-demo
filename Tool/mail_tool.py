from typing import Optional, Type, Any
from langchain.tools import BaseTool,tool
from pydantic import BaseModel, Field

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)

class MailSchema(BaseModel):
    recipient: str = Field(description="收件人",pattern="")
    subject: str = Field(description="邮件主题")
    content: str = Field(description="邮件内容")

class SendMailTool(BaseTool):
    name = "email"
    description = "这个是一个发信工具"
    args_schema: Type[MailSchema] = MailSchema

    def _run(self, recipient: str, subject: str, content: str ,run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        print(recipient,subject,content)
        return '发送完成'



class EmailAddressInput(BaseModel):
    recipient: str = Field(description="收件人")

class EmailAddressTool(BaseTool):
    name = "email_address_tool"
    description = "发送邮件之前，需要使用这个工具，收件人转换邮箱地址"
    def _run(self, recipient: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        return "123456@qq.com"



