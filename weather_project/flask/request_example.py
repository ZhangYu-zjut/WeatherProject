
from urllib3 import *
import re
import requests
import json
import pymysql
import time
import datetime
# 爬取天气预报数据并更新到数据库中
# Get the headers information
def str2headers(file):
    header_dict = {}
    f = open(file ,'r')
    text = f.read()
    contents = re.split('\n' ,text)
    for line in contents:
        result =re.split(':', line, maxsplit=1)
        header_dict[result[0]] = result[1]
    f.close()
    return header_dict

# Get the whole cities information
def getCityList(file):
    cityList = []
    f = open(file, encoding='utf-8')
    contents = f.read()
    contents = re.split('\n', contents)
    for str in contents:
        cityCode = re.split('=', str)
        cityList.append(cityCode[0])
    # print(len(cityList)) # 2654 cities
    return cityList

# Get the city weather by city code
def get_city_weather(city_code):
    http = PoolManager()
    url = 'http://d1.weather.com.cn/sk_2d/' + city_code + '.html?_=1583040735053'
    r = requests.get(url,headers=headers,allow_redirects=False)
    # str2city_code("北京")
    str = r.content.decode('utf8')
    if r.status_code == 200:
        n = len("var dataSK = ")
        # http://d1.weather.com.cn/sk_2d/101011700.html?_=1583040735053
        str = str[n:]
        # print("new str us",str)
        weatherDict = json.loads(str)
        return weatherDict
    else:
        return None

# insert the data into mysql
def insert_data(weather):
    db = pymysql.connect("175.24.55.162", "root", "123456", "weather", charset="utf8")
    # INSERT INTO Persons VALUES ('Gates', 'Bill', 'Xuanwumen 10', 'Beijing')
    cursor = db.cursor()
    sql = "select cityName from t_weather"
    if 'aqi_pm25' not in weather or 'limitnumber' not in weather:
        return
    result = cursor.execute(sql)  # type result is <class 'int'>
    if True:
        sql = "insert into t_weather values "
        sql += "('" + weather['city'] + "','" + weather['cityname'] + "','" \
               + weather['nameen'] + "','" + weather['weather'] + "','" + weather['temp'] + "','" \
               + weather['sd'] + "','" + weather['njd'] + "','" + weather['WD'] + "','" \
               + weather['WS'] + "','" + weather['aqi_pm25'] + "','" + weather['limitnumber'] + "');"
        try:
            result2 = cursor.execute(sql)
            #print("result is",result2)
            # 提交到数据库执行
            db.commit()
        except Exception as e:
            time1_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print("time is:",time1_str)
            print("Exception:",e)
            # Rollback in case there is any error
            db.rollback()
        db.close()

# input the city weather Dict and save it into the Mysql
def save_data(weather,db,city):
    #print("weather is", weather)
    if 'aqi_pm25' not in weather or 'limitnumber' not in weather:
        return
    # update t_weather set (a = 'Gates',b = 'Bill',c = 'Beijing') where cityNumber = 'citycode'
    # sjon key words -> table column names
    wdata = {}
    wdata['cityNumber'] = weather['city']
    wdata['cityName'] = weather['cityname']
    wdata['cityNameen'] = weather['nameen']
    wdata['cityWeather'] = weather['weather']
    wdata['temp'] = weather['temp']
    wdata['sd'] = weather['sd']
    wdata['njd'] = weather['njd']
    wdata['wd'] = weather['WD']
    wdata['ws'] = weather['WS']
    wdata['pm25'] = weather['aqi_pm25']
    wdata['limitnumber'] = weather['limitnumber']
    cursor = db.cursor()
    sql = "update t_weather set "
    for var in wdata:
        if var == 'cityNumber':
            continue
        sql += (var + "='" + wdata[var] + "',")
    sql = sql.rstrip(',')
    "It is because the column name in Mysql is cityNuvber"
    sql += " where cityNumver = " + city + ";"
    #print("sql is",sql)
    cursor.execute(sql)
    try:
        #result2 = cursor.execute(sql)
        # print("result is",result2)
        # 提交到数据库执行
        db.commit()
    except Exception as e:
        time1_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print("time is:", time1_str)
        print("Exception:", e)
        # Rollback in case there is any error
        db.rollback()
    #db.close()

# citycode
# http://toy1.weather.com.cn/search?cityname=%E4%B8%8A%E6%B5%B7&callback=success_jsonpCallback&_=1583032681612

# http://d1.weather.com.cn/sk_2d/101210401.html?_=1583040735053
INTERVAL = 60 * 60
while True:
    http = PoolManager()
    headers = str2headers('head.txt')
    url = 'http://d1.weather.com.cn/sk_2d/101210401.html?_=1583040735053'
    r = requests.get(url, allow_redirects=False)  # 直接用requests时候，这里不需要headers
    city_code = getCityList('city_list.txt')
    # print(get_city_weather('101210401'))
    db = pymysql.connect("175.24.55.162", "root", "123456", "weather", charset="utf8")
    for city in city_code:
        weather = get_city_weather(city)
        if weather == None or weather['cityname'] == '平安':
            continue
        "When the database has no data, you should insert the data into table first!"
        #insert_data(weather)
        "When the database has data, you don't need to insert the data into table,just use the save_data function!"
        save_data(weather,db,city)
    db.close()
    #print("save finished!")
    time.sleep(INTERVAL)
