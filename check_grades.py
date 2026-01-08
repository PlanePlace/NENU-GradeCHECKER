import requests
import json
import os
import urllib.parse
from datetime import datetime
from zoneinfo import ZoneInfo # 用作判断时区

# Bark配置
BARK_TOKEN = os.environ["BARK_TOKEN"]

# 成绩数据接口URL
GRADES_URL = "https://bkjx.nenu.edu.cn/new/student/xskccj/kccjDatas"

# Cookie
COOKIES = {
    "JSESSIONID": os.environ["JSESSIONID"],
    "iPlanetDirectoryPro": os.environ["IPLANETDIRECTORYPRO"],
    "acw_tc": os.environ["ACW_TC"]
}

# 数据存储文件
DATA_FILE = "grades.json"

def is_night_time():
    # 使用推荐的 datetime.now(ZoneInfo("UTC"))
    beijing_time = datetime.now(ZoneInfo("UTC")).astimezone(ZoneInfo("Asia/Shanghai"))
    hour = beijing_time.hour
    # 您可以去掉这行print，或者保留它以便观察
    print(f"当前北京时间是: {hour}点")
    return hour >= 22 or hour < 8

def fetch_grades():
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://bkjx.nenu.edu.cn',
        'Referer': 'https://bkjx.nenu.edu.cn/new/student/xskccj/kccjList.page',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"'
    }
    # Payload 构建
    payload = {
        'xnxqdm': '202501', # Correct academic semester code
        'source': 'kccjlist',
        'page': '1',
        'rows': '150', # Using a large number to get all grades at once
        'sort': 'xnxqdm,kcmc',
        'order': 'asc'
    }
    r = requests.post(GRADES_URL, headers=headers, cookies=COOKIES, data=payload)
    r.raise_for_status()
    data = r.json()
    courses = []
    for item in data["rows"]:
        # 你可以自行决定要用什么字段做“唯一标识”
        # 这里用课程名 + 分数
        course_str = f"{item['kcmc']} - {item['zcj']}分"
        courses.append(course_str)
    return courses

def load_old_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def send_bark(title, body):
    # 为了能正确处理中文、空格等特殊字符，需要进行URL编码
    encoded_title = urllib.parse.quote(title)
    encoded_body = urllib.parse.quote(body)

    # 重新构造正确的Bark URL
    url = f"https://api.day.app/{BARK_TOKEN}/{encoded_title}/{encoded_body}"

    # 【可选建议】您可以加上group参数，让来自这个脚本的通知自动分组
    url += "?group=教务通知"

    print(f"正在发送Bark通知...")
    requests.get(url)

def main():
    if is_night_time():
        print("夜间时间，停止检查")
        return

    # --- 请确保以下关键步骤顺序正确 ---
    
    # 1. 从服务器获取最新成绩。
    courses = fetch_grades()
    
    # 2. 从文件加载之前保存的旧成绩。
    old_courses = load_old_data()
    
    # 3. 通过对比两个列表，定义 'new_courses'。
    new_courses = [c for c in courses if c not in old_courses]

    # 4. 现在，检查 'new_courses' 列表里是否有内容。
    if new_courses:
        title = "🎉 新成绩发布"
        body = "、".join(new_courses)
        send_bark(title, body)
        print("新成绩:", new_courses)
    else:
        print("暂无新成绩")

    # 5. 为下一次运行保存最新的成绩。
    save_data(courses)

if __name__ == "__main__":
    main()
