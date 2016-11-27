'''
Created on 18 Nov 2016

@author: colin
'''

import time

from MplayerController import MplayerController

def finishedPlayingTrack():
    print 'Finished playing track'

if __name__ == '__main__':
    mplayer = MplayerController(finishedPlayingTrack);
    
    mplayer.play('/home/colin/Music/Inkubus Sukkubus/Supernature/01-Supernature.mp3')
    time.sleep(5)
    
    mplayer.pause()
    time.sleep(5)
    
    mplayer.pause()
    time.sleep(5)
    
    mplayer.play('/home/colin/Music/Inkubus Sukkubus/Wild/08-Storm.mp3')
    time.sleep(5)
    
    for i in range(5):
        mplayer.volumeUp()
        time.sleep(1)
        
    for i in range(5):
        mplayer.volumeDown()
        time.sleep(1)
    
    mplayer.stop()
    
    mplayer.quit()