#===============================================================================
#  Author : Tidiane Seri-Gnoleba tidianeseri@gmail.com
#===============================================================================

from bs4 import BeautifulSoup
import requests

from lse.utils.cleaner import cleanQuery, formatHTMLNewLines
from lse.utils.strikeamatch import compare_strings


class BaseEngine:


    def __init__(self):
        self.results = []
        self.libparser = 'html5lib'

    def songsDiv(self, response): pass
    def getLink(self, song): pass
    def getTitle(self, song): pass
    def getArtist(self, song): pass
    def getLyrics(self, response): pass
    def getMoreInfo(self, response): pass

    def searchSongs(self, query):
        '''
        Search a song
        '''
        query = cleanQuery(query)
        payload = {'q': query[:40]}
        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
        r = requests.get(self.SEARCH_URL, params=payload, headers=headers)
        self.resultIndex = 0

        if (r.status_code == 200):
            self.results = self.songResultsParser(r.text, query)

        else:
            return "HTTP error: %s" % (r.status_code)

    def searchSongLyrics(self, link):
        '''
        Search song lyrics
        '''
        headers = {'Accept': 'text/html'}
        r = requests.get(link, headers=headers)

        if (r.status_code == 200):
            result = self.lyricsParser(r.text)
            result['link'] = link
            return result
        else:
            return "HTTP error: %s" % (r.status_code)

    def songResultsParser(self, htmlResponse, query):
        '''
        Parse the songs results
        '''

        results = BeautifulSoup(htmlResponse, self.libparser)
        songs = self.songsDiv(results)
        songArray = []

        for song in songs:
            link = self.getLink(song)

            title = self.getTitle(song)
            artist = self.getArtist(song)
            score = compare_strings(query, artist + " " + title)

            if score >= 0.5:
                songParsed = {'title':title, 'artist':artist, 'link':link, 'score':score}
                songArray.append(songParsed)

        songArray = sorted(songArray, key=lambda score: score['score'], reverse=True)
        return songArray

    def lyricsParser(self, html):
        '''
        Parse the lyrics
        '''
        response = BeautifulSoup(html, self.libparser)
        lyrics = self.getLyrics(response)
        moreInfo = self.getMoreInfo(response)

        lyrics = formatHTMLNewLines(lyrics)

        if(len(moreInfo) > 0):
            moreInfo = formatHTMLNewLines(moreInfo)

        if(len(moreInfo) > 0):
            song = {'lyrics':lyrics, 'more_info':moreInfo}
        else:
            song = {'lyrics':lyrics}

        return song


class RapGeniusEngine(BaseEngine, object):

    def __init__(self):
        super(RapGeniusEngine, self).__init__()

        self.GENIUS_URL = "http://genius.com"
        self.ARTIST_URL = "http://genius.com/artists"
        self.EXPLANATION_URL = self.GENIUS_URL + "/annotations/for_song_page"
        self.SEARCH_URL = "http://genius.com/search"

    def songsDiv(self, response):
        return response.find(id="main").find_all(class_="song_link", limit=5)

    def getLink(self, songResponse):
        return songResponse['href']

    def getTitle(self, songResponse):
        return songResponse.find(class_="title_with_artists").find(class_="song_title").text

    def getArtist(self, songResponse):
        return songResponse.find(class_="title_with_artists").find(class_="artist_name").text

    def getLyrics(self, response):
        return response.find(class_="lyrics").text


class AZLyricsEngine(BaseEngine, object):

    def __init__(self):
        super(AZLyricsEngine, self).__init__()

        self.SEARCH_URL = "http://search.azlyrics.com/search.php"

    def songsDiv(self, response):
        return response.find(id="inn").find_all(class_="sen", limit=5)

    def getLink(self, songResponse):
        return songResponse.a.get('href')

    def getTitle(self, songResponse):
        return songResponse.a.text

    def getArtist(self, songResponse):
        return songResponse.b.text

    def getLyrics(self, response):
        return response.find(id="main").find(class_="ringtone").find_next_sibling("div").text

