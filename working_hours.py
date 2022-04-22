# coding: UTF-8
import json
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
#エラーが起きたら下記「chromedriver_binary」「webdriver_manager」インストールしてください
import chromedriver_binary
from webdriver_manager.chrome import ChromeDriverManager
import time

# ********************　必読　********************

# ■　■　■　■　■　■　■　前提条件 ■　■　■　■　■　■　■　

# Python3がインストール済みであること
# ブラウザ「Google Chrome」がインストール済みであること

# コマンドラインで以下をインストール
#             pip install selenium
# brewをアップデート
# 　　　　　　　brew tap homebrew/cask
# chromedriverをインストール
# 　　　　　　　brew install chromedriver

# ■　■　■　■　■　■　■　手順 ■　■　■　■　■　■　■　

# 1:user_idにKING OF TIME の ID を入力

# 2:my_passにKING OF TIME の パスワード を入力

# 3:range_startからrange_endまで各項目を入力（月初から月末の場合は変更なしでOK）

# 4:ファイルを保存してターミナルを起動

# 5:python working_hours_csv.py　入力

# 6:自動的にchromeが起動される
# ※macはこのスクリプトの初回起動時にシステム環境設定＞セキュリティより許可が必要

# ********************個人設定********************


# KING OF TIME の ID を入力
user_id = ""

# KING OF TIME の パスワード を入力
my_pass = ""

# 取得範囲 ※1日から取得する場合は0
range_start = 0
# 末日
today = datetime.date.today()
lastday = calendar.monthrange(today.year, today.month)
range_end = lastday[1]

# ********************コード********************

webdriver = webdriver.Chrome(ChromeDriverManager().install())
#webdriver = webdriver.Chrome()
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

# 日付ごとの勤務時間を格納（日付、スケジュール、出勤、退勤、休憩開始、休憩終了）
working_hours_list = {}

for i in range(range_start,range_end):
    # 日付欄
    day_xpath = "/html/body/div/div[2]/div/div[5]/div[1]/table/tbody/tr[" + str(i+1) +"]/td[2]/p"
    # スケジュール欄
    day_schedule_xpath = "/html/body/div/div[2]/div/div[5]/div[1]/table/tbody/tr[" + str(i+1) +"]/td[4]/p"
    # 出勤欄
    td6_xpath = "/html/body/div/div[2]/div/div[5]/div[1]/table/tbody/tr[" + str(i+1) + "]/td[6]/p"
    # 退勤欄
    td7_xpath = "/html/body/div/div[2]/div/div[5]/div[1]/table/tbody/tr[" + str(i+1) + "]/td[7]/p"
    # 休憩開始欄
    td8_xpath = "/html/body/div/div[2]/div/div[5]/div[1]/table/tbody/tr[" + str(i+1) + "]/td[8]/p"
    # 休憩終了欄
    td9_xpath = "/html/body/div/div[2]/div/div[5]/div[1]/table/tbody/tr[" + str(i+1) + "]/td[9]/p"
    
    try :
        # 日付
        day = webdriver.find_element_by_xpath(day_xpath).text
        # スケジュール
        day_schedule = webdriver.find_element_by_xpath(day_schedule_xpath).text
        # 出勤時間
        td6 = webdriver.find_element_by_xpath(td6_xpath).text
        # 退勤時間
        td7 = webdriver.find_element_by_xpath(td7_xpath).text
        # 休憩開始時間
        td8 = webdriver.find_element_by_xpath(td8_xpath).text
        # 休憩終了時間
        td9 = webdriver.find_element_by_xpath(td9_xpath).text

        # 日付、スケジュール
        working_hours_list[i] = {"day" : day, "day_schedule" : day_schedule}

        # 出勤時間
        if not td6:
            working_hours_list[i]["start_work"] = td6
        else:
            td6 = re.search("\d+:\d+", td6)
            working_hours_list[i]["start_work"] = td6.group()
        # 退勤時間
        if not td7:
            working_hours_list[i]["end_work"] = td7
        else:
            td7 = re.search("\d+:\d+", td7)
            working_hours_list[i]["end_work"] = td7.group()
        # 休憩開始時間
        if not td8:
            working_hours_list[i]["start_break"] = td8
        else:
            td8 = re.search("\d+:\d+", td8)
            working_hours_list[i]["start_break"] = td8.group()
        # 休憩終了時間
        if not td9:
            working_hours_list[i]["end_break"] = td9
        else:
            td9 = re.search("\d+:\d+", td9)
            working_hours_list[i]["end_break"] = td9.group()
    except :
        print("勤務時間の取得でエラーが発生しました。")
        break

webdriver.close()
webdriver.quit()

# スプレッドシートへの書き込み
url = "https://script.google.com/macros/s/AKfycbxvMHZQcTPhIokrCFLWlMsnCtISCShJYlCqTuE56LkXAgONuvfz0VW2lKQqpxmea_bB/exec"

for working_hour in working_hours_list.values():
    try:
        response = requests.post(url, data=working_hour)
    except:
        print("スプレッドシートへの書き込みでエラーが発生しました。")
        break

print(response)