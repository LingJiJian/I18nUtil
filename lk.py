#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import os
import re
import json
import sys

class Singleton(type):
	"""docstring for Singleton"""
	def __init__(self, name,bases,dic):
		super(Singleton, self).__init__(name,bases,dic)
		self.instance = None

	def __call__(self,*args,**kwargs):
		if self.instance is None:
			self.instance = super(Singleton,self).__call__(*args,**kwargs)
		return self.instance

class FileManager:
	""" 文件管理器 """

	__metaclass__ = Singleton

	def __init__(self):
		super(FileManager, self).__init__()
		self.__scanFilePaths = {} #文件内容
		self.__tranWordArrs = {}  #匹配到的 字符串
		self.__tranWordDic = {} #匹配到的 字符串

	def setInDir(self,path):
		self.__inDir = path

	def setOutDir(self,path):
		self.__outDir = path

	def setLogCallFuc(self,func):
		self.__logCallFunc = func

	def run(self):
		self.__preload()
		self.__scanInDir(self.__inDir)
		self.__progressFiles()
		self.__exportFile()

	#预加载 配置
	def __preload(self):
		path = sys.path[0]
		if os.path.isfile(path):
			path = os.path.dirname(path)
		pFile = open(os.path.join(path,"config.json"),"r")
		self.__config = json.loads(pFile.read())

	#扫描目录
	def __scanInDir(self,path):
		arr = os.listdir(path)
		for line in arr:
			if self.__isIgnoreScan(line):
				pass
			else:
				filepath = os.path.join(path,line)
				if os.path.isdir(filepath):
					self.__scanInDir(filepath)
				else:
					if os.path.splitext(filepath)[1] in self.__config["scan_suffix"]:
						pFile = open(filepath,"r")
						try:
							self.__scanFilePaths[filepath] = pFile.read()
							self.__tranWordArrs[filepath] = []
						finally:
							pFile.close()
		
	def __progressFiles(self):
		idx = 0
		for path,content in self.__scanFilePaths.items():
			idx += 1
			tmpStr = ""
			markFlag = False
			for i,ch in enumerate(content):
				if ch == "\"":
					if content[i-1] == "\\":
						if markFlag:
							tmpStr += "\""
							continue;

					markFlag = not markFlag;

					if markFlag == False :
						tmpStr += "\""
						if self.has_zh(tmpStr.decode('utf-8')):
							key = "\"a"+self.__getWordIdx()+"\"";
							self.__tranWordArrs[path].append({"key":key,"val":tmpStr})					
							self.__tranWordDic[ key ] = tmpStr
						tmpStr = ""

				if markFlag :
					tmpStr += ch	
		self.__logCallFunc({"isFinish":True})

	def has_zh(self,txt):
		zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
		ret = False
		if zhPattern.search(txt):
			ret = True
		else:
			ret = False
		return ret

	#是否忽略扫描的文件
	def __isIgnoreScan(self,path):
		ret = False
		for ignore_path in self.__config["ignore_path"]:
			# print(os.path.join(self.__inDir,ignore_path), os.path.join(self.__inDir,path))
			if os.path.join(self.__inDir,ignore_path) == os.path.join(self.__inDir,path):
				ret = True
				break
		return ret

	def __getWordIdx(self):
		idx = 10000;
		while True:
			if self.__tranWordDic.has_key("\"a"+str(idx)+"\""):
				idx += 1
				continue;
			else:
				return str(idx);

	def __exportFile(self):
		content = "i18n = {} \n";
		for k,v in self.__tranWordDic.items():
			content += "i18n[" + k + "] = " + self.__tranWordDic[k] + "\n";

		pFile = open(self.__outDir,"w")
		pFile.write(content)
		pFile.close()

		for path,content in self.__scanFilePaths.items():
			if len(self.__tranWordArrs[path]) > 0 :
				for param in self.__tranWordArrs[path]:
					content = content.replace(param.get("val"),"i18n["+param.get("key")+"]")
				self.__scanFilePaths[path] = content
				pFile = open(path,"w")
				pFile.write(content)
				pFile.close()
