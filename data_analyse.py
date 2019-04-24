#  __author__: wurj
#  date: 2019/4/24

import pandas as pd
from pyecharts import Pie, Line, Scatter
import os
import numpy as np
import jieba
import jieba.analyse
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

font = FontProperties(fname=r'c:\windows\fonts\simsun.ttc')

os.chdir('E:\\data_analyse')
data = pd.read_csv('bilibili_comment3.csv', encoding='ansi')
print(list(data))

del data['ctime']
del data['cursor']
del data['liked']

scores = data.score.groupby(data['score']).count()

print('123')
# pie1 = Pie("评分", title_pos='center', width=900)
# pie1.add(
#     "评分",
#     ['一星', '二星', '三星', '四星', '五星'],
#     scores.values,
#     radius=[40, 75],
#     #    center=[50, 50],
#     is_random=True,
#     #    radius=[30, 75],
#     is_legend_show=False,
#     is_label_show=True
# )
# pie1.render('scores.html')

###########################################################################
# 评论时间分布
data['dates'] = data.date.apply(lambda x: pd.Timestamp(x).date())
data['time'] = data.date.apply(lambda x: pd.Timestamp(x).time().hour)
# print(data.author)
num_date = data.author.groupby(data['dates']).count()

chart = Line("评论数时间分布")
chart.use_theme('dark')
chart.add('评论时间', num_date.index, num_date.values, is_fill=True, line_opacity=0.2, area_opacity=0.4, symbol=None)

chart.render('comment_time_stamp.html')

# 好评字数分析
datalikes=['num','likes']
datalikes = data.loc[data.likes > 5]
datalikes['num'] = datalikes.content.apply(lambda x: len(x))
chart = Scatter("likes")
chart.use_theme('dark')
chart.add('likes', np.log(datalikes.likes), datalikes.num, is_visualmap=True, xaxis_name='log(评论字数）')
chart.render('好评字数分析.html')
