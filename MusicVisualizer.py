# This program is a music visualizer and player for .WAV files.
# This project was created between 1/21/2021 and 1/23/2021 for the Badger Hackathon.

# Authors: Nathanael Acker, Khalil Horton, Alex Sannikov
# GitHub repository link: https://github.com/TheRealPiGuy/Badger-Hackathon-2021

# Helpful Resources:
    # Visualizer with Librosa and Pygame: https://medium.com/analytics-vidhya/how-to-create-a-music-visualizer-7fad401f5a69
    # Player with Tkinter: https://kalebujordan.com/make-your-own-music-player-in-python/
    # Pygame functions: https://www.pygame.org/docs/ref/music.html



import librosa
import numpy as np
import pygame
import math
from tkinter import *
from tkinter import filedialog
from tkinter import colorchooser
import os


playing = False # Global variable, represents if music is playing or not


def clamp(min_value, max_value, value):
    if value < min_value:
        return min_value
    if value > max_value:
        return max_value
    return value




class AudioBar:

    def __init__(self, x, y, freq, color, width=50, min_height=10, max_height=100, min_decibel=-80, max_decibel=0):
        self.x, self.y, self.freq = x, y, freq
        self.color = color
        self.width, self.min_height, self.max_height = width, min_height, max_height
        self.height = min_height
        self.min_decibel, self.max_decibel = min_decibel, max_decibel
        self.__decibel_height_ratio = (self.max_height - self.min_height)/(self.max_decibel - self.min_decibel)

    def update(self, dt, decibel,color):
        self.color = color
        desired_height = decibel * self.__decibel_height_ratio + self.max_height
        speed = (desired_height - self.height)/0.1
        self.height += speed * dt
        self.height = clamp(self.min_height, self.max_height, self.height)

    def render(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y + self.max_height - self.height, self.width, self.height))


filename = "silence.wav"
#filePath = filedialog.askopenfilename(title="Select a Music File",filetypes=[(".WAV Files",'*.wav')]) # Use this line if you want
                                                                                                       # to be prompted for a file
                                                                                                       # instantly.



# Color Wheel
bar_color = (71,159,161)
colorWheelRadius = 50

def color():
    try:
        new_color = colorchooser.askcolor()[1]
        print("" + new_color)
        return new_color
    except Exception:
        return bar_color

# Background Color Stuff
def get_background_color(background_color):
    red = (255,0,0)
    orange = (255,127,0)
    yellow = (255,255,0)
    green = (0,255,0)
    blue = (0,0,225)
    indigo = (75,0,130)
    violet = (148,0,211)
    black = (0,0,0)
    white = (255,255,255)
    if background_color == black: return white # Set colors, and cycle between them for the background.
    #elif background_color == white: return red
    #elif background_color == red: return orange
    #elif background_color == orange: return yellow 
    #elif background_color == yellow: return green 
    #elif background_color == green: return blue 
    #elif background_color == indigo: return violet
    else: return black

def get_text_color(background_color):
    black = (0,0,0)
    white = (255,255,255)
    if background_color == black:
        return white
    else:
        return black
    #return (255-background_color[0],255-background_color[1],255-background_color[2])

background_color = (0,0,0)
text_color = get_background_color(background_color)




time_series, sample_rate = librosa.load(filename)  # getting information from the file # Based on: Medium article

# getting a matrix which contains amplitude values according to frequency and time indexes
stft = np.abs(librosa.stft(time_series, hop_length=512, n_fft=2048*4)) # Based on: Medium article
spectrogram = librosa.amplitude_to_db(stft, ref=np.max)  # converting the matrix to decibel matrix # Based on: Medium article
frequencies = librosa.core.fft_frequencies(n_fft=2048*4)  # getting an array of frequencies # Based on: Medium article

# getting an array of time periodic
times = librosa.core.frames_to_time(np.arange(spectrogram.shape[1]), sr=sample_rate, hop_length=512, n_fft=2048*4) # Based on: Medium article
time_index_ratio = len(times)/times[len(times) - 1] # Based on: Medium article
frequencies_index_ratio = len(frequencies)/frequencies[len(frequencies)-1] # Based on: Medium article


def get_decibel(target_time, freq): # Based on: Medium article
    return spectrogram[int(freq * frequencies_index_ratio)][int(target_time * time_index_ratio)] 




icon = pygame.image.load("icon.png") # Set the window icon image

pygame.init()
pygame.display.set_caption("Music Visualizer") # Set the window text
pygame.display.set_icon(icon)


infoObject = pygame.display.Info() # Based on: Medium article


screen_w = int(infoObject.current_w/2.5) # Based on: Medium article
screen_h = int(infoObject.current_w/2.5) # Based on: Medium article



    


# Set up the drawing window
#screen = pygame.display.set_mode([screen_w, screen_h])
screen = pygame.display.set_mode([500, 500]) # Use this to make window size standard across all machines

