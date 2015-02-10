# lyricsSearchEngine
This tool let you easily find lyrics from various lyrics sites
Included lyrics site parsers are 'RapGenius', 'SongLyrics', 'AZLyrics', 'Wikia' and 'LyricsMania'.

# Install
To install:
python setup.py install

# How to use
Import the client:
from lse.client import LyricsSearch

client = LyricsSearch()

Search:
client.search("Enter your query")

The results are stored and sorted by relevance in an array:
client.results

Get the lyrics:
client.getLyrics()
or client.getLyricsIndex(idx)  //idx is the position of a specific result 

Show the lyrics:
client.showLyrics()
or client.showLyricsIndex(idx)

Advance to the next result:
client.nextResult()

# Example
client = LyricsSearch()

client.search("Kendrick Lamar Hiiipower")

client.getLyrics()

client.nextResult()

client.getLyrics
