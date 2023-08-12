# Import libraries
from urllib.request import urljoin
from bs4 import BeautifulSoup
import requests
from urllib.request import urlparse


# Set for storing urls with same domain
links_intern = set()
input_url = "https://www.geeksforgeeks.org/machine-learning/"
depth = 1

# Set for storing urls with different domain
links_extern = set()

content = ""


# Method for crawling a url at next level
def level_crawler(input_url):
    temp_urls = set()
    current_url_domain = urlparse(input_url).netloc

    # Creates beautiful soup object to extract html tags # used lxml before
    beautiful_soup_object = BeautifulSoup(requests.get(input_url).content, "html.parser") 


    # Access all anchor tags from input
    # url page and divide them into internal
    # and external categories

    for anchor in beautiful_soup_object.findAll('a'):
        #print(beautiful_soup_object.findAll('a'))
        href = anchor.attrs.get("href")
        if(href != "" or href != None):
            href = urljoin(input_url, href)
            href_parsed = urlparse(href)
            href = href_parsed.scheme
            href += "://"
            href += href_parsed.netloc
            href += href_parsed.path
            final_parsed_href = urlparse(href)
            is_valid = bool(final_parsed_href.scheme) and bool(
                final_parsed_href.netloc)
            if is_valid:
                
                if current_url_domain not in href and href not in links_extern:
                    print("Extern - {}".format(href))
                    links_extern.add(href)
                if current_url_domain in href and href not in links_intern:
                    print("Intern - {}".format(href))
                    global content 
                    content = content + content_collect(href) + '\n'
                    links_intern.add(href)
                    temp_urls.add(href)
    return temp_urls

def content_collect(link):
    temp = ""
    bs = BeautifulSoup(requests.get(link).content, "html.parser")

    for para in bs.findAll('p'):
        text = para.getText()
        temp = temp + text

    return temp 

if(depth == 0):
	print("Intern - {}".format(input_url))

elif(depth == 1):
    level_crawler(input_url)
    print()
    print(content)

else:
	# We have used a BFS approach
	# considering the structure as
	# a tree. It uses a queue based
	# approach to traverse
	# links upto a particular depth.
	queue = []
	queue.append(input_url)
	for j in range(depth):
		for count in range(len(queue)):
			url = queue.pop(0)
			urls = level_crawler(url)
			for i in urls:
				queue.append(i)
