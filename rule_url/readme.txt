1.需要python环境2.7/3.6
2.使用方式:python 脚本名 url [可选参数s：数字] [可选参数c：True/False]
3.可选参数s的作用：指定从第几个'/'（不计算'://'中的'/'）之前的字符串作为前缀，之后的正则化  默认为1
	如：https://blog.csdn.net/dQCFKyQDXYm3F8rB0/article/details/123123
	python rule_url_py2 "https://blog.csdn.net/dQCFKyQDXYm3F8rB0/article/details/123123" 
	python rule_url_py2 "https://blog.csdn.net/dQCFKyQDXYm3F8rB0/article/details/123123" -s 2
	可选参数-s的值为1和2，执行结果分别为：
	1：https://blog\.csdn\.net/([^/]+/){3}[0-9]+
	2：https://blog\.csdn\.net/dQCFKyQDXYm3F8rB0/([^/]+/){2}[0-9]+
4.可选参数c的作用：用来判定是否清除参数，默认值为false，
	如：http://sports.sina.com.cn/zl/football/ihht3.shtml?cre=zhuanlanpc&mod=g
	python rule_url_py2 "http://sports.sina.com.cn/zl/football/ihht3.shtml?cre=zhuanlanpc&mod=g" 
	python rule_url_py2 "http://sports.sina.com.cn/zl/football/ihht3.shtml?cre=zhuanlanpc&mod=g" -c True
	可选参数c为False和True的结果分别为：
	False: http://sports\.sina\.com\.cn/([^/]+/){2}[a-zA-Z0-9]+\.[a-zA-Z]+\?cre=[^&]*&mod;=[^&]*
	True: http://sports\.sina\.com\.cn/([^/]+/){2}[a-zA-Z0-9]+\.[a-zA-Z]+\
