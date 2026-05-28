import requests                                         # 建立各種HTTP 請求並從網頁伺服器上取得想要的資料
from bs4 import BeautifulSoup                           # 快速解析網頁 HTML 碼
import lxml                                             # 解析XML結構
import os                                               # 獲取檔案的所在路徑
import csv                                              # 讀取與寫入csv

### 取得每頁30個室內設計案例各10張照片網址，共5頁
# 將室內設計案例照片網址儲存到csv
with open('tcode/OrderHouseLink.csv', 'w', encoding='UTF-8-Sig', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    # 爬取第1個到第五個分頁
    i = 1
    for i in range(5):
        i += 1
        j = str(i)
        url = "https://www.order.com.tw/case.php?page=" + j     # 用for迴圈取得1-5頁網頁連結
        response = requests.get(url = url)                      # 透過requests請求網頁內容
        soup = BeautifulSoup(response.text,"html.parser")       # 將網頁資料以html.parser解析
        sel = soup.select("div.pic a")                          # 取得HTML的 <div class="pic"></div> 中的<a>標籤存入sel
        # 爬取第1個到第30個室內設計案例
        for s in sel:
            title = s["title"]
            url = "https://www.order.com.tw/" + s["href"]       # 用for迴圈取得第i頁的所有室內設計案例網址(30個)
            response = requests.get(url = url)                  # 透過requests請求網頁內容
            soup_2 = BeautifulSoup(response.text, "lxml")       # 將網頁資料以lxml解析
            results = soup_2.find_all("img", {"class": "img-responsive"}, limit=11)    # 取得HTML中最多10個<img>標籤
            image_links = [result.get("src") for result in results][1:]                # 取得圖片來源連結

            # 建立空list，並將圖片來源連結放入list
            article = []
            for p in image_links:
                article.append(p)

            # 將list中的text元素合併成一個字串，並以'\n'來間隔
            articleAll = '\n'.join(article)

            # 將字串以'\n'分割
            m = 0
            for article in articleAll.split('\n'):
                m += 1
                num = title + "照片" + str(m) + ": "
                house_net = "https://www.order.com.tw/" + article
                csv_writer.writerow([num, house_net])              # 寫入室內設計案例名稱及照片網址

# 讀取csv檔
with open('tcode/OrderHouseLink.csv', 'r', encoding='UTF-8-Sig') as csv_file:
    house_ = csv.reader(csv_file, delimiter=",")
    for row in house_:
        print(row[0] + row[1])     # 輸出第一欄和第二欄


