from PIL import Image
import sys
import math
import numpy as np

'''
dda_setup function: 
    inputs: two endpoints a and b, and the dimension that we are scanning
    output: a 10-dimensional vertex (x,y,z,w,r,g,b,a,s,t) that describes the 
            step distance in the dimension we are in
'''
def dda_setup(a, b, dimension):
    if(dimension == "x"):   
        d = 0 
    else:
        d = 1

    if(a[d] == b[d]):
        if(dimension == "x"):
            return [0,0,0,0,0,0,0,0,0,0]
        return [0,0,0,0,0,0,0,0,0,0]
    
    elif(a[d] > b[d]): # swap a and b
        # print("a, b:", a,b)
        temp = a
        a = b
        b = temp

        # print("a, b:", a,b)

    pointDiff = []

    for i in range(10):
        pointDiff += [b[i] - a[i]]



    # print("colorDiff: ", colorDiff, " b_rgba: ", b_rgba, " a_rgba: ", a_rgba)

    s = []
    for p_coord in pointDiff:
        s.append(p_coord/(b[d] - a[d])) # s is now ([] of 10)/dimensional diff
    

    # print("s: ", s)

    return s # s should be [] of size 10


'''
dda_firstPoint function: 
    inputs: two endpoints a and b, and the dimension that we are scanning
    output: a 10-dimensional vertex (x,y,z,w,r,g,b,a,s,t) that describes
            the first potential point; accounts for next integer offset
'''
def dda_firstPoint(a, b, dimension):
    if(dimension == "x"):
        d = 0 
    else:
        d = 1
    
    s = dda_setup(a, b, dimension)
    if(a[d] > b[d]): # swap a and b
        temp = a
        a = b
        b = temp
    # print("s: ", s)
    
    o = []
    p = []
   
    # print("o, s:", o, s)
    e = math.ceil(a[d]) - a[d] # calculates distance between a_d and next integer
    # print("e: ", e)
    for i in range(10):
        o.append(s[i]*e) # o is of distance e and obtains the direction of s vector
        p += [a[i] + o[i]]

    # print("p: ",p)
    return p

'''
dda_allPoints function: 
    inputs: two endpoints a and b, and the dimension that we are scanning
    output: returns all of the 10-dimensional vertices with integer coordinates
            between endpoints a and b along the dimension we are scanning
'''
def dda_allPoints(a, b, dimension):
    all_p = []
    # print("dimensions", dimension)
    p = dda_firstPoint(a, b, dimension)
    
    # print("p: ", p)

    if(dimension == "x"):
        d = 0 
    else:
        d = 1
    
    s = dda_setup(a, b, dimension)
    if(a[d] > b[d]): # swap a and b
        temp = a
        a = b
        b = temp

    while p[d] < b[d]:
        all_p.append(p.copy())
       
        for i in range(10):
            p[i] += s[i]
            # print("p[i]: ", p[i], "s[i]: ", s[i])
    # print("all_p,dimension", all_p,dimension)
    return all_p

'''
scanline_algo function: 
    inputs: three 10-dimensional vertices x,y,z in the form of (x,y,z,w,r,g,b,a,s,t)
            representing the info of points of a triangle
    output: returns all of the 10-dimensional vertices with integer coordinates
            within the triangle bounded by points x,y,z
'''
def scanline_algo(x, y, z):
    t = None
    b = None
    m = None
    trianglePoints = [x, y, z]
    # print("triangle points: ", trianglePoints)
    y_points = [x[1], y[1], z[1]]

    
    
    for i in range(3):
        if(min(y_points) == y_points[i] and t == None):
            t = trianglePoints[i]

        elif(max(y_points) == y_points[i] and b == None):
            b = trianglePoints[i]

        else:
            m = trianglePoints[i]

    # print("t, b, m: ", t, b, m)

    # step 4
    s_long = dda_setup(t, b, "y")   # setup for long edge
    if(s_long == []):
        return
    p_long = dda_firstPoint(t, b, "y")
    # print("p_long: ", p_long)
    
    # find points in top half of triangle
    # step 5
    s = dda_setup(t, m, "y")
    p = dda_firstPoint(t, m , "y")

    # step 6
    points = []
    while p[1] < m[1]:
        points += dda_allPoints(p, p_long, "x")
        # print("points: ", points)
        for i in range(10):
            p[i] += s[i]
            p_long[i] += s_long[i]

    # find points in bottom half of triangle
    # step 7
    s = dda_setup(m, b, "y")
    p = dda_firstPoint(m, b, "y")

    # step 8
    while p[1] < b[1]:
        points += dda_allPoints(p, p_long, "x")
        
        for i in range(10):
            p[i] += s[i]
            p_long[i] += s_long[i]

    return points

