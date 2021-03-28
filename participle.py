import csv
import jieba
from scipy.misc import imread
from wordcloud import WordCloud


def draw_wordcloud():
    """
    绘制词云图
    :return:
    """
    word_list = []  # 定义一个新列表，放入文件中的评论
    mask = imread('词云元素\\玫瑰.png')
    with open('文件\\袜子.csv', encoding='utf-8-sig', newline='') as f:
        readers = csv.reader(f)
        for reader in readers:
            word_list.append(reader[1])
        word_list = [word for word in jieba.cut(''.join(word_list))]
        new_txt = "".join(word_list)
        wordcloud = WordCloud(background_color="white",  # 背景色
                              font_path='词云元素\\msyh.ttc',  # 字体
                              max_words=600,  # 显示的词的最大个数
                              height=3000,  # 高度
                              width=3000,  # 宽度
                              stopwords={',', '？', '：', '）', '。', '...', '//、/、/、、、'},
                              mask=mask  # 设置词云形状
                              ).generate(new_txt)

        wordcloud.to_file("词云图.png")
        print('词云图保存成功……')


draw_wordcloud()
