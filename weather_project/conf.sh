#!/bin/bash
# create database and table in mysql!
mysql -uroot -p
create database weather character set utf8;
USE weather;
create table t_weather (cityNumver INT(25),cityName VARCHAR(255),
cityNameen VARCHAR(255),cityWeather VARCHAR(255),
temp VARCHAR(255),sd VARCHAR(255),njd VARCHAR(255),
wd VARCHAR(255),ws VARCHAR(255),pm25 VARCHAR(255),
limitnumber VARCHAR(255)) default charset = utf8;

# ctrl + z, quit the mysql
echo -e '\032' 

# move the cofiguration file to the destination
pwd_file=`pwd`

cp -r "$pwd_file/weather_project/user_conf" "/etc/nginx"

# install the dependencies in Anaconda env
conda env create -f "$pwd_file/weather_project/environment.yaml"

source activate web

cd "${pwd_file}/weather_project/flask"

# start the flask with gunicorn configuration in "gunicorn_conf.py"
gunicorn -c gunicorn_conf.py server:app

sudo service nginx restart
######################

# start python spider
nohup python request_example.py &
