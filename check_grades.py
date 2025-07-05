import requests
import json
import os
import urllib.parse
from datetime import datetime # 用作具体时间,可以用来实现定时获取的效果
from zoneinfo import ZoneInfo # 用作判断时区

# Bark配置
BARK_TOKEN = os.environ["BARK_TOKEN"]

# 成绩数据接口 URL
GRADES_URL = "https://bkjx.nenu.edu.cn/new/student/xskccj/kccjDatas"

# Cookies
COOKIES = {
    "JSESSIONID": os.environ["JSESSIONID"],
    "iPlanetDirectoryPro": os.environ["IPLANETDIRECTORYPRO"],
    "acw_tc": os.environ["ACW_TC"]
}

# 成绩数据的存储文件
DATA_FILE = "grades.json"

# 设定时区,避免GitHub造成的时区不符,同时是一个定时器,8:00-22:00检查,其他时间段不工作
def is_night_time():
    # 使用推荐的 datetime.now(ZoneInfo("UTC"))
    beijing_time = datetime.now(ZoneInfo("UTC")).astimezone(ZoneInfo("Asia/Shanghai"))
    hour = beijing_time.hour
    print(f"当前北京时间是: {hour}点")
    return hour >= 22 or hour < 8

# 获取成绩数据:以下为请求头数据,请根据自己的"kccjData"请求头进行修改
def fetch_grades():
    headers = {
        'Accept': '请替换',
        'Accept-Language': '请替换',
        'Connection': '请替换',
        'Content-Type': '请替换',
        'Origin': '请替换',
        'Referer': '请替换',
        'Sec-Fetch-Dest': '请替换',
        'Sec-Fetch-Mode': '请替换',
        'Sec-Fetch-Site': '请替换',
        'User-Agent': '请替换',
        'X-Requested-With': '请替换',
        'sec-ch-ua': '请替换',
        'sec-ch-ua-mobile': '请替换',
        'sec-ch-ua-platform': '请替换'
    }
    # Payload 数据,请根据自己的“kccjData“Payload进行修改
    payload = {
        'xnxqdm': '请替换', # 这个是学期代码,比如202401、202402这样的 01就是秋季学期 02就是秋季学期
        'source': '请替换',
        'page': '请替换',
        'rows': '请替换',
        'sort': '请替换',
        'order': '请替换'
    }
    r = requests.post(GRADES_URL, headers=headers, cookies=COOKIES, data=payload)
    r.raise_for_status()
    data = r.json()
    courses = []
    for item in data["rows"]:
        course_str = f"{item['kcmc']} - {item['zcj']}分" # 获取的关键信息,这里用了课程名称和课程分数
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
    encoded_title = urllib.parse.quote(title)
    encoded_body = urllib.parse.quote(body)

    url = f"https://api.day.app/{BARK_TOKEN}/{encoded_title}/{encoded_body}"

    url += "?group=教务通知" # 可选

    print(f"正在发送Bark通知...")
    requests.get(url)

def main():
    if is_night_time():
        print("夜间时间，停止检查")
        return

    courses = fetch_grades()
    
    old_courses = load_old_data()
    
    new_courses = [c for c in courses if c not in old_courses]

    if new_courses:
        title = "🎉 新成绩发布"
        body = "、".join(new_courses)
        send_bark(title, body)
        print("新成绩:", new_courses)
    else:
        print("暂无新成绩")

    save_data(courses)

if __name__ == "__main__":
    main()
