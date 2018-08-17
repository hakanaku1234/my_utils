#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import sys
import getopt

# 脚本功能：根据输入的url生成对应的正则规则
# 启动方式：python 脚本文件名 url字符串 [可选参数1:slash_num] [可选参数2:clear_params]
# slash_num用来确定前缀长度：从第几个'/'（不包含://中的'/'）之前截取作为前缀
# clear_params用来判定是否清除参数


class UrlPattern(object):

	def __init__(self, slash_num=1, clear_params=False):
		# slash_num为斜杠的个数 用于确定取前缀时取第几个'/'之前的字符 slash_num自动向下兼容
		self.slash_num = slash_num
		# url的匹配规则
		self.url_regexp = ""
		self.clear_params = clear_params

	def get_prefix(self, url):
		# url前缀的正则规
		prefix_regexp = re.compile(r'(https?|ftp|file):/{2,3}([^/]+/){1,%d}' % self.slash_num)
		# 尝试对url进行匹配
		res = prefix_regexp.match(url)
		if not res:
			raise ValueError("Please enter a standard url")
		# 获取前缀
		prefix = res.group()
		return prefix
		
	def rule2slash(self, chars):
		"""
		使用'/'对字符串进行分割
		添加斜杠之前的正则
		"""
		endwith = ""
		split_char = ("?" in chars and "?") or ('#' in chars and "#") or ""
		if split_char:
			split_res = chars.split(split_char)
			chars = split_res[0]
			endwith = split_char + split_res[-1]
		# 使用斜杠对url去除前缀后的部分进行分割
		split_slash = chars.split("/")
		# 获取斜杠的个数
		slash_num = len(split_slash) - 1
		# 补充正则规则
		if slash_num > 0:
			if slash_num == 1:
				self.url_regexp += '[^/]+/'
			else:
				self.url_regexp += '([^/]+/){%d}' % slash_num
		# 获取最后一个'/'之后的字符串
		endwith = split_slash[-1] + endwith
		return endwith

	def rule_chars(self, chars):
		"""
		对短字符串进行正则化
		"""
		end_char = ""
		if chars[-1] in ["-", "_", ".", "?", '#']:
			end_char = chars[-1]
			chars = chars[:-1]
		if chars.isdigit():
			chars_regexp = "0-9"
		elif chars.isalpha():
			chars_regexp = "a-zA-Z"
		elif chars.isalnum():
			chars_regexp = "a-zA-Z0-9"
		else:
			chars_regexp = ""
		if chars_regexp:
			chars_regexp = '[%s]+' % chars_regexp
		chars_regexp += end_char
		return chars_regexp

	def rule2question_mark(self, str_):
		"""
		尝试对'?'之前的内容进行正则
		"""
		chars = ""
		for index, char in enumerate(str_):
			chars += char
			if char in ["-", "_", ".", "?", '#'] or index == len(str_) - 1:
				chars_regexp = self.rule_chars(chars)
				self.url_regexp += chars_regexp
				if char in '?#':
					endwith = str_[index + 1:]
					break
				if index == len(str_) - 1:
					endwith = ""
					continue
				chars = ""
		return endwith

	def rule_param(self, chars):
		"""
		对url中的参数部分进行正则化
		"""
		param_regexp = re.compile(r'([^&|]+?=)')
		res = param_regexp.findall(chars)
		for index, regex in enumerate(res):
			if index == len(res) - 1:
				self.url_regexp += "%s[^&]*" % regex
			else:
				self.url_regexp += "%s[^&]*&" % regex
	
	def rule_url(self, url):
		"""
		对url进行规则 得到url的正则表达式
		"""
		if self.clear_params:
			split_char = ("?" in url and "?") or ('#' in url and "#") or ""
			if split_char:
				url = url.split(split_char)[0]
		prefix = self.get_prefix(url)
		self.url_regexp += prefix
		# 获取url去除前缀后的字符串
		endwith = url[len(prefix):]
		# 如果后面有字符串，尝试对'/'之前的内容进行正则
		if endwith:
			endwith = self.rule2slash(endwith)
		if endwith:
			endwith = self.rule2question_mark(endwith) 
		if endwith:
			endwith = self.rule_param(endwith)
		if not endwith:
			self.url_regexp = "".join(map(lambda char:char in [".", '?'] and '\%s' % char or char, self.url_regexp))
			return self.url_regexp
		else:
			raise UserWarning("I'm sorry, I think i need an upgrade！")
	
	@classmethod
	def help(cls):
		print("启动方式: pyhon %s url [-n int] [-b bool]" % sys.argv[0])
		print("\t--help: 获取这份说明")
		print("\t--num: 指定保留第几个'/'(不包括'://'中的'/')之前的字符,默认为1")
		print("\t--bool: 指定是否清除参数, 默认为False")
		print("example:")
		url = "https://blog.csdn.net/GitChat/article/details/81703229"
		regexp = cls().rule_url(url)
		print('\tpython %s "%s"' % (sys.argv[0], url))
		print("\t输入url为：%s" % url)
		print("\t正则表达式：%s" % regexp)


if __name__ == "__main__":
	args = sys.argv
	if len(args) == 1 or args[1] == "-h" or args[1] == "--help":
		UrlPattern.help()
		exit(1)
	url = args[1]
	slash_num = 1
	clear_params = False
	try:
		opts, _ = getopt.getopt(args[2:], 'hu:n:b:', ["help", "url=", "num=", "bool="])
	except getopt.GetoptError:
		UrlPattern.help()
		sys.exit(1)
	for opt, val in opts:
		if opt == "-n" or opt == "--num":
			slash_num = val.isdigit() and int(val) or 1
		elif opt == "-b" or opt == "--bool":
			clear_params = (val == "True" or val == "False") and eval(val) or False
		elif opt == "-h" or opt == "--help":
			UrlPattern.help()
			exit(1)
		else:
			UrlPattern.help()
			exit(1)
	url_pattern = UrlPattern(slash_num=slash_num, clear_params=clear_params)
	regexp = url_pattern.rule_url(url)
	print(regexp)

"""
__title__ = ''
__author__ = 'v_sungensheng'
__mtime__ = '2018/8/8'
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""
