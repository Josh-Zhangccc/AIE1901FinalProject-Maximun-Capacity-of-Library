from backend.agents import Clients
from backend.prompt import schedule_prompt

# 测试agents的重试机制
print("测试agents重试机制...")

client = Clients()

# 测试日程生成提示
test_schedule_prompt = schedule_prompt.format(
    schedule_type="正常",
    focus_type="中",
    course_situation="中"
)

print("发送日程生成请求...")
try:
    response = client.response(test_schedule_prompt, max_retries=2)
    print(f"收到响应类型: {type(response)}")
    print(f"响应内容: {str(response)[:200]}...")  # 只显示前200个字符
    if isinstance(response, list):
        print("成功解析为日程列表")
    elif isinstance(response, dict):
        print("成功解析为字典")
    else:
        print("返回了默认结构")
except Exception as e:
    print(f"请求失败: {e}")
    import traceback
    traceback.print_exc()

print("\n测试完成")