'''
mult_matrix helper function: 
    inputs: matrices a and b
    output: returns the product of matrices a and b
'''
def mult_matrix(a, b):
    rows_a, cols_a = len(a), len(a[0])
    rows_b, cols_b = len(b), len(b[0])

    result = [[0 for _ in range(cols_b)] for _ in range(rows_a)]

    for i in range(rows_a):
        for j in range(cols_b):
            for k in range(cols_a):
                result[i][j] += a[i][k] * b[k][j]

    return result

'''
srgbToLinear helper function: 
    inputs: the sRGB values that need to be converted into linear
    output: the linear values of the sRGB version passed in
'''
def srgbToLinear(sRGB):
    for i in range(3):
        if(sRGB[i] <= 1 and sRGB[i] >= 0):
            if(sRGB[i] <= 0.04045):
                sRGB[i] /= 12.92
            else:
                sRGB[i] = ((sRGB[i] + 0.055)/1.055)**2.4
        if sRGB[i] > 1:
            sRGB[i] = 1
        elif sRGB[i] < 0:
            sRGB[i] = 0
    
    return sRGB

'''
linearToSRGB helper function: 
    inputs: the linear values that need to be converted into sRGB
    output: the sRGB values of the linear version passed in
'''
def linearToSRGB(linear):
    for i in range(3):
        if(linear[i] <= 1 and linear[i] >= 0):
            if(linear[i] <= 0.0031308):
                linear[i] *= 12.92
            else:
                linear[i] = 1.055*linear[i]**(1/2.4) - 0.055
        if linear[i] > 1:
            linear[i] = 1
        elif linear[i] < 0:
            linear[i] = 0
    
    return linear
        


# ((x/w+1)*width/2, (y/w+1)*height/2)
# width = 20
# height = 30

# a = [(-1/4+1)*width/2, (-2/4+1)*height/2]
# b = [(1/4+1)*width/2, (3.5/4+1)*height/2]
# c = [(2/2+1)*width/2, (0/2+1)*height/2]
# print("a,b,c: ",a,b,c)

# a_rgba = [1,1,1,1]
# b_rgba = [1,1,1,1]
# c_rgba = [0,0,0,1]

# # p = dda_firstPoint(a, b, "y")
# # print(dda_allPoints(a, b, "y", a_rgba, b_rgba))
# print(scanline_algo(a,b,c, a_rgba, b_rgba, c_rgba))

existingPos = None

# flags for elective attributes
depth = False
sRGB = False
hyp = False
uniform = False
texture = False
color = False
pointSize = False

currPixels = []

