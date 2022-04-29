# coding: UTF-8
import datetime
import calendar
import re
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

# ********************個人設定********************

# KING OF TIMEのIDを入力する
user_id = ""

# KING OF TIMEのパスワードを入力する
my_pass = ""

# 取得範囲 ※1日から取得する場合は0を指定する
range_start = 0
# 末日を指定する
today = datetime.date.today()
lastday = calendar.monthrange(today.year, today.month)
range_end = lastday[1]

# Apps ScriptのURLを入力する
url = ""

# ********************コード********************

def getInputValue(path):
    """
    KING OF TIMEの勤務時間入力欄から値を取得する

    Parameters
    ----------
    path : str
        勤務時間入力欄のHTMLでのパス

    Returns
    -------
    inputValue : str
        勤務時間入力欄の値
    """
    return webdriver.find_element_by_xpath(path).text

def changeInputValue(input_value):
    """
    勤務時間入力欄の値を 00:00 の形式にする

    Parameters
    ----------
    input_value : str
        勤務時間入力欄の値

    Returns
    -------
    work_time : str
        00:00 形式の勤務時間
    """
    return re.sub("^\D*", "", input_value)

webdriver = webdriver.Chrome(ChromeDriverManager().install())
webdriver.get("https://s2.kingtime.jp/admin/yC6jmVwSsiEOPtg6kcE7uf3XZpZIi32KF")
# 画面表示まで待つ
element = WebDriverWait(webdriver, 10).until(
    expected_conditions.presence_of_element_located((By.XPATH, "/html/body/div/div[1]/div[1]/div/form/input[1]"))
)

webdriver.find_element_by_xpath("/html/body/div/div[1]/div[1]/div/form/input[1]").send_keys(user_id)
webdriver.find_element_by_xpath("/html/body/div/div[1]/div[1]/div/form/input[2]").send_keys(my_pass)
webdriver.find_element_by_xpath("/html/body/div/div[1]/div[1]/div/form/input[6]").click()

# ログイン完了まで待つ
element = WebDriverWait(webdriver, 10).until(
    expected_conditions.presence_of_element_located((By.XPATH, "/html/body/div/div[2]/div/div[5]/div[1]/table/tbody/tr"))
)

# 勤務時間を格納する（日付、スケジュール、出勤、退勤、休憩開始、休憩終了）
working_hours_list = {}

for i in range(range_start,range_end):
    day_xpath = "/html/body/div/div[2]/div/div[5]/div[1]/table/tbody/tr[" + str(i+1) +"]/td[2]/p"
    day_schedule_xpath = "/html/body/div/div[2]/div/div[5]/div[1]/table/tbody/tr[" + str(i+1) +"]/td[4]/p"
    start_work_xpath = "/html/body/div/div[2]/div/div[5]/div[1]/table/tbody/tr[" + str(i+1) + "]/td[6]/p"
    end_work_xpath = "/html/body/div/div[2]/div/div[5]/div[1]/table/tbody/tr[" + str(i+1) + "]/td[7]/p"
    start_break_xpath = "/html/body/div/div[2]/div/div[5]/div[1]/table/tbody/tr[" + str(i+1) + "]/td[8]/p"
    end_break_xpath = "/html/body/div/div[2]/div/div[5]/div[1]/table/tbody/tr[" + str(i+1) + "]/td[9]/p"
    
    try :
        day = getInputValue(day_xpath)
        day_schedule = getInputValue(day_schedule_xpath)
        start_work = getInputValue(start_work_xpath)
        end_work = getInputValue(end_work_xpath)
        start_break = getInputValue(start_break_xpath)
        end_break = getInputValue(end_break_xpath)

        working_hours_list[i] = {"day" : day, "day_schedule" : day_schedule}
        working_hours_list[i]["start_work"] = changeInputValue(start_work)
        working_hours_list[i]["end_work"] = changeInputValue(end_work)
        working_hours_list[i]["start_break"] = changeInputValue(start_break)
        working_hours_list[i]["end_break"] = changeInputValue(end_break)
    except :
        print("勤務時間の取得でエラーが発生しました。")
        break

webdriver.close()
webdriver.quit()

# スプレッドシートへの書き込み
for working_hour in working_hours_list.values():
    try:
        response = requests.post(url, data=working_hour)
        print(working_hour["day"] + "の入力が完了しました。")
    except:
        print("スプレッドシートへの書き込みでエラーが発生しました。")
        break