# PCRD-TW-webhook-crawler

從 [台版《超異域公主連結☆Re：Dive》官方網站](http://www.princessconnect.so-net.tw/news) 進行爬蟲解析，抓取最新的公告並透過 webhook 發佈到 Discord 上。

## 例子

<img src="https://i.imgur.com/Yvwwpz2.png" width="250">

## 開始使用

### 環境需求

- [Python 3.8.0+](https://www.python.org/)

### 安裝方式

若要執行 PCRD-TW-webhook-crawler，需要安裝額外的套件，使用終端機至此專案的資料夾中執行此指令：

```bash
pip3 install -r requirements.txt
```

### 設定

用任意的文字編輯器開啟 `pcrd_news.py`，在

```py
webhook_links = []
```

插入 Discord 的 webhook 連結，如下：

```py
webhook_links = [ 'https://discordapp.com/api/webhooks/.../...' ]
```

如果您有超過一個連結需要加入，請使用逗號分隔：

```py
webhook_links = [ 'https://discordapp.com/api/webhooks/.../...',
                  'https://discordapp.com/api/webhooks/.../...'
                ]
```

### 使用方式

使用終端機至專案資料夾執行此指令：

```bash
python3 pcrd_news.py
```

## 作者

- 原作者 [@jinan-tw](https://github.com/jinan-tw)
- 優化 [@terry3041](https://github.com/terry3041)
