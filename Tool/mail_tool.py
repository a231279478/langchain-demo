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



class SaveAddressBookSchema(BaseModel):
    name: str = Field(description="名字",pattern="")
    mail_address: str = Field(description="邮箱地址")


class SaveAddressBookTool(BaseTool):
    name = "save_address_book"
    description = "将用户信息保存到通讯录"
    args_schema: Type[SaveAddressBookSchema] = SaveAddressBookSchema

    def _run(self, name: str, mail_address: str,run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        print(name,mail_address)
        if not mail_address or '@example.com' in mail_address:
           return '缺少邮箱地址'
        if not name:
            return "缺少用户名"

        return '保存成功    '



class QueryAddressBookTool(BaseTool):
    name = "query_address_book"
    description = "根据用户姓名查询通讯录中的邮箱地址"
    def _run(self, name: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        print('query_address_book',name)
        return "123456@qq.com"