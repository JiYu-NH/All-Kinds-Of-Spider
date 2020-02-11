import requests
from lxml import etree
import os, sys

#   下载链接(一个主题)里的所有图片
url = 'https://www.mzitu.com/199451'

#   请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; CrOS i686 4319.74.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36 ',
    'Referer': url
}


def start_spider(url):
    #   第一页
    req = requests.get(url, headers=headers)
    selector_start = etree.HTML(req.text)
    # 标题
    title = selector_start.xpath('//h2/text()')[0]
    print(title)
    # 图片地址
    url = selector_start.xpath('//div[@class="main-image"]/p/a/img/@src')[0]
    # 下一页
    next_page = selector_start.xpath('//span[contains(text(),"下一页")]/../@href')[0]
    #   图片路径
    path = 'D:\\' + title
    #   判断文件夹是否存在
    if os.path.exists(path):
        # 存在则结束对此主题的下载
        print('此主题已存在')
        sys.exit()
    else:  # 不存在就创建
        os.mkdir(path)
    #   进入文件夹
    os.chdir(path)
    #   保存图片
    save_img(url)
    #   循环下载到最后一页
    while True:
        url_list = urls(next_page)
        #   保存图片
        save_img(url_list[0])
        #   列表长度不等于2时，表示已经到最后一页，没有下一页的链接
        if len(url_list) != 2: break
        #   继续下一页
        next_page = url_list[1]


#   取出当前页面的图片地址和下一页的地址
def urls(url):
    response = requests.get(url, headers=headers)
    selector = etree.HTML(response.text)
    urls = []
    #   当前页面的图片地址
    urls.append(selector.xpath('//div[@class="main-image"]/p/a/img/@src')[0])
    #   下一页的地址
    page = selector.xpath('//span[contains(text(),"下一页")]/../@href')
    if page:
        #   最后一页没有下页的链接，即为空，不添加
        urls.append(page[0])
    return urls


#   保存图片
def save_img(img_url):
    print('正在下载图片：', img_url)
    # 图片的内容
    data = requests.get(img_url, headers=headers).content
    #   图片名
    img_name = img_url.split('/')[-1]
    with open(img_name, 'wb') as f:
        f.write(data)


start_spider(url)
print('====    下载完毕！    ====')
