import json
from openai import OpenAI
from openai.types.chat import ChatCompletionMessage
from openai.types.chat.chat_completion_message_tool_call import ChatCompletionMessageToolCall, Function
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("API_KEY"),
    base_url=os.getenv("BASE_URL")
)

def call_llm(messages: list, tools_schema: list = None):
    """
    流式调用大模型，实时输出内容
    :param messages: 对话历史
    :param tools_schema: 工具描述（传入时模型才会尝试调用工具）
    :return: 完整的消息对象
    """
    kwargs = {
        "model": os.getenv("MODEL_NAME"),
        "messages": messages,
        "stream": True,
    }
    
    if tools_schema:
        kwargs["tools"] = tools_schema
        kwargs["tool_choice"] = "auto"
    
    stream = client.chat.completions.create(**kwargs)
    
    content_chunks = []
    tool_calls_data = {}
    
    for chunk in stream:
        delta = chunk.choices[0].delta
        
        if delta.content:
            print(delta.content, end="", flush=True)
            content_chunks.append(delta.content)
        
        if delta.tool_calls:
            for tc in delta.tool_calls:
                idx = tc.index
                if idx not in tool_calls_data:
                    tool_calls_data[idx] = {"id": "", "name": "", "arguments": ""}
                
                if tc.id:
                    tool_calls_data[idx]["id"] = tc.id
                if tc.function:
                    if tc.function.name:
                        tool_calls_data[idx]["name"] = tc.function.name
                    if tc.function.arguments:
                        tool_calls_data[idx]["arguments"] += tc.function.arguments
    
    print()
    
    content = "".join(content_chunks) or None
    
    tool_calls = None
    if tool_calls_data:
        tool_calls = []
        for idx in sorted(tool_calls_data.keys()):
            data = tool_calls_data[idx]
            tool_calls.append(ChatCompletionMessageToolCall(
                id=data["id"],
                function=Function(
                    name=data["name"],
                    arguments=data["arguments"]
                ),
                type="function"
            ))
    
    return ChatCompletionMessage(
        role="assistant",
        content=content,
        tool_calls=tool_calls
    )
