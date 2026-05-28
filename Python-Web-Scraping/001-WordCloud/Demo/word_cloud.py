import pandas as pd                                     # 資料處理和資料分析
from wordcloud import WordCloud                         # 文字雲
from matplotlib.font_manager import FontProperties      # 顯示字體
import matplotlib.pyplot as plt                         # 視覺化

# 設定停用字詞
stopwords = {}.fromkeys(['也', '但', '來', '個', '再', '的', '和', '是', '有', '更', '會', '可能', '有何', '從', '對', '就', '或', '了', '後', '去', '來', '越', '為', '即', '這種', '多', '越來', '像', '在', '與', '於', '讓', '被', '您', '他', '她', '我', '人', '中', '日', '上', '堆', '阿', '啊', '嗎', '那', '說', '啦', '你', '覺得', '就是', '跟', '很', '什麼', '都', '才', '表示', '造成', '事件', '報導', '指出', '[^\w\s]', '／', '《', '》', '，', '。', '「', '」', '（', '）', '！', '？', '、', '▲', '…', '...', '：', ':', ' ', '~', '_', '#', '!', '.', '=', '?', '-', '/', '(', ')', '“', '”', '～', '"', ',', '；', '‵', '′', '・', '【', '】','[', ']', ' ', '', '．'])

# 1. 讀取 CSV 檔案 # 確保編碼正確 (中文常用 utf-8-sig 或 gbk)
df = pd.read_csv('tcode/WordFrequency.csv')

# 2. 將 DataFrame 轉換為 {詞: 頻率} 的字典格式 # 假設第一列是 word，第二列是 freq
word_freq = dict(zip(df['斷詞'].dropna().astype(str), df['次數']))  # 將NaN(float)轉成str
# 文字雲
wc = WordCloud(font_path="C:/NotoSansCJKtc-hinted/NotoSansMonoCJKtc-Bold.otf",      # 設置字體
               background_color="white",
               width = 1000,
               height = 500,
               scale = 1.5,                                                         # 背景顏色
               max_words = 2000,                                                    # 文字雲顯示最大詞數
               stopwords=stopwords)                                                 # 停用字詞
wc.generate_from_frequencies(word_freq)
# 視覺化呈現
plt.imshow(wc)
plt.axis("off")
#plt.figure(figsize=(100,100))                                # 顯示圖框架大小
plt.show()
wc.to_file("tcode/WordCloudPlt.png")

# 取前15筆資料製作圓餅圖及長條圖
df_3 = df.head(15)
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


