# coding:utf8
import  urllib.request
import  http.cookiejar
import  bs4



url = "http://www.baidu.com"

print("第一种方法")
response1 = urllib.request.urlopen(url)
print(response1.getcode())
print(len(response1.read()))

print("the second method")
request1 =  urllib.request.Request(url)
request1.add_header("user-agent","Mozilla/5.0")
response2 = urllib.request.urlopen(request1)
print(response2.getcode())
print(len(response2.read()))

print(" The third method")
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
urllib.request.install_opener(opener)
response3 = urllib.request.urlopen(request1)
print(response3.getcode())
print(cj)
print(response3.read().decode('utf-8'))