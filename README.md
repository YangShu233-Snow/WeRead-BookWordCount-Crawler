# WeRead-BookWordCount-Crawler

这是一个可以按照关键词，自动爬取微信读书上书籍字数信息的爬虫。开发其的主要目的是为我的博客的一个插件功能提供数据源。

## 依赖

+ python >= 3.8
+ requests
+ lxml

## 下载

您可以选择将本仓库克隆到本地，使用以下命令：

```bash
git clone https://github.com/YangShu233-Snow/WeRead-BookWordCount-Crawler.git
```

如果您喜欢ssh，同样可以：

```bash
git clone git@github.com:YangShu233-Snow/WeRead-BookWordCount-Crawler.git
```

本项目理论上在`python >= 3.8`下均可运行，但是并没有做相应的测试，我在此项目所使用的Python版本是`3.12.3`。

## 介绍

本项目主要服务于我个人博客的特殊需求，我需要一个自动化的脚本来帮我获得相应的书籍字数数据。

这个脚本的运作原理如下：

1. 加载待搜索的书目
2. 使用相应的书本名称，请求微信读书的API，获得搜索结果
3. 解析搜索结果，请求解析出的所有书本结果分别对应的阅读器页面。
4. 从阅读器页面中解析出其提供的书本字数信息

## 使用

如果你想要使用这个脚本，可以使用以下命令：

```bash
cd to/the/programe/root_dir
python main.py
```

当然，在此之前你需要现在项目下的`input/`中提供待搜索的书目清单，使用`.txt`文本文件，格式如下：

```bash
book1
book2
book3
```

如果没有提供书目清单，脚本会载入默认搜索书目《百年孤独》。

本脚本提供了书目预加载程序，如果你没有相应的书目清单，可以执行以下命令：

```bash
cd to/the/programe/root_dir
python search_keywords_load.py
```

该程序会自动爬取豆瓣读书Top250榜上的所有书籍信息，加入到`input/books.txt`中。

爬虫脚本会将所有结果输出为一个`YAML`文件，数据格式为：

```yaml
- name: "百年孤独"
  words: 228000
- name: "百年孤独：张学良大传（尊荣与耻辱、得意与失意、成功与失败纠缠的传奇一生）"
  words: 158000
```