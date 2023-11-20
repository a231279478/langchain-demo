from typing import Optional, Type, Any
from langchain.tools import BaseTool
from pydantic import BaseModel, Field

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)

class MailSchema(BaseModel):
    recipient: str = Field(description="邮件收件人或者邮箱地址")
    subject: str = Field(description="邮件主题")
    content: str = Field(description="邮件内容")

class SendMailTool(BaseTool):
    name = "send_mail"
    description = "当你需要发送邮件时，可以使用这个。"
    args_schema: Type[MailSchema] = MailSchema

    def _run(self, recipient: str, subject: str, content: str ,run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        print(recipient,subject,content)
        return '发送完成'




