import xlwt
import csv
import requests
from lxml import etree
import time
from tqdm import tqdm
# 加随机ua，使用fake-useragent库，构造随机ua
from fake_useragent import UserAgent

list_movie = []
# 请求头
headers = {'User-Agent': str(UserAgent().random)}

# 爬取的内容保存在csv文件中
f = open(r"C:\Users\tanzhijingg\Desktop\douban_music.csv", "w+", newline='', encoding="gb18030")
writer = csv.writer(f, dialect='excel')
# csv文件中第一行写入标题
writer.writerow(["song", "singer", "time", "liupai", "mark", "comment"])


# 定义爬取内容的函数
def music_info(url):
    html = requests.get(url, headers=headers)
    selector = etree.HTML(html.text)

    infomation = selector.xpath('//tr[@class="item"]')
    for info in infomation:
        song = info.xpath('td[2]/div/a/text()')[0].strip()
        singer = info.xpath('td[2]/div/p/text()')[0].split("/")[0]
        times = info.xpath('td[2]/div/p/text()')[0].split("/")[1]
        liupai = info.xpath('td[2]/div/p/text()')[0].split("/")[-1]
        mark = float(info.xpath('td[2]/div/div/span[2]/text()')[0].strip())
        comment = int(
            info.xpath('td[2]/div/div/span[3]/text()')[0].strip().strip("(").strip(")").replace('人评价', '').strip())

        list_info = [song, singer, times, liupai, mark, comment]
        writer.writerow([song, singer, times, liupai, mark, comment])
        list_movie.append(list_info)

    # 防止请求频繁，故睡眠1秒
    time.sleep(1)


if __name__ == '__main__':
    urls = ['https://music.douban.com/top250?start={}'.format(str(i)) for i in range(0, 250, 25)]
    # 调用函数music_info循环爬取内容
    for url in tqdm(urls):
        music_info(url)
    # 关闭csv文件
    f.close()
    # 爬取的内容保存在xls文件中
    header = ["song", "singer", "time", "liupai", "mark", "comment"]

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
    sheet.col(1).width = 256 * 20
    sheet.col(2).width = 256 * 10
    sheet.col(3).width = 256 * 15
    sheet.col(4).width = 256 * 10
    sheet.col(5).width = 256 * 10

    # 保存文件
    book.save('douban_music.xls')
