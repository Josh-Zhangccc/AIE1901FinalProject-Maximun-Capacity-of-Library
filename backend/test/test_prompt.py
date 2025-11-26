from ..agents import Clients
from ..prompt import schedule_prompt

student_params = {
    "schedule_type": "晚",    # 对应 {schedule_type}
    "focus_type": "中",       # 对应 {focus_type}
    "course_situation": "多"  # 对应 {course_situation}
}
client = Clients()
formatted_prompt = schedule_prompt.format(**student_params)
#print(client.response(formatted_prompt))
print(formatted_prompt)

"""python -m backend.test.test_prompt.py"""