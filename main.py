import network
from microWebSrv import MicroWebSrv
import time
import ntptime
import network
import max7219
import urequests
import gc,ure,ujson
from machine import Pin,SPI,RTC
import _thread


ap= network.WLAN(network.AP_IF)
ap.active(True)
with open("config.json",'r') as f:
    conf=ujson.loads(f.read())
ap.config(essid="mc", authmode=network.AUTH_WPA_WPA2_PSK, password=conf['clock'])

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
try:
    ap_list=sta_if.scan()
except Exception as e:
    ap_list=[]     
se="<select name='wifi' class='form-control'>"
for i in ap_list:
    se=se+"<option value ='%s'>%s</option>" % (bytes.decode(i[0]),bytes.decode(i[0]),)
se=se+"</select>"

def wjson(a,b,c,d,e):
    ac={}
    ac['name']=a
    ac['password']=b
    ac['id']=str(c)
    ac['city']=str(d)
    ac['clock']=str(e)
    qc=ujson.dumps(ac)
    with open("config.json",'w') as f:
        f.write(qc)

#-----------------------------
class clock:
    def __init__(self):
        with open("config.json","r") as f:
            cv=ujson.loads(f.read()) 
        self.id=cv['id'] 
        self.wifi=cv['name'] 
        self.password=cv["password"]
        # self.city=cv['city']
        self.ntp()
        self.dp()
        self.se=0
        self.rtc=RTC()
        self.fans()
        self.acfun=[[4, 1], [12, 1], [13, 1], [14, 1], [4, 2], [12, 2], [3, 3], [5, 3], [9, 3], [10, 3], [12, 3], [16, 3], [19, 3], [21, 3], [22, 3], [23, 3], [24, 3], [3, 4], [5, 4], [8, 4], [12, 4], [13, 4], [14, 4], [16, 4], [19, 4], [21, 4], [24, 4], [3, 5], [4, 5], [5, 5], [8, 5], [12, 5], [16, 5], [19, 5], [21, 5], [24, 5], [2, 6], [6, 6], [8, 6], [12, 6], [16, 6], [19, 6], [21, 6], [24, 6], [2, 7], [6, 7], [9, 7], [10, 7], [12, 7], [16, 7], [17, 7], [18, 7], [19, 7], [21, 7], [24, 7]]
    def net(self):
        if not sta_if.isconnected(): 
            sta_if.connect(self.wifi,self.password) 
    def dp(self):
        spi = SPI(baudrate=100000, polarity=1, phase=0, mosi=Pin(27),sck=Pin(25), miso=Pin(33))
        self.display = max7219.Matrix8x8(spi,Pin(26),4)
    def ntp(self):
        self.net()
        time.sleep(5)
        ntptime.host="ntp1.aliyun.com"
        ntptime.NTP_DELTA = 3155644800
        try:
            ntptime.settime()
        except Exception as e:
            pass
    def show_time(self):
        date=self.rtc.datetime()
        self.m=date[5]
        self.h=date[4]
        self.display.fill(0)
        self.display.text(str(self.h) if len(str(self.h))==2 else ' '+str(self.h) ,0,1,1)
        self.display.pixel(16,2,self.se)        
        self.display.pixel(16,4,self.se)        
        self.display.text(str(self.m) if len(str(self.m))==2 else '0'+str(self.m) ,17,1,1)
        self.se=0 if self.se==1 else 1
        self.display.show()
    def fans(self):
        gc.collect()    
        url="https://www.acfun.cn/rest/pc-direct/user/userInfo?userId="+str(self.id)
        headers = {'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36' }
        try:
            re=urequests.get(url,headers=headers)
            ca=re.text
            cc=ujson.loads(ca)
        except Exception as e:
            cc=[]
            cc['result']=1
        if cc['result']==0:
            self.fan=cc['profile']['followed'].replace('\u4e07','W')
        else:
            self.fan='0'
    def show_myfans(self):
        for j in range(len(self.fan)):
            self.display.fill(0)
            for i in self.acfun:
                self.display.pixel(i[0]-8*j,i[1],1)
            self.display.text(self.fan,25-8*j,1,1)
            self.display.show()
            time.sleep(0.5)





# ----------------------------------------------------------------------------

@MicroWebSrv.route('/s')
def _httpHandlerTestGet(httpClient, httpResponse) :
    content="1233333"
    httpResponse.WriteResponseOk( headers= None,contentType	 = "text/html",contentCharset = "UTF-8",content = content )

@MicroWebSrv.route('/')
def _httpHandlerTestGet(httpClient, httpResponse) :
	content = """\
	<!DOCTYPE html>
	<html lang=en>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="/b.css">
        	<meta charset="UTF-8" />
            <title>ACFUN Clock设置</title>
        </head>
        <body class="container">
            <h1>ACFUN Clock</h1>

            <br />
			<form action="/" method="post" accept-charset="ISO-8859-1">
				时钟密码: <input type="text" name="set_password" class="form-control" value="12345678"><br />
				WIFI名称: %s <br />
                wifi名称不显示请点击<a href="/start.html" class="btn btn-sm btn-primary">手动填写</a><br>
                wifi密码: <input type="password" name="password" class="form-control"><br />
				ACFUN ID: <input type="number" name="id" class="form-control" value="0"><br />
				<!-- 城市 ID: <input type="text" name="city_id" value="0" class="form-control"><br />-->
				<input type="submit" value="提交修改" class="btn btn-info">
			</form>
        </body>
    </html>
	""" % (se,)
	httpResponse.WriteResponseOk( headers= None,contentType	 = "text/html",contentCharset = "UTF-8",content = content )


@MicroWebSrv.route('/', 'POST')
def _httpHandlerTestPost(httpClient, httpResponse) :
    formData  = httpClient.ReadRequestPostedFormData()
    wifi = formData["wifi"]
    password  = formData["password"]
    set_password  = formData["set_password"]
    xid  = formData["id"]
    cid="0"
    # cid  = formData["city_id"]
    wjson(wifi,password,xid,cid,set_password)
    content = """\
	<!DOCTYPE html>
	<html lang=en>
        <head>
            <link rel="stylesheet" href="/b.css">
        	<meta charset="UTF-8" />
            <title>ACFUN Clock设置</title>
        </head>
        <body class="container">
            <div class="jumbotron">
            <h1>ACFUN Clock</h1>
            <p>已经完成配置，请重新断开电源。</p>
            </div>
        </body>
        </html>
    """
    httpResponse.WriteResponseOk(headers=None,contentType="text/html",contentCharset="UTF-8",content=content)

def odx(a,b):
    Clock=clock()
    oldM=0
    while 1:
        Clock.show_time()
        time.sleep(1)
        Clock.show_myfans()
        if Clock.m!=oldM and Clock.m%5!=0:
            Clock.ntp()
            oldM=Clock.m
            Clock.fans()

_thread.start_new_thread(odx,(3,4))

srv=MicroWebSrv(webPath=".")
srv.Start()
