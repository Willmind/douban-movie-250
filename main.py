import xlwt
import csv
import requests
from lxml import etree
import time
from tqdm import tqdm

list_music = []
# 请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"}
# 爬取的内容保存在csv文件中
f = open(r"C:\Users\tanzhijingg\Desktop\test2.csv", "w+", newline='', encoding="gb18030")
writer = csv.writer(f, dialect='excel')
# csv文件中第一行写入标题
writer.writerow(["name", "time", "mark", "coment", "quote"])


# 定义爬取内容的函数
def music_info(url):
    html = requests.get(url, headers=headers)
    selector = etree.HTML(html.text)

    infos = selector.xpath('//div[@class="item"]')
    for info in infos:
        name = info.xpath('div[2]/div[1]/a/span[1]/text()')[0].strip()
        time1 = int(info.xpath('div[2]/div[2]/p[1]/text()')[1].strip()[0:4])

        mark = float(info.xpath('div[2]/div[2]/div/span[2]/text()')[0].strip())
        coment = int(
            info.xpath('div[2]/div[2]/div/span[4]/text()')[0].strip().strip("(").strip(")").replace('人评价', '').strip())
        try:
            quote = info.xpath('div[2]/div[2]/p[@class="quote"]/span/text()')[0].strip()
        except:
            quote = ""

        list_info = [name, time1, mark, coment, quote]
        writer.writerow([name, mark, coment, quote, time1])
        list_music.append(list_info)

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
    header = ["name", "time", "mark", "coment", "quote", ]

    #设置列头加粗
    font = xlwt.Font()
    font.bold = True

    #设置列头单元格居中
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
    for list in list_music:
        j = 0
        for data in list:
            sheet.write(i, j, data)
            j += 1
        i += 1
    #设置单元格宽度
    sheet.col(0).width = 256 * 30
    sheet.col(1).width = 256 * 10
    sheet.col(2).width = 256 * 10
    sheet.col(3).width = 256 * 15
    sheet.col(4).width = 256 * 60

    # 保存文件
    book.save('doubanmovie.xls')
