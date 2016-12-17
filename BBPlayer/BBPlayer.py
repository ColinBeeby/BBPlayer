#!/usr/bin/python
'''
Created on 20 Nov 2016

@author: colin
'''
from os import listdir
from os.path import isdir, join

from Tkinter import *

from MplayerController import MplayerController
from PlaylistController import PlaylistController
import tkFont

class GUIInterfaceController(object):
    '''
    Class to provide functions to interface to the MplayerController
    '''
    
    MUSIC_PATH = '/home/colin/Music/'
    INFO_FRAME_HEIGHT = 75
    FOOTER_FRAME_HEIGHT = 75
    FONT_SIZE = 30
    
    def __init__(self):
        '''
        Constructor
        '''   
        self.mplayer = MplayerController(self.finishedPlayingTrack)
        self.playlist = PlaylistController()
        self.playListLength = 0
    
        self.root = Tk()
        
        self.customFont = tkFont.Font(family="Helvetica", size=self.FONT_SIZE)
        
        self.root.title('BBPlayer')
        self._fullScreen()
        #self.root.geometry("500x500") #take this out for production
        self._hideTitleBar()
        
        #Set up the info frame
        self._addInfoFrame(self.INFO_FRAME_HEIGHT)
        #Set up the main frames
        self._addMainFrame()
        #Set up the footer frame
        self._addFooterFrame(self.FOOTER_FRAME_HEIGHT)
        
        self.root.focus_set()
        mainloop()
        
    def _addInfoFrame(self, frameHeight):
        self.infoFrame = Frame(self.root, height=frameHeight, bg="blue")
        self.infoFrame.pack_propagate(0)
        self.infoFrame.pack(side=TOP, fill=X)
        self.playlistLengthEntry = Entry(self.infoFrame, width=3, font=self.customFont)
        self.playlistLengthEntry.pack(side=RIGHT, fill=Y)
        self.playlistLengthEntry.insert(0, '{0}'.format(self.playListLength))
        self.currentlyPlayingEntry = Entry(self.infoFrame, font=self.customFont)
        self.currentlyPlayingEntry.pack(side=LEFT, fill=BOTH, expand=1)
        
    def _addMainFrame(self):
        self.mainFrame = Frame(self.root, bg="red")
        self.mainFrame.pack_propagate(0)
        self.mainFrame.pack(side=TOP, fill=BOTH, expand=1)
        self._addControlsFrame()
        self._addFilesFrame()
        
    def _addControlsFrame(self):
        self.controlsFrame = Frame(self.mainFrame, bg="yellow")
        self.controlsFrame.pack_propagate(0)
        self.controlsFrame.pack(side=TOP, fill=BOTH, expand=1)
        self.pauseButton = Button(self.controlsFrame, text='Play/Pause', command=self.pause, font=self.customFont, bg="green")
        self.pauseButton.pack(side=LEFT, fill=BOTH, expand=1)
        self.nextButton = Button(self.controlsFrame, text='Next', command=self.next, font=self.customFont, width=20, bg="yellow")
        self.nextButton.pack(side=RIGHT, fill=BOTH)
        
        
    def _addFilesFrame(self):
        self.filesFrame = Frame(self.mainFrame)
        self.filesFrame.pack_propagate(0)
        self.artistListBox = Listbox(self.filesFrame, selectmode=SINGLE, font=self.customFont, width=10)
        self.artistListBox.bind('<<ListboxSelect>>', self.onArtistSelect)
        self.artistListBox.pack(side=LEFT, fill=BOTH)
        self.artistList = []
        self.albumListBox = Listbox(self.filesFrame, selectmode=SINGLE, font=self.customFont)
        self.albumListBox.bind('<<ListboxSelect>>', self.onAlbumSelect)
        self.albumListBox.pack(side=RIGHT, fill=BOTH, expand=1)
        self.albumList = []
        self._getArtists()
        
        
        
    def _addFooterFrame(self, frameHeight):
        self.footerFrame = Frame(self.root, height=frameHeight, bg="green")
        self.footerFrame.pack_propagate(0)
        self.footerFrame.pack(side=BOTTOM, fill=X)
        self.controlsButton = Button(self.footerFrame, text="< Back", width=10, command=lambda: self.showControlsFrame(), font=self.customFont, bg="cyan3")
        #self.controlsButton.pack(side=RIGHT, fill=BOTH)
        self.addButton = Button(self.footerFrame, text='Add', width=10, command=lambda: self.showFilesFrame(), font=self.customFont, bg="cyan3")
        self.addButton.pack(side=RIGHT, fill=BOTH)
        self.quitButton = Button(self.footerFrame, text='Quit', command=self.quit, font=self.customFont)
        self.quitButton.pack(side=LEFT, fill=BOTH, expand=1)
        
        
    def _fullScreen(self):
        w, h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry("%dx%d+0+0" % (w, h))
        
    def _hideTitleBar(self):
        self.root.overrideredirect(True)
        
    def _getArtists(self):
        self.artistListBox.delete(0, END)
        self.artistList = []
        if isdir(self.MUSIC_PATH):
            for artistDir in listdir(self.MUSIC_PATH):
                if isdir(join(self.MUSIC_PATH, artistDir)):
                    self.artistListBox.insert(END, artistDir)
                    self.artistList.append(join(self.MUSIC_PATH, artistDir))
                
        
    def onArtistSelect(self, evt):
        artist = evt.widget
        if artist.curselection():
            index = int(artist.curselection()[0])
            value = self.artistList[index]
            self._getAlbums(value)
        
    def _getAlbums(self, artistPath):
        self.albumListBox.delete(0, END)
        self.albumList = []
        if isdir(artistPath):
            for albumDir in listdir(artistPath):
                if isdir(join(artistPath, albumDir)):
                    self.albumListBox.insert(END, albumDir)
                    self.albumList.append(join(artistPath, albumDir))
                    
    def onAlbumSelect(self, evt):
        album = evt.widget
        if album.curselection():
            index = int(album.curselection()[0])
            value = self.albumList[index]
            currentPlaylistLength = self.playListLength
            self.playListLength = self.playlist.addDirectoryToPlaylist(value)
            self._updatePlayListLengthEntry()
            if self.playListLength > 0 and currentPlaylistLength == 0:
                self.nextTrack = self.playlist.getNextTrack()
                self.play()
        
        
        
    def finishedPlayingTrack(self):
        self._playNextTrack()
        
    def _updatePlayListLengthEntry(self):
        self.playlistLengthEntry.delete(0, END)
        self.playlistLengthEntry.insert(0, '{0}'.format(self.playListLength))
    
    def play(self):
        if not self.nextTrack == None:
            self.mplayer.play(self.nextTrack['FilePath'])
            self.currentlyPlayingEntry.delete(0, END)
            self.currentlyPlayingEntry.insert(0, '{0} - {1}'.format(self.nextTrack['Artist'], self.nextTrack['Title']))
            
    def pause(self):
        self.mplayer.pause()
        
    def stop(self):
        self.mplayer.stop()
        
    def quit(self):
        self.mplayer.quit()
        self.root.destroy()
        
    def next(self):
        self._playNextTrack()
        
    def showFilesFrame(self):
        self.controlsFrame.pack_forget()
        self.filesFrame.pack(side=TOP, fill=BOTH, expand=1)
        #This is bad design - this method is doing two different things!!
        self.addButton.pack_forget()   #pack(side=RIGHT, fill=BOTH)
        self.controlsButton.pack(side=RIGHT, fill=BOTH)
        
    def showControlsFrame(self):
        self.filesFrame.pack_forget()
        self.controlsFrame.pack(side=TOP, fill=BOTH, expand=1)
        #This is bad design - this method is doing two different things!!
        self.controlsButton.pack_forget()
        self.addButton.pack(side=RIGHT, fill=BOTH)
        
    def _playNextTrack(self):
        if self.playListLength > 0 :
            self.playListLength -= 1
            self._updatePlayListLengthEntry()
            self.nextTrack = self.playlist.getNextTrack()
            if not self.nextTrack == None:
                self.play()
        
    

if __name__ == '__main__':
    controller = GUIInterfaceController()
