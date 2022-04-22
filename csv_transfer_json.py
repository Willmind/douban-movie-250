import json

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
