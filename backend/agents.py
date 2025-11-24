"""
agents.py
准备基于LLM的AGENTs
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import BASE_URL,API_KEY,MODEL

from prompt import test_prompt
from openai import OpenAI

class Clients:
    def __init__(self) -> None:
            
        self.client = OpenAI(
            base_url=BASE_URL,
            api_key=API_KEY,
        )
        self.test_response = self.client.chat.completions.create(
            model=MODEL,
            messages=[
                {'role':'user','content':test_prompt},
            ],
            stream=False,
            temperature=0.3,  #越高越随机
            max_tokens=150,#最大输出长度
            top_p=0.95,#核采样
            frequency_penalty=0.0,#避免重复
            presence_penalty=0.0#新话题鼓励x

        )

    def response(self,prompt):
        response = self.client.chat.completions.create(
            model=MODEL,
            messages=[
                {'role':'system','content':prompt},
            ],
            stream=False,
            temperature=0.7,
            max_tokens=1000,
            top_p=0.95,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        return response.choices[0].message.content