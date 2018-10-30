from bs4 import BeautifulSoup
import requests
import sys

def rating(name):
    #------------------------- For all 'Movies' results -------------------------
    #search ='http://www.imdb.com/find?q='
    #search += '%20'.join(movie_name.split())
    #search += '&s=tt&ttype=ft&ref_=fn_ft'
    #------------ For all results: Movie, TV, TV Episode, Video Game ------------
    movies_info = []
    search ='http://www.imdb.com/find?ref_=nv_sr_fn&q='
    search += '+'.join(name.split())
    search += '&s=all'

    try:
        response_search_page = requests.get(search)
        soup = BeautifulSoup(response_search_page.text,'lxml')
        article_div = soup.find('div',{'class':'article'})
        result_header = soup.find(['h1']).text
        if result_header.find('No results') >= 0:
            sys.exit()
        print('Displaying results ...','\n')
        movieListSection = article_div.find('table',{'class':'findList'})
        moviesList = movieListSection.find_all('td',{'class':'result_text'})
    except:
        sys.exit()

    for movie in moviesList:
        info = {}
        info['name'] = movie.text.strip()
        if name.upper() not in info['name'].upper():
            continue
        info['link'] = movie.find(['a'])['href']
        movie_page_response = requests.get('http://www.imdb.com'+info['link'])
        movie_soup = BeautifulSoup(movie_page_response.text,'lxml')
        title_strip = movie_soup.find('div',{'class':'title_bar_wrapper'})     
        title_bar = title_strip.find('div',{'class':'subtext'})
        dur = title_bar.find('time')
        info['duration'] = dur.text.strip()
        rating_div = title_strip.find('div',{'class':'ratingValue'})
        if rating_div == None:
            info['rating'] = 'Unrated'
        else:
            info['rating'] = rating_div.text.strip()
                
        print('Name:',info['name'])
        print('Duration:',info['duration'])
        if info['rating'] == 'Unrated':
            print('Unrated Movie')
        else:
            print('Rating:',info['rating'])

        print('Link: http://www.imdb.com'+info['link'])
        print('\n')
        movies_info.append(info)

    print('-----------------------------------------------------------------------------\n')

name = input("Enter name of movie: ")
rating(name)
