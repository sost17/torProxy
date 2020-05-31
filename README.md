# 前言
互联网技术的不断发展，网页数据抓取越来越不简单，往往都会遇到ip地址被封的情况，一般情况都会使用IP代理池进行伪装ip地址，但如今那些免费的IP代理池早已被各大厂商的网站运维拉黑。
但是那些数据很想要，又不想花钱，没事，Tor代理为我们完成这一事。关于Tor代理实现原理，网上自行搜索！！
本文纯属个人经验分享，随便转载，不喜勿喷，谢谢。

由于Mac、Linux使用Tor代理特别简单，使用软件安装器一装即可，因此本文使用的Windows 10 环境。
## 0001-Tor下载
Tor软件可以去官网下载Tor-browser，也可以下载Console界面的软件，只需配置下配置文件即可。
Console界面的可以下载源码自行DIY，编译，安装即可。也可以下载Windows Expert Bundle，里面版本是Tor 0.4.2.7
[下载地址]([https://www.torproject.org/download/tor/](https://www.torproject.org/download/tor/)
)
![](https://upload-images.jianshu.io/upload_images/3429964-4f008a46a862daee.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## 0010-Tor 配置
想要连接到Tor服务，需要走个前置代理或者网桥，如果自己有一个science Network 的代理，直接在配置文件中添加。
如果走网桥的话，需要自己发邮件获取，地址为： [bridges@torproject.org](mailto:bridges@torproject.org)![](https://upload-images.jianshu.io/upload_images/3429964-18cda4311353e4ec.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

#### 使用Tor  0.4.2.7，需要在自己电脑用户文件夹中创建配置文件，具体路径为：{$用户文件}\AppData\Roaming\tor\torrc
![](https://upload-images.jianshu.io/upload_images/3429964-ddfa2735dc30920d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

```

CookieAuthentication 1
#Tor 程序控制端口，通过控制可变更ip
ControlPort 9051 

#data 目录,解压文件目录
DataDirectory {your directory}\tor\Data\Tor
GeoIPFile {your directory}\tor\Data\Tor\geoip
GeoIPv6File {your directory}\tor\Data\Tor\geoip6

#HTTP前置代理，使用http和socks都行
HTTPSProxy 127.0.0.1:8888 

#网桥 可发送邮件获取，使用网桥，将其取消注释即可
#Bridge obfs4 86.12.244.17:80 9E39713B73FE0F21E71DEA359A9810004E182D6E cert=U5pg5uiUBUD4d5LWp+6I++WHf1jtEfg6/lJHOzy3crrnQHRhU0AAxqJMq2buJ9Lj623FVQ iat-mode=0
#Bridge obfs4 5.196.74.8:7778 712D2EEDEB02A07639D44C1B00C0013FBA0F2176 cert=nH47UcTTIpZfRLoYpToOJZe1dPaxHuvdlegB7ujbia+xHxiuIxiummTj6gt1O7auR1s7eA iat-mode=0
#Bridge obfs4 89.72.10.147:54554 88B74AC941A8E5084D7A777B5F7666C65EA568F2 cert=RPQyxGIRnUasPwlx3QkqAbOQny8XApwZWaG8Ci6KjOpOONvbHt/WXjiOBKMGtXQ8e6weHA iat-mode=0
#UseBridges 1
```

## 0011-Tor运行
配置完后，运行tor.exe即可，会提示连接情况，从0%一直到100%，100%即连接Tor服务成功。Tor会监听9050端口，通过该端口进行代理。

![](https://upload-images.jianshu.io/upload_images/3429964-c026f5ab1350fa5e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## 0100-Tor+Python
Tor运行成功后，可使用Socks和Http为python程序代理
### SOCKS
```
# coding=utf-8

import socket
import socks
import requests

socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
socket.socket = socks.socksocket

print(requests.get('https://api.ipify.org/?format=json').text)
```

### HTTP
因为有的网站socks代理不能进行访问，因此将socks转换成http
```
import requests
proxies = {
                'http': 'socks5://127.0.0.1:9050',
                'https': 'socks5://127.0.0.1:9050'
            }
print(requests.get('https://api.ipify.org/?format=json', proxies=proxies).text)
```
### Tor控制
通过9051端口可进行Tor控制变更ip
```
from stem import Signal
from stem.control import Controller

with Controller.from_port(port = 9051) as controller:
    controller.authenticate()
    controller.signal(Signal.NEWNYM)
```

## end
使用Tor代理python爬虫的原理到此ending，至于爬虫抓取代码自行研究了O(∩_∩)O哈哈~

如果有其他好的方法，欢迎给我留言。。。
