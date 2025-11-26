"""
prompt.py
提供LLM所需的提示词
"""


test_prompt = "This is a test prompt. If you can hear me, reply'Test succeeded!'"

schedule_prompt = """你是一个图书馆学生行为模拟器。请根据以下信息规划学生一天的日程
学生特征：
- 作息类型：{schedule_type}
- 专注类型：{focus_type}
- 课程情况：{course_situation}
日程概览：从早晨7点开始到晚上12点结束。
  - 日程包含六种行为：
      1. 开始一天(start)
      2. 在图书馆学习(learn)
      3. 进食（一日三餐）(eat)
      4. 上课(course)
      5. 休息(rest)
      6. 结束一天(end)
  - 具体信息：
      1. 学生每天有2-4节课，每节课时间在1-2.5h.一天的课程时间不会超过8h。
      2. 进食时间在0.5-1h之间。
      3. 学生休息时间不在图书馆
      4. 学生一天开始时间在7点到11点
示例：
作息：早；专注：中；课程：少
[
{{"time":"07:30:00","action":"start"}},
{{"time":"07:30:00","action":"eat"}},
{{"time":"08:00:00","action":"course"}},
{{"time":"09:00:00","action":"learn"}},
{{"time":"12:00:00","action":"eat"}},
{{"time":"13:00:00","action":"course"}},
{{"time":"14:15:00","action":"rest"}},
{{"time":"16:15:00","action":"course"}},
{{"time":"17:00:00","action":"learn"}},
{{"time":"18:00:00","action":"eat"}},
{{"time":"18:45:00","action":"learn"}},
{{"time":"20:00:00","action":"rest"}},
{{"time":"10:30:00","action":"end"}}
]
请严格按照以下JSON格式回复，不要添加其他内容：
[{{"time":"xx:xx:00","action":"(六种行为之一)"}}]
"""

leave_prompt = """你是一个图书馆学生行为模拟器。请根据以下信息判断学生离开图书馆时是否选择占座行为。

- 个人性格：{character}
- 座位满意度(5分制)：{satisfaction}
- 当前时间：{time}
- 图书馆对占座可能最大容忍时间：{limit_time}
- 日程：{schedule}

日程解析：除"learn"状态外,均不在图书馆
示例：
守序,2,12:00:00,2h,[
{{"time":"07:30:00","action":"start"}},
{{"time":"07:30:00","action":"eat"}},
{{"time":"08:00:00","action":"course"}},
{{"time":"09:00:00","action":"learn"}},
{{"time":"12:00:00","action":"eat"}},
{{"time":"13:00:00","action":"course"}},
{{"time":"14:15:00","action":"rest"}},
{{"time":"16:15:00","action":"course"}},
{{"time":"17:00:00","action":"learn"}},
{{"time":"18:00:00","action":"eat"}},
{{"time":"18:45:00","action":"learn"}},
{{"time":"20:00:00","action":"rest"}},
{{"time":"10:30:00","action":"end"}}
]
回复：{{"action":"leave"}}
请严格按照以下JSON格式回复，不要添加其他内容：
{{
  "action":"leave"或"reverse"(不占座和占座)
}}"""