### 4.24
更新打包exe/macos-app文件  
```
pyinstaller --console --onefile 文件名(不可有中文路径和空格)
```
添加数据可视化demo图片  

![image](https://raw.githubusercontent.com/Willmind/douban-movie-250/master/demo.png)

### 4.22
webstorm 自带local history,切换分支忘记提交代码也可以代码历史记录回溯  
添加随机ua，使用fake-useragent库，构造随机ua   
添加requirements.txt配置文件Python一键安装所有依赖  
在新的工作空间一键安装

    pip install -r requirements.txt


### 4.20～21学习爬虫记录
在apple music听陶喆的专辑  
然后就想去百度搜国内的专辑榜单  
搜到豆瓣音乐评分前250  
进去以后发现没有筛选和对应的数据提取功能  
就想怎么把数据爬下来  

#### 步骤：  
了解爬虫知识和网络请求协议  
下载并安装pycharm IDE  
上网搜索相关爬虫代码  
发现豆瓣数据不走network请求，所以不抓取网络，直接爬取页面源码  
使用xpath库截取网页html数据，并用正则表达式匹配  
使用xlwt库保存数据并写入csv和生成excel文件  

#### 问题：  
多次爬取触发网站反爬机制，ip被封禁  
爬虫过程等待时间较长，且过程中并未知道具体数据  

#### 解决方案：   
搭建并使用ip数据流量池  
- [x] 通过asleep降低请求频率  
- [x] 添加进度条  

#### 后续研究：  
- [x] 如何打包生成exe文件  
- [x] 把csv格式转成json数据，并增加数据分析  
- [x] 添加数据可视化  
- [x] Python项目依赖环境怎么做成一键配置  
后续可扩展至其他网站的数据爬取  

#### 学习要点：  
新版pycharm内置虚拟机解释器，可无需安装python  
Python语法回顾并学习  
Python工程构建和对应调试  
相关依赖库的学习  
如何破解反爬机制  



