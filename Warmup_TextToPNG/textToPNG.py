from PIL import Image
import PIL
import sys

pixelsXY = []
pixelsRGBA = []
currPixel = 0

with open(sys.argv[1], 'r') as filename:
    fileContents = filename.readlines()
    for line in fileContents:
        if line.find(".png") != -1:
            for word in line.split():
                if ".png" in word:
                    pngName = word
                    line = line.replace(word, '')
            line = line.replace("png", '')
            width, height = (int(i) for i in line.split())
            image = Image.new("RGBA", (width, height), (0,0,0,0))
            print(width, height)

        elif line.find("position 2") != -1:
            line = line.replace("position 2", '')
            # x, y = (int(i) for i in line.split())
            for i in line.split():
                pixelsXY.append(int(i))
                # print(pixelsXY)

        elif line.find("color 4") != -1:
            line = line.replace("color 4", '').replace("\t", '')
            # red, green, blue, alpha = 
            for i in line.split():
                pixelsRGBA.append(int(i))
            # print(pixelsRGBA)

        elif line.find("drawPixels") != -1:
            line = line.replace("drawPixels", ''). replace(" ", '').replace("\t", '').replace("\n", '')
            print(fileContents)
            pixelNumber = line
            print(pixelNumber)
            for i in range(int(pixelNumber)):
                print(i)
                print(pixelsXY[currPixel*2],pixelsXY[(currPixel*2)+1])
                print(pixelsRGBA[i*4], pixelsRGBA[(i*4)+1], pixelsRGBA[(i*4)+2], pixelsRGBA[(i*4)+3])
                image.putpixel((pixelsXY[currPixel*2],pixelsXY[(currPixel*2)+1]), 
                    (pixelsRGBA[i*4], pixelsRGBA[(i*4)+1], pixelsRGBA[(i*4)+2], pixelsRGBA[(i*4)+3]))
                # print(pngName)
                currPixel+=1
                
image.save(pngName, "PNG")
# ...

