import xlwt
import csv
import requests
from lxml import etree
import time
from tqdm import tqdm
# 加随机ua，使用fake-useragent库，构造随机ua
from fake_useragent import UserAgent
import re
import json

list_movie = []
# 请求头
headers = {'User-Agent': str(UserAgent().random)}

# 爬取的内容保存在csv文件中
f = open(r"douban_movie.csv", "w+", newline='', encoding="gb18030")
writer = csv.writer(f, dialect='excel')
# csv文件中第一行写入标题
writer.writerow(["name", "year", "mark", "comment", "quote", "area"])


# 定义爬取内容的函数
def music_info(url):
    html = requests.get(url, headers=headers)
    selector = etree.HTML(html.text)

    infomation = selector.xpath('//div[@class="item"]')
    for info in infomation:
        name = info.xpath('div[2]/div[1]/a/span[1]/text()')[0].strip()
        year = int(info.xpath('div[2]/div[2]/p[1]/text()')[1].strip()[0:4])
        area = re.findall(".*/(.*)/.*", info.xpath('div[2]/div[2]/p[1]/text()')[1].strip())[0].strip()
        print(area)
        mark = float(info.xpath('div[2]/div[2]/div/span[2]/text()')[0].strip())
        comment = int(
            info.xpath('div[2]/div[2]/div/span[4]/text()')[0].strip().strip("(").strip(")").replace('人评价', '').strip())
        # noinspection PyBroadException
        try:
            quote = info.xpath('div[2]/div[2]/p[@class="quote"]/span/text()')[0].strip()
        except:
            quote = ""

        list_info = [name, year, mark, comment, quote, area]
        writer.writerow([name, year, mark, comment, quote, area])
        list_movie.append(list_info)

    # 防止请求频繁，故睡眠1秒
    time.sleep(1)


if __name__ == '__main__':
    urls = ['https://movie.douban.com/top250?start={}'.format(str(i)) for i in range(0, 250, 25)]
    # 调用函数music_info循环爬取内容
    for url in tqdm(urls):
        music_info(url)
    # 关闭csv文件
    f.close()
    # 爬取的内容保存在xls文件中
    header = ["name", "year", "mark", "comment", "quote", "area"]

    # 设置列头加粗
    font = xlwt.Font()
    font.bold = True

    # 设置列头单元格居中
    alignment = xlwt.Alignment()
    alignment.horz = 0x02

    style = xlwt.XFStyle()
    style.font = font
    style.alignment = alignment

    # 打开工作簿
    book = xlwt.Workbook(encoding='utf-8')
    # 建立Sheet1工作表
    sheet = book.add_sheet('Sheet1')
    for h in range(len(header)):
        sheet.write(0, h, header[h], style)
    i = 1
    for item in list_movie:
        j = 0
        for data in item:
            sheet.write(i, j, data)
            j += 1
        i += 1
    # 设置单元格宽度
    sheet.col(0).width = 256 * 30
    sheet.col(1).width = 256 * 10
    sheet.col(2).width = 256 * 10
    sheet.col(3).width = 256 * 15
    sheet.col(4).width = 256 * 60
    sheet.col(5).width = 256 * 20

    # 保存文件
    book.save('douban_movie.xls')

    f = open("douban_movie.csv", "r", encoding='gbk')  #
    ls = []
    for line in f:
        line = line.replace("\n", "")
        ls.append(line.split(","))

    f.close()
    fw = open("douban_movie.json", "w", encoding='utf-8')
    for i in range(1, len(ls)):
        ls[i] = dict(zip(ls[0], ls[i]))
    a = json.dumps(ls[1:], sort_keys=True, indent=4, ensure_ascii=False)
    fw.write(a)
    fw.close()
