1.��Ҫpython����2.7/3.6
2.ʹ�÷�ʽ:python �ű��� url [��ѡ����s������] [��ѡ����c��True/False]
3.��ѡ����s�����ã�ָ���ӵڼ���'/'��������'://'�е�'/'��֮ǰ���ַ�����Ϊǰ׺��֮�������  Ĭ��Ϊ1
	�磺https://blog.csdn.net/dQCFKyQDXYm3F8rB0/article/details/123123
	python rule_url_py2 "https://blog.csdn.net/dQCFKyQDXYm3F8rB0/article/details/123123" 
	python rule_url_py2 "https://blog.csdn.net/dQCFKyQDXYm3F8rB0/article/details/123123" -s 2
	��ѡ����-s��ֵΪ1��2��ִ�н���ֱ�Ϊ��
	1��https://blog\.csdn\.net/([^/]+/){3}[0-9]+
	2��https://blog\.csdn\.net/dQCFKyQDXYm3F8rB0/([^/]+/){2}[0-9]+
4.��ѡ����c�����ã������ж��Ƿ����������Ĭ��ֵΪfalse��
	�磺http://sports.sina.com.cn/zl/football/ihht3.shtml?cre=zhuanlanpc&mod=g
	python rule_url_py2 "http://sports.sina.com.cn/zl/football/ihht3.shtml?cre=zhuanlanpc&mod=g" 
	python rule_url_py2 "http://sports.sina.com.cn/zl/football/ihht3.shtml?cre=zhuanlanpc&mod=g" -c True
	��ѡ����cΪFalse��True�Ľ���ֱ�Ϊ��
	False: http://sports\.sina\.com\.cn/([^/]+/){2}[a-zA-Z0-9]+\.[a-zA-Z]+\?cre=[^&]*&mod;=[^&]*
	True: http://sports\.sina\.com\.cn/([^/]+/){2}[a-zA-Z0-9]+\.[a-zA-Z]+\
