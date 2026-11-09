import math
from PIL import Image
# import cmath

maxIt = 0
var = 2

# def isPartOld(c):
#     # the formula, just as a reminder: z[i+1] = z[i]**2 + c
#     z = complex(0,0)
#     zp = complex(0,0)
#     It = 0
#     maxIt = 15
#     numLim = 1e15 # z[0] < numLim and z[1] < numLim and
#     while abs(z) >= abs(zp) and It < maxIt:
#         zp = z
#         try: z = z**4 + c
#         except: return False

#         try: abs(z)
#         except: return False
#         It += 1
#     if It < maxIt:
#         return True
#     else:
#         return False

def isPart(c):
    z = complex(0,0)
    zp = complex(0,0)
    It = 0
    numLim = 3 # z[0] < numLim and z[1] < numLim and
    while abs(z) <= numLim and It < maxIt:
        zp = z
        try: z = complex(math.sin(z.imag), math.cos(z.real))**var - c
        except: return 0

        try: abs(z)
        except: return 0
        It += 1
    if It < maxIt:
        return It/maxIt
    else:
        return 0

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
maxIt = int(input("Input max amount of iterations: "))
var = float(input("Choose the variable inside the function: "))
zoom = float(input("Desired zoom (2.0 to see all): "))
offsetIn = input("Desired offset (as 'off_re,off_im'): ").split(",")
colorsIn = input("Colored(1) or B&W(0)?: ")
colorMode = int(colorsIn)
offset = [float(offsetIn[0]), float(offsetIn[1])]

checkpoints = [True, False, False, False, False, False, False, False, False, False]

i = 0
k = 0

# input(complex(((3*(i - res[0]/2)/res[0]) + offset[0])*zoom, ((3*(k - res[1]/2)/res[1]) - offset[1])*zoom))

while k < res[1]:
    while i < res[0]:
        # if isPart(complex((3*(i - res[0]/2)/res[0]/2)*zoom, (3*(k - res[1]/2)/res[1]/2)*zoom)) == True:
        #     img.putpixel((i, k), (255,255,255))
        # mand = mandGrowth(complex(((3*(i - res[0]/2)/res[0]/2) + offset[0])*zoom, ((3*(k - res[1]/2)/res[1]/2) - offset[1])*zoom))
        result = isPart(complex(((3*(i - res[0]/2)/res[0])/zoom) + offset[0], ((3*(k - res[1]/2)/res[1])/zoom) - offset[1]))
        if colorMode == 0:
            img.putpixel((i, k), (int(255*result),int(255*result),int(255*result)))
        elif colorMode == 1:
            img.putpixel((i, k), colorPhase(result))
        i += 1
    k += 1
    i = 0
    if k/res[0] > 0.1 and checkpoints[1] == False:
        print("10%")
        checkpoints[1] = True
    elif k/res[0] > 0.2 and checkpoints[2] == False:
        print("20%")
        checkpoints[2] = True
    elif k/res[0] > 0.3 and checkpoints[3] == False:
        print("30%")
        checkpoints[3] = True
    elif k/res[0] > 0.4 and checkpoints[4] == False:
        print("40%")
        checkpoints[4] = True
    elif k/res[0] > 0.5 and checkpoints[5] == False:
        print("50%")
        checkpoints[5] = True
    elif k/res[0] > 0.6 and checkpoints[6] == False:
        print("60%")
        checkpoints[6] = True
    elif k/res[0] > 0.7 and checkpoints[7] == False:
        print("70%")
        checkpoints[7] = True
    elif k/res[0] > 0.8 and checkpoints[8] == False:
        print("80%")
        checkpoints[8] = True
    elif k/res[0] > 0.9 and checkpoints[9] == False:
        print("90%")
        checkpoints[9] = True

img.save(f"out/{res[0]}x{res[1]}, iter={maxIt}, var={var}, offset={offset}, zoom={zoom}.png")