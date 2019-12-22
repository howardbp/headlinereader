import requests
from lxml import html

class headlinereader():

	def clean_url(self,urlin):
		base = urlin.split('?')[0]
		if 'http' in base:
			url = base
		else:
			url = 'http://' + base
		return url
	def source(self,urlin):
		parsed_url = self.clean_url(urlin)

		remove_strings = ['www.','http://:','https://']

		for i in remove_strings:
			parsed_url = parsed_url.replace(i,'')
		domain = parsed_url.split('.')[1].split('/')[0]
		return parsed_url.split('.')[0] + '.' + domain

	def makepage(self,response):
		page = html.fromstring(response.text)
		return page

	def testxpath(self,xpath):
		if len(xpath) == 1:
			return xpath[0].text.strip()
		else:
			return 'No Headline Found'

	def request_and_parse_page(self,urlin,headers=None,cookies=None):
		r = requests.get(urlin,headers=headers,cookies=cookies)
		page = self.makepage(r)
		return page

	def bloomberg(self,urlin):
		headers = {'Content-Length': '4595','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36', 'Via': '1.1 varnish', 'X-Cache': 'MISS', 'Content-Encoding': 'gzip', 'Accept-Ranges': 'bytes, bytes', 'X-Timer': 'S1574721448.725254,VS0,VE11', 'Vary': 'Accept-Encoding', 'X-Served-By': 'cache-ewr18139-EWR', 'Server': 'nginx', 'Last-Modified': 'Mon, 25 Nov 2019 16:01:35 GMT', 'Connection': 'keep-alive', 'ETag': 'W/"5ddbfadf-2abc"', 'X-Cache-Hits': '0', 'Cache-Control': 'public, max-age=5, private, no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0', 'Date': 'Mon, 25 Nov 2019 22:37:27 GMT', 'Content-Type': 'text/html, text/html; charset=utf-8', 'Age': '0, 0'}
		cookies = {'_px2': 'eyJ1IjoiZmE4OGI4NDAtMjRlYi0xMWVhLWEwMGUtNTMzZWY0MTBhOGU2IiwidiI6ImM3YzNkNmMwLWZlNzUtMTFlOS05NDA3LTZmYWUxOWQzMDdjYiIsInQiOjE1NzcwNDA5NTQyMDcsImgiOiI5YjUxM2Q0NmVlZWU3OGYxNGQ0YzIwZWZiNjEzOWJhZGM5NmViMjYwNTRlZTVlNWQ0OGRkOWVhZGQ0NzcxNTJmIn0='}
		page = self.request_and_parse_page(urlin,headers,cookies)
		h = page.xpath("//h1[@class='lede-text-v2__hed']")
		return self.testxpath(h)

	def wsj(self,urlin):
		page = self.request_and_parse_page(urlin)
		h = page.xpath("//h1[@class='wsj-article-headline']")
		return self.testxpath(h)

	def ft(self,urlin):
		page = self.request_and_parse_page(urlin)
		h = [page.xpath("//h1/span")[1]]
		return self.testxpath(h)

	def buzfeed(self,urlin):
		page = self.request_and_parse_page(urlin)
		h = page.xpath("//h1[@class='news-article-header__title']")
		return self.testxpath(h)

	def thecut(self,urlin):
		page = self.request_and_parse_page(urlin)
		h = page.xpath("//h1[@class='headline-primary']")
		return self.testxpath(h)

	def gq(self,urlin):
		page = self.request_and_parse_page(urlin)
		h = page.xpath("//h1[@class='content-header__row content-header__hed']")
		return self.testxpath(h)

	funclookup = {
		'bloomberg.com':bloomberg,
		'wsj.com':wsj,
		'ft.com':ft,
		'buzzfeednews.com':buzfeed,
		'thecut.com':thecut,
		'gq.com':gq
	}

	def getheadline(self,urlin):
		source = self.source(urlin)
		headline = self.funclookup[source](self,urlin)
		return source,headline
