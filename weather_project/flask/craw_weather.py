

from urllib3 import *
import re
import requests
import json
import pymysql
import time
# Get the headers information
def str2headers(file):
    header_dict = {}
    f = open(file,'r')
    text = f.read()
    contents = re.split('\n',text)
    for line in contents:
        result =re.split(':', line,maxsplit=1)
        header_dict[result[0]] = result[1]
    f.close()
    return header_dict

# Get the whole cities information
def getCityList(file):
    cityList = []
    f = open(file,encoding='utf-8')
    contents = f.read()
    contents = re.split('\n', contents)
    for str in contents:
        cityCode = re.split('=',str)
        cityList.append(cityCode[0])
    # print(len(cityList)) # 2654 cities
    return cityList

# Get the city weather by city code
def get_city_weather(city_code):
    http = PoolManager()
    url = 'http://d1.weather.com.cn/sk_2d/'+city_code+'.html?_=1583040735053'
    r = http.request('get', url, headers=headers)
    # str2city_code("北京")
    str = r.data.decode('utf-8')
    n = len("var dataSK = ")
    str = str[n:]
    weatherDict = json.loads(str)
    return weatherDict

# insert the data into mysql
def insert_data(weather):
    print("weather is",weather)
    db = pymysql.connect("localhost","root","123456","weather",charset="utf8")
    # INSERT INTO Persons VALUES ('Gates', 'Bill', 'Xuanwumen 10', 'Beijing')
    cursor = db.cursor()
    sql = "select cityName from t_weather"
    result = cursor.execute(sql) # type result is <class 'int'>
    if result == 0:
        sql = "insert into t_weather values "
        try:
            sql += "('" + weather['city'] + "','" + weather['cityname'] + "','" \
            + weather['nameen'] +"','"+ weather['weather'] + "','"+weather['temp']+"','" \
            + weather['sd']+"','" + weather['njd']+"','" + weather['WD']+"','" \
            + weather['aqi_pm25']+"','" + weather['limitnumber'] + "');"
            #print("var is",var)
            #print("values is",weather[var])
            # += ("'" + weather[var] +"'),"
        except Exception as e:
            print(e)
        print("sql is ",sql)
        #sql.rstrip(',')+";"
        cursor.execute(sql)
        sql = ""
    db.close()

# input the city weather Dict and save it into the Mysql
def save_data(weather):
    db = pymysql.connect("localhost", "root", "123456", "weather", charset="utf8")
    print("db is", db)
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
    wdata['pm25'] = weather['api_pm25']
    wdata['limitnumber'] = weather['limitnumber']
    cursor = db.cursor()
    sql = "update t_weather set"
    for var in weather:
        #sql += "('" + weather[var] + "'),"
        sql += (var + "='" + weather[var] +"',")
    sql.rstrip(',') + "where cityNumber = '" + citycode + "'"
    cursor.execute(sql)
    db.close()

# citycode
# http://toy1.weather.com.cn/search?cityname=%E4%B8%8A%E6%B5%B7&callback=success_jsonpCallback&_=1583032681612

# http://d1.weather.com.cn/sk_2d/101210401.html?_=1583040735053
http = PoolManager()
headers = str2headers('head.txt')
url = 'http://d1.weather.com.cn/sk_2d/101210401.html?_=1583040735053'
r = requests.get(url,allow_redirects=False) # 直接用requests时候，这里不需要headers
#str2city_code("北京")
city_code = getCityList('city_list.txt')
#print(get_city_weather('101210401'))
for city in city_code:
    weather = get_city_weather(city)
    insert_data(weather)
    #save_data(weather)
    time.sleep(1)
"""
# 将数据导入到mysql中
import pymysql
db = pymysql.connect('localhost','root','123456','weather',charset='utf-8')
cursor = db.cursor()
def saveWeatherInofe(cityCode):
    

db.close()
"""

"""
patt = '"temp":"(\d+)"'
group = re.search(patt,weather)
print("group is",group[1])
#weather_json = json.loads(weather)
"""
