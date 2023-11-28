# flake8: noqa
PODCAST_DOCS = """API documentation:
Endpoint: http://192.168.80.8
GET /studio/auth/sys/sysContacts/list

这个api是用来搜索通讯录人员.

Query parameters table:
name: | string | 搜索的姓名| required

Response schema (JSON object):
code | integer | optional
message | string | optional
results.records | array[object] (名字列表)
"""
