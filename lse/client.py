'''
Created on Feb 7, 2015

@author: chaikou
'''

from engines import RapGeniusEngine, AZLyricsEngine, SongLyricsEngine, LyricsManiaEngine, WikiaEngine

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

        return self.results

    def getLyrics(self):
        if len(self.results) > 0:

            if self.results[self.resultsIndex]['score'] < 0.75:
                print "Result score is only " + str(self.results[self.resultsIndex]['score'])

            print "Showing: " + self.results[self.resultsIndex]['artist'] + " " + self.results[self.resultsIndex]['title'] + "\n"

            classname = self.results[self.resultsIndex]['engine']
            engine_class = globals()[classname]
            return engine_class().searchSongLyrics(self.results[self.resultsIndex]['link'])

        else:
            noResults = {}
            noResults['link'] = ''
            noResults['lyrics'] = 'No results'
            return noResults

    def nextResult(self):
        if len(self.results) > (self.resultsIndex + 2):
            self.resultsIndex += 1

    def getResults(self):
        return self.results