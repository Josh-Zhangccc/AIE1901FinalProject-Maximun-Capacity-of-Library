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
            base_url=BASE_URL,
            api_key=API_KEY,
        )

    def response(self,prompt:str):
        response = self.client.chat.completions.create(
            model=MODEL,
            messages=[
                {'role':'system','content':prompt}
            ],
            stream=False,
            temperature=0.7,
            max_tokens=1000,
            top_p=0.95,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        reply = response.choices[0].message.content
        return self._transform_to_json(reply)
    
#    def _test(self):
#        print(self.response(test_prompt))

    def _transform_to_json(self,llm_response):
        try:
            llm_response = json.loads(llm_response)  # 转换为字典
        except json.JSONDecodeError as e:
            # 处理解析失败的情况（如 LLM 输出格式错误）
            print(f"JSON 解析失败: {e}")
            llm_response = {"action": None}
        finally:
            return llm_response