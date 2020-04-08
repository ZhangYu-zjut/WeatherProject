# A Weather Query Project

# Requirements
- Aginx 1.14.0
- python 3.6
  - all python dependencies are in "environment.yaml"
- mysql Ver 14.14
- Anaconda 1.6.14
- A domain address
- A SSL certificate

Attention: Please install these dependences at first, and we assume that you have already installed these dependences.

## Qulick start the configuration
"""
1.go to the configuration of nginx and add one line code in "nginx.conf"
  cd /etc/nginx
  sudo vim nginx.conf
under the code "include /etc/nginx/sites-enabled/*;", please add the following code line
  include /etc/nginx/user_conf/*.conf;

2.run "conf.sh" to configure some environment configurations, including Aginx,gunicorn and license.

NOTE: As I have got the 'domain address' and 'SSL certificate',so the setup are adjustable to my address and SSL.
If you want to switch to your 'domain address' and 'SSL certificate',you need to:
- change the "1_serverzy.top_bundle.crt" and "2_serverzy.top,key" to your own SSL certificate.
- modify the configuration file "flask_ssl.conf" to your own certificate.
- change the url request address to your own address in the miniprogram code file "index.js".
- change the https request responce to your own in the code file "server.py".
- other modifications that you need without my mention.

"""


## The steps that enjoy this application.
"""
1.Touch the "search" button in Wechat.
2.Input "小天和小气遇到了鱼宝"(Chinese) and search the miniprogram.
3.Get into the miniprogram.
4.Input the city name and search the weather as the UI shows,enjoy your time, (:
"""
