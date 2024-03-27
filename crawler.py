import os

try:
    os.system('pip install requests')
    os.system('pip install beautifulsoup4')
except Exception as e:
    print(f"Error installing dependencies: {e}")
    exit(1)

import requests
from bs4 import BeautifulSoup

# Define the crawl function
def crawl(url : str):
    """
    Crawl the given URL and return a list of links found on the page.
    
    Args:
        url (str): The URL to crawl
    
    Returns:
        list: A list of links found on the page
    """

    # Initialize the list of links
    links = []

    # Try to access the URL
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(f"Error accessing {url}: {e}")
        return links

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all the links on the page
    for link in soup.find_all('a'):
        href = link.get('href')
        
        if href is None: # Skip if no href attribute
            continue
        if href.startswith('/'): # Convert relative URLs to absolute URLs
            domain = url.split('//')[1].split('/')[0]
            href = 'https://' + domain + href
        elif not href.startswith('http') and not href.startswith('www'): # Skip if not an absolute URL
            continue

        if href not in links: # Add the link to the list
            links.append(href)    
    return links

# Initialize variables  
queue = []
visited = set()

# Ask user for input
start_url = input("Enter start URL: https://")
crawl_depth = int(input("Enter crawl depth (0 = infinity): "))

# Add the start URL to the queue and visited set
queue.append('https://' + start_url)
visited.add('https://' + start_url)

# Get the script directory
script_dir = os.path.dirname(os.path.realpath(__file__))
output_dir = os.path.join(script_dir, 'out')
output = os.path.join(output_dir, start_url + '_' + str(crawl_depth) + '.txt') # Output file in format <start_url>_<crawl_depth>.txt

# Crawl the web
with open(output, 'w') as file:
    while len(visited) < crawl_depth and len(queue) > 0:
        url = queue.pop(0)
        links = crawl(url)
        for link in links:
            if link not in visited:
                print(link)
                try:
                    file.write(link + '\n')
                except Exception as e:
                    print(f"Error writing to file: {e}")
                queue.append(link)
                visited.add(link)