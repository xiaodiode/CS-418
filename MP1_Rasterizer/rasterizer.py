from PIL import Image
import sys
import math
import numpy as np

def dda_setup(a, b, dimension, a_rgba, b_rgba):
    if(dimension == "x"):
        d = 0 
    else:
        d = 1

    if(a[d] == b[d]):
        if(dimension == "x"):
            return [0,0,0,0,0,0,0,0]
        return [0,0,0,0,0,0,0,0]
    
    elif(a[d] > b[d]): # swap a and b
        # print("a, b:", a,b)
        temp = a
        a = b
        b = temp

        temp = a_rgba
        a_rgba = b_rgba
        b_rgba = temp
        # print("a, b:", a,b)

    pointDiff = []
    colorDiff = []

    for i in range(4):
        pointDiff += [b[i] - a[i]]

    for i in range(4):
        colorDiff += [b_rgba[i] - a_rgba[i]]


    # print("colorDiff: ", colorDiff, " b_rgba: ", b_rgba, " a_rgba: ", a_rgba)

    s = []
    for p_coord in pointDiff:
        s.append(p_coord/(b[d] - a[d])) # s is now ([] of 4)/dimensional diff
    
    for c_coord in colorDiff:
        s.append(c_coord/(b[d] - a[d]))

    # print("s: ", s)

    return s # s should be [] of size 6

def dda_firstPoint(a, b, dimension, a_rgba, b_rgba):
    if(dimension == "x"):
        d = 0 
    else:
        d = 1
    
    s = dda_setup(a, b, dimension, a_rgba, b_rgba)
    if(a[d] > b[d]): # swap a and b
        temp = a
        a = b
        b = temp

        temp = a_rgba
        a_rgba = b_rgba
        b_rgba = temp
    # print("s: ", s)
    
    o = []
    p = []
   
    # print("o, s:", o, s)
    e = math.ceil(a[d]) - a[d] # calculates distance between a_d and next integer
    # print("e: ", e)
    for i in range(8):
        o.append(s[i]*e) # o is of distance e and obtains the direction of s vector
        
        if(i < 4):
            p += [a[i] + o[i]]

        else:
            p += [a_rgba[i-4] + o[i]]

    # print("p: ",p)
    return p

def dda_allPoints(a, b, dimension, a_rgba, b_rgba):
    all_p = []
    # print("dimensions", dimension)
    p = dda_firstPoint(a, b, dimension, a_rgba, b_rgba)
    
    # print("p: ", p)

    if(dimension == "x"):
        d = 0 
    else:
        d = 1
    
    s = dda_setup(a, b, dimension, a_rgba, b_rgba)
    if(a[d] > b[d]): # swap a and b
        temp = a
        a = b
        b = temp

        temp = a_rgba
        a_rgba = b_rgba
        b_rgba = temp

    while p[d] < b[d]:
        all_p.append(p.copy())
       
        for i in range(8):
            p[i] += s[i]
            # print("p[i]: ", p[i], "s[i]: ", s[i])
    # print("all_p,dimension", all_p,dimension)
    return all_p

def scanline_algo(x, y, z, x_rgba, y_rgba, z_rgba):
    t = None
    b = None
    m = None
    trianglePoints = [x, y, z]
    rgbaPoints = [x_rgba, y_rgba, z_rgba]
    # print("triangle points: ", trianglePoints)
    y_points = [x[1], y[1], z[1]]

    
    
    for i in range(3):
        if(min(y_points) == y_points[i] and t == None):
            t = trianglePoints[i]
            t_rgba= rgbaPoints[i]

        elif(max(y_points) == y_points[i] and b == None):
            b = trianglePoints[i]
            b_rgba = rgbaPoints[i]

        else:
            m = trianglePoints[i]
            m_rgba = rgbaPoints[i]

    # print("t, b, m: ", t, b, m)

    # step 4
    s_long = dda_setup(t, b, "y", t_rgba, b_rgba)   # setup for long edge
    if(s_long == []):
        return
    p_long = dda_firstPoint(t, b, "y", t_rgba, b_rgba)
    # print("p_long: ", p_long)
    
    # find points in top half of triangle
    # step 5
    s = dda_setup(t, m, "y", t_rgba, m_rgba)
    p = dda_firstPoint(t, m , "y", t_rgba, m_rgba)

    # step 6
    points = []
    while p[1] < m[1]:
        points += dda_allPoints(p[0:4], p_long[0:4], "x", p[4:], p_long[4:])
        # print("points: ", points)
        for i in range(8):
            p[i] += s[i]
            p_long[i] += s_long[i]

    # find points in bottom half of triangle
    # step 7
    s = dda_setup(m, b, "y", m_rgba, b_rgba)
    p = dda_firstPoint(m, b, "y", m_rgba, b_rgba)

    # step 8
    while p[1] < b[1]:
        points += dda_allPoints(p[0:4], p_long[0:4], "x", p[4:], p_long[4:])
        
        for i in range(8):
            p[i] += s[i]
            p_long[i] += s_long[i]

    return points

