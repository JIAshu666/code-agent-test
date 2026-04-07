import json
from llm_client import call_llm
from file_tool import AVAILABLE_TOOLS

def main():
    # 1. 加载系统提示词
    with open("system_prompt.md", "r", encoding="utf-8") as f:
        system_prompt = f.read()
    
    # 2. 加载工具描述
    with open("tools_schema.json", "r", encoding="utf-8") as f:
        tools_schema = json.load(f)

    # 3. 初始化对话历史（第一轮必须是系统提示词）
    messages = [{"role": "system", "content": system_prompt}]

    print("====== 最简编程 Agent 已启动 ======")
    print("提示：你可以让它写代码，然后你自己去运行，把报错信息直接复制粘贴发给它。\n")

    # 4. 主交互循环
    while True:
        user_input = input("你: ")
        if user_input.lower() in ['exit', 'quit']:
            break
        
        # 将用户输入加入历史
        messages.append({"role": "user", "content": user_input})

        # 5. Agent 内部思考与行动循环（因为模型可能要读文件然后再写文件，需要循环）
        while True:
            # 调用大模型
            llm_response = call_llm(messages, tools_schema)
            
            # 情况 A：模型决定不调用工具，直接回复了（说明任务结束或需要你提供更多信息）
            if not llm_response.tool_calls:
                print(f"\nAgent: {llm_response.content}\n")
                # 把模型的回复加入历史，跳出内部循环，等待用户下一次输入
                messages.append(llm_response)
                break
            
            # 情况 B：模型决定调用工具（读文件或写文件）
            # 【关键】必须把模型“想要调用工具”的这个动作也记录进历史！
            messages.append(llm_response)

            # 遍历模型想要调用的工具（通常一次只调一个）
            for tool_call in llm_response.tool_calls:
                func_name = tool_call.function.name
                # 解析模型传过来的参数（JSON字符串转字典）
                func_args = json.loads(tool_call.function.arguments)
                
                print(f"[Agent 行动] 正在调用: {func_name}, 参数: {func_args.get('path', '')}")

                # 从字典里找到并执行真正的 Python 函数
                result = AVAILABLE_TOOLS[func_name](**func_args)
                print(f"[系统反馈] {result}\n")

                # 【关键】把工具执行的结果告诉模型，这也必须加入历史！
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id, # 必须带ID，模型才能对应上
                    "content": result
                })
            
            # 工具执行完后，不跳出循环，继续下一轮 while，让模型根据工具结果继续思考
            # （比如：读了文件 -> 发现错误 -> 再次调用写文件）

if __name__ == "__main__":
    main()
