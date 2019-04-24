#  __author__: wurj
#  date: 2019/4/23

import requests

from fake_useragent import UserAgent
import json
import pandas as pd
import time
import datetime

headers = {"User-Agent": UserAgent(verify_ssl=False).random}
comment_api = 'https://bangumi.bilibili.com/review/web_api/short/list?media_id=23371915&folded=0&page_size=20&sort=0'

response_comment = requests.get(comment_api, headers=headers)
json_comment = response_comment.text
json_comment = json.loads(json_comment)

total = json_comment['result']['total']

cols = ['author', 'score', 'diliked', 'likes', 'liked', 'ctime', 'score', 'content', 'last_ep_index', 'cursor']

data_all = pd.DataFrame(index=range(total), columns=cols)

j = 0
while j < total:
    n = len(json_comment['result']['list'])
    for i in range(n):
        data_all.loc[j, 'author'] = json_comment['result']['list'][i]['author']['uname']
        data_all.loc[j, 'score'] = json_comment['result']['list'][i]['user_rating']['score']
        data_all.loc[j, 'disliked'] = json_comment['result']['list'][i]['disliked']
        data_all.loc[j, 'likes'] = json_comment['result']['list'][i]['likes']
        data_all.loc[j, 'liked'] = json_comment['result']['list'][i]['liked']
        data_all.loc[j, 'ctime'] = json_comment['result']['list'][i]['ctime']
        data_all.loc[j, 'content'] = json_comment['result']['list'][i]['content']
        data_all.loc[j, 'cursor'] = json_comment['result']['list'][n - 1]['cursor']
        j += 1
    try:
        data_all.loc[j, 'last_ep_index'] = json_comment['result']['list'][i]['user_saeson']['last_ep_index']
    except:
        pass

    comment_api = comment_api + '&cursor=' + data_all.loc[j - 1, 'cursor']
    response_comment = requests.get(comment_api, headers=headers)
    json_comment = response_comment.text
    json_comment = json.loads(json_comment)

    if j % 50 == 0:
        print('已完成{}%！'.format(round(j / total * 100, 2)))
    time.sleep(0.5)

data_all = data_all.fillna(0)


def getDate(x):
    x = time.gmtime(x)
    return (pd.Timestamp(datetime.datetime(x[0], x[1], x[2], x[3], x[4], x[5])))


data_all['date'] = data_all.ctime.apply(lambda x:getDate(x))

data_all.to_csv('e:/bilibili_comment3.xlsx', index=False)
