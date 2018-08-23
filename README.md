# Fly job

### what to do

#### 为寻找工作机会的同胞,提供数据支持

------

#### what look like 

```
#目前项目结构
	spider \         # 爬虫部分
		__init__.py 
		config.py          # 爬虫配置
		spider_util.py     # 爬虫类
		dataapi.py 		   # 存储类
	data_show \      # 数据清洗展示部分
		__init__.py
		data.py 	   # 从数据库中取出数据
		show.py        # 生成视图api
	FlyJob \         # web平台
		main \         # 主模块
			views.py       # 主逻辑模块
 			__init__.py    # 蓝图初始化
 		templates \   # HTML模板目录
 			index.html     # 首页
 			result.html	   # 视图生成页面		
 		static\ 
 			js \
 				echarts.js      # echarts js库
 				china.js	    # 地图js库
 				worldcloud.js   # 词云js库
 				..
 				..
 			css \
 				..
 		startapi.py        # 对外接口(集合爬虫与存储)
		manage.py     # 服务器启动文件
		__init__.py   # 服务器初始化
		keyword.json  # 数据存储文件
```

------

#### what we used 

###### requests      # 爬虫 

###### Flask             # web平台

###### MongoDB    # 数据库

###### python3.5   # python 版本

###### pyecharts   # echarts库

###### jieba             # 中文分词库

###### redis            # 缓存(效果并不比直接存在文件里好)



