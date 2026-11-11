import math
from PIL import Image
import cv2
import random
# import sys
import numpy
# import cmath

maxIt = [100,100]
power = [2,2]

def isPart(c):
    # the formula, just as a reminder: z[i+1] = z[i]**2 + c
    z = complex(0,0)
    zp = complex(0,0)
    It = 0
    maxIt = 15
    numLim = 1e15 # z[0] < numLim and z[1] < numLim and
    while abs(z) >= abs(zp) and It < maxIt:
        zp = z
        try: z = z**4 + c
        except: return False

        try: abs(z)
        except: return False
        It += 1
    if It < maxIt:
        return True
    else:
        return False

def mandGrowth(c, maxItG, powerG):
    # the formula, just as a reminder: z[i+1] = z[i]**2 + c
    z = complex(0,0)
    It = 0
    numLim = 3 # z[0] < numLim and z[1] < numLim and
    while abs(z) <= numLim and It < maxItG:
        try: z = z**powerG + c
        except: return -1
        try: abs(z)
        except: return -1
        It += 1
    if It < maxItG:
        return It/maxItG
    else:
        return -1

def colorPhase(a):
    b = a*7
    # print(f"b = {b}")
    if b >= 0 and b <= 1: return (int(b*255),0,0)
    elif b > 1 and b <= 2: return (255, int((b-1)*255),0)
    elif b > 2 and b <= 3: return (int(255*(1-(b-2))), 255, 0)
    elif b > 3 and b <= 4: return (0,255, int((b-3)*255))
    elif b > 4 and b <= 5: return (0, int(255*(1-(b-4))), 255)
    elif b > 5 and b <= 6: return (int((b-5)*255), 0, 255)
    elif b > 6 and b <= 7: return (255, int((b-6)*255), 255)

resIn = input("Input image resolution (as 'width,height'): ").split(",")
res = [int(resIn[0]),int(resIn[1])]
# if res[0]%2 == 0 or res[1]%2 == 0:
#     if res[0]%2 == 0:
#         res[0] = res[0] - 1
#     if res[1]%2 == 0:
#         res[1] = res[1] - 1
#     print(f"Dimensions chosen are even; substracting 1 to simplify the calculations; resulting resolution: {res[0]}x{res[1]}")

img = Image.new("RGB", (res[0], res[1]))
maxItIn = input("Input max amounts of iterations (as 'maxIt1,maxIt2'): ").split(",")
maxIt = [float(maxItIn[0]), float(maxItIn[1])]

if maxIt[0] != maxIt[1]: 
    maxItDiff = True
else: 
    maxItDiff = False

powerIn = input("Choose powers inside the function z = z^power + c (2 for the classic fractal) (as 'power1, power2'): ").split(",")
power = [float(powerIn[0]), float(powerIn[1])]

if power[0] != power[1]: 
    powerDiff = True
else: 
    powerDiff = False

# if power[0] < power[1]:
#     deltapower = abs(power[0] - power[1])
# elif power[0] > power[1]:
#     deltapower = -abs(power[0] - power[1])
zoomIn = input("Desired zooms (0.5 to see most) (as 'zoom1,zoom2'): ").split(",")
zoom = [float(zoomIn[0]), float(zoomIn[1])]

if zoom[0] != zoom[1]: 
    zoomDiff = True
else: 
    zoomDiff = False

offsetIn = input("Desired offsets (as 'off_re1,off_im1;off_re2,off_im2'): ").split(";")
offsetIn1 = offsetIn[0].split(",")
offsetIn2 = offsetIn[1].split(",")
offset = [[float(offsetIn1[0]), float(offsetIn1[1])], [float(offsetIn2[0]), float(offsetIn2[1])]]

if offset[0] != offset[1]: 
    offsetDiff = True
else: 
    offsetDiff = False

colorsIn = input("Colored(1) or B&W(0)?: ")
colorMode = int(colorsIn)
fps = int(input("FPS of the final video: "))
vidLength = int(input("Video length (in frames): "))
# dpower = deltapower/vidLength
randomIndex = random.randint(0,4800)

if zoomDiff == True:
    deltaZoom = zoom[1] - zoom[0]
    dzoom = round(deltaZoom/vidLength, 2)

checkpoints = [False, False, False, False, False, False, False, False, False]

i = 0
k = 0
frameCount = 0

print("\n[MandelbrotSetAnim.py]: Starting frames render")
print("="*40)

