from PIL import Image
import PIL
import sys
import math

def dda_setup(a, b, dimension):
    if(dimension == "x"):
        d = 0 
    else:
        d = 1
    # print("a and d: ", a,d)
    # a_d = a[d]
    # # print("a_d: ", a_d)
    # b_d = b[d]
    # print("a_d and b_d, dimension: ", a_d,b_d,dimension)
    if(a[d] == b[d]):
        if(dimension == "x"):
            return [0,0]
        return []
    
    elif(a[d] > b[d]): # swap a and b
        # print("a, b:", a,b)
        temp = a
        a = b
        b = temp
        # print("a, b:", a,b)

    pointDiff = [b[0]-a[0], b[1]-a[1]]
    s = []
    for p_coord in pointDiff:
        s.append(p_coord/(b[d] - a[d])) # s is now ([] of 4)/dimensional diff

    return s

def dda_firstPoint(a, b, dimension):
    if(dimension == "x"):
        d = 0 
    else:
        d = 1
    
    s = dda_setup(a, b, dimension)
    if(a[d] > b[d]): # swap a and b
        # print("a, b:", a,b)
        temp = a
        a = b
        b = temp
        # print("a, b:", a,b)
    # print("s: ", s)
    
    o = []
    p = []
   
    e = math.ceil(a[d]) - a[d] # calculates distance between a_d and next integer
    # print("e: ", e)
    for s_coord in s:
        o.append(s_coord*e) # o is of distance e and obtains the direction of s vector
    
    # print("o, a, b, dimension, s, e: ", o,a,b,dimension,s,e)

    for i in range(2):
        p.append(a[i] + o[i])
        # print("p[i]+s[i]: ", p[i],s[i])
        # p[i] += s[i]
        # print("a,o,p: ", a,o,p)
    # print("p: ",p)
    return p

def dda_allPoints(a, b, dimension):
    all_p = []
    # print("dimensions", dimension)
    p = dda_firstPoint(a, b, dimension)
    # all_p.append(p.copy())
    
    # print("all_p: ", all_p)
    # print("p: ", p)

    if(dimension == "x"):
        d = 0 
        # if(a == b):
            # print("matching: ",a)
            # all_p.append(a)
            # print("matching, all_p: ",a)
    else:
        d = 1
    
    s = dda_setup(a, b, dimension)
    if(a[d] > b[d]): # swap a and b
        # print("a, b:", a,b)
        temp = a
        a = b
        b = temp
        # print("a, b:", a,b)
    # print("a,b,d,s: ", a,b,d,s)
    # print("p[d],b[d]",p[d],b[d])
    while p[d] < b[d]:
        all_p.append(p.copy())
        for i in range(2):
            p[i] += s[i]
        # if(a[d] == b[d] and dimension == "x"):
        #     print("hereeee")
        #     all_p.append(a)
            # print("p[i]: ", p[i], "s[i]: ", s[i])
        # print("new p: ", p)
    # print("all_p,dimension", all_p,dimension)
    return all_p

def scanline_algo(x, y, z, rgba):
    trianglePoints = [x, y, z]
    # print("triangle points: ", trianglePoints)
    y_points = [x[1], y[1], z[1]]
    
    for i in range(3):
        if(min(y_points) == y_points[i]):
            t = trianglePoints[i]
        elif(max(y_points) == y_points[i]):
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
    # print("s_long,p_long,s,p: ", s_long,p_long,s,p)

    # step 6
    points = []
    while p[1] < m[1]:
        # print("top p,p_long: ",p,p_long)
        points += dda_allPoints(p, p_long, "x")
        # if(p == p_long):
        #     print("matching: ",p)
        #     points += p
        #     print(points)
        # print("points: ", points)
        for i in range(2):
            p[i] += s[i]
            p_long[i] += s_long[i]

    # find points in bottom half of triangle
    # step 7
    s = dda_setup(m, b, "y")
    p = dda_firstPoint(m, b, "y")

    # step 8
    while p[1] < b[1]:
        # print("bottom p,p_long: ",p,p_long)
        points += dda_allPoints(p, p_long, "x")
        # if(p == p_long):
        #     print("matching: ",p)
        #     points += p
        for i in range(2):
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
# p = dda_firstPoint(a, b, "y")
# print(dda_allPoints(a, b, "y"))
# print(scanline_algo(a,b,c))


