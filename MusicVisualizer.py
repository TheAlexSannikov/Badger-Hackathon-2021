import librosa
import numpy as np
import pygame
import math
import tkinter as tk
from tkinter import filedialog
from tkinter import colorchooser

import os

playing = True


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

    #modified to include color update
    def update(self, dt, decibel,color):
        self.color = color
        desired_height = decibel * self.__decibel_height_ratio + self.max_height
        speed = (desired_height - self.height)/0.1
        self.height += speed * dt
        self.height = clamp(self.min_height, self.max_height, self.height)

    def render(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y + self.max_height - self.height, self.width, self.height))


filename = "Alan Walker - Force [NCS Release].wav"
filePath = filedialog.askopenfilename(title="Select a Music File",filetypes=[(".WAV Files",'*.wav')])


#color wheel
bar_color = (71, 159, 161)
colorWheelRadius = 50

def color() :
    try:
        new_color = colorchooser.askcolor()[1]
        print("" + new_color) #seems to fix crash
        return new_color
    except Exception:
        return bar_color

#background color stuff
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
    if background_color == black: return white
    elif background_color == white: return red
    elif background_color == red: return orange
    elif background_color == orange: return yellow 
    elif background_color == yellow: return green 
    elif background_color == green: return blue 
    elif background_color == indigo: return violet
    else: return black

def get_text_color(background_color):
    return (255-background_color[0],255-background_color[1],255-background_color[2])

background_color = (0,0,0)
text_color = get_background_color(background_color)



time_series, sample_rate = librosa.load(filePath)  # getting information from the file

# getting a matrix which contains amplitude values according to frequency and time indexes
stft = np.abs(librosa.stft(time_series, hop_length=512, n_fft=2048*4))
spectrogram = librosa.amplitude_to_db(stft, ref=np.max)  # converting the matrix to decibel matrix
frequencies = librosa.core.fft_frequencies(n_fft=2048*4)  # getting an array of frequencies

# getting an array of time periodic
times = librosa.core.frames_to_time(np.arange(spectrogram.shape[1]), sr=sample_rate, hop_length=512, n_fft=2048*4)
time_index_ratio = len(times)/times[len(times) - 1]
frequencies_index_ratio = len(frequencies)/frequencies[len(frequencies)-1]


def get_decibel(target_time, freq):
    return spectrogram[int(freq * frequencies_index_ratio)][int(target_time * time_index_ratio)]



icon = pygame.image.load("icon.png")

pygame.init()
pygame.display.set_caption("Music Visualizer")
pygame.display.set_icon(icon)



infoObject = pygame.display.Info()


screen_w = int(infoObject.current_w/2.5)
screen_h = int(infoObject.current_w/2.5)



    


# Set up the drawing window
screen = pygame.display.set_mode([screen_w, screen_h])



bars = []


frequencies = np.arange(100, 8000, 100)

r = len(frequencies)


width = screen_w/r


x = (screen_w - width*r)/2

for c in frequencies:
    bars.append(AudioBar(x, 300, c, (71, 159, 161), max_height=250, width=width))
    x += width

t = pygame.time.get_ticks()
getTicksLastFrame = t

pygame.mixer.music.load(filePath)
pygame.mixer.music.play(0)
pygame.mixer.music.set_volume(0.05)


myFont = pygame.font.SysFont('Courier New',20)
# text = myFont.render('Now Playing: ' + os.path.basename(filePath),True,text_color) #moved in while loop

playPauseImage = pygame.image.load('playpause2.png')
folderImage = pygame.image.load('folder2.png')



songName = ''
# Run until the user asks to quit
running = True
while running:

    text = myFont.render('Now Playing: ' + os.path.basename(filePath),True,text_color)
    
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
        if event.type == pygame.MOUSEBUTTONDOWN:
            #check if pause/play was clicked
            if math.sqrt(sqx + sqy) < 75:
                if(playing):
                    playing = False
                    pygame.mixer.music.pause()
                    print('off')
                else:
                    playing = True
                    pygame.mixer.music.unpause()
                    print('on')
            #check if folder was clicked
            elif math.sqrt(sqx2+sqy2) < 60:
                pygame.mixer.music.stop()
                item = filedialog.askopenfilename(title="Select a Music File",filetypes=[(".WAV Files",'*.wav')])
                if(item != ''):
                    songName = os.path.basename(item)
                    time_series, sample_rate = librosa.load(item)  # getting information from the file

                    # getting a matrix which contains amplitude values according to frequency and time indexes
                    stft = np.abs(librosa.stft(time_series, hop_length=512, n_fft=2048*4))
                    spectrogram = librosa.amplitude_to_db(stft, ref=np.max)  # converting the matrix to decibel matrix
                    frequencies = librosa.core.fft_frequencies(n_fft=2048*4)  # getting an array of frequencies
                    pygame.mixer.music.load(item)
                    pygame.mixer.music.play()
                
                text = myFont.render('Now Playing: ' + songName,True,(255,255,255))
            #check if color wheel was clicked
            elif math.sqrt(sqx3 + sqy3) < colorWheelRadius:
                try:
                    bar_color = color()
                except Exception:
                    print(Exception)
            #if nothing else is clicked, toggle through background colors
            else:
                background_color = get_background_color(background_color)
                text_color = get_text_color(background_color)
                

    # Fill the background
    screen.fill(background_color)

    #folder icon stuff
    pygame.draw.circle(screen,(0,0,0),[420,150],50)  
    sqx2 = (x - 420)**2
    sqy2 = (y - 150)**2
    
    #render things
    screen.blit(playPauseImage,(150,50))
    screen.blit(folderImage,(360,100))
    screen.blit(text,(20,270))

    #render color wheel
    sqx3 = (x - 90)**2
    sqy3 = (y - 150)**2
    colorWheel = pygame.image.load('colorWheel.png')
    screen.blit(colorWheel,(15,97))

    #update bars throughout song
    for b in bars:
        b.update(deltaTime, get_decibel(pygame.mixer.music.get_pos()/1000.0, b.freq),bar_color)
        b.render(screen)

    # Flip the display
    pygame.display.flip()
    


# Done! Time to quit.
pygame.quit()
