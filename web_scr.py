# Import libraries
from urllib.request import urljoin
from bs4 import BeautifulSoup, SoupStrainer
import requests
from urllib.request import urlparse

#NOTE: USE SOUPSTRAINER WITH BS4. IMPORVES SPEED.
#req_length = input(enter required length: ) // optional
#input_url = input(enter source url: )
#depth = int(input(enter depth of bfs: ))

# Set for storing urls with same domain
links_intern = set()
input_url = "https://www.geeksforgeeks.org/machine-learning/"
depth = int(input("enter depth of bfs: "))
keywords = input("enter keywords: ").split(',')
req_length = input("enter required length: ")

# Set for storing urls with different domain
links_extern = set()

content = ""


# Method for crawling a url at next level
def level_url_crawler(input_url):
    temp_urls = set()
    current_url_domain = urlparse(input_url).netloc

    # Creates beautiful soup object to extract html tags # used lxml before
    only_a = SoupStrainer("a")
    beautiful_soup_object = BeautifulSoup(requests.get(input_url).text, "lxml", parse_only=only_a) 

    # Access all anchor tags from input
    # url page and divide them into internal
    # and external categories

    for anchor in beautiful_soup_object.findAll('a'):
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
                    
                    links_intern.add(href)
                    temp_urls.add(href)
    return temp_urls

def content_collect(link):
    temp = ""
    only_p = SoupStrainer("p")
    bs = BeautifulSoup(requests.get(link).text, "lxml",parse_only=only_p)
    count = 0

    for para in bs.findAll('p'):
        text = para.getText()
        temp = temp + text
        count += 1
        if(count==2):
            break

    return temp 

def gen_prompt(keywords,req_length):
    prompt = '''Please summarize below text. Remove repetitive and irrelevant data.
    make sure length is around {req_length}. Use {keywords} as reference. text begins now:'''
    print(prompt)
    return

if(depth == 0):
	print("Intern - {}".format(input_url))

elif(depth == 1):
    level_url_crawler(input_url)


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
			urls = level_url_crawler(url)
			for i in urls:
				queue.append(i)


for link in list(links_intern):

    count = 0
    for word in keywords:
        if word in link:
            count+=1
            content += content_collect(link) + '\n'
            break
    if(count==3):
        break

gen_prompt(keywords, req_length)
print(content)
