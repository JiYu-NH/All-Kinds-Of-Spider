import re
import json
import requests
from lxml import etree


class filmReviews():

    def __init__(self, movieUrl, pageNum):
        # 豆瓣电影
        self.movieUrl = movieUrl
        # 需要的影评页数
        self.pageNum = pageNum
        # 代理
        self.IP = '106.5.10.43:4213'
        self.proxy = {
            'http': self.IP,
            'https': self.IP
        }
        # 请求头
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; rv:22.0) Gecko/20130405 Firefox/22.0'
        }

    # 每页的影评
    def CommentPage(self, num: int):
        # 第一页从0开始，每页20条影评
        pageNum = 20 * num

        # url为：最新发布栏的影评
        url = '{}/reviews?sort=time&start={}'.format(movieUrl, pageNum)

        res = requests.get(url, headers=self.headers, proxies=self.proxy)
        selector = etree.HTML(res.text)

        # 每页的影评列表
        commentsList = selector.xpath('//div[@class="review-list  "]/div[@data-cid]')

        # 每条影评的详细信息
        for comment in commentsList:
            # 影评ID
            commentID = comment.xpath('./@data-cid')[0]
            # 影评发表者
            commentAuthor = comment.xpath('./div/header/a[@class="name"]/text()')[0]
            # 影评时间
            commentTime = comment.xpath('./div/header/span/text()')[0]
            # 完整影评
            commentContent = self.CompleteComment(commentID)

            # 打印得到的数据（可将数据保存）
            print(commentID, commentAuthor, commentTime)
            print(commentContent)

    # 通过评论的ID，得到完整影评
    def CompleteComment(self, id):
        # 完整影评的URL，异步加载，F12中的XHR可见
        url = 'https://movie.douban.com/j/review/%s/full' % id

        commentRes = requests.get(url, headers=self.headers, proxies=self.proxy)
        commentDict = json.loads(commentRes.text)

        # 用换行符替换p标签
        return '\n'.join(re.findall(r'<p>(.*?)</p>', commentDict['html'], re.S))

    # 爬取影评
    def crawlComments(self):
        # 爬取pageNum数量页的影评
        for i in range(self.pageNum):
            self.CommentPage(i)


if __name__ == '__main__':
    # 豆瓣电影的URL
    movieUrl = 'https://movie.douban.com/subject/1295644'
    # 需要的影评页数
    pageNum = 3

    # 开始爬取影评
    filmReviews(movieUrl, pageNum).crawlComments()