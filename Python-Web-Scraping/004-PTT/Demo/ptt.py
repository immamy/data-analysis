import requests                                         # 建立各種HTTP 請求並從網頁伺服器上取得想要的資料
from bs4 import BeautifulSoup                           # 快速解析網頁 HTML 碼
import re                                               # 正則表達式
import pandas as pd                                     # 資料處理和資料分析
import jieba                                            # 分割文章
from wordcloud import WordCloud                         # 文字雲
import matplotlib.pyplot as plt                         # 視覺化
import matplotlib.font_manager as fm                    # 字體管理
from matplotlib.font_manager import FontProperties      # 顯示字體
from collections import Counter                         # 計算數量

# 取得ptt看板網址
r = requests.get("https://www.ptt.cc/bbs/MobileComm/index.html") #將網頁資料GET下來
soup = BeautifulSoup(r.text, 'lxml')
# 看版網頁原始碼
titles = soup.findAll('div', class_ = 'title')
# 看板標題
sel = soup.select("div.title a")   #取HTML標中的 <div class="title"></div> 中的<a>標籤存入sel
results = []
for s in sel:
    title_ = s.text
    results.append(title_)
# 看板連結
urlList = []
for s in sel:
    href_ = s["href"]
    title_ = s.text
    url = "https://www.ptt.cc" + s["href"]
    urlList.append(url)
# 看板標題及連結
URLlist = {
    "title": results,
    "links": urlList,
}
df = pd.DataFrame(URLlist)
# 儲存成csv檔
df.to_csv("tcode/PttTitlesAndLinks.csv", encoding="utf-8-sig")
# 儲存excel，index = False表示不存入索引值。
# df.to_excel("tcode/PttTitlesAndLinks.xlsx", index = False)

# 抓網頁內的第2個連結得到留言
url = df['links'][1]
response = requests.get(url = url)
soup_2 = BeautifulSoup(response.text, 'lxml')
print("看板連結:{}".format(df['links'][1]) )
print("看板標題:{}".format(df['title'][1]) )
# 看板內所有留言
messagesList = []
timeList = []
sel_2 = soup_2.find_all("div", "push") #取HTML標中的 <div class="title"></div> 中的<a>標籤存入sel
for item in sel_2:
    # 遇到"檔案過大！部分文章無法顯示"時，跳出該次迴圈。
    if soup_2.find_all("div", "push center warning-box"):
        continue
    else:
        content = item.find('span', 'f3 push-content')
        time = item.find('span', 'push-ipdatetime')
        #print(title_, content.text, time.text)
        messagesList.append(content.text)
        timeList.append(time.text)
# 看板留言及時間
MessagesLIST = {
    "messages": messagesList,
    "time": timeList,
}
df = pd.DataFrame(MessagesLIST)
# 儲存成csv檔
df.to_csv("tcode/PttMessagesAndTime.csv", encoding="utf-8-sig")
# 儲存excel，index = False表示不存入索引值。
# df.to_excel("tcode/PttMessagesAndTime.xlsx", index = False)

# 將list中的text元素合併成一個字串，並移除標點符號
text = messagesList
Str = "".join(text)
Str_2 = re.sub("\n", " ", Str)
string_data = Str_2.replace('[^\w\s]','').replace('／',"").replace('《','').replace('》','').replace('，','').replace('。','').replace('「','').replace('」','').replace('（','').replace('）','').replace('！','').replace('？','').replace('、','').replace('▲','').replace('…','').replace('...','').replace('：','').replace(':','').replace(' ','').replace('~','').replace('_','').replace('#','').replace('!','').replace('.','').replace('=','').replace('?','').replace('-','').replace('/','').replace('(','').replace(')','').replace('“','').replace('”','').replace('～','').replace('"','').replace(',',"").replace('；',"").replace('‵',"").replace('′',"").replace('・',"").replace('【',"").replace('】',"").replace('[',"").replace(']',"").replace(' ',"").replace('',"").replace('．',"")
print(string_data)
# 輸入自己字典的路徑
jieba.load_userdict('tcode\dict.txt')
# 文章斷詞
Sentence = jieba.cut(string_data, cut_all = False)
#Sentence = jieba.cut_for_search(string_data)
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
wc_list.to_csv("tcode/PttWordFrequency.csv", encoding="utf-8-sig")

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
#plt.figure(figsize=(100,100))                   # 顯示圖框架大小
plt.show()
wc.to_file("tcode/PttWordCloudPlt.png")

# 重新命名標題
new_colunms = ['斷詞', '次數']
# 讀取.csv檔
df_2 = pd.read_csv('tcode/PttWordFrequency.csv', names = new_colunms, header = 0)
# 寫入.csv檔
df_2.to_csv("tcode/PttWordFrequency.csv", encoding="utf-8-sig")

# 取前15筆資料製作圓餅圖及長條圖
df_3 = df_2.head(15)
print(df_3)

# 圓餅圖 #Pie chart
labels = df_3["斷詞"]                                       # 製作圓餅圖的類別標籤
size = df_3["次數"]                                         # 製作圓餅圖的數值來源
plt.figure(figsize=(20,10), dpi = 200)                      # 顯示圖框架大小
plt.pie(size,                                               # 數值
        labels = labels,                                    # 標籤
        autopct = "%1.1f%%",                                # 將數值百分比並留到小數點一位
        pctdistance = 0.6,                                  # 數字距圓心的距離
        textprops = {"fontsize" : 12},                      # 文字大小
        shadow=False)                                       # 設定陰影
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK TC']      # 將字體換成思源黑體
plt.axis('equal')                                           # 使圓餅圖比例相等
plt.title("Pie chart", {"fontsize" : 18})                   # 設定標題及其文字大小
plt.legend(loc = "best")
#plt.figure(figsize=(100,100))                               # 顯示圖框架大小
#plt.show()
plt.savefig("tcode\PttPieChartPlt.jpg",                          # 儲存圖檔
            bbox_inches='tight',                            # 去除座標軸占用的空間
            pad_inches=0.0)                                 # 去除所有白邊
plt.close()                                                 # 關閉圖表

# 長條圖 #Bar chart
df_3.plot.bar(x="斷詞",y="次數")
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK TC']      # 將字體換成思源黑體
plt.title('Bar chart')                                      # 設定圖表標題
plt.xlabel('item')                                          # 設定x軸標題
plt.ylabel('frequency')                                     # 設定y軸標題
plt.legend(loc = "best")
#plt.figure(figsize=(100,100))                               # 顯示圖框架大小
#plt.show()
lgd = plt.legend(loc='best')
plt.savefig("tcode\PttBarChartPlt.jpg",                          # 儲存圖檔
            dpi = 200,                                      # 設定圖框架大小
            pad_inches=0.0,                                 # 去除所有白邊
            bbox_extra_artists=(lgd))                       # 設定圖例
plt.close()                                                 # 關閉圖表


