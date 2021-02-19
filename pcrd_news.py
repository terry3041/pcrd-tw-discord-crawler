import datetime
import requests
import threading
import urllib.parse
import re
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook, DiscordEmbed

base_Url = 'http://www.princessconnect.so-net.tw'
current_title = None
timer_interval = 600
webhook_links = ['']

def get_pcrd_news():
    global current_title
    global timer_interval
    
    # File Input
    f = open('pcrd_titles.txt','r+', encoding="utf-8")
    readTitles = f.readlines()
    writeTitles = readTitles

    # Crawler
    r = requests.get("http://www.princessconnect.so-net.tw/news")
    soup = BeautifulSoup(r.text, 'html.parser')
    divObjects = soup.find_all("dd")
    dtObjects = soup.find_all("dt")

    r = requests.get("http://www.princessconnect.so-net.tw/news?page=2") # Page 2
    soup = BeautifulSoup(r.text, 'html.parser')
    divObjects += soup.find_all("dd")
    dtObjects += soup.find_all("dt")

    isUpdated = False
    for i in range(len(divObjects)):
        title = list(reversed(divObjects))[i].findAll("a", recursive=False)[0]
        event_type = dtObjects[i].findAll("span", recursive=False)[0].get_text()

        # tag color
        tag_color = 16077457
        if event_type == '活動':
            tag_color = 3775462
        elif event_type == '系統':
            tag_color = 10512325

        current_title = title['title']
        find_news = False
        for line in readTitles:
            if current_title in line:
                find_news = True
                break

        if find_news == False and "外掛停權" not in current_title:
            writeTitles.insert(0, current_title + '\n')
            current_link = title['href']
            r = requests.get(base_Url + current_link)
            soup = BeautifulSoup(r.text, 'html.parser')

            news_link = urllib.parse.urljoin(base_Url, current_link)

            section = soup.select('body > main > article > article > section > p')
            content = ''
            for e in section:
                b = re.sub("(<br *\/?>\s*)(<br *\/?>\s*)(<br *\/?>\s*)+", "<br/><br/>", str(e))
                fb = b.replace("<br/>", "\n")
                content += BeautifulSoup(fb, "html.parser").get_text()
            content = content.replace('*', '×')
            content = (content[:1000] + ' ......\n[詳細內容](' + news_link + ')') if len(content) > 1000 else content

            embed = DiscordEmbed()
            embed.set_author(name='超異域公主連結☆Re：Dive - ' + event_type, icon_url='http://www.princessconnect.so-net.tw/images/pc-icon.png')
            embed.title = current_title
            embed.url = news_link
            embed.description = content
            embed.color = tag_color
            
            for link in webhook_links:
                new_embed = embed
                webhook = DiscordWebhook(url=link)
                webhook.add_embed(new_embed)
                webhook.execute()
            print("已更新：" + current_title)
            isUpdated = True
        else:
            print("未更新：" + current_title)

    while len(writeTitles) > 20:
        writeTitles.pop()

    if isUpdated:
        print("已儲存檔案")
        f.seek(0)
        f.truncate(0)
        f.writelines(writeTitles)
    f.close()


if __name__ == '__main__':
    get_pcrd_news()
