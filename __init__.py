from bs4 import BeautifulSoup
import requests
import csv
import json
import pandas as pd
import jieba
import os
import matplotlib.pyplot as plt
from wordcloud import WordCloud


def url2json(url):
    u_response = requests.get(url)
    u_json_data = u_response.json()
    return u_json_data


def watch_data(uid, page=0):
    url = f"https://ukamnads.icu/api/v2/user?uId=" + str(uid) + "&pageNum=" + str(
        page) + "&pageSize=50&target=-1&useEmoji=true"
    return url2json(url)['data']


def generate_cloud(uid):
    data = watch_data(uid)['data']

    word_freq = {}
    for user in data:
        count = user['count']
        name = user['uName']
        word_freq[name] = count

    text = ''.join(jieba.cut(' '.join(word_freq.keys())))

    if len(word_freq) == 0:
        print("This person has never watched a live stream.")
        return

    wordcloud = WordCloud(font_path='ZiYuYongSongTi-2.ttf', width=800, height=400, background_color='white')

    wordcloud.generate_from_frequencies(word_freq)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()
    # wordcloud.to_file("wordcloud.png")


def uid_search(uid):
    ##  定义key, type0为评论，2为消费，4为进场消息
    keys = ['cUid', 'cUname', 'cParentArea', 'cArea', 'type', 'sendDate', 'message', 'price', 'count']
    df = pd.DataFrame(columns=keys)

    file_name = str(uid) + ".csv"
    folder_name = "users"

    current_directory = os.getcwd()
    folder_path = os.path.join(current_directory, folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    file_path = os.path.join(folder_path, file_name)

    page_num = 0

    while True:
        w_data = watch_data(uid, page_num)

        if w_data['total'] == 0 or w_data['total'] == -1:
            return
        flag = w_data['hasMore']
        w_data = w_data['data']
        page_num += 1

        records = w_data['records']
        # 依次遍历每一页的每一条
        for record in records:
            cUid = record['channel']['uId']
            cUname = record['channel']['uName']
            cParentArea = record.get('live', {}).get('parentArea', '')
            cArea = record.get('live', {}).get('area', '')
            danmakus = record['danmakus']

            for danmaku in danmakus:
                row = {}
                row['cUid'] = cUid
                row['cUname'] = cUname
                row['cParentArea'] = cParentArea
                row['cArea'] = cArea

                for key in keys:
                    if key in danmaku:
                        row[key] = danmaku[key]

                df = pd.concat([df, pd.DataFrame(row, index=[0])], ignore_index=True)

        if not flag:
            break

    df.to_csv(file_path, index=False)


# uid_range
start_uid = 210097
end_uid = 210098
for i in range(start_uid, end_uid):
    print(i)
    uid_search(i)

