from enum import Enum


test_prompt = "This is a test prompt. If you can hear me, reply'Test succeeded!'"

routine_prompt = """你是一个图书馆学生行为模拟器。请根据以下信息规划学生一天的日程
学生特征：
- 作息类型：{schedule_type}
日程概览：从早晨7点开始到晚上12点结束。
  - 日程包含五种行为：
      1. 在图书馆学习
      2. 进食（一日三餐）
      3. 上课
      4. 休息
      5. 结束一天
  - 具体信息：
      1. 学生每天有2-4节课，每节课时间在1-2.5h.一天的课程时间不会超过8h。
      2. 进食时间在0.5-1h之间。
      3. 学生

请严格按照以下JSON格式回复，不要添加其他内容：
{
  "action": "stay" 或 "leave",
  "reason": "简要说明原因",
  "reserve_seat": true 或 false (当action为leave时，表示是否占座)
}"""

leave_prompt = """你是一个图书馆学生行为模拟器。请根据以下信息判断学生回到图书馆时是否需要重新选择座位。

学生特征：
- 个人性格：{character}
- 作息类型：{schedule_type}
- 座位偏好：插座{socket_pref}%，台灯{lamp_pref}%，空旷{open_pref}%

当前状态：
- 原座位是否仍被保留：{original_seat_status}
- 原座位属性：{original_seat_attributes}
- 当前图书馆可选座位情况：{available_seats_info}

请严格按照以下JSON格式回复，不要添加其他内容：
{
  "action": "return_original" 或 "find_new",
  "reason": "简要说明原因"
}"""
class Character(Enum):
    ORDERLY = "守序"  # 遵守规则的学生
    SELFISH = "利己"  # 以自我为中心的学生