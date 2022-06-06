<!--
created by Irony-H
-->

#### create_ap
  github上的开源项目,用于开启树莓派的wifi.
  具体使用方法可参考:[create_ap](https://github.com/oblique/create_ap)
- - - 
+ #### Script
    脚本文件
 - AP.sh
    * 脚本文件
 - rc.local
    * 树莓派开机自启动文件
- - -
#### test
    编写代码时的测试文件,包含串口测试、socket测试
- - - 
#### WIFI.py
    最后的程序代码
- - -
#### 缺陷
 - socket发送信息缺少终止符
 - py文件没有写入到开机自启动,可自行添加.