import numpy as np
from sklearn.preprocessing import StandardScaler
import sqlite3
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime

def pre(y):
    total_year = 13
    request_year = 2024 - y

    conn = sqlite3.connect('期末/data.db')
    cur = conn.cursor()

    cur.execute(f'SELECT * FROM record')
    data = cur.fetchall()
    data = [d for i, d in enumerate(data) if i % total_year < request_year]

    data = np.array(data)
    X = data[:, :-2]
    y = data[:, -2:]

    scalerx = StandardScaler()
    X = scalerx.fit_transform(X)
    scalery = StandardScaler()
    y = scalery.fit_transform(y)



    s = {3, 7, 9, 13, 14, 16}
    mapping = {
        '靜風': 0,
        '北': 0,
        '北北東': 22.5,
        '東北': 45,
        '東北東': 67.5,
        '東': 90,
        '東南東': 112.5,
        '東南': 135,
        '南南東': 157.5,
        '南': 180,
        '南南西': 202.5,
        '西南': 225,
        '西南西': 247.5,
        '西': 270,
        '西北西': 292.5,
        '西北': 315,
        '北北西': 337.5
    }

    url = 'https://www.cwa.gov.tw/V8/C/W/OBS_Station.html?ID=46694'
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, features='lxml')
    driver.quit()

    current_date = datetime.now()
    formatted_date = current_date.strftime("%m%d")
    date_as_int = int(formatted_date)
    day = (date_as_int % 100) + (date_as_int // 100) * 31
    day *= total_year

    now_data = []
    titles=soup.find_all("tr")  
    for title in titles[1:]: 
        tmp = [day]
        for i, x in enumerate(title.contents):
            if x.name == 'td' and i in s:
                if x.contents[0].text == '-' or x.contents[0].text == '－':
                    tmp.append(0)
                    continue
                
                if i == 7:
                    tmp.append(mapping.get(x.contents[0].text, None))
                elif i == 9:
                    tmp.append(float(x.contents[0].text))
                elif i == 13:
                    if '>' in x.contents[0].text:
                        tmp.append(float(x.contents[0].text[1:]))
                    elif '-' in x.contents[0].text:
                        t = x.contents[0].text.split('-')
                        tmp.append((float(t[0]) + float(t[1])) / 2)
                    else:
                        tmp.append(float(x.contents[0].text))
                else:
                    tmp.append(float(x.contents[0].text))
        now_data.append(tmp)

    new_data_point = np.array(now_data).mean(axis=0)
    print(new_data_point)
    new_data_point_sca = scalerx.transform(new_data_point.reshape(1, 7)).reshape(7)
    k = 3*request_year
    
    distances=np.linalg.norm(X-new_data_point_sca, axis=1) #計算資料案例與新案例的距離list
    nearest_neighbor_ids = distances.argsort()[:k] #排序距離list並取前k個案例
    nearest_neighbor_rings = y[nearest_neighbor_ids] 
    prediction = nearest_neighbor_rings.mean(axis=0) 
    
    nearest_neighbor_ids += request_year 
    nearest_neighbor_ids %= len(X)
    nearest_neighbor_rings2 = y[nearest_neighbor_ids] 
    prediction2 = nearest_neighbor_rings2.mean(axis=0) 

    print("Sci Learn prediction:")
    print(scalery.inverse_transform(prediction.reshape(1, -1))[0])
    print(scalery.inverse_transform(prediction2.reshape(1, -1))[0])
    
    return list(new_data_point), list(scalery.inverse_transform(prediction.reshape(1, -1))[0]), \
            list(scalery.inverse_transform(prediction2.reshape(1, -1))[0])

# a = pre(2018)


