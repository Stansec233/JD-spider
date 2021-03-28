import csv
import time

import requests
from scipy.misc import imread
from wordcloud import WordCloud
import jieba


class JingDong:
    """定义类"""

    def __init__(self, page, productId):
        """
        初始化方法
        :param page:
        :param productId:
        """
        self.url = ' https://club.jd.com/comment/productPageComments.action'
        self.headers = {
            'Referer': 'https://item.jd.com/',
            'Host': 'club.jd.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 FS'
        }
        self.page = page  # 页数
        self.productId = productId  # 产品id

    def extract(self):
        """
        获取数据
        :return: response.json()
        """
        params = {
            'productId': str(self.productId),
            'score': '0',
            'sortType': '5',
            'page': str(self.page),
            'pageSize': '10',
            'isShadowSku': '0',
            'rid': '0',
            'fold': '1'

        }
        response = requests.get(url=self.url, headers=self.headers, params=params)
        return response.json()

    def parse_json(self, json_data):
        """
        解析数据，得到数据
        """
        comments = json_data['comments']
        for comment in comments:
            id_ = comment['id']  # 用户id
            content = comment['content']  # 评论
            creationTime = comment['creationTime']  # 购买时间
            yield id_, content, creationTime

    def save_data(self, data):
        """
        数据持久化
        :param data:
        :return: word_list
        """
        word_list = [] # 定义新列表
        for id_, content, creationTime in data:
            """保存文件可自定义，后缀不要更改"""
            with open('文件\\袜子.csv', mode='a', newline='', encoding='utf-8-sig') as f:
                csv_writer = csv.writer(f)
                csv_writer.writerow([id_, content, creationTime])
            print([id_, content.strip('\n'), creationTime])
            word_list.append(content)
        return word_list

    def start(self):
        """
        作为程序开始的函数
        :return:
        """
        json_data = self.extract()
        data = self.parse_json(json_data)
        self.save_data(data)


def draw_wordcloud():
    """
    绘制词云图
    :return:
    """
    word_list = []  # 定义一个新列表，放入文件中的评论
    mask = imread('词云元素\\玫瑰.png')
    """词云根据指定文件进行绘制"""
    with open('文件\\袜子.csv', encoding='utf-8-sig', newline='') as f:
        readers = csv.reader(f)
        for reader in readers:
            word_list.append(reader[1])
        word_list = [word for word in jieba.cut(''.join(word_list))]
        new_txt = "".join(word_list)
        wordcloud = WordCloud(background_color="white",  # 背景色
                              font_path='词云元素\\msyh.ttc',  # 字体
                              max_words=400,  # 显示的词的最大个数
                              height=2000,  # 高度
                              width=2000,  # 宽度
                              stopwords={',', '？', '：', '）', '。', '...', '//、/、/、、、'},
                              mask=mask  # 设置词云形状
                              ).generate(new_txt)

        wordcloud.to_file("词云图\\词云图.png")
        print('词云图保存成功……')


if __name__ == '__main__':
    """程序入口"""
    for page in range(1, 20):
        print(f"**********正在爬取第{page}页**********")
        """
        产品id ：17128036687、55631811238、66711160216、52028187811
        """
        jd = JingDong(page, 72322659325)
        jd.start()
        time.sleep(2)
    draw_wordcloud()
