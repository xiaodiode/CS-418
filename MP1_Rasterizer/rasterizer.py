from PIL import Image
import sys
import math

def dda_setup(a, b, dimension, a_rgba, b_rgba):
    if(dimension == "x"):
        d = 0 
    else:
        d = 1

    # print("a, b: ", a,b)
    # print("a and d: ", a,d)
    # a_d = a[d]
    # # print("a_d: ", a_d)
    # b_d = b[d]
    # print("a_d and b_d, dimension: ", a_d,b_d,dimension)
    if(a[d] == b[d]):
        if(dimension == "x"):
            return [0,0,0,0,0,0]
        return [0,0,0,0,0,0]
    
    elif(a[d] > b[d]): # swap a and b
        # print("a, b:", a,b)
        temp = a
        a = b
        b = temp

        temp = a_rgba
        a_rgba = b_rgba
        b_rgba = temp
        # print("a, b:", a,b)

    pointDiff = [b[0]-a[0], b[1]-a[1]]
    colorDiff = []

    for i in range(4):
        colorDiff += [b_rgba[i] - a_rgba[i]]


    # print("colorDiff: ", colorDiff, " b_rgba: ", b_rgba, " a_rgba: ", a_rgba)

    s = []
    for p_coord in pointDiff:
        s.append(p_coord/(b[d] - a[d])) # s is now ([] of 4)/dimensional diff
    
    for c_coord in colorDiff:
        s.append(c_coord/(b[d] - a[d]))

    # s += b_rgba 

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
   
    print("o, s:", o, s)
    e = math.ceil(a[d]) - a[d] # calculates distance between a_d and next integer
    # print("e: ", e)
    for i in range(6):
        o.append(s[i]*e) # o is of distance e and obtains the direction of s vector
        if(i < 2):
            p += [a[i] + o[i]]
        else:
            p += [a_rgba[i-2] + o[i]]

    print("p: ",p)
    return p

def dda_allPoints(a, b, dimension, a_rgba, b_rgba):
    all_p = []
    # print("dimensions", dimension)
    p = dda_firstPoint(a, b, dimension, a_rgba, b_rgba)
    # all_p.append(p.copy())
    
    # print("all_p: ", all_p)
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

    # print("a,b,d,s: ", a,b,d,s)
    # print("p[d],b[d]",p[d],b[d])
    while p[d] < b[d]:
        all_p.append(p.copy())
        # p = s[:2] + b_rgba
        # print("p: ", p)
        for i in range(6):
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
            print("m: ",m)
            m_rgba = rgbaPoints[i]

    print("t, b, m: ", t, b, m)

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
    # print("s_long,p_long,s,p: ", s_long,p_long,s,p)

    # step 6
    points = []
    while p[1] < m[1]:
        # print("top p,p_long: ",p,p_long)
        points += dda_allPoints(p[0:2], p_long[0:2], "x", p[2:], p_long[2:])
        # print("points: ", points)
        for i in range(6):
            p[i] += s[i]
            p_long[i] += s_long[i]

    # find points in bottom half of triangle
    # step 7
    s = dda_setup(m, b, "y", m_rgba, b_rgba)
    p = dda_firstPoint(m, b, "y", m_rgba, b_rgba)

    # step 8
    while p[1] < b[1]:
        # print("bottom p,p_long: ",p,p_long)
        points += dda_allPoints(p[0:2], p_long[0:2], "x", p[2:], p_long[2:])
        # if(p == p_long):
        #     print("matching: ",p)
        #     points += p
        for i in range(6):
            p[i] += s[i]
            p_long[i] += s_long[i]

    return points
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

positions = []
colors = []


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

        elif line.startswith("position"):
            coordSize = int(line.split()[1]) # stores the size of the coordinates
            floatsString = line.split()[2:]
            # line = line.replace("position", '')
            # print("line", line)
            print("coordSize: ", coordSize)
            
            floats = [float(num) for num in floatsString]
            print("floats for position: ", floats)

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
            colorSize = int(line.split()[1])
            floatsString = line.split()[2:]
            # line = line.replace("color", '')
            #  # stores the size of the color
            # line = ''.join(line.split()[1:]) # removes size so rest of line are rgba vals
            
            floats = [float(num) for num in floatsString]
            print("floats for color: ", floats)

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
            
            pixelsToDraw = []

            for i in range(0, count, 3):
                positionsToDraw = [positions[first + i], positions[first + i + 1], positions[first + i + 2]]
                colorsToDraw = [colors[first + i], colors[first + i + 1], colors[first + i + 2]]

                pointsToDraw = []
            
                for j in range(3):
                    x = positionsToDraw[j][0]
                    y = positionsToDraw[j][1]
                    z = positionsToDraw[j][2]
                    w = positionsToDraw[j][3]

                    pointsToDraw.append([(x/w+1)*width/2, (y/w+1)*height/2])

                print("pointsToDraw: ", pointsToDraw)
                print("colorsToDraw: ", colorsToDraw)

                a = pointsToDraw[0]
                b = pointsToDraw[1]
                c = pointsToDraw[2]

                a_rgba = colorsToDraw[0]
                b_rgba = colorsToDraw[1]
                c_rgba = colorsToDraw[2]

                pixelsToDraw += scanline_algo(a, b, c, a_rgba, b_rgba, c_rgba)
                

                for pixel in pixelsToDraw:
                    x = pixel[0]
                    y = pixel[1]
                    r = pixel[2]*255
                    g = pixel[3]*255
                    b = pixel[4]*255
                    a = pixel[5]*255
                    # print("rgba: ", r,g,b,a)

                    image.putpixel((int(x),int(y)), (int(r),int(g),int(b),int(a)))
                # print("pixelsToDraw: ", pixelsToDraw)

            
                
image.save(pngName, "PNG")
# ...

