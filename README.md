# kmail v0.1
 基于python（imaplib,click）开发的console app 实现的对Bestbuy,Target order 邮件的管理
 ！！！目前仅支持Bestbuy和Target的订单邮件的tracking number,order number等等的信息管理
 
 ！！！目前仅支持gmail邮箱登录
## 操作说明

 ### 下载
 
 1. 可以直接下载下来所有的.py文件 然后在cmd运行main.py
 2. 可以下载kmail.exe文件执行安装程序
 
 ### 使用
 
 1. 如果是使用方法1下载 则在当前目录下的cmd输入python main.py开始使用
 2. 如果是使用方法2下载 则在当然目录下的cmd输入cmdadpp.exe则可以直接运行
 3. 程序目前提供2个方法 login start
 4. login 提供的参数为 -e 邮箱 -p 密令 -g 邮件分组 
 5. start 提供的参数为 -o 可选参数 例如 date,order number,tracking等 -t 选择对BestBuy或者Target爬取 -n 生成文件的名字（生成的是excel文件） -S 开始时间 -E 结束时间 （-e -p -g同上）
 6. 建议先使用login后使用start 因为login会保存登录信息 以免使用start方法时多次输入邮箱密码
 
 ### 问题/bug反馈
 欢迎联系GUW18@pitt.edu
