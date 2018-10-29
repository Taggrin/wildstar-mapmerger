# This script merges extracted WildStar map tiles into one image.
# Made by Taggrin, 23/09/2018

# Standard libraries
import os, sys

# Python Image Library to merge images
try:
    from PIL import Image
except ImportError:
    print "PIL library not installed. Please refer to the manual to resolve this problem."
    sys.exit()
    
# Input/Output locations
inputdir = "./Map/"
outputdir = "./Out/"

custominputdir = raw_input("Where are your map tiles located?\nDefault expected path: ./Map/\n\nLocation (leave empty for default): ")

if custominputdir != "":
    inputdir = custominputdir

# Get all maps found in the input directory
maps = os.listdir(inputdir)
print "\nTarget directory: %s"%(inputdir)
print "Found %s maps to reconstruct.\n"%(len(maps))

# Loop through each map
for worldmap in maps:
    currentDir = "%s/%s/"%(inputdir, worldmap)
    print "Reconstructing %s ..."%(worldmap)

    # Put all image tiles per map into a list
    imagelist = os.listdir(currentDir)

    # Next we want to sort the images so its easier to fill the grid
    # Images use 4 hexvalues, we just gonna loop through it and grab anything we see
    # Not best for performance, but oh well can't be bothered to think of something else
    imagelistsorted = []
    for i in range(0x0000, 0xFFFF):
        for image in imagelist:
            if hex(i).split("x")[1].zfill(4) in image:
                imagelistsorted.append(image)

    # Now we need to know how big the image will be
    # The amount of duplicates within the first two hexvalues will indicate the width
    # Split hexvalue pairs for easier data management
    xhexes = []
    yhexes = []
    for image in imagelistsorted:
        xhexes.append(image.split(".")[-3][2:])
        yhexes.append(image.split(".")[-3][:2])

    # Find the corners of the map
    # X1: lowest first hexvalue pair
    # Y1: lowest last hexvalue pair
    # X2: highest first hexvalue pair
    # Y2: highest last hexvalue pair
    x1 = x2 = y1 = y2 = ""
    for i in range(0x00, 0xFF):
        hexvalue = hex(i).split("x")[1].zfill(2)
        if hexvalue in xhexes:
            if x1 == "":
                x1 = hexvalue
            x2 = hexvalue
        if hexvalue in yhexes:
            if y1 == "":
                y1 = hexvalue
            y2 = hexvalue

    # Now that we need the corners we need to count the amount of tiles across each axis
    xcount = int(x2, 16) - int(x1, 16) + 1
    ycount = int(y2, 16) - int(y1, 16) + 1

    # We have all data now to start merging the map!
    # Move to the map directory
    os.chdir(currentDir)

    # Tile image size is 512px
    offset = 512
    # Total image size
    width = 512 * xcount
    height = 512 * ycount

    # Image template
    image = Image.new('RGB', (width, height))

    # Triggers and positioning for pasting tiles
    offsetx = 0
    offsety = 0
    xactive = False
    yactive = False
    counter = 0

    # Placeholder image for missing tiles
    blank = Image.new('RGB', (offset, offset), color = (120, 117, 120))
    
    # Loop through the hexvalues and paste any tiles
    for i in range(0x0000, 0xFFFF):
        hexvalue = hex(i).split("x")[1].zfill(4)
        # Starting range of pasting
        if hexvalue[:2] == y1:
            yactive = True
        if hexvalue[2:] == x1:
            xactive = True

        if xactive and yactive:
            found = False
            for tile in imagelistsorted:
                if hexvalue in tile:
                    # If we can find an image we put it in its place
                    try:
                        img = Image.open(tile)
                        image.paste(img, (offsetx, offsety))
                        img.close()
                    except IOError:
                        image.paste(blank, (offsetx, offsety))
                    found = True
                    break
            if not found:
                # If not we put a blank image
                image.paste(blank, (offsetx, offsety))  
            counter += 1
            # Reposition pasting
            if counter >= xcount:
                offsetx = 0
                offsety += offset
                counter = 0
            else:
                offsetx += offset

        # End range of pasting
        if hexvalue[2:] == x2:
            xactive = False
            if hexvalue[:2] == y2:
                yactive = False

    # Move back to the script directory
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    # Check if output directory exists, if not create it
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)
    # Save the image
    image.save("%s/%s.jpg"%(outputdir,worldmap))

raw_input("FINISHED!")
