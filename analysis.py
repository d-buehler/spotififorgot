from collections import namedtuple
from operator import attrgetter 

AggregatedAlbumStats = namedtuple('AggregatedAlbumStats',
                                  ['albumName', 'nrQueriesMatched', 'maxSimilarity', 'maxPopularity', 'releaseDate', 'artists'])

class AlbumQueryStats(object):
    '''Class to house aggregated stats per-album from a single Track query'''
    def __init__(self, userTrackName, querySimilarity, releaseDate, queriedTrackPopularity, trackName, artists):
        self.query = userTrackName
        self.similarity = querySimilarity
        self.releaseDate = releaseDate
        self.popularity = queriedTrackPopularity
        self.trackName = trackName
        self.artists = artists
            
    def __str__(self):
        return str(self.__dict__[['query', 'similarity', 'releaseDate', 'popularity', 'trackName', 'artists']])
    
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def updateStats(self, userTrackName, querySimilarity, releaseDate, queriedTrackPopularity, trackName):
        '''
        Updates the album's stats if a more similar result is found. The intention is to only store the stats
            for the MOST SIMILAR track (vs the user's search term). Purposefully skipping updates for fields
            that should not change like artists and releaseDate
        '''
        if self.similarity < querySimilarity:
            self.similarity = querySimilarity
            self.popularity = queriedTrackPopularity
            self.trackName = trackName

def jaccard(stringA, stringB):
    '''
    Returns the Jaccard similarity for two strings (0 if either string is empty)
    :param stringA: One string to compare
    :param stringB: The other string to compare
    '''
    
    if len(stringA) == 0 or len(stringB) == 0:
        return 0
    
    setWordsA = set(str(stringA).lower().strip().split(' '))
    setWordsB = set(str(stringB).lower().strip().split(' '))
    
    intersection = setWordsA & setWordsB
    union = setWordsA | setWordsB
    
    return float( len(intersection) / len(union) )
    
def getAlbumStats(userTrackName, queryResults, debug=False):
    '''
    Distills a set of track query results from the Spotify API into a dict of stats
    :param userTrackName: the track that the user searched for, as they had entered it
    :param queryResults: the results from the Spotify search API for the user-entered track
    :param debug: true = more stuff is printed
    '''
    
    resultsAlbumStats = {}
    i = 0
    
    for track in queryResults:
        
        if debug and i == 0:
            print(track)
            i += 1
        
        querySimilarity = jaccard(userTrackName, track.get('name', ''))
        releaseDate = track.get('album', {}).get('release_date', '1900-01-01')
        trackPopularity = track.get('popularity', 0)
        albumName = track.get('album', {}).get('name', 'No Album Found')
        trackName = track.get('name', '<No Name Found>')
        artists = ','.join([ artist.get('name', 'No Artist Name') for artist in track.get('artists', []) ])
        
        
        if albumName not in resultsAlbumStats.keys():
            resultsAlbumStats[albumName] = AlbumQueryStats(userTrackName=userTrackName,
                                                           querySimilarity=querySimilarity, 
                                                           releaseDate=releaseDate,
                                                           queriedTrackPopularity=trackPopularity,
                                                           trackName=trackName,
                                                           artists=artists)
            
        else:
            # print("Updating {}".format(albumName))
            resultsAlbumStats[albumName].updateStats(userTrackName=userTrackName,
                                                     querySimilarity=querySimilarity,
                                                     releaseDate=releaseDate,
                                                     queriedTrackPopularity=trackPopularity,
                                                     trackName=trackName)
        
    # print("END - MBDTF - ",  resultsAlbumStats.get('My Beautiful Dark Twisted Fantasy', 'NA'))
    return resultsAlbumStats


def updateAllStats(thisAlbumStats, userInput, allAlbumStats):
    '''
    Updates the collection of album stats from all entered tracks
    :param thisAlbumStats: the batch of album stats to add to the collection (dict)
    :param userInput: the user input that generated this batch of album stats
    :param allAlbumStats: the complete collection of album stats (dict)
    :return: the updated, complete collection of album stats
    '''
    newAlbums = [ album for album in thisAlbumStats.keys() if album not in allAlbumStats.keys() ]
    for album in newAlbums:
        allAlbumStats[album] = {}

    for album in thisAlbumStats.keys():
        allAlbumStats[album][userInput] = thisAlbumStats[album]
        
    return allAlbumStats


def getTopAlbums(allAlbumStats, nrAlbums):
    '''
    Returns a sorted version of the passed list of AggregatedAlbumStats, containing nrAlbums albums
        in descending order of likelihood to match the queries, based on the below sort:
    Sort album stats by...
        1) Number of matched queries
        2) Max similarity of a query to an album track
        3) Popularity
        4) Release date
    ...and return the top nrAlbums albums
    :param aggregatedStats: list containing AggregatedAlbumStats objects
    :param nrAlbums: the number of albums to return
    :return: sorted version of the input list
    '''
    aggregatedStats = []
    for album, allQueryStats in allAlbumStats.items():

        albumAgg = AggregatedAlbumStats(albumName=album,
                                        artists=list(allQueryStats.values())[0].artists,
                                        nrQueriesMatched=len(list(allQueryStats.keys())),
                                        maxSimilarity=max([ stats.similarity for stats in allQueryStats.values() ]),
                                        maxPopularity=max([ stats.popularity for stats in allQueryStats.values() ]),
                                        releaseDate=max([ stats.releaseDate for stats in allQueryStats.values() ]))

        aggregatedStats.append(albumAgg)
    
    topAlbums = sorted(aggregatedStats, 
                       reverse=True,
                       key=attrgetter('nrQueriesMatched', 'maxSimilarity', 'maxPopularity', 'releaseDate'))
    
    return topAlbums[0:nrAlbums]