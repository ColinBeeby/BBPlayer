'''
Created on 18 Nov 2016

@author: colin
'''

import thread
import time

from mplayer import Player

class MplayerController(object):
    '''
    Class providing functions to control mplayer
    '''

    def __init__(self, callback):
        '''
        Constructor
        '''
        self.player = Player()
        self.stopPlaying = False
        self.monitoring = False
        self.endOfTrackCallback = callback
        
    def play(self,path):
        # If something is already playing, stop the monitoring of it
        if self.monitoring:
            self.stop()
            
        self.player.loadfile(path)
        if self.player.paused:
            self.player.pause() #initial unpause of trace
            
        # Thread off a job to raise an event when this file has finished playing
        self.stopPlaying = False
        thread.start_new_thread(self._monitorPlayback, (1,))
        
    def pause(self):
        self.player.pause()
        
    def stop(self):
        self.player.stop()
        self.stopPlaying = True
        # Give _monitorPlayback enough time to shutdown
        time.sleep(2)
        
    def quit(self):
        self.player.quit()
        
    def volumeUp(self):
        if self.player.volume < 90:
            self.player.volume += 10
        
    def volumeDown(self):
        if self.player.volume > 10:
            self.player.volume -= 10
            
    def getVolume(self):
        return self.player.volume
        
    def _monitorPlayback(self,_):
        self.monitoring = True
        while (self.player.stream_pos < self.player.stream_length) and not self.stopPlaying:
            print self.player.stream_pos
            time.sleep(1)
            
        self.monitoring = False
        if not self.stopPlaying:
            self.endOfTrackCallback()
