import bs4
import requests
import sys
from SpacyComparison import *


def main():
    #get command line arguments
    start_url = "https://en.wikipedia.org/wiki/Special:Random"
    end_url = "https://en.wikipedia.org/wiki/Special:Random"
    if len(sys.argv) > 1:
        start_url = sys.argv[1]
    if len(sys.argv) > 2:
        end_url = sys.argv[2]
    
    start_page_name = get_page_title(start_url)
    global end_page_name
    end_page_name = get_page_title(end_url) #this is messy, so maybe change it later
    print(f'Start={start_page_name} -> end={end_page_name}')

    result = []
    wiki_search(start_url, end_page_name,end_url, 7, 2, result)
    print('--------SOLUTION---------\n')
    print(f'[{format_path(result)}]')

def model_test(string1, string2):
    print(compare_strings(NLP, string1, string2))

def wiki_search1(start_url, end_page_name, end_page_url, max_depth, path):
    # print('evaluating ' + start_url + ' with max depth ' + str(max_depth) + ' and path ' + str(path))
    print(f'path length: {len(path)} depth: {max_depth}')
    if max_depth == 0:
        del path[-1]
        return False
    elif get_page_title(start_url) == end_page_name:
        path.append(end_page_name)
        return True
    if path is None:
        path = [get_page_title(start_url)]
    else: 
        path.append(get_page_title(start_url))
    #get all links from start page
    # start_page_soup = get_page_soup(start_url)
    # links = start_page_soup.select("a[href^='/wiki/']")

    #get all links from start page inside paragraphs with no class
    start_page_soup = get_page_soup(start_url)
    links = start_page_soup.select("p:not([class]) a[href^='/wiki/']")
    # print("got links")
    
    #sort links by text similarity to end page name
    links = sorted(links, key=sort_links, reverse=True)
    # print("sorted links")

    #filter out links with the same href
    links = [link for i, link in enumerate(links) if link.get("href") not in [link.get("href") for link in links[:i]]]
    # print("filtered links")


    #check if any of the links are the end page
    # for link in links[:20]:
    #     if (name := "https://en.wikipedia.org" + link.get("href")) == end_page_url:
    #         return path + [end_page_name]
    #     # print('link: ' + name)

    # print("no end page found")

    for link in links[:5]:
        # print(f'{start_url} -> {link.text}')
        if wiki_search(start_url="https://en.wikipedia.org" + link.get('href'), end_page_name=end_page_name, max_depth=max_depth - 1, end_page_url=end_page_url, path=path):
            return True
    path = path[:-1]
    return False

def wiki_search(start_url, end_page_name, end_page_url, max_depth, max_breadth, path, visited=None):
    if visited is None:
        visited = set(start_url)
    else:
        visited.add(start_url)

    page_title = get_page_title(start_url)
    path.append(page_title)
    print(format_path(path) + '\n')
    if max_depth == 0:
        # print("MAX DEPTH REACHED")
        # print(format_path(path))
        del path[-1]
        # print(format_path(path))
        return False
    elif page_title == end_page_name:
        return True
    
    #get all links from start page inside paragraphs with no class
    start_page_soup = get_page_soup(start_url)
    links = start_page_soup.select("p:not([class]) a[href^='/wiki/']")

    #sort links by text similarity to end page name
    links = sorted(links, key=sort_links, reverse=True)

    #filter out links with the same href, or that have already been visited
    links = [link for i, link in enumerate(links) if link.get("href") not in [link.get("href") for link in links[:i]] and "https://en.wikipedia.org" + link.get("href") not in visited]

    for link in links[:max_breadth]:
        if wiki_search(start_url="https://en.wikipedia.org" + link.get('href'), end_page_name=end_page_name, max_depth=max_depth - 1, end_page_url=end_page_url, max_breadth=max_breadth, path=path, visited=visited):
            return True
    del path[-1]
    return False

def format_path(path):
    return ' -> '.join(path)

def sort_links(link):
    # print(f'comparing {link.text} to {end_page_name}')
    return compare_strings(NLP, link.text, end_page_name)

def get_page_title(url):
    res = requests.get(url)
    res.raise_for_status()
    page_name = bs4.BeautifulSoup(res.text, "html.parser")
    page_name = page_name.select("#firstHeading")[0].text
    return page_name

def get_page_soup(url):
    res = requests.get(url)
    res.raise_for_status()
    return bs4.BeautifulSoup(res.text, "html.parser")

# print(compare_strings("Hello World", "Hello World"))
# model_test("Hello World", "Hello World")


if __name__ == '__main__':
    NLP = spacy.load('en_core_web_sm')
    main()