def drawPixels():
    pointsToDraw = []
    pixelsToDraw = []

    for j in range(3):
        x = positionsToDraw[j][0]
        y = positionsToDraw[j][1]
        z = positionsToDraw[j][2]
        w = positionsToDraw[j][3]

        # print("old xyzw: ", x,y,z,w)
        
        posMatrix = [[x],[y],[z],[w]]
        productMatrix = []

        if uniform:
            productMatrix = mult_matrix(uniformMatrix, posMatrix)
            x = productMatrix[0][0]
            y = productMatrix[1][0]
            z = productMatrix[2][0]
            w = productMatrix[3][0]
                
            # print("new xyzw: ", x,y,z,w)

        pointsToDraw.append([(x/w+1)*width/2, (y/w+1)*height/2, z/w, 1/w])

    # print("positionsToDraw: ", positionsToDraw)
    # print("pointsToDraw: ", pointsToDraw)
    # print("colorsToDraw: ", colorsToDraw, " original w: ", w)

    a = pointsToDraw[0]
    b = pointsToDraw[1]
    c = pointsToDraw[2]

    a_rgba = []
    b_rgba = []
    c_rgba = []

    a_st = []
    b_st = []
    c_st = []

    if hyp:
        if texture:
            for i in range(2):
                a_st += [texelsToDraw[0][i]/(1/a[3])]
                b_st += [texelsToDraw[1][i]/(1/b[3])]
                c_st += [texelsToDraw[2][i]/(1/c[3])]
        else:
            a_st = [0,0]
            b_st = [0,0]
            c_st = [0,0]
        
        if color:
            for i in range(3): # divides each point's rgb value by its respective w
                a_rgba += [colorsToDraw[0][i]/(1/a[3])] 
                b_rgba += [colorsToDraw[1][i]/(1/b[3])]
                c_rgba += [colorsToDraw[2][i]/(1/c[3])]
            a_rgba += [colorsToDraw[0][3]]
            b_rgba += [colorsToDraw[1][3]]
            c_rgba += [colorsToDraw[2][3]]
        else:
            a_rgba = [0,0,0,0]
            b_rgba = [0,0,0,0]
            c_rgba = [0,0,0,0]

    else:
        if texture:
            a_st += texelsToDraw[0]
            b_st += texelsToDraw[1]
            c_st += texelsToDraw[2]
        else:
            a_st = [0,0]
            b_st = [0,0]
            c_st = [0,0]
        
        if color:
            a_rgba = colorsToDraw[0]
            b_rgba = colorsToDraw[1]
            c_rgba = colorsToDraw[2]
        else:
            a_rgba = [0,0,0,0]
            b_rgba = [0,0,0,0]
            c_rgba = [0,0,0,0]

    a += a_rgba + a_st
    b += b_rgba + b_st
    c += c_rgba + c_st

    # print("new colorsToDraw: ", a_rgba, b_rgba, c_rgba)

    pixelsToDraw += scanline_algo(a, b, c)
    # print("all pixelsToDraw: ", pixelsToDraw)

    for pixel in pixelsToDraw:
        x = pixel[0]
        y = pixel[1]
        z = pixel[2]
        w = pixel[3]

        vertColor = pixel[4:8]

        s = pixel[8]
        t = pixel[9]

        # print("s,t: ", s,t)
        if texture:
            s /= w
            t /= w

            # handle wrap coordinates
            while s > 1:
                s -= 1
            while s < 0:
                s += 1

            while t > 1:
                t -= 1
            while t < 0:
                t += 1

            texel = (s*textureWidth, t*textureHeight) # need to scale texel coord to texture png dimensions
            # print("textureWidth, textureHeight, texel: ", textureWidth, textureHeight, texel)
            textureRGBA = list(texturePNG.getpixel(texel))  # get the rgba value at the texel coord in texture image
            # print("textureRGBA: ", textureRGBA)
            for i in range(len(textureRGBA)):
                textureRGBA[i] /= 255.0
            if len(textureRGBA) == 3:
                textureRGBA += [1.0]
            
            textureRGBA = srgbToLinear(textureRGBA)
        # print("new w: ", w)
        # print("rgb without w division: ", pixel[4:8])
        if color:
            for i in range(3):
                if hyp:
                    vertColor[i] /= w # divide rgb by interpolated 1/w
        
        finalColor = []
        if texture and color:
            for i in range(3):
                finalColor += [textureRGBA[i]*textureRGBA[3] + vertColor[i]*(1-textureRGBA[3])]   # including vertex color underneath transparent texture
            finalColor += [textureRGBA[3] + vertColor[3] - (textureRGBA[3]*vertColor[3])]
        elif texture:
            finalColor = textureRGBA
        elif color:
            finalColor = vertColor
        
        if sRGB:
            if texture:
                textureRGBA = linearToSRGB(textureRGBA)
            if color:
                vertColor = linearToSRGB(vertColor)
        # print("new color rgb: ", pixel[4:7])

        if(-width < x < width and -height < y < height):
            existingPos = [pix for pix in currPixels if pix[:2] == [x,y]]
            # print("existingPos: ", existingPos)

            if(existingPos):
                if(existingPos[0][2] >= z):
                    d_rgba = srgbToLinear(existingPos[0][4:8])
                    s_rgba = srgbToLinear(finalColor)
                    new_rgba = []

                    new_a = s_rgba[3] + d_rgba[3]*(1 - s_rgba[3])
                    # print("s_rgba[3], d_rgba[3]: ", s_rgba[3]*255, d_rgba[3]*255)
                    # print("new_a: ", new_a*255)

                    for i in range(3):
                        new_rgba += [(s_rgba[3]/new_a)*s_rgba[i] + (((1 - s_rgba[3])*d_rgba[3])/new_a)*d_rgba[i]]
                        # print("(s_rgba[3]/new_a)*s_rgba[i]: ", (s_rgba[3]/new_a)*s_rgba[i])
                    
                    new_rgba += [new_a]

                    new_rgba = linearToSRGB(new_rgba)
                    # print("new_rgba: ", new_rgba[0]*255,new_rgba[1]*255,new_rgba[2]*255,new_rgba[3]*255)
                    
                    r = new_rgba[0]
                    g = new_rgba[1]
                    b = new_rgba[2]
                    a = new_rgba[3]

                    currPixels.remove(existingPos[0])
                    image.putpixel((int(x),int(y)), (int(r*255),int(g*255),int(b*255),int(a*255)))
                    currPixels.append([x,y,z,w,r,g,b,a])

            else:
                r = finalColor[0]
                g = finalColor[1]
                b = finalColor[2]
                a = finalColor[3]
                image.putpixel((int(x),int(y)), (int(r*255),int(g*255),int(b*255),int(a*255)))
                # print("put down pixel xyrgba: ", x,y,r,g,b,a)
                currPixels.append([x,y,z,w,r,g,b,a])
    # print("pixelsToDraw: ", pixelsToDraw)

