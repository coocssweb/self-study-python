"""
01 - Function Calling 基础

Function Calling 是 Agent 的底层机制。
LLM 本身不能执行代码，但它可以"告诉你它想调用什么函数、传什么参数"。

类比前端：就像 React 的事件系统。
组件（LLM）不直接操作 DOM（执行工具），而是发出事件（function call），
由事件处理器（你的代码）去执行，再把结果传回来。

流程：
1. 你告诉 LLM 有哪些函数可用（函数名、参数、描述）
2. LLM 根据用户问题，决定是否需要调用函数
3. 如果需要，LLM 返回函数名和参数（JSON 格式）
4. 你的代码执行函数，把结果传回 LLM
5. LLM 基于函数结果生成最终回答
"""

import os
import json
from openai import OpenAI

# ============================================================
# 初始化客户端
# ============================================================
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

# ============================================================
# 第一步：定义工具函数
# 这些是真正会被执行的 Python 函数
# ============================================================

def get_weather(city: str) -> str:
    """模拟获取天气信息（实际项目中会调真实 API）"""
    # 模拟数据
    weather_data = {
        "北京": "晴天，25°C",
        "上海": "多云，22°C",
        "深圳": "小雨，28°C",
    }
    return weather_data.get(city, f"暂无 {city} 的天气数据")


def calculate(expression: str) -> str:
    """计算数学表达式"""
    try:
        result = eval(expression)  # 仅用于演示，生产环境不要用 eval
        return str(result)
    except Exception as e:
        return f"计算出错: {e}"


# ============================================================
# 第二步：定义工具描述（告诉 LLM 有哪些工具可用）
# 这是 OpenAI 格式的 tools 定义，DeepSeek 兼容这个格式
# ============================================================

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称，如：北京、上海"
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "计算数学表达式，支持加减乘除",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "数学表达式，如：2 + 3 * 4"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]

# 函数名到函数对象的映射，方便后续调用
available_functions = {
    "get_weather": get_weather,
    "calculate": calculate,
}

# ============================================================
# 第三步：发送请求，让 LLM 决定是否调用函数
# ============================================================

def chat_with_tools(user_message: str):
    """带工具调用的对话"""
    print(f"\n{'='*50}")
    print(f"用户: {user_message}")
    print(f"{'='*50}")

    messages = [
        {"role": "system", "content": "你是一个有用的助手，可以查天气和做计算。"},
        {"role": "user", "content": user_message}
    ]

    # 第一次调用：LLM 决定是否需要调用工具
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        tools=tools,
        tool_choice="auto"  # auto = LLM 自己决定要不要调工具
    )

    assistant_message = response.choices[0].message

    print("++++++++++++++++++++++++++++", assistant_message)

    # 检查 LLM 是否想调用工具
    if assistant_message.tool_calls:
        print(f"\n🔧 LLM 决定调用工具:")

        # 把 LLM 的回复加入消息历史
        messages.append(assistant_message)

        # 执行每个工具调用
        for tool_call in assistant_message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)

            print(f"   函数: {function_name}")
            print(f"   参数: {function_args}")

            # 执行函数
            function = available_functions[function_name]
            result = function(**function_args)
            print(f"   结果: {result}")

            # 把函数执行结果传回 LLM
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })

        # 第二次调用：LLM 基于工具结果生成最终回答
        final_response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
        )
        final_answer = final_response.choices[0].message.content
    else:
        # LLM 认为不需要调工具，直接回答
        final_answer = assistant_message.content

    print(f"\n🤖 助手: {final_answer}")
    return final_answer


# ============================================================
# 测试不同场景
# ============================================================

if __name__ == "__main__":
    # 场景1：需要调用天气工具
    chat_with_tools("北京今天天气怎么样？")

    # # 场景2：需要调用计算工具
    # chat_with_tools("帮我算一下 123 * 456 + 789")

    # # 场景3：不需要工具，LLM 直接回答
    # chat_with_tools("你好，介绍一下你自己")
