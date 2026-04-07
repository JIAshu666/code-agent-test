import json
from openai import OpenAI
from dotenv import load_dotenv
import os

# 加载 .env 文件
load_dotenv()

# 初始化 OpenAI 客户端（绝大多数国内模型都兼容这个 SDK）
client = OpenAI(
    api_key=os.getenv("API_KEY"),
    base_url=os.getenv("BASE_URL")
)

def call_llm(messages: list, tools_schema: list = None):
    """
    调用大模型
    :param messages: 对话历史
    :param tools_schema: 工具描述（传入时模型才会尝试调用工具）
    """
    kwargs = {
        "model": os.getenv("MODEL_NAME"),
        "messages": messages,
    }
    
    # 如果传了工具描述，就加上
    if tools_schema:
        kwargs["tools"] = tools_schema
        kwargs["tool_choice"] = "auto" # 让模型自己决定用不用工具
    
    response = client.chat.completions.create(**kwargs)
    return response.choices[0].message
