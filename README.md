# SQLi-Boolean
MySQL 布尔盲注脚本 基于二进制方式提取数据


## 说明

- 原理是通过MySQL的bin函数来获取二进制字符，这样每次获取一个比特位，所以每一个字符最多查询8次。

- 本脚本主要自用，函数名和变量名的命名方式都不够好，目前也还不支持命令行传参，注入点、成功条件、查询命令 都需要去修改py源码。

- 目前只是一个样例，大家可以自行修改，比如可以改成时间盲注，也欢迎大家一起帮我修改完善源码


---

### 盲注测试靶场：
[墨者学院](https://www.mozhe.cn/bug/detail/UDNpU0gwcUhXTUFvQm9HRVdOTmNTdz09bW96aGUmozhe)

---

### 提示

> 尽量不要查询太长的数据内容，以免因为网络延迟导致出错

> 比如查询 (select group_concat(name,0x7e,password) from member)
> 可以分为两次查询    
> (select group_concat(name) from member)     
> (select group_concat(password) from member)    

