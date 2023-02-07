import urllib.request
from bs4 import BeautifulSoup
from tqdm.auto import tqdm

arxiv = urllib.request.urlopen("https://export.arxiv.org/archive/cs")
data = arxiv.read()
soup = BeautifulSoup(str(data), features="html.parser")

fields = []
for s in list(soup.find_all('li'))[11:51]:
    fields.append(str(s)[10:12])

url = 'http://export.arxiv.org/list/cs.{}/{}{}?show=1000'
# fields = ['CV', 'DS', 'LO', 'LG', 'OS']
# keywords = ["deep", "learn", "convolution", "recurrent", "neural", "network", "bound", "parallel", "approximation", "graph", "graphs", "algorithm", "dynamic", "random", "parameterized", "benchmark"]
months = ['{:0>2d}'.format(i+1) for i in range(12)]
years = ['{:0>2d}'.format(i) for i in range(12, 21)]

f = open("./../data/paperlinks.txt", "wt", encoding = "utf8")

for field in fields:
    # f = open("./../data/arxiv/%s.txt" % (field), "wt", encoding = "utf8")
    print('Retrieving data from {}'.format(field))
    for year in years:
        for month in months:
            query_url = url.format(field, year, month)
            print('Retrieving {}'.format(query_url))
            try:
                uh = urllib.request.urlopen(query_url)
                data = uh.read()
                soup = BeautifulSoup(str(data), features="html.parser")
                titles = soup.findAll('div', {'class': 'list-title'})
                authors = soup.findAll('div', {'class': 'list-authors'})
                paper_urls = soup.findAll('span', {'class': 'list-identifier'})
                if len(titles) != len(authors):
                    print(str(len(titles)) + " != " + str(len(titles)))
                    print('Error: Title and Author mismatch')
                else:
                    for title, author, paper_url in zip(titles, authors, paper_urls):
                        title = title.contents[-1].strip()
                        paper_url = 'http://export.arxiv.org' + paper_url.contents[0].attrs['href']
                        paper_authors = [au.string.strip() for au in author.findAll('a')]
                        low_title = title.lower()
                        # if any(k in low_title for k in keywords):
                        f.write(title + "\n")
                        f.write(paper_url + "\n")
            except:
                print("Can't access URL: %s" % (query_url))

f.close()