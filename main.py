import json
from llm_client import call_llm
from file_tool import AVAILABLE_TOOLS

def main():
    with open("system_prompt.md", "r", encoding="utf-8") as f:
        system_prompt = f.read()
    with open("tools_schema.json", "r", encoding="utf-8") as f:
        tools_schema = json.load(f)

    messages = [{"role": "system", "content": system_prompt}]

    print("====== 最简编程 Agent 已启动 ======")
    print("提示：你可以让它写代码，然后你自己去运行，把报错信息直接复制粘贴发给它。\n")

    while True:
        user_input = input("你: ")
        if user_input.lower() in ['exit', 'quit']:
            break
        
        messages.append({"role": "user", "content": user_input})

        while True:
            llm_response = call_llm(messages, tools_schema)
            
            if not llm_response.tool_calls:
                messages.append(llm_response)
                print()
                break
            
            messages.append(llm_response)

            for tool_call in llm_response.tool_calls:
                func_name = tool_call.function.name
                
                try:
                    if not tool_call.function.arguments:
                        print("[错误] 工具调用参数为空")
                        error_message = "工具调用参数为空，请提供有效的JSON格式参数。"
                        messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": error_message})
                        continue
                    
                    func_args = json.loads(tool_call.function.arguments)
                    print(f"[Agent 行动] 正在调用: {func_name}, 参数: {func_args.get('path', '')}")
                except json.JSONDecodeError as e:
                    print(f"[错误] 解析工具参数失败: {e}")
                    print(f"[错误] 原始参数: '{tool_call.function.arguments}'")
                    error_message = f"工具调用参数解析失败: {e}。请确保参数是有效的JSON格式。"
                    messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": error_message})
                    continue

                try:
                    result = AVAILABLE_TOOLS[func_name](**func_args)
                    print(f"[系统反馈] {result}\n")
                except TypeError as e:
                    print(f"[错误] 调用工具失败: {e}")
                    error_message = f"工具调用失败: {e}。请确保提供了所有必要的参数。"
                    messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": error_message})
                    continue

                messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": result})

if __name__ == "__main__":
    main()
