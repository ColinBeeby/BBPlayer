'''
Created on 19 Nov 2016

@author: colin
'''
from os import listdir
from os.path import isdir, isfile, join
import re
import eyed3

class PlaylistController(object):
    '''
    class to maintain and control a playlist
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.playlist = []
        self.currentItemIndex = 0
        self.nextTrackIndex = 0
        
    def addFileToPlaylist(self, path):
        '''
        Add an individual file to the playlist
        '''
        self.playlist.append(path)
        
    def addDirectoryToPlaylist(self, path):
        '''
        Add all files in a folder to the playlist
        '''
        if isdir(path):
            #filesInDir = [join(path, f) for f in listdir(path) if isfile(join(path, f))]
            #There is probably some clever way to do this with a list comprehension
            filesInDir = []
            for trackFile in listdir(path):
                if isfile(join(path, trackFile)) and re.match('.*\.mp3$', trackFile, 0):
                    #filesInDir.append(join(path, trackFile))
                    audio = eyed3.load(join(path, trackFile))
                    trackDict = self._createTrackDict(audio.tag, join(path, trackFile))
                    filesInDir.append(trackDict)
            self.playlist = self.playlist + filesInDir
            
        return len(self.playlist)
    
    def _createTrackDict(self, tag, filePath):
        trackDict = {
            'Artist':tag.artist,
            'Album':tag.album,
            'Title':tag.title,
            'TrackNumber':tag.track_num,
            'FilePath':filePath
            }
        return trackDict
            
    def getCurrentTrack(self):
        if self.playlist and self.currentItemIndex < len(self.playlist):
            track = self.playlist[self.currentItemIndex]
            self.currentItemIndex += 1
            return track
        return None
    
    def getNextTrack(self):
        if self.playlist and self.nextTrackIndex < len(self.playlist):
            track = self.playlist[self.nextTrackIndex]
            self.nextTrackIndex += 1
            return track
        return None
            
            