while frameCount < vidLength:
    # powerSpec = power[0] + dpower*frameCount
    frameCount += 1

    if powerDiff == True:
        powerSpec = power[0] + (power[1] - power[0])*((frameCount - 1)/(vidLength - 1))
    else:
        powerSpec = power[0]

    if maxItDiff == True:
        maxItSpec = math.floor(maxIt[0] + (maxIt[1] - maxIt[0])*((frameCount - 1)/(vidLength - 1)))
    else:
        maxItSpec = maxIt[0]

    if zoomDiff == True:
        zoomSpec = zoom[0] + round((dzoom*(frameCount - 1))**2/deltaZoom, 2)
        # zoomSpec = zoom[0] + round((dzoom*math.sqrt(frameCount - 1)), 2)
    else:
        zoomSpec = zoom[0]

    if offsetDiff == True:
        offsetSpec = [offset[0][0] + (offset[1][0] - offset[0][0])*((frameCount - 1)/(vidLength - 1)), offset[0][1] + (offset[1][1] - offset[0][1])*((frameCount - 1)/(vidLength - 1))]
    else:
        offsetSpec = offset[0]

    print(f"vid{randomIndex}_frame{frameCount}: power = {powerSpec}, maxIt = {maxItSpec}, zoom = {zoomSpec}, offset = {offsetSpec}")    
    print("-"*30)

    while k < res[1]:
        while i < res[0]:
            mand = mandGrowth(complex(((3*(i - res[0]/2)/res[0])/zoomSpec)+offsetSpec[0], ((3*(k - res[1]/2)/res[1])/zoomSpec) - offsetSpec[1]), maxItSpec, powerSpec)
            if mand == -1:
                img.putpixel((i, k), (0,0,0))
            else:
                if colorMode == 0:
                    img.putpixel((i, k), (int(255*mand),int(255*mand),int(255*mand)))
                elif colorMode == 1:
                    img.putpixel((i, k), colorPhase(mand))
            i += 1
        k += 1
        i = 0

        if k/res[0] > 0.1 and checkpoints[0] == False:
            print(f"frame {frameCount}/{vidLength} - 10%")
            checkpoints[0] = True
        elif k/res[0] > 0.2 and checkpoints[1] == False:
            print(f"frame {frameCount}/{vidLength} - 20%")
            checkpoints[1] = True
        elif k/res[0] > 0.3 and checkpoints[2] == False:
            print(f"frame {frameCount}/{vidLength} - 30%")
            checkpoints[2] = True
        elif k/res[0] > 0.4 and checkpoints[3] == False:
            print(f"frame {frameCount}/{vidLength} - 40%")
            checkpoints[3] = True
        elif k/res[0] > 0.5 and checkpoints[4] == False:
            print(f"frame {frameCount}/{vidLength} - 50%")
            checkpoints[4] = True
        elif k/res[0] > 0.6 and checkpoints[5] == False:
            print(f"frame {frameCount}/{vidLength} - 60%")
            checkpoints[5] = True
        elif k/res[0] > 0.7 and checkpoints[6] == False:
            print(f"frame {frameCount}/{vidLength} - 70%")
            checkpoints[6] = True
        elif k/res[0] > 0.8 and checkpoints[7] == False:
            print(f"frame {frameCount}/{vidLength} - 80%")
            checkpoints[7] = True
        elif k/res[0] > 0.9 and checkpoints[8] == False:
            print(f"frame {frameCount}/{vidLength} - 90%")
            checkpoints[8] = True

    img.save(f"out/frames/vid{randomIndex}_frame{frameCount}.png")
    print(f"frame {frameCount}/{vidLength} - 100%")
    print("-"*30)
    print("="*30)
    k = 0
    i = 0
    checkpoints = [False, False, False, False, False, False, False, False, False]

print("\n[MandelbrotSetAnim.py]: All frames rendered")

vidTitle = "_"

vidTitle += f"res{res}FPS{fps}len{vidLength}"

vidTitle += "_"


if maxItDiff == True:
    vidTitle += f"maxIt{maxIt}"
else:
    vidTitle += f"maxIt{maxIt[0]}"
if powerDiff == True:
    vidTitle += f"pow{power}"
else:
    vidTitle += f"pow{power[0]}"
if zoomDiff == True:
    vidTitle += f"zoom{zoom}"
else:
    vidTitle += f"zoom{zoom[0]}"
if offsetDiff == True:
    vidTitle += f"offs{offset}"
else:
    vidTitle += f"offs{offset[0]}"


finVid = cv2.VideoWriter("out/vid" + str(randomIndex) + vidTitle + ".mp4", cv2.VideoWriter_fourcc(*'XVID'), fps, res)
print("[MandelbrotSetAnim.py]: Compiling the video...")
while i < vidLength:
    i += 1
    frameIm = Image.open("out/frames/vid" + str(randomIndex) + "_frame" + str(i) + ".png")
    frame = numpy.asarray(frameIm)
    finVid.write(frame)

print("[MandelbrotSetAnim.py]: Video render finished")
finVid.release()