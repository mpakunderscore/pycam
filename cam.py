# http server

import threading

from SimpleHTTPServer import SimpleHTTPRequestHandler
from BaseHTTPServer import HTTPServer

PORT = 8000

server = HTTPServer(("", PORT), SimpleHTTPRequestHandler)
thread = threading.Thread(target = server.serve_forever)
thread.daemon = True

try:
    thread.start()
except KeyboardInterrupt:
    server.shutdown()
    sys.exit(0)

print ("Serving at port", PORT)

# end server


import time
import sys
import picamera
import picamera.array
# from PIL import Image

width = 2560
height = 1440

# width = 3296
# height = 1856

# width = 1280
# height = 720

heating = 10
training = 20

inaccuracy = 20

with picamera.PiCamera() as camera:
    with picamera.array.PiRGBArray(camera, size=(width, height)) as output:

        print ("Init")

        ra = []
        ga = []
        ba = []
        for i in range(width):
            ra.append(0)
            ga.append(0)
            ba.append(0)

        camera.hflip = True
        camera.vflip = True
        # camera.contrast = 50
        # camera.brightness = 70
        # camera.exposure_mode = "night"
        camera.awb_mode = "off"
        camera.awb_gains = 1.5

        camera.resolution = (width, height)

        # print ("Heating")

        camera.capture("cami.jpg")

        n = 0
        while True:

            # print ("--")

            bias = 0

            start = time.time()

            camera.capture(output, "rgb")

            end1 = time.time()
            print (end1 - start)

            # print("Captured %dx%d image" % (
            #     output.array.shape[1], output.array.shape[0]))

            # output.truncate(0)
            # continue

            # im = Image.open("foo.jpg")
            # rgb_im = im.convert("RGB")

            # if n < heating:
            #     n = n + 1
            #     output.truncate(0)
            #     continue

            if n < training:
                for i in range(0, width):

                    if i == width / 2:

                        r = output.array[height / 2, i, 0]
                        g = output.array[height / 2, i, 1]
                        b = output.array[height / 2, i, 2]

                        print ("RGB center: ", r, g, b)

                    ra[i] += output.array[height/2, i, 0]
                    ga[i] += output.array[height/2, i, 1]
                    ba[i] += output.array[height/2, i, 2]

                # print ("R", n)
                n = n + 1
                output.truncate(0)
                continue

            if n == training:
                for i in range(0, width):
                    ra[i] /= training
                    ga[i] /= training
                    ba[i] /= training

                camera.capture("cam.jpg")

                print ("Remembered", ra[width/2], ga[width/2], ba[width/2])
                n = n + 1
                output.truncate(0)
                continue

            if n > training:

                marker = ""

                distinction = 0

                row = 0
                biggest = 0

                # for j in range(height / 2 - 10, height / 2 + 10):

                j = height / 2

                for i in range(0, width):

                        r = output.array[j, i, 0]
                        g = output.array[j, i, 1]
                        b = output.array[j, i, 2]

                        rd = abs(ra[i] - r)
                        gd = abs(ga[i] - g)
                        bd = abs(ba[i] - b)

                        difference = (gd + bd) # rd +

                        if i == width / 2:
                            print ("RGB center:", r, g, b, difference)

                        if difference > inaccuracy:
                            distinction += 1
                            row += 1
                        else:
                            row = 0

                        if row > biggest:
                            biggest = row

                        if i % 15 == 0:
                            if row > 5:
                                marker += "|"
                            else:
                                marker += "."

                    # print bias


                print (distinction, biggest)

                # print marker
                print (marker)

                output.truncate(0)

                # end2 = time.time()
                # print (end2 - end1, "image check")
                continue