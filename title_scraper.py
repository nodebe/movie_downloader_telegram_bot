from bs4 import BeautifulSoup
import requests

global top_results, suggestions

top_results = []
suggestions = []

def download_scraper(movie_link):
    download_source = requests.get(movie_link+'/download').text
    download_results = BeautifulSoup(download_source, 'html.parser')

    return download_results

def movie_arranger(raw_movie):
    arranged = {}

    movie_link = raw_movie.find('a')['href']
    
    # Fetch download page HTML
    download_results = download_scraper(movie_link)

    arranged['title'] = raw_movie.find('a').get_text()
    arranged['image'] = raw_movie.img['src']
    arranged['download_link'] = movie_link + '/download'
    arranged['size'] = download_results.find(attrs={'class':'size-number'}).get_text()
    
    # Arrange results based on top 3 and put other 2 as suggestions
    if len(top_results) < 3:
        top_results.append(arranged)
    else:
        suggestions.append(arranged)

def net_naija_searcher(movie_title):
    url = 'https://www.thenetnaija.net'
    source = requests.get(url + f"/search?folder=videos&t={movie_title.split(' ')}").text

    soup = BeautifulSoup(source, 'html.parser')
    results = soup.find_all(attrs={"class":"sr-one"})

    for result in results:
        # We don't want to parse too many suggestions
        if len(suggestions) == 2:
            break

        movie_arranger(result)

net_naija_searcher('the batman')