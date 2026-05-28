import selenium.webdriver.support.ui as ui                    # 每五秒檢查元素是否存在
from selenium import webdriver                                # 開啟瀏覽器
from selenium.webdriver.common.by import By                   # 定位元素
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.select import Select          # 檢查給定的元素是select tag
from webdriver_manager.chrome import ChromeDriverManager      # 使用chrome瀏覽器
import time                                                   # 時間處理
import pandas as pd                                           # 資料處理和資料分析
import csv                                                    # 讀取與寫入csv
#pip install webdriver-manager
#python.exe -m pip install --upgrade pip
#driver = webdriver.Chrome(ChromeDriverManager().install())   # 使用ChromeDriverManager自動下載chromedriver

driver = webdriver.Chrome()                                          # 使用ChromeDriverManager自動下載chromedriver
driver.get("https://www.hilife.com.tw/storeInquiry_street.aspx")     # 打開網站
time.sleep(5)                                                        # 等待5秒

### 所有縣市的所有鄉鎮市區的分店資訊
# 將萊爾富分店資訊儲存到csv
with open('tcode/HiLifeShop.csv', 'w', encoding='UTF-8-Sig', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    ### 第一個縣市的所有鄉鎮市區的分店資訊
    # 第一個縣市的第一個鄉鎮市區的分店資訊
    num_tr= driver.find_elements(By.XPATH, '//table/tbody/tr')       # 找到所有表格列元素
    for tr_ in num_tr:
        for tr_2 in tr_.text.split('\n'):                            # 將字串以'\n'分割
            print(tr_2)                                              # 輸出text文字
            csv_writer.writerow([tr_2])                              # 寫入csv

    # 第一個縣市的第二個到第十二個鄉鎮市區的分店資訊
    j = 0
    for j in range(11):
        j += 1
        sel_2 = Select(driver.find_element(By.NAME, "AREA"))         # 找到鄉鎮市區元素
        sel_2.options[j].click()                                     # .click()模擬使用者依序點擊下一個鄉鎮市區(第二個到第十二個鄉鎮市區)
        time.sleep(5)                                                # 等待5秒

        num_tr= driver.find_elements(By.XPATH, '//table/tbody/tr')   # 找到所有表格列元素
        for tr_ in num_tr:
            for tr_2 in tr_.text.split('\n'):                        # 將字串以'\n'分割
                print(tr_2)                                          # 輸出text文字
                csv_writer.writerow([tr_2])                          # 寫入csv

    ### 第二個縣市到第十七個縣市的所有鄉鎮市區的分店資訊
    i = 0
    j = 0
    k = 0
    nums = [12, 6, 23, 9, 10, 13, 12, 28, 17, 10, 12, 12, 24, 29, 17, 3, 2]   # 列出所有縣市的鄉鎮市區數量

    # 第二個縣市到第十七個縣市
    for i in range(16):
        i += 1
        sel = Select(driver.find_element(By.NAME, "CITY"))           # 找到縣市元素
        sel.options[i].click()                                       # .click()模擬使用者依序點擊下一個縣市(第二個到第十七個縣市)
        time.sleep(5)                                                # 等待5秒

        # 第一個鄉鎮市區的所有店面資訊
        num_tr= driver.find_elements(By.XPATH, '//table/tbody/tr')   # 找到所有表格列元素
        for tr_ in num_tr:
            for tr_2 in tr_.text.split('\n'):                        # 將字串以'\n'分割
                print(tr_2)                                          # 輸出text文字
                csv_writer.writerow([tr_2])                          # 寫入csv

        # 第二個到第k個鄉鎮市區的所有店面資訊
        k += 1
        for j in range(nums[k]-1):
            j += 1
            sel_2 = Select(driver.find_element(By.NAME, "AREA"))           # 找到鄉鎮市區元素
            sel_2.options[j].click()                                       # .click()模擬使用者依序點擊下一個鄉鎮市區(第二個到第k個鄉鎮市區)
            time.sleep(5)                                                  # 等待5秒

            num_tr= driver.find_elements(By.XPATH, '//table/tbody/tr')     # 找到所有表格列元素
            for tr_ in num_tr:
                for tr_2 in tr_.text.split('\n'):                          # 將字串以'\n'分割
                    print(tr_2)                                            # 輸出text文字
                    csv_writer.writerow([tr_2])                            # 寫入csv

# 讀取csv檔
with open('tcode/HiLifeShop.csv', 'r', encoding='UTF-8-Sig') as csv_file:
    house_ = csv.reader(csv_file, delimiter=",")
    for row in house_:
        print(row[0])         # 輸出第一欄


