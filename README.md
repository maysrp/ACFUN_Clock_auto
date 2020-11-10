# ACFUN_Clock_auto
ACFUN电子钟自动配网版

# Acfun_clock
ESP32 Micropython ESP32 Clock acfun fans clock


你的ESP32首先要刷好了Micropython固件


按照下图连线：  

|esp32 |    max7219  |
|----|----|
|5v（或者3v3）| vcc|  
|GND   |GND|  
|G27   |DIN|  
|G26  |CS|  
|G25| CLK|  



上传main.py和config.json到你的ESP32上
max7219.py这个库文件也上传到你的esp32上


手机搜索热点mc，默认密码12345678，连接后 用浏览器打开 http://192.18.4.1/ 按照上面网页填写，完成提交后重新断开电源即可
你的acfun的时钟就完成了

