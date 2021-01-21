# PCRD-TW-webhook-crawler
> PCRD-TW-webhook-crawler 將從[超異域公主連結RE:DIVE 台灣官方網站](http://www.princessconnect.so-net.tw/news)進行爬蟲解析，抓取最新的公告並透過webhook發佈到Discord上

# 開始使用
## 環境需求
- Python 3.8.0+ (https://www.python.org/)
- 需要安裝在requirements.txt中額外的套件

## 安裝方式
若要執行PCRD-TW-webhook-crawler，需要安裝額外的套件，使用終端機至此專案的資料夾中下此指令：

```
pip install -r requirements.txt
```

## 設定
用任意的文字編輯器開啟 "pcrd_news.py"，在
```py
webhook_links = []
```
插入Discord的webhook連結，如下：
```py
webhook_links = [ 'https://discordapp.com/api/webhooks/.../...']
```
如果您有超過一個連結需要加入，請使用逗號分隔：
```py
webhook_links = [ 'https://discordapp.com/api/webhooks/.../...',
                  'https://discordapp.com/api/webhooks/.../...'
                ]
```
## 使用方式
使用終端機至專案資料夾執行此指令：
```
python pcrd_news.py
```
或
```
python3 pcrd_news.py
```
