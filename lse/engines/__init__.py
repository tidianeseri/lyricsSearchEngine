#===============================================================================
#  Author : Tidiane Seri-Gnoleba tidianeseri@gmail.com
#===============================================================================

from bs4 import BeautifulSoup
import requests

from lse.utils.cleaner import cleanQuery, formatHTMLNewLines
from lse.utils.strikeamatch import compare_strings

TIMEOUT = 5

class BaseEngine:


    def __init__(self):
        self.results = []
        self.libparser = 'html5lib'
        self.queryString = 'q'

    def setPayload(self, query):
        return {self.queryString: query}

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
        payload = self.setPayload(query)
        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
        r = requests.get(self.SEARCH_URL, params=payload, headers=headers, timeout=TIMEOUT)
        self.resultIndex = 0

        if (r.status_code == 200):
            self.results = self.songResultsParser(r.text, query)

            if ((len(self.results) == 0 or self.results[0]['score'] < 0.75) and hasattr(self, "nextEngine")):
                self.results += self.nextEngine.searchSongs(query)

        else:
            return "HTTP error: %s" % (r.status_code)

        return self.results

    def searchSongLyrics(self, link):
        '''
        Search song lyrics
        '''
        headers = {'Accept': 'text/html'}
        r = requests.get(link, headers=headers, timeout=TIMEOUT)

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
                songParsed = {'title':title, 'artist':artist, 'link':link, 'score':score, 'engine':self.__class__.__name__}
                songArray.append(songParsed)

        songArray = sorted(songArray, key=lambda score: score['score'], reverse=True)
        return songArray

    def setSuccessor(self, engine):
        self.nextEngine = engine

    def lyricsParser(self, html):
        '''
        Parse the lyrics
        '''
        response = BeautifulSoup(html, self.libparser)
        lyrics = self.getLyrics(response)
        moreInfo = self.getMoreInfo(response)

        lyrics = formatHTMLNewLines(lyrics)

        if moreInfo is not None:
            moreInfo = formatHTMLNewLines(moreInfo)

        if moreInfo is not None:
            song = {'lyrics':lyrics, 'more_info':moreInfo}
        else:
            song = {'lyrics':lyrics}

        return song


class RapGeniusEngine(BaseEngine, object):

    def __init__(self):
        super(self.__class__, self).__init__()

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
        super(self.__class__, self).__init__()

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

class SongLyricsEngine(BaseEngine, object):

    def __init__(self):
        super(self.__class__, self).__init__()

        self.SEARCH_URL = "http://www.songlyrics.com/index.php"
        self.queryString = "searchW"

    def setPayload(self, query):
        return {'section':'search', self.queryString: query}

    def songsDiv(self, response):
        return response.find_all(class_='serpresult', limit=5)

    def getLink(self, songResponse):
        return songResponse.a.get('href')

    def getTitle(self, songResponse):
        return songResponse.h3.a.text[:-7]

    def getArtist(self, songResponse):
        return songResponse.find(class_='serpdesc-2').p.a.text

    def getLyrics(self, response):
        return response.find(id="songLyricsDiv").text

class LyricsManiaEngine(BaseEngine, object):

    def __init__(self):
        super(self.__class__, self).__init__()

        self.SEARCH_URL = "http://www.lyricsmania.com/searchnew.php"
        self.URL = "http://www.lyricsmania.com/"
        self.queryString = "k"

    def songsDiv(self, response):
        return response.find(class_="col-left").find_all("li", limit=5)

    def getLink(self, songResponse):
        return self.URL + songResponse.a.get('href')

    def getTitle(self, songResponse):
        return songResponse.a.get('title')

    def getArtist(self, songResponse):
        response = songResponse.a
        title = response.get('title')
        title = title.replace(" lyrics", "")
        artist = response.text
        artist = artist.replace(" - " + title, "")
        return artist

    def getLyrics(self, response):
        response = response.find(class_="lyrics-body")
        response.div.clear()
        return response.text

class Lyrics007Engine(BaseEngine, object):

    def __init__(self):
        super(self.__class__, self).__init__()

        self.URL = "http://www.lyrics007.com/"
        self.SEARCH_URL = "http://www.lyrics007.com/search.php"

    def songsDiv(self, response):
        songs = response.find(class_="content").find_all("h2", limit=5)
        songsh3 = response.find(class_="content").find_all("h3", limit=5)
        for idx, song in enumerate(songs):
            songs[idx].append(songsh3[idx])
        return songs

    def getLink(self, songResponse):
       return self.URL + songResponse.a.get('href')

    def getTitle(self, songResponse):
        title = songResponse.h3.text
        title = title.replace("Song: ", "")
        title = title.replace(" Lyrics", "")
        return title

    def getArtist(self, songResponse):
        artist = songResponse.text
        artist = artist.replace("Artist: ", "")
        idx = artist.find("Song:")
        return artist[:idx]

    def getLyrics(self, response):
        response = response.find(class_="content")
        response.div.clear()
        return response.text

class WikiaEngine(BaseEngine, object):

    def __init__(self):
        super(self.__class__, self).__init__()

        self.SEARCH_URL = "http://lyrics.wikia.com/Special:Search"
        self.queryString = "search"

    def songsDiv(self, response):
        return response.find_all(class_="result", limit=10)

    def getLink(self, songResponse):
        return songResponse.a.get('href')

    def getTitle(self, songResponse):
        response = songResponse.h1.a.text
        idx = response.find(':')
        if idx > 0:
            response = response[:idx]
        return response

    def getArtist(self, songResponse):
        response = songResponse.h1.a.text
        idx = response.find(':')
        if idx > 0:
            response = response[idx + 1:]
        return response

    def getLyrics(self, response):
        to_clean = response.find(class_="lyricbox")
        scripts = to_clean.find_all("script")
        for scr in scripts:
            scr.clear()
        br = to_clean.find_all("br")
        for b in br:
            b.replace_with("\n")
        return to_clean.text