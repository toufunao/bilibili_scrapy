#  __author__: wurj
#  date: 2019/4/24

import pandas as pd
from pyecharts import Line, Scatter
from pyecharts import Pie
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
del data['score.1']

score = data.score.groupby(data['score']).count()
print(list(data))
print(score.values)
pie = Pie("评分", title_pos='center', width=900)
pie.add(
    '评分',
    ['四星', '五星'],
    score.values,
    radius=[40, 75],
    #    center=[50, 50],
    is_random=True,
    #    radius=[30, 75],
    is_legend_show=False,
    is_label_show=True,
)
pie.render('scores.html')

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

##################################################
# 好评字数分布
datalikes = ['num', 'likes']
datalikes = data.loc[data.likes > 0]
datalikes['num'] = datalikes.content.apply(lambda x: len(x))
chart = Scatter("likes")
chart.use_theme('dark')
chart.add('likes', np.log(datalikes.likes), datalikes.num, is_visualmap=True, xaxis_name='log(评论字数）')
chart.render('好评字数分析.html')

###############################################################
# 评论每日内的时间分布
num_time = data.author.groupby(data['time']).count()

# 时间分布

chart = Line("评论时间分布")
chart.use_theme('dark')
chart.add("评论数", x_axis=num_time.index.values, y_axis=num_time.values,
          is_label_show=True,
          mark_point_symbol='diamond', mark_point_textcolor='#40ff27',
          line_width=2
          )
chart.render('评论时间分布.html')

###########################################################
# 评论分析
texts = ';'.join(data.content.tolist())
cu_txt = ''.join((jieba.cut(texts)))

keywords = jieba.analyse.extract_tags(cu_txt, topK=200, withWeight=True, allowPOS=('a', 'e', 'n', 'nr', 'ns'))
text_cloud = dict(keywords)
pd.DataFrame(keywords).to_excel('TF_IDF关键词前200.xlsx')

bg = plt.imread("hh.png")

wc = WordCloud(
    background_color="white",
    # width=640,
    # height=400,
    mask=bg,
    random_state=2,
    max_font_size=500,
    font_path="STSONG.TTF"
).generate_from_frequencies(text_cloud)

plt.imshow(wc)

# bg_color = ImageColorGenerator(bg)
# plt.imshow(wc.recolor(color_func=bg_color))

plt.axis("off")
plt.show()
wc.to_file("词云.png")
