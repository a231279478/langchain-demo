from typing import Optional, Type, Any
from langchain.tools import BaseTool,tool
from pydantic import BaseModel, Field
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
import requests
from flask import Flask, request, jsonify, send_file
import json


base_url = 'http://183.62.118.51:9999'
class EmailAddressTool(BaseTool):
    name = "email_address_tool"
    description = "发送邮件之前，需要使用这个工具，收件人转换邮箱地址"
    def _run(self, recipient: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        return "123456@qq.com"



class SaveAddressBookSchema(BaseModel):
    name: str = Field(description="名字")
    mail_address: str = Field(description="邮箱地址")


class SaveAddressBookTool(BaseTool):
    name = "save_address_book"
    description = "将用户信息保存到通讯录"
    args_schema: Type[SaveAddressBookSchema] = SaveAddressBookSchema

    def _run(self, name: str, mail_address: str,run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        print(name,mail_address)
        if not mail_address:
           return '缺少邮箱地址'
        if not name:
            return "缺少用户名"
        token = request.headers.get('X-Access-Token')
        tenant_id = request.headers.get('Tenant-Id')

        headers = {
            "X-Access-Token": token,
            'Content-Type': 'application/json',
            'Tenant-Id': tenant_id
        }

        payload = {
            'belongGroup': '0',
            'email': mail_address,
            'name': name,
        }

        response = requests.post(base_url + '/studio/auth/sys/sysContacts/add', data=json.dumps(payload), headers=headers)
        if response.status_code == 200:
            result = response.json()
            # try:
            #     code = result['code']
            #     if code == 510:
            #         return "token过期，请刷新token", None, 'token_expired'
            #     if code != 200:
            #         return "草稿保存失败", None, None
            # except Exception as e:
            #     pass

        return '保存成功'



class QueryAddressBookTool(BaseTool):
    name = "query_address_book"
    description = "根据用户姓名查询通讯录中的邮箱地址"
    def _run(self, name: str, run_manager: Optional[CallbackManagerForToolRun] = None):
        print('query_address_book',name)

        token = request.headers.get('X-Access-Token')
        tenant_id = request.headers.get('Tenant-Id')

        headers = {
            "X-Access-Token": token,
            'Content-Type': 'application/json',
            'Tenant-Id': tenant_id
        }

        payload = {
            'name': name,
        }

        response = requests.get(base_url + '/studio/auth/sys/sysContacts/list', params=payload, headers=headers)
        if response.status_code == 200:
            result = response.json()
            e_list = [{item['email']} for item in result['result']['records']]
            if len(e_list):
                return e_list
            # try:
            #     code = result['code']
            #     if code == 510:
            #         return "token过期，请刷新token", None, 'token_expired'
            #     if code != 200:
            #         return "草稿保存失败", None, None
            # except Exception as e:
            #     pass

        return "为找到对应邮箱"