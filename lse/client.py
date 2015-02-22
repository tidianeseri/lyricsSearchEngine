'''
Created on Feb 7, 2015

@author: chaikou
'''

import sys
from engines import *

class LyricsSearch:
    """
    main class module
    """

    def __init__(self, query=""):
        self.query = query
        self.results = []
        self.resultsIndex = 0
        self.enginesNameList = ['RapGeniusEngine', 'SongLyricsEngine', 'AZLyricsEngine', 'WikiaEngine', 'LyricsManiaEngine' ]
        self.enginesList = []
        self.nbResults = 0
        self.initEngines()

    def initEngines(self):

        for idx, engine in enumerate(self.enginesNameList):
            engineName = self.enginesNameList[idx]
            engine_class = globals()[engineName]
            engine = engine_class()
            self.enginesList.append(engine)

            if idx > 0:
                self.enginesList[idx - 1].setSuccessor(engine)

        self.engine = self.enginesList[0]

    def search(self, query):
        self.query = query
        self.results = self.engine.searchSongs(query)
        self.results = sorted(self.results, key=lambda score: score['score'], reverse=True)
        self.resultsIndex = 0
        self.nbResults = len(self.results)

        return self.results

    def getLyrics(self, formating=True):
        if len(self.results) > 0:

            # if self.results[self.resultsIndex]['score'] < 0.75:
                # print "Result score is only " + str(self.results[self.resultsIndex]['score'])

            # print "Showing: " + self.results[self.resultsIndex]['artist'] + " " + self.results[self.resultsIndex]['title'] + "\n"

            classname = self.results[self.resultsIndex]['engine']
            engine_class = globals()[classname]
            if formating == True:
                engine_class().searchSongLyrics(self.results[self.resultsIndex]['link'])['lyrics'].replace('<br \>', '\n')
                return engine_class().searchSongLyrics(self.results[self.resultsIndex]['link'])
            else:
                return engine_class().searchSongLyrics(self.results[self.resultsIndex]['link'])

        else:
            noResults = {}
            noResults['link'] = ''
            noResults['lyrics'] = 'No results'
            return noResults

    def getLyricsIndex(self, index, formating=True):
        if index >= 0 and index < len(self.results):
            self.resultsIndex = index
            return self.getLyrics()

    def showLyrics(self, formating=True):
        try:
            if formating == True:
                lyrics = self.getLyrics()['lyrics'].replace('<br \>', '\n')
            else:
                lyrics = self.getLyrics()['lyrics']
            print lyrics
            return lyrics
        except:
            print "Unexpected error:", sys.exc_info()[0]

    def showLyricsIndex(self, index, formating=True):
        try:
            if formating == True:
                lyrics = self.getLyricsIndex(index)['lyrics'].replace('<br \>', '\n')
            else:
                lyrics = self.getLyricsIndex(index)['lyrics']
            print lyrics
            return lyrics
        except:
            print "Unexpected error:", sys.exc_info()[0]

    def nextResult(self):
        if len(self.results) >= (self.resultsIndex + 2):
            self.resultsIndex += 1

    def getResults(self):
        return self.results
