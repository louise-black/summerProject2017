import pygame
import sys

# Constants
WINDOW_WIDTH  = 1024
WINDOW_HEIGHT = 600

CRT_WIDTH  =  400
CRT_HEIGHT =  400

BIT_WIDTH    = 5
BIT_HEIGHT   = 5
BIT_SPACING  = 10
LINE_SPACING = 8
DISPLAY_REG_LINE_SPACING = 15

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
DIM_GREEN = (0, 50, 0)

# Testing
testDelayData = "DISPLAY_REG 10000000000000000000000000000000  00000000000000000000000000000000  00000000000000000000000000000000  00000000000000000000000000000000  00000000000000000000000000000000 00000000000000000000000000000000 00000000000000000000000000000000 00000000000000000000000000000000  00000000000000000000000000000000 00000000000000000000000000000000 00000000000000000000000000000000 00000000000000000000000000000000  00000000000000000000000000000000 00000000000000000000000000000000  00000000000000000000000000000000 00000000000000000000000000000000  00000000000000000000000000000000 00000000000000000000000000000000\nDISPLAY_DL 1 01001101110110000000000000000001 00000000000000000000000000000000 01001101110011000000000000000001 00000000000000000000000000000000 01001011001110000000000000000001 00000000000000000000000000000000 01001101111110000000000000000001 00000000000000000000000000000000 01001101100001000000000000000001 00000000000000000000000000000000 01000000110111000000000000000001 01001111110111000000000000000000 01000111010110000000000000000001 00000000000000000000000000000000 01001111010011000000000000000001 00000000000000000000000000000000 01001011011110000000000000000001 00000000000000000000000000000000 01000000110011000000000000000001 00000000000000000000000000000000 01001011000001000000000000000001 00000000000000000000000000000000 01001011011011000000000000100101 00000000000000000000000000000000 00000000000000000000000000000000 00000000000000000000000000000000 00000000000000000000000000000000 00000000000000000000000000000000 00000000000000000000000000000000 00000000000000000000000000000000 00000000000000000000000000000000 00000000000000000000000000000000"

# Functions
def drawWord(canvas, word, x, y):
    data = map(int,word)
    for n in range(0,31):
        for i in data:
            if i == 1:
                pygame.draw.line(canvas, GREEN, (x, y), (x + BIT_WIDTH, y), BIT_HEIGHT)
            elif i == 0:
                pygame.draw.line(canvas, DIM_GREEN, (x, y), (x + BIT_WIDTH, y), BIT_HEIGHT)
            x += BIT_SPACING

def drawDelayLine(canvas, delayLineData):
    y = 5 # Start in from the edge
    for data in delayLineData:
        x = 5 # Start in from the edge
        drawWord(canvas, data, x, y)
        y += LINE_SPACING

def drawDisplayReg(canvas, displayRegData):
    y = 5 #Start in from the edge
    i = 1
    # 4 x 1 line
    # 3 x 2 lines
    # 2 x 4 lines
    lineSpaces = [1,2,3,4,6,8,10,14]
    for data in displayRegData:
        x = 5
        drawWord(canvas, data, x, y)
        if i in lineSpaces:
            y += DISPLAY_REG_LINE_SPACING
        else:
            y += BIT_HEIGHT
        i += 1

# Initialise Pygame
pygame.init()
canvas = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN)

if len(sys.argv) != 2:
    print ("Usuage display.py <dataFile>")
    exit(-1)
else:
    dataFile = sys.argv[1]

displayRegSurface  = pygame.Surface((CRT_WIDTH, CRT_HEIGHT))
displayLineSurface = pygame.Surface((CRT_WIDTH, CRT_HEIGHT))

while True:
    with open(dataFile, 'r') as f:
        selectedDL = 1
        for line in f.readlines():
            dataPoints = line.split()
            #FIXME: Add error checking
            if len(dataPoints) > 0:
                if dataPoints[0] == "DISPLAY_DL_SEL":
                    selectedDL = dataPoints[1]

                if dataPoints[0] == "DISPLAY_REG":
                    displayRegData = dataPoints[1:]

                if dataPoints[0] == "DISPLAY_DL":
                    num = dataPoints[1]
                    if num == selectedDL:
                        delayLineData = dataPoints[2:]


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(-1)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit(-1)

    canvas.fill(BLACK)

    drawDisplayReg(displayRegSurface, displayRegData)
    drawDelayLine(displayLineSurface, delayLineData)

    canvas.blit(displayRegSurface,  (20, 20, 500, 500))
    canvas.blit(displayLineSurface, (600, 20, 1000, 500))

    pygame.display.flip()