bars = [] # Based on: Medium article

frequencies = np.arange(100, 8000, 100) # Based on: Medium article

r = len(frequencies) # Based on: Medium article

width = screen_w/r # Based on: Medium article

x = (screen_w - width*r)/2 # Based on: Medium article

for c in frequencies: # Based on: Medium article
    bars.append(AudioBar(x, 300, c, (71, 159, 161), max_height=250, width=width))
    x += width

t = pygame.time.get_ticks() # Based on: Medium article
getTicksLastFrame = t # Based on: Medium article

# Use these if you want to play the loaded music right away
#pygame.mixer.music.load(filePath)
#pygame.mixer.music.play(0)
#pygame.mixer.music.set_volume(0.05)


myFont = pygame.font.SysFont('Courier New',20) # Set the text font and size
text = myFont.render('Now Playing: ',True,(255,255,255)) # Set the actual text and color

playPauseImage = pygame.image.load('playpause2.png') # Load the play/pause image
folderImage = pygame.image.load('folder2.png') # Load the folder image


# The while loop structure is based on the Medium article, and is fairly standard.
# Run until the user asks to quit
running = True
while running:

    #text = myFont.render('Now Playing: ',True,text_color)
    
    
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    pygame.draw.circle(screen,(255,0,0),[250,150],75)
    x = pygame.mouse.get_pos()[0]
    y = pygame.mouse.get_pos()[1]
    sqx = (x - 250)**2
    sqy = (y - 150)**2
    
    t = pygame.time.get_ticks()
    deltaTime = (t - getTicksLastFrame) / 1000.0
    getTicksLastFrame = t

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN: # If mouse button is clicked (ONCE)
            if math.sqrt(sqx + sqy) < 75:
                if(playing): # If music is playing
                    playing = False 
                    pygame.mixer.music.pause() # Pause the music
                    print('off') # Print to the console
                else:
                    playing = True
                    pygame.mixer.music.unpause() # Otherwise, play the music
                    print('on')
            elif math.sqrt(sqx2+sqy2) < 60: # If mouse is over file button
                root = Tk()
                pygame.mixer.music.stop()
                item = filedialog.askopenfilename(title="Select a Music File",filetypes=[(".WAV Files",'*.wav')]) # Prompt for .WAV file
                
                root.destroy()
                if(item != ''): # This prevents an error if no file is selected
                    time_series, sample_rate = librosa.load(item)  # getting information from the file

                    # Update variables for the audio bar
                    # getting a matrix which contains amplitude values according to frequency and time indexes
                    stft = np.abs(librosa.stft(time_series, hop_length=512, n_fft=2048*4))
                    spectrogram = librosa.amplitude_to_db(stft, ref=np.max)  # converting the matrix to decibel matrix
                    frequencies = librosa.core.fft_frequencies(n_fft=2048*4)  # getting an array of frequencies
                    times = librosa.core.frames_to_time(np.arange(spectrogram.shape[1]), sr=sample_rate, hop_length=512, n_fft=2048*4)
                    time_index_ratio = len(times)/times[len(times) - 1]
                    frequencies_index_ratio = len(frequencies)/frequencies[len(frequencies)-1]
       
                    pygame.mixer.music.load(item)
                    pygame.mixer.music.play()
                    
                
                text = myFont.render('Now Playing: ' + os.path.basename(item),True,text_color) # Change text to the file name
                
            elif math.sqrt(sqx3 + sqy3) < colorWheelRadius: # If over color wheel
                try:
                    root2 = Tk()
                    bar_color = color()
                    root2.destroy()
                except Exception:
                    print(Exception)
            else:
                background_color = get_background_color(background_color)
                text_color = get_text_color(background_color)
                


    # Fill the background with black
    screen.fill((0, 0, 0))
    #screen.fill(background_color)
    
    # Math for calculating circle/button areas
    pygame.draw.circle(screen,(0,0,0),[420,150],50) 
    sqx2 = (x - 420)**2
    sqy2 = (y - 150)**2

    # screen.blit adds images and text to the screen at the specified x/y values.
    # (0,0) is top left of the window
    screen.blit(playPauseImage,(150,50))
    screen.blit(folderImage,(360,100))
    screen.blit(text,(20,270))

    sqx3 = (x - 90)**2
    sqy3 = (y - 150)**2
    colorWheel = pygame.image.load('colorWheel.png')
    screen.blit(colorWheel,(15,97))

    # Update the visualizer bars
    # Mostly from Medium article, we added the color changer.
    for b in bars:
        b.update(deltaTime, get_decibel(pygame.mixer.music.get_pos()/1000.0, b.freq),bar_color)
        b.render(screen)

    
    pygame.display.flip() # Flip display (update)
    


pygame.quit() # Quit
