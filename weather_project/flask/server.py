from flask import *
import json
import pymysql
# web后端flask程序
app = Flask(__name__)
# 定义一个打开数据库，执行sql语句并返回结果的函数
def mySqlConnect(sql):
    # 打开名为weather的数据库，记得编码要是utf-8
    db = pymysql.connect('175.24.55.162','root','123456','weather',charset='utf8')
    cursor = db.cursor()
    cursor.execute(sql)
    data = cursor.fetchone()
    data = json.dumps(data) #string -> json
    db.close()
    return data

@app.route('/weather')
def index():
    cityName = request.values.get('city')
    sql = "select * from t_weather where cityName like '%" + cityName + "%' or cityNameen like '%"+ cityName + "%'"
    info = mySqlConnect(sql)
    return info



if __name__ == '__main__':
    from werkzeug.contrib.fixers import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app)
    #app.run()
