from datetime import datetime
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
    
    now = datetime.now()
    time = now.strftime("%Y/%m/%d %H:%M:%S")

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
        event_type = list(reversed(dtObjects))[i].findAll("span", recursive=False)[0].get_text()

        # tag color
        if event_type == '更新':
            tag_color = 16077457
        elif event_type == '系統':
            tag_color = 10512325
        else:
            tag_color = 3775462

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
            content = ""
            for e in section:
                for x in e.find_all():
                    if len(x.get_text(strip=True)) == 0 and x.name != 'br':
                        x.extract()
                for div in e.find_all('div'):
                    div.unwrap()
                brtag = str(e).replace("<br/>", "\n")
                multiblank = re.sub("([ \t]*\n){3,}", "\n\n", brtag)
                content += BeautifulSoup(multiblank, "html.parser").get_text()
            content = content.replace('*', '×')
            content = (content[:500] + ' ......\n[詳細內容](' + news_link + ')') if len(content) > 500 else content

            embed = DiscordEmbed()
            embed.set_author(name='超異域公主連結☆Re：Dive', icon_url='http://www.princessconnect.so-net.tw/images/pc-icon.png')
            embed.title = current_title
            embed.url = news_link
            embed.description = content
            embed.color = tag_color
            
            for link in webhook_links:
                new_embed = embed
                webhook = DiscordWebhook(url=link)
                webhook.add_embed(new_embed)
                webhook.execute()
            print(f'[{time}] - 已更新：{current_title}')
            isUpdated = True
        else:
            print(f'[{time}] - 未更新：{current_title}')

    while len(writeTitles) > 20:
        writeTitles.pop()

    if isUpdated:
        print(f'[{time}] - 已儲存檔案')
        f.seek(0)
        f.truncate(0)
        f.writelines(writeTitles)
    f.close()


if __name__ == '__main__':
    get_pcrd_news()
