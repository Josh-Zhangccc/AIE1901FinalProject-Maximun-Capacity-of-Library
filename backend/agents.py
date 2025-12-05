"""
agents.py
准备基于LLM的AGENTs
"""
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import BASE_URL,API_KEY,MODEL

#from prompt import test_prompt
from openai import OpenAI

class Clients:
    def __init__(self) -> None:
            
        self.client = OpenAI(
            base_url=BASE_URL["shubiaobiao"],
            api_key=API_KEY["shubiaobiao"],
        )

    def response(self,prompt:str, max_retries=3):
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=MODEL,
                    messages=[
                        {'role':'system','content':prompt}
                    ],
                    stream=False,
                    temperature=0.7,  # 降低temperature以获得更一致的输出
                    max_tokens=1000,
                    top_p=0.8,      # 降低top_p以获得更一致的输出
                    frequency_penalty=0.2,
                    presence_penalty=0.2
                )
                reply = response.choices[0].message.content
                
                if reply is None:
                    print(f"LLM返回空响应，尝试 {attempt + 1}")
                    continue
                
                # 尝试解析回复
                parsed_reply = self._transform_to_json(reply)
                
                # 如果解析成功且包含必要的字段，返回结果
                if parsed_reply is not None:
                    if isinstance(parsed_reply, dict) and "action" in parsed_reply:
                        return parsed_reply
                    elif isinstance(parsed_reply, list):
                        # 对于日程列表，检查是否包含必要字段
                        if all(isinstance(item, dict) and "time" in item and "action" in item for item in parsed_reply):
                            return parsed_reply
                        else:
                            print(f"LLM返回的列表格式不正确: {parsed_reply}")
                            continue  # 继续尝试
                    # 如果已经是正确的格式，直接返回
                    return parsed_reply
                else:
                    print(f"无法解析LLM响应，尝试 {attempt + 1}")
                    continue
                
            except Exception as e:
                print(f"尝试 {attempt + 1} 失败: {e}")
                if attempt == max_retries - 1:  # 如果是最后一次尝试
                    print(f"LLM请求失败，经过 {max_retries} 次尝试")
                    # 返回一个空的结构来避免程序崩溃
                    if "日程" in prompt or "schedule" in prompt.lower():
                        return []
                    else:
                        return {"action": None}
                continue  # 继续下一次尝试

        return {"action": None}
    
#    def _test(self):
#        print(self.response(test_prompt))

    def _transform_to_json(self,llm_response):
        # 如果响应不是字符串，直接返回
        if not isinstance(llm_response, str):
            return llm_response

        # 尝试直接解析JSON
        try:
            return json.loads(llm_response)
        except json.JSONDecodeError:
            pass

        # 如果直接解析失败，尝试从响应中提取JSON部分
        try:
            # 查找可能的JSON内容（在代码块中或直接是JSON）
            import re
            # 尝试匹配 ```json ... ``` 或 ``` ... ``` 代码块
            json_match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', llm_response)
            if json_match:
                json_content = json_match.group(1).strip()
                try:
                    return json.loads(json_content)
                except json.JSONDecodeError:
                    pass

            # 尝试匹配花括号内的内容
            # 简单提取大括号内容
            start_idx = llm_response.find('{')
            end_idx = llm_response.rfind('}')
            if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
                json_content = llm_response[start_idx:end_idx+1]
                try:
                    return json.loads(json_content)
                except json.JSONDecodeError:
                    pass

            # 如果以上都失败，使用默认响应
            print(f"JSON 解析失败，LLM响应: {llm_response[:200]}...")  # 只打印前200个字符
            return None  # 返回None而不是{"action": None}，让调用者处理
        except Exception as e:
            print(f"处理LLM响应时发生错误: {e}")
            return None  # 返回None而不是{"action": None}，让调用者处理