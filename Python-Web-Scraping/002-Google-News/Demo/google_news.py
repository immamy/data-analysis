import requests                                         # 建立各種HTTP 請求並從網頁伺服器上取得想要的資料
import pandas as pd                                     # 資料處理和資料分析
import os                                               # 獲取檔案的所在路徑
import jieba                                            # 分割文章
import nltk                                             # 自然語言處理
import numpy as np                                      # 對陣列運算提供大量的數學函數函式庫
from bs4 import BeautifulSoup                           # 快速解析網頁 HTML 碼
from wordcloud import WordCloud                         # 文字雲
from matplotlib.font_manager import FontProperties      # 顯示字體
import matplotlib.pyplot as plt                         # 視覺化

# google新聞網址
url = 'https://news.google.com/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRGx1YlY4U0JYcG9MVlJYR2dKVVZ5Z0FQAQ?hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant'
r = requests.get(url)                                   # 令r 透過reuqests存取我們在網頁想要的資料
web_content = r.text                                    # 令web_content為文章字串
soup = BeautifulSoup(web_content,'lxml')

# 進入Google新聞，國際，新聞標題右鍵，檢查，目標是爬到新聞標題與連結。
# 觀察每一個新聞標題與連結的標籤框架，向上收合div，找出能包裹新聞標題與連結的div class。
title = soup.find_all('div', class_='f9uzM')  # gPFEn  # WwrzSb  # XlKvRb  # MCAGUe
# 新聞標題
titles = [t.find('a').text for t in title]
# 新聞連結
newUrls = [requests.get(t.find('a')['href'].replace('.','https://news.google.com', 1)).url for t in title]
# 將新聞標題跟新聞連結表格化
df = pd.DataFrame(
{
    'title': titles,
    'links': newUrls
})
# 抓網頁內的第2個連結得到文章
url = df['links'][1]
r = requests.get(url)
web_content = r.text
soup = BeautifulSoup(web_content, 'lxml')
print("新聞網址:{}".format(df['links'][1]))
# 新聞文章
articleContent = soup.find_all('p')
print("新聞:{}".format(articleContent))
# 個別取出文章的每個字並放進list。
article = []
for p in articleContent:
    article.append(p.text)

# 將list合併成字串，並以'\n'來間隔
articleAll = '\n'.join(article)
# 移除標點符號
d = articleAll.replace('[^\w\s]','').replace('／',"").replace('《','').replace('》','').replace('，','').replace('。','').replace('「','').replace('」','').replace('（','').replace('）','').replace('！','').replace('？','').replace('、','').replace('▲','').replace('…','').replace('...','').replace('：','').replace(':','').replace(' ','').replace('~','').replace('_','').replace('#','').replace('!','').replace('.','').replace('=','').replace('?','').replace('-','').replace('/','').replace('(','').replace(')','').replace('“','').replace('”','').replace('～','').replace('"','').replace(',',"").replace('；',"").replace('‵',"").replace('′',"").replace('・',"").replace('【',"").replace('】',"").replace('[',"").replace(']',"").replace(' ',"").replace('',"").replace('．',"")
print(d)
# 輸入字典的路徑
jieba.load_userdict('tcode\dict.txt')
# 文字分割
Sentence = jieba.cut_for_search(d)
# 設定停用字詞
stopwords = {}.fromkeys(['也', '但', '來', '個', '再', '的', '和', '是', '有', '更', '會', '可能', '有何', '從', '對', '就', '或', '了', '後', '去', '來', '越', '為', '即', '這種', '多', '越來', '像', '在', '與', '於', '讓', '被', '您', '他', '她', '我', '人', '中', '日', '上', '堆', '阿', '啊', '嗎', '那', '說', '啦', '你', '覺得', '就是', '跟', '很', '什麼', '都', '才', '表示', '造成', '事件', '報導', '指出'])
# 建立空list儲存斷詞，遇到停用字詞則跳過。
word_list = []
for i in Sentence:
    if i in stopwords:
        continue
    else:
        word_list.append(i.strip())
print(word_list)

# 計算詞頻
#print(Counter(word_list))
# 將斷詞存入字典
word_count = dict()
for k in word_list:
    if k in word_count.keys():
        word_count[k] += 1
    else:
        word_count[k] = 1
# 輸出dataframe並儲存成csv檔
wc_list = pd.DataFrame.from_dict(word_count, orient="index", columns=['次數'])
wc_list = wc_list.sort_values(by=['次數'], ascending=False)
wc_list.to_csv("tcode/WordFrequency.csv", encoding="utf-8-sig")

# 文字雲
wc = WordCloud(font_path="C:/NotoSansCJKtc-hinted/NotoSansMonoCJKtc-Bold.otf",      # 設置字體
               background_color="white",
               width = 1000,
               height = 500,
               scale = 1.5,                                                         # 背景顏色
               max_words = 2000,                                                    # 文字雲顯示最大詞數
               stopwords=stopwords)                                                 # 停用字詞
wc.generate_from_frequencies(word_count)
# 視覺化呈現
plt.imshow(wc)
plt.axis("off")
#plt.figure(figsize=(100,100))                  # 顯示圖框架大小
plt.show()
wc.to_file("tcode/WordCloudPlt.png")

# 重新命名標題
new_colunms = ['斷詞', '次數']
# 讀取.csv檔
df_2 = pd.read_csv('tcode/WordFrequency.csv', names = new_colunms, header = 0)
# 寫入.csv檔
df_2.to_csv("tcode/WordFrequency.csv", encoding="utf-8-sig")

# 取前15筆資料製作圓餅圖及長條圖
df_3 = df_2.head(15)
print(df_3)

# 圓餅圖 #Pie chart
labels = df_3["斷詞"]                                          # 製作圓餅圖的類別標籤
size = df_3["次數"]                                            # 製作圓餅圖的數值來源
plt.figure(figsize=(20,10), dpi = 200)                         # 顯示圖框架大小
plt.pie(size,                                                  # 數值
        labels = labels,                                       # 標籤
        autopct = "%1.1f%%",                                   # 將數值百分比並留到小數點一位
        pctdistance = 0.6,                                     # 數字距圓心的距離
        textprops = {"fontsize" : 12},                         # 文字大小
        shadow=False)                                          # 設定陰影
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK TC']         # 將字體換成思源黑體
plt.axis('equal')                                              # 使圓餅圖比例相等
plt.title("Pie chart", {"fontsize" : 18})                      # 設定標題及其文字大小
plt.legend(loc = "best")
#plt.figure(figsize=(100,100))                                 # 顯示圖框架大小
#plt.show()
plt.savefig("tcode\PieChartPlt.jpg",  # 儲存圖檔
            bbox_inches='tight',                               # 去除座標軸占用的空間
            pad_inches=0.0)                                    # 去除所有白邊
plt.close()

# 長條圖 #Bar chart
df_3.plot.bar(x="斷詞",y="次數")
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK TC']         # 將字體換成思源黑體
plt.title('Bar chart')                                         # 設定圖表標題
plt.xlabel('item')                                             # 設定x軸標題
plt.ylabel('frequency')                                        # 設定y軸標題
plt.legend(loc = "best")
#plt.figure(figsize=(100,100))                                 # 顯示圖框架大小
#plt.show()
lgd = plt.legend(loc='best')
plt.savefig("tcode\BarChartPlt.jpg",  # 儲存圖檔
            dpi = 200,                                         # 設定圖框架大小
            pad_inches=0.0,                                    # 去除所有白邊
            bbox_extra_artists=(lgd))                          # 設定圖例
plt.close()


