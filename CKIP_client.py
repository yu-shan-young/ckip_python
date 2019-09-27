﻿import socket
import xml.parsers.expat
import sys

##sys.version_info 表示當前pythin版本
if sys.version_info >= (3, 0):
	import configparser as ConfigParser
else:
	import ConfigParser


my_format = "<?xml version=\"1.0\"?><wordsegmentation version=\"0.1\" charsetcode=\"utf-8\"><option showcategory=\"1\"/>%s<text>%s</text></wordsegmentation>"

#生成config對象
config = ConfigParser.ConfigParser()

#用config對象讀取配置文件
config.read('config.ini')

##Config.get():取得文本
？？？？？？這在做哈？？？？？
authentication_string = "<authentication username=\"%s\" password=\"%s\"/>" % (config.get("Authentication","Username"), config.get("Authentication","Password"))
connect_target = config.get("Server","IP"), int(config.get("Server","Port"))

class parse_xml:
	def __init__(self,input_xml_str):
		self.status_code, self.status_str, self.result = None, '', ''
		self.core = xml.parsers.expat.ParserCreate('utf-8'). ###創utf-8編碼的解析器
		self.core.StartElementHandler = self.start_element
		self.core.EndElementHandler = self.end_element
		self.core.CharacterDataHandler = self.char_data
		self.pointer = None
		if type(input_xml_str) is str:
			self.core.Parse(input_xml_str.strip(),1)
		else:
			self.core.Parse(input_xml_str.encode('utf-8').strip(),1)
	def start_element(self,name,attrs):
		if name == "processstatus":
			self.status_code = int(attrs['code'])
			self.pointer = name
		elif name == "sentence":
			self.pointer = name
	def end_element(self,name):
		if name == "wordsegmentation":
			self.result = self.result.strip()
	def char_data(self,data):
		if self.pointer is None:
			return None
		if self.pointer == "processstatus":
			self.status_str = data
		elif self.pointer == "sentence":
			self.result+= data
		self.pointer = None


def ckip_client(input_text,output_file=None):
	input_text = input_text.replace('　',' ').strip()
	input_text = input_text.replace('&', '&amp;')
	input_text = input_text.replace('<', '&lt;')
	input_text = input_text.replace('>', '&gt;')
	input_text = input_text.replace('\'','&apos;')
	input_text = input_text.replace('"', '&quot;')
	text = my_format % (authentication_string, input_text)
	if sys.version_info >= (3, 0) and len(text) >= 7900:
		raise ValueError("Your input text is too long.")
	elif sys.version_info < (3, 0) and len(text.decode('utf-8')) >= 7900:
		raise ValueError("Your input text is too long.")
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect(connect_target)
	try:
		sock.sendall(text)
		downloaded = ''
		stop_word = "</wordsegmentation>"
	except:
		sock.sendall(text.encode('utf-8'))
		downloaded = b''
		stop_word = b"</wordsegmentation>"
	while stop_word not in downloaded:
		chunk = sock.recv(4096)
		downloaded +=chunk
	result = parse_xml(downloaded.decode('utf-8'))
	if result.status_code == 0:
		if output_file:
			output = open(output_file,'wb')
			output.write(result.result.encode('utf-8'))
			output.close()
		try:
			return result.result, len(text.decode('utf-8'))
		except:
			return result.result, len(text)
	else:
		class CKIPException(Exception):
			pass
		raise CKIPException("status_code: %d, %s" % (result.status_code, result.status_str))



if __name__ == "__main__":
	text = "Facebook 是一個聯繫朋友、工作夥伴、同學或其他社交圈之間的社交工具。你可以利用Facebook 與朋友保持密切聯絡，無限量地上傳相片，分享轉貼連結及影片。"
	ckip_client(text,"output.txt")
