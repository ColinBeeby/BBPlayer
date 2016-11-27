'''
Created on 20 Nov 2016

@author: colin
'''
import time

from Tkinter import *

from MplayerController import MplayerController
from PlaylistController import PlaylistController

class GUIInterfaceController(object):
    '''
    Class to provide functions to interface to the MplayerController
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        self.mplayer = MplayerController(self.finishedPlayingTrack)
        self.playlist = PlaylistController()
    
        self.root = Tk()
        self.root.title('BBPlayer')
        #self._fullScreen()
        self.root.geometry("500x500")
        #self._hideTitleBar() PUT THIS BACK IN FOR PRODUCTION
        
        #Label(text='Hello World!!').pack()
        #Button(self.root, text='Play', command=self.play).pack()
        #Button(self.root, text='Stop', command=self.stop).pack()
        Button(self.root, text='Pause', command=self.pause).pack()
        Button(self.root, text='Next', command=self.next).pack()
        Button(self.root, text='Quit', command=self.quit).pack()
        self.trackDetails = Entry(self.root, width=100)
        self.trackDetails.pack()
        #self.root.protocol("WM_DELETE_WINDOW", self.quit)
        self.playListLength = self.playlist.addDirectoryToPlaylist('/home/colin/Music/Inkubus Sukkubus/Supernature')
        if self.playListLength > 0:
            self.nextTrack = self.playlist.getNextTrack()
            self.play()
            
        self.root.focus_set()
        mainloop()
        
    def _fullScreen(self):
        w, h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry("%dx%d+0+0" % (w, h))
        
    def _hideTitleBar(self):
        self.root.overrideredirect(True)
        
    def finishedPlayingTrack(self):
        self._playNextTrack()
        pass
    
    def play(self):
        if not self.nextTrack == None:
            self.mplayer.play(self.nextTrack['FilePath'])
            self.trackDetails.delete(0, END)
            self.trackDetails.insert(0, '{0} {1}'.format(self.nextTrack['TrackNumber'], self.nextTrack['Title']))
            
    def pause(self):
        self.mplayer.pause()
        
    def stop(self):
        self.mplayer.stop()
        
    def quit(self):
        self.mplayer.quit()
        self.root.destroy()
        
    def next(self):
        self._playNextTrack()
        
    def _playNextTrack(self):
        self.nextTrack = self.playlist.getNextTrack()
        if not self.nextTrack == None:
            self.play()
        
    

if __name__ == '__main__':
    controller = GUIInterfaceController()