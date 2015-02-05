'''
Created on Feb 3, 2015

@author: Tidiane Seri-Gnoleba
'''
import re

def replaceWords(query, wordsList):
    for word in wordsList:
        pattern = re.compile(word, re.IGNORECASE)
        query = pattern.sub("", query)

    return query

def cleanQuery(query):
    beg = query.find('(')
    end = query.find(')')

    while (beg != -1 and end != -1):
        query = query[:beg] + query[end + 1:]
        beg = query.find('(')
        end = query.find(')')

    beg = query.find('[')
    end = query.find(']')

    while (beg != -1 and end != -1):
        query = query[:beg] + query[end + 1:]
        beg = query.find('[')
        end = query.find(']')

    query = query.replace(' - ', ' ')
    query = query.replace('-', ' ')
    query = query.replace('\"', '')
    query = query.replace(' f. ', ' ')

    query = replaceWords(query, {'ft', 'official video', 'clip officiel', 'clip', 'lyrics'})
    query = removeDigits(query)

    return query

def formatHTMLNewLines(text):
    return text.replace("\n", "<br \>")

def removeDigits(text):
    # Remove digits
    text = ''.join([i for i in text if not i.isdigit()])
    return text
