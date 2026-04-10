import smtplib
import random
import requests
from email.mime.text import MIMEText
import pymysql
import pandas as pd
from bs4 import BeautifulSoup
import schedule
import time
import sys          # 用于读取命令行参数
from email.utils import parseaddr, formataddr
from email.header import Header

# ---------- 配置区域 ----------#只需要修改以下配置项即可，其他代码无需修改，请勿删除或改动以下配置项的变量名和注释，否则可能导致程序无法正常运行。
# 数据库配置
#切记Mysql中的代码也要插入到goodnight_db数据库中，表名分别为user、weather、word，字段和数据请参考代码示例。
user_name = '*****'   # 统一用户名，请改成你实际使用的数据库用户名（例如 root）
password = '******'   # 统一密码，请改成你实际使用的数据库密码（例如 123456）
address = '*******'    # 统一地址，请改成你实际使用的数据库地址（例如 localhost 或
port = ********    # 统一端口，请改成你实际使用的数据库端口（例如 3306）
DB_NAME = 'goodnight_db'   # 统一数据库名，请改成你实际使用的数据库名（例如 goodnight_db）

# 邮件配置
mail_host = "smtp.qq.com"
mail_user = "*****@qq.com"   # 统一邮箱用户名，请改成你实际使用的邮箱用户名
mail_pass = "******"   # QQ邮箱授权码（授权码去QQ邮箱设置中获取）

# -----------------------------

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def send_mail(to_list, sub, content):
    me = "test" + "<" + mail_user + ">"
    msg = MIMEText(content, _subtype='html', _charset='utf-8')
    msg['Subject'] = sub
    msg['From'] = _format_addr('来自火星的好朋友<%s>' % mail_user)
    msg['To'] = to_list
    try:
        server = smtplib.SMTP_SSL(host='smtp.qq.com')
        server.connect(host='smtp.qq.com', port=465)
        server.login(mail_user, mail_pass)
        server.sendmail(me, to_list, msg.as_string())
        server.close()
        return True
    except Exception as e:
        print(f"邮件发送失败: {e}")
        return False


def Read_database(user_name, password, address, port, database_name, sql):
    conn = pymysql.connect(host=address, user=user_name, passwd=password,
                           db=database_name, port=int(port), charset="utf8mb4")
    try:
        df = pd.read_sql(sql, con=conn)
    except Exception as e:
        print(f'\n Reading Error: {e} \n')
        df = pd.DataFrame()
    finally:
        conn.close()
    print('\n Completion of data reading \n')
    return df


def _weather(url, word):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        html = r.text
    except:
        html = "err"
        return "<html><body>天气信息获取失败</body></html>"

    final_list = []
    soup = BeautifulSoup(html, 'html.parser')
    body = soup.body
    data = body.find('div', {'id': '7d'})
    if not data:
        return "<html><body>无法解析天气页面，请检查URL</body></html>"
    ul = data.find('ul')
    lis = ul.find_all('li')
    for day in lis:
        temp_list = []
        date = day.find('h1').string
        temp_list.append(date)
        info = day.find_all('p')
        temp_list.append(info[0].string)
        if info[1].find('span') is None:
            temperature_highest = ' '
        else:
            temperature_highest = info[1].find('span').string.replace('℃', ' ')
        if info[1].find('i') is None:
            temperature_lowest = ' '
        else:
            temperature_lowest = info[1].find('i').string.replace('℃', ' ')
        temp_list.append(temperature_highest)
        temp_list.append(temperature_lowest)
        wind_scale = info[2].find('i').string
        temp_list.append(wind_scale)
        final_list.append(temp_list)

    if len(final_list) < 2:
        return "<html><body>天气数据不足</body></html>"
    final = final_list[1]

    message = f"""
    <!DOCTYPE HTML>
    <html>
    <head>
    <meta charset="utf-8"/>
    <title>晚安邮件</title>
    <style>
        .p1{{text-indent: 40px;}}
        .p2{{text-indent: 3em;}}
    </style>
    </head>
    <body>
        <p><img src="https://p2.piqsels.com/preview/375/839/586/food-bowl-fruit-healthy-thumbnail.jpg"></p>
        <p>{word}</p>
        <p style="text-align:left">明日天气：{final[1]}</p>
        <p style="text-align:left">最高温度：{final[2]} ℃</p>
        <p style="text-align:left">最低温度：{final[3]} ℃</p>
        <p style="text-align:right">--晚安！</p>
    </body>
    </html>
    """
    return message


def main():
    print("开始执行晚安邮件发送任务...")
    # 使用统一的数据库名 DB_NAME
    people_df = Read_database(user_name, password, address, port, DB_NAME, 'SELECT * FROM user;')
    weather_df = Read_database(user_name, password, address, port, DB_NAME, 'SELECT * FROM weather;')
    words_df = Read_database(user_name, password, address, port, DB_NAME, 'SELECT * FROM word;')

    if people_df.empty or weather_df.empty or words_df.empty:
        print("数据表为空，请先插入数据")
        return

    words = words_df.values
    db = people_df.values
    db2 = weather_df.values

    # 动态获取词库数量
    word_count = len(words)
    if word_count == 0:
        print("词库表无数据")
        return
    sui = random.randint(0, word_count - 1)


    #输出随机选中的晚安语
    word =words[sui][0]
    print(f"今日晚安语: {word}")

    for a in db:
        to_addrs = a[2]   # email
        city = a[1]       # city
        print(f"收件人: {to_addrs}, 城市: {city}")

        url = None
        for b in db2:
            if b[0] == city:
                url = b[1]
                print(f"找到天气URL: {url}")
                break
        if url is not None:
            neirong = _weather(url, word)
            success = send_mail(to_addrs, "晚安鸭!", neirong)
            if success:
                print(to_addrs + " success")
            else:
                print(to_addrs + " 发送失败")
        else:
            print(to_addrs + " 未找到对应城市的天气URL")
    print("任务执行完毕。")


if __name__ == "__main__":
    # 检查命令行参数
    if len(sys.argv) > 1 and sys.argv[1] in ('--test', '-t'):
        print("=== 测试模式：立即执行一次 ===")
        main()
    else:
        print("=== 定时模式：每天23:00执行 ===")
        schedule.every().day.at("23:00").do(main)
        while True:
            schedule.run_pending()
            time.sleep(1)
'''
立即测试一次
打开终端（命令行），执行：
python new_goodnight.py --test
'''