def matrix_multiply(a, b):
    rows_a, cols_a = len(a), len(a[0])
    rows_b, cols_b = len(b), len(b[0])

    if cols_a != rows_b:
        raise ValueError("Number of columns in 'a' must be equal to the number of rows in 'b'.")

    result = [[0 for _ in range(cols_b)] for _ in range(rows_a)]

    for i in range(rows_a):
        for j in range(cols_b):
            for k in range(cols_a):
                result[i][j] += a[i][k] * b[k][j]

    return result

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

depth = False
sRGB = False
hyp = False
uniform = False

currPixels = []

with open(sys.argv[1], 'r') as filename:
    fileContents = filename.readlines()
    for line in fileContents:
        if line.find(".png") != -1: # check to see if .png is in this line
            for word in line.split():
                if ".png" in word:  # check to see if word in line ends with .png
                    pngName = word
                    line = line.replace(word, '')
            line = line.replace("png", '')
            width, height = (int(i) for i in line.split())
            image = Image.new("RGBA", (width, height), (0,0,0,0))
            # print(width, height)
            
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
            colorsToDraw = []
            
            for i in range(0, count, 3):
                positionsToDraw = [positions[first + i], positions[first + i + 1], positions[first + i + 2]]
                colorsToDraw = [colors[first + i], colors[first + i + 1], colors[first + i + 2]]

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
                        productMatrix = matrix_multiply(uniformMatrix, posMatrix)
                        x = productMatrix[0][0]
                        y = productMatrix[1][0]
                        z = productMatrix[2][0]
                        w = productMatrix[3][0]
                            
                        # print("new xyzw: ", x,y,z,w)


                    pointsToDraw.append([(x/w+1)*width/2, (y/w+1)*height/2, z/w, 1/w])

                print("positionsToDraw: ", positionsToDraw)
                print("pointsToDraw: ", pointsToDraw)
                print("colorsToDraw: ", colorsToDraw, " original w: ", w)

                a = pointsToDraw[0]
                b = pointsToDraw[1]
                c = pointsToDraw[2]

                a_rgba = []
                b_rgba = []
                c_rgba = []

                if hyp:
                    for i in range(3): # divides each point's rgb value by its respective w
                        a_rgba += [colorsToDraw[0][i]/(1/a[3])] 
                        b_rgba += [colorsToDraw[1][i]/(1/b[3])]
                        c_rgba += [colorsToDraw[2][i]/(1/c[3])]
                    a_rgba += [colorsToDraw[0][3]]
                    b_rgba += [colorsToDraw[1][3]]
                    c_rgba += [colorsToDraw[2][3]]

                else:
                    a_rgba = colorsToDraw[0]
                    b_rgba = colorsToDraw[1]
                    c_rgba = colorsToDraw[2]


                # print("new colorsToDraw: ", a_rgba, b_rgba, c_rgba)

                pixelsToDraw += scanline_algo(a, b, c, a_rgba, b_rgba, c_rgba)

                # currPixels = []

                for pixel in pixelsToDraw:
                    x = pixel[0]
                    y = pixel[1]
                    z = pixel[2]
                    w = pixel[3]
                    # print("new w: ", w)
                    # print("rgb without w division: ", pixel[4:8])
                    for i in range(4,8):
                        if hyp:
                            pixel[i] /= w # divide rgb by interpolated 1/w
                            
                        if sRGB:
                            if(pixel[i] <= 1 and pixel[i] >= 0):
                                if(pixel[i] <= 0.0031308):
                                    pixel[i] *= 12.92
                                else:
                                    pixel[i] = 1.055*pixel[i]**(1/2.4) - 0.055
                            if pixel[i] > 1:
                                pixel[i] = 1
                            elif pixel[i] < 0:
                                pixel[i] = 0
                    # print("new color rgb: ", pixel[4:7])
                    
                    r = pixel[4]*255
                    g = pixel[5]*255
                    b = pixel[6]*255
                    a = pixel[7]*255
                    
                    
                    if(-width < x < width and -height < y < height):
                        if depth:
                            existingPos = [pix for pix in currPixels if pix[:2] == [x,y]]
                            # print("existingPos: ", existingPos)
                        if(existingPos):
                            if(existingPos[0][2] > z):
                                currPixels.remove(existingPos[0])
                                image.putpixel((int(x),int(y)), (int(r),int(g),int(b),int(a)))
                                currPixels.append([x,y,z])

                        else:
                            image.putpixel((int(x),int(y)), (int(r),int(g),int(b),int(a)))
                            # print("put down pixel xyrgba: ", x,y,r,g,b,a)
                            currPixels.append([x,y,z])
                        
                # print("pixelsToDraw: ", pixelsToDraw)

        elif line.find("elements") != -1:
            intString = line.split()[1:]
            
            elements = [int(num) for num in intString]

            # print("elements: ", elements)

        elif line.find("drawElementsTriangles") != -1:
            count = int(line.split()[1]) # stores how many triangles
            offset = int(line.split()[2])

            positionsToDraw = []
            colorsToDraw = []

            for i in range(0, count, 3):
                positionsToDraw = [positions[elements[offset + i]], positions[elements[offset + i + 1]], positions[elements[offset + i + 2]]]
                colorsToDraw = [colors[elements[offset + i]], colors[elements[offset + i + 1]], colors[elements[offset + i + 2]]]

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
                        productMatrix = matrix_multiply(uniformMatrix, posMatrix)
                        x = productMatrix[0][0]
                        y = productMatrix[1][0]
                        z = productMatrix[2][0]
                        w = productMatrix[3][0]
                            
                        # print("new xyzw: ", x,y,z,w)

                    pointsToDraw.append([(x/w+1)*width/2, (y/w+1)*height/2, z/w, 1/w])

                print("positionsToDraw: ", positionsToDraw)
                print("pointsToDraw: ", pointsToDraw)
                print("colorsToDraw: ", colorsToDraw, " original w: ", w)

                a = pointsToDraw[0]
                b = pointsToDraw[1]
                c = pointsToDraw[2]

                a_rgba = []
                b_rgba = []
                c_rgba = []

                if hyp:
                    for i in range(3): # divides each point's rgb value by its respective w
                        a_rgba += [colorsToDraw[0][i]/(1/a[3])] 
                        b_rgba += [colorsToDraw[1][i]/(1/b[3])]
                        c_rgba += [colorsToDraw[2][i]/(1/c[3])]
                    a_rgba += [colorsToDraw[0][3]]
                    b_rgba += [colorsToDraw[1][3]]
                    c_rgba += [colorsToDraw[2][3]]

                else:
                    a_rgba = colorsToDraw[0]
                    b_rgba = colorsToDraw[1]
                    c_rgba = colorsToDraw[2]


                print("new colorsToDraw: ", a_rgba, b_rgba, c_rgba)

                pixelsToDraw += scanline_algo(a, b, c, a_rgba, b_rgba, c_rgba)

                # currPixels = []

                for pixel in pixelsToDraw:
                    x = pixel[0]
                    y = pixel[1]
                    z = pixel[2]
                    w = pixel[3]
                    # print("new w: ", w)
                    # print("rgb without w division: ", pixel[4:8])
                    for i in range(4,8):
                        if hyp:
                            pixel[i] /= w # divide rgb by interpolated 1/w
                            
                        if sRGB:
                            if(pixel[i] <= 1 and pixel[i] >= 0):
                                if(pixel[i] <= 0.0031308):
                                    pixel[i] *= 12.92
                                else:
                                    pixel[i] = 1.055*pixel[i]**(1/2.4) - 0.055
                            if pixel[i] > 1:
                                pixel[i] = 1
                            elif pixel[i] < 0:
                                pixel[i] = 0
                    # print("new color rgb: ", pixel[4:7])
                    
                    r = pixel[4]*255
                    g = pixel[5]*255
                    b = pixel[6]*255
                    a = pixel[7]*255
                    
                    if(-width < x < width and -height < y < height):
                        if depth:
                            existingPos = [pix for pix in currPixels if pix[:2] == [x,y]]
                            # print("existingPos: ", existingPos)
                        if(existingPos):
                            if(existingPos[0][2] > z):
                                currPixels.remove(existingPos[0])
                                image.putpixel((int(x),int(y)), (int(r),int(g),int(b),int(a)))
                                currPixels.append([x,y,z])

                        else:
                            image.putpixel((int(x),int(y)), (int(r),int(g),int(b),int(a)))
                            # print("put down pixel xyrgba: ", x,y,r,g,b,a)
                            currPixels.append([x,y,z])
                        
                # print("pixelsToDraw: ", pixelsToDraw)

            
        
         
                
image.save(pngName, "PNG")
# ...