coordXYZW = []
coordRGBA = []


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
            floatsString = line.split()[2:]
            line = line.replace("position", '')
            # print("line", line)
            coordSize = int(line.split()[0]) # stores the size of the coordinates
            print("coordSize: ", coordSize)
            line = ''.join(line.split()[1:]) # removes size so rest of line are coordinates
            # x, y = (int(i) for i in line.split())
            tempCount = 0
            
            floats = [float(num) for num in floatsString]
            # print("floats: ", floats)
            for i in floats:
                coordXYZW.append(float(i))
                tempCount += 1 
                # accounts for missing coordinates to make 4-vectors
                if(coordSize == 2 and tempCount%4 != 0 and tempCount%2 == 0): 
                    coordXYZW.append(0)
                    coordXYZW.append(1)
                elif(coordSize == 3 and tempCount%3 == 0):
                    coordXYZW.append(1)
                # print(coordXYZW)
            print("coordXYZW: ", coordXYZW)

        elif line.find("color") != -1:
            colorSize = int(line.split()[1])
            floatsString = line.split()[2:]
            # line = line.replace("color", '')
            #  # stores the size of the color
            # line = ''.join(line.split()[1:]) # removes size so rest of line are rgba vals
            
            floats = [float(num) for num in floatsString]
            tempCount = 0 
            for i in floats:
                coordRGBA.append(int(i))
                tempCount += 1

                if(colorSize == 3 and tempCount%3 == 0):
                    coordRGBA.append(1)
            print("coordRGBA",coordRGBA)
            # print(coordRGBA)

        elif line.find("drawArraysTriangles") != -1:
            first = int(line.split()[1]) # stores the size of the color
            count = int(line.split()[2])
            line = line.replace("drawArraysTriangles", ''). replace(" ", '').replace("\t", '').replace("\n", '')
            
            # print("first, count: ",first,count)
            line = ''.join(line.split()[2:])
            # print(fileContents)

            pointsToDraw = []
            for i in range(int(count/3)):
                print(i)
                x1 = coordXYZW[first*4*(i+1)]
                y1 = coordXYZW[(first*4*(i+1))+1]
                z1 = coordXYZW[(first*4*(i+1))+2]
                w1 = coordXYZW[(first*4*(i+1))+3]
                
                # ((x/w+1)*width/2, (y/w+1)*height/2)
                newX1 = (x1/w1+1)*width/2
                newY1 = (y1/w1+1)*height/2

                # print("first*4*(i+2): ",first*4*(i+1))
                x2 = coordXYZW[(first*4*(i+1))+4]
                y2 = coordXYZW[(first*4*(i+1))+5]
                z2 = coordXYZW[(first*4*(i+1))+6]
                w2 = coordXYZW[(first*4*(i+1))+7]
                
                # ((x/w+1)*width/2, (y/w+1)*height/2)
                newX2 = (x2/w2+1)*width/2
                newY2 = (y2/w2+1)*height/2

                x3 = coordXYZW[(first*4*(i+1))+8]
                y3 = coordXYZW[(first*4*(i+1))+9]
                z3 = coordXYZW[(first*4*(i+1))+10]
                w3 = coordXYZW[(first*4*(i+1))+11]
                # print("x3,y3,z3,w3: ",x3,y3,z3,w3)
                
                # ((x/w+1)*width/2, (y/w+1)*height/2)
                newX3 = (x3/w3+1)*width/2
                newY3 = (y3/w3+1)*height/2

                print("newXs and newYs: ", newX1,newY1,newX2,newY2,newX3,newY3)
                print(coordRGBA[first*4:first*4+4])
                pointsToDraw += scanline_algo([newX1,newY1],[newX2,newY2],[newX3,newY3], coordRGBA[first*4:first*4+4])
                print("pointsToDraw: ",pointsToDraw)
                # print(coordXYZW[first*4],coordXYZW[(first*4)+1],coordXYZW[(first*4)+2],coordXYZW[(first*4)+3])
                # print(coordRGBA[i*4], coordRGBA[(i*4)+1], coordRGBA[(i*4)+2], coordRGBA[(i*4)+3])
            currPixel = 0
            while currPixel < count:
                for point in pointsToDraw:
                    # print("point:", point)
                    x = point[0]
                    y = point[1]
                    image.putpixel((int(x),int(y)), (coordRGBA[first*4*(currPixel+1)], 
                    coordRGBA[first*4*(currPixel+1)+1], coordRGBA[first*4*(currPixel+1)+2], 
                    coordRGBA[first*4*(currPixel+1)+3]))
                    currPixel += 1
                # print(pngName)
            
                
image.save(pngName, "PNG")
# ...

