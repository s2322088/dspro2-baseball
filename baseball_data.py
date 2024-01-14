from bs4 import BeautifulSoup
from time import sleep
import requests
import csv
import pandas as pd
import sqlite3
df = pd.DataFrame(columns = ['No', '選手名', '生年月日', '身長', '体重', '投', '打', '備考'])
teams = ['s', 'db', 't', 'g', 'c', 'd', 'b', 'h', 'l', 'e', 'm', 'f']
for team in teams:
    url = "https://npb.jp/bis/teams/rst_"+team+".html"
    r = requests.get(url)
    data = BeautifulSoup(r.content, "html.parser")
    getData = data.find("table", "rosterlisttbl")
    player = getData.find_all("td")
    count = 5
    num_player = len(player)
    for kk in range(int((num_player-5)//8)):
        list_data = []
        for t in range(8):
            list_data.append(player[count].text)
            count += 1
        df = pd.concat([df, pd.DataFrame([list_data], columns=df.columns)], ignore_index=True)

con = sqlite3.connect('baseball.sqlite')

# DataFrameをSQLiteデータベースのテーブルに書き込む
df.to_sql('baseball_data', con, index=False, if_exists='replace')

# 接続を閉じる
con.close()