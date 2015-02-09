'''
Created on Feb 7, 2015

@author: chaikou
'''

from engines import RapGeniusEngine, AZLyricsEngine, SongLyricsEngine, LyricsManiaEngine

class LyricsSearch:
    """
    main class module
    """

    def __init__(self, query=""):
        self.query = query
        self.initEngines()
        self.results = []
        self.resultsIndex = 0

    def initEngines(self):
        self.engine = RapGeniusEngine()
        self.engine2 = SongLyricsEngine()
        self.engine3 = AZLyricsEngine()
        self.engine4 = LyricsManiaEngine()
        self.engine.setSuccessor(self.engine2)
        self.engine2.setSuccessor(self.engine3)
        self.engine3.setSuccessor(self.engine4)

    def search(self, query):
        self.query = query
        self.results = self.engine.searchSongs(query)
        self.resultsIndex = 0

        return self.results

    def getLyrics(self):
        if len(self.results) > 0:
            if self.results[self.resultsIndex]['score'] < 0.75:
                print "Result score is only " + str(self.results[self.resultsIndex]['score'])

            results = sorted(self.results, key=lambda score: score['score'], reverse=True)
            print "Showing: " + self.results[self.resultsIndex]['artist'] + " " + self.results[self.resultsIndex]['title'] + "\n"

            classname = results[self.resultsIndex]['engine']
            engine_class = globals()[classname]
            return engine_class().searchSongLyrics(results[0]['link'])

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
