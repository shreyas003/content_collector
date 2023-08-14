# Import libraries
from urllib.request import urljoin
from bs4 import BeautifulSoup, SoupStrainer
import requests
from urllib.request import urlparse

#NOTE: USE SOUPSTRAINER WITH BS4. IMPORVES SPEED.
#req_length = input(enter required length: ) // optional
#input_url = input(enter source url: )
#depth = int(input(enter depth of bfs: ))


#change collect content functions as para(link, keys):
#if any(keys) in link: then exec

# Set for storing urls with same domain
links_intern = set()
input_url = "https://www.geeksforgeeks.org/machine-learning/"
depth = int(input("enter depth of bfs: "))
keywords = input("enter keywords: ").split(',')

# Set for storing urls with different domain
links_extern = set()

content = ""


# Method for crawling a url at next level
def level_crawler(input_url):
    temp_urls = set()
    current_url_domain = urlparse(input_url).netloc

    # Creates beautiful soup object to extract html tags # used lxml before
#<<<<<<< test
    only_a = SoupStrainer("a")
    beautiful_soup_object = BeautifulSoup(requests.get(input_url).text, "lxml", parse_only=only_a) 
#=======
    #beautiful_soup_object = BeautifulSoup(requests.get(input_url).text, "html.parser") 
#>>>>>>> main


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
#<<<<<<< test
    only_p = SoupStrainer("p")
    bs = BeautifulSoup(requests.get(link).text, "lxml",parse_only=only_p)
#=======
    #bs = BeautifulSoup(requests.get(link).text, "html.parser")
#>>>>>>> main
    count = 0

    for para in bs.findAll('p'):
        text = para.getText()
        temp = temp + text
        count += 1
        if(count==2):
            break

    return temp 

if(depth == 0):
	print("Intern - {}".format(input_url))

elif(depth == 1):
    level_crawler(input_url)


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


for link in list(links_intern):

    count = 0
    for word in keywords:
        if word in link:
            count+=1
            content += content_collect(link) + '\n'
            break
    if(count==3):
        break


print(content)

#if i havent please remind me to use soupStrainer along beautifulSoup to improve parsing speed


'''
chatgpt prompt template.

below data is related to {{topics}}. please go through the follwing data and summarize
it. remove repetetive and unrelevant content. make sure the length is around {{req_length}}.
make the summary concise, to the point and as simple as possible. take your time.

{{content}}
'''
