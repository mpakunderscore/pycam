# SERVER


import threading

import sys
from os import curdir, sep

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

# from cam import training, state

PORT = 8000


class CameraHandler(BaseHTTPRequestHandler):

    # Handler for the GET requests
    def do_GET(self):

        global training
        global biggest

        if self.path == "/cam.jpg":
            f = open(curdir + sep + self.path)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(f.read())
            f.close()

        if self.path == "/":
            self.path = "/index.html"
            f = open(curdir + sep + self.path)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(f.read())
            f.close()

        if self.path == "/test":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write("test")

        if self.path == "/train":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write("train")

            training = True

        if self.path == "/state":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(biggest)


def run():

    server = HTTPServer(("", PORT), CameraHandler)
    thread = threading.Thread(target = server.serve_forever)
    thread.daemon = True

    try:
        thread.start()
    except KeyboardInterrupt:
        server.shutdown()
        sys.exit(0)

    print ("Serving at port", PORT)


# CAMERA


import time
import sys
import os
import picamera
import picamera.array

width = 2560
height = 1440
# width = 3296
# height = 1856
# width = 1280
# height = 720

# Center line
center = height / 2

# Iteration of training
approach = 20

# Do we train?
training = False

# Available pixel difference
accuracy = 20

# Output biggest row
biggest = -1

# Reference (r, g, b) arrays of the center line
ra = []
ga = []
ba = []
for i in range(width):
    ra.append(0)
    ga.append(0)
    ba.append(0)

# def settraining(val):
#     global training
#     training = val


def train():

    print ("Train")

    global training

    # First 2 for camera heating
    for n in range(2, approach):

        start = time.time()
        camera.capture(output, "rgb")
        end = time.time()
        print (end - start, "camera")

        for i in range(0, width):

            if i == width / 2:
                r = output.array[center, i, 0]
                g = output.array[center, i, 1]
                b = output.array[center, i, 2]

                print ("RGB CENTER:", r, g, b)

            ra[i] += output.array[center, i, 0]
            ga[i] += output.array[center, i, 1]
            ba[i] += output.array[center, i, 2]

        output.truncate(0)

    reference = open("reference.txt", "w")

    for i in range(0, width):
        ra[i] /= (approach - 2)
        ga[i] /= (approach - 2)
        ba[i] /= (approach - 2)

        reference.write("%s\n" % ra[i])
        reference.write("%s\n" % ga[i])
        reference.write("%s\n" % ba[i])

    camera.capture("cam.jpg")

    print ("R:", ra[width / 2], ga[width / 2], ba[width / 2])

    training = False

    output.truncate(0)


def check():

    print ("Check")

    while True:

        if training:
            train()

        start = time.time()
        camera.capture(output, "rgb")
        end = time.time()
        # print (end - start, "camera")

        marker = ""

        rowdifference = 0

        row = 0

        global biggest

        biggest = 0

        for i in range(0, width):

            r = output.array[center, i, 0]
            g = output.array[center, i, 1]
            b = output.array[center, i, 2]

            rd = abs(ra[i] - r)
            gd = abs(ga[i] - g)
            bd = abs(ba[i] - b)

            pixeldifference = (gd + bd)  # rd +

            # center

            if i == width / 2:
                print ("RGB CENTER:", r, g, b, "|", rd, gd, bd, "|", pixeldifference)

            # all

            if pixeldifference > accuracy:
                rowdifference += 1
                row += 1

            else:
                row = 0

            if row > biggest:
                biggest = row

            # marker row

            if i % 15 == 0:
                if row > 5:
                    marker += "|"
                else:
                    marker += "."

        print (rowdifference, "|", biggest)

        print (marker)

        output.truncate(0)


def readfile():
    # Check if error here
    reference = open("reference.txt", "r")
    for i in range(0, width):

        for i, line in enumerate(reference):

            if i % 3 == 0:
                ra[i / 3] = int(line.replace("\n", ""))

            if i % 3 == 1:
                ga[i / 3] = int(line.replace("\n", ""))

            if i % 3 == 2:
                ba[i / 3] = int(line.replace("\n", ""))


with picamera.PiCamera() as camera:
    with picamera.array.PiRGBArray(camera, size=(width, height)) as output:

        run()

        print ("Init")

        camera.hflip = True
        camera.vflip = True
        # camera.contrast = 50
        # camera.brightness = 70
        # camera.exposure_mode = "night"
        camera.awb_mode = "off"
        camera.awb_gains = 1.5

        camera.resolution = (width, height)

        # cam setting

        camera.capture("cami.jpg")

        # INFINITY

        # training

        # print (os.stat("reference.txt").st_size)

        if os.path.exists("reference.txt"):
            readfile()

        else:
            training = True

        check()