'''
Parses through filename found from run command argument and reads through the file
line by line. Detects any keywords and performs specific logic exclusive to the keyword's
functionality/purpose
'''
with open(sys.argv[1], 'r') as filename:
    fileContents = filename.readlines()
    for line in fileContents:
        if line.find(".png") != -1: # check to see if .png is in this line
            if line.find("texture ") != -1:
                texture = True
                for word in line.split():
                    if ".png" in word:  # check to see if word in line ends with .png
                        texturePNG = Image.open(word)
                        textureWidth, textureHeight = texturePNG.size
                        # texturePNG.show()
                        # print("texturePNG: ", word)
                        line = line.replace(word, '')
                line = line.replace("png", '')
            else:
                for word in line.split():
                    if ".png" in word:  # check to see if word in line ends with .png
                        pngName = word
                        line = line.replace(word, '')
                line = line.replace("png", '')
                width, height = (int(i) for i in line.split())
                image = Image.new("RGBA", (width, height), (0,0,0,0))
                # print(width, height)
        
        elif line.find("texcoord") != -1:
            texelCoords = []
            floatsString = line.split()[2:]
            
            floats = [float(num) for num in floatsString]
            print("floats: ", floats)

            for i in range(0, len(floats), 2):
                texel = [floats[i], floats[i+1]] 
                texelCoords.append(texel)
            print("texelCoords: ", texelCoords) 
            # print("colors", colors)

        elif line.find("depth") != -1:    
            depth = True
        
        elif line.find("sRGB") != -1:
            sRGB = True

        elif line.find("hyp") != -1:
            hyp = True

        elif line.find("uniformMatrix") != -1:
            uniform = True
            uniformMatrix = []
            uniformRow = []
            floatsString = line.split()[1:] # stores all elements of uniformMatrix from file

            floats = [float(num) for num in floatsString]

            print("floats for uniform: ", floats)

            floatIndex = 0

            for i in range(4):
                for j in range(4):
                    uniformRow += [floats[i + j*4]]
                uniformMatrix.append(uniformRow)
                uniformRow = []

            print("uniformMatrix: ", uniformMatrix)
        
        elif line.find("pointsize") != -1:
            pointSize = True
            pointSizes = []
            floatsString = line.split()[2:] # stores all point sizes 

            floats = [float(num) for num in floatsString]

            for num in floats:
                pointSizes.append(num)

            print("pointSizes: ", pointSizes)

        elif line.startswith("position"):
            positions = []
            coordSize = int(line.split()[1]) # stores the size of the coordinates
            floatsString = line.split()[2:]

            # print("coordSize: ", coordSize)
            
            floats = [float(num) for num in floatsString]
            # print("floats for position: ", floats)

            if coordSize == 2:
                for i in range(0, len(floats), 2):
                    coordXYZW = floats[i:i+2] + [0.0, 1.0]
                    positions.append(coordXYZW)
            elif coordSize == 3:
                for i in range(0, len(floats), 3):
                    coordXYZW = floats[i:i+3] + [1.0]
                    positions.append(coordXYZW)
            elif coordSize == 4:
                for i in range(0, len(floats), 4):
                    coordXYZW = floats[i:i+4]
                    positions.append(coordXYZW)
            
            print("positions: ", positions)

        elif line.find("color") != -1:
            color = True
            colors = []
            colorSize = int(line.split()[1])
            floatsString = line.split()[2:]
            
            floats = [float(num) for num in floatsString]
            # print("floats for color: ", floats)

            if colorSize == 3:
                for i in range(0, len(floats), 3):
                    coordRGBA = floats[i:i+3] + [1.0]
                    colors.append(coordRGBA)
            elif colorSize == 4:
                for i in range(0, len(floats), 4):
                    coordRGBA = floats[i:i+4]
                    colors.append(coordRGBA)

            print("colors", colors)

        elif line.find("drawArraysTriangles") != -1:
            first = int(line.split()[1]) # stores the size of the color
            count = int(line.split()[2])

            positionsToDraw = []
            texelsToDraw = []
            colorsToDraw = []
            
            for i in range(0, count, 3):
                positionsToDraw = [positions[first + i], positions[first + i + 1], positions[first + i + 2]]
                if texture:
                    texelsToDraw = [texelCoords[first + i], texelCoords[first + i + 1], texelCoords[first + i + 2]]
                if color:
                    colorsToDraw = [colors[first + i], colors[first + i + 1], colors[first + i + 2]]

                print("texelsToDraw: ", texelsToDraw)
                drawPixels()
                

        elif line.find("elements") != -1:
            intString = line.split()[1:]
            
            elements = [int(num) for num in intString]

            # print("elements: ", elements)

        elif line.find("drawElementsTriangles") != -1:
            count = int(line.split()[1]) # stores how many triangles
            offset = int(line.split()[2])

            positionsToDraw = []
            texelsToDraw = []
            colorsToDraw = []

            for i in range(0, count, 3):
                positionsToDraw = [positions[elements[offset + i]], positions[elements[offset + i + 1]], positions[elements[offset + i + 2]]]
                if texture:
                    texelsToDraw = [texelCoords[elements[offset + i]], texelCoords[elements[offset + i + 1]], texelCoords[elements[offset + i + 2]]]
                if color:
                    colorsToDraw = [colors[elements[offset + i]], colors[elements[offset + i + 1]], colors[elements[offset + i + 2]]]

                print("texelsToDraw: ", texelsToDraw)
                
                drawPixels()
        
        elif line.find("drawArraysPoints") != -1:
            first = int(line.split()[1]) # stores the size of the color
            count = int(line.split()[2])

            positionsToDraw = []
            texelsToDraw = []
            colorsToDraw = []
            
            for i in range(0, count):
                radius = pointSizes[first + i]/2

                topPoint = [positions[first + i][0], positions[first + i][1] + radius, positions[first + i][2:]]
                bottomPoint = [positions[first + i][0], positions[first + i][1] - radius, positions[first + i][2:]]
                leftPoint = [positions[first + i][0] - radius, positions[first + i][1], positions[first + i][2:]]
                rightPoint = [positions[first + i][0] + radius, positions[first + i][1], positions[first + i][2:]]

                positionsToDraw = [leftPoint, topPoint, rightPoint] # draw top half of triangle
                if texture:
                    texelsToDraw = [texelCoords[first + i], texelCoords[first + i], texelCoords[first + i]]
                if color:
                    colorsToDraw = [colors[first + i], colors[first + i], colors[first + i]]

                drawPixels()

                positionsToDraw = [leftPoint, bottomPoint, rightPoint] # draw bottom half of triangle to complete the square
                drawPixels()

            
        
         
                
image.save(pngName, "PNG")
# ...