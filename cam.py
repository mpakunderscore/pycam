from server import run

run()

import time
import sys
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
training = True

# Available pixel difference
accuracy = 20

state = 0

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

                print ("RGB center: ", r, g, b)

            ra[i] += output.array[center, i, 0]
            ga[i] += output.array[center, i, 1]
            ba[i] += output.array[center, i, 2]

        output.truncate(0)

    for i in range(0, width):
        ra[i] /= approach - 2
        ga[i] /= approach - 2
        ba[i] /= approach - 2

    camera.capture("cam.jpg")

    print ("Remembered", ra[width / 2], ga[width / 2], ba[width / 2])

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
                print ("RGB center:", r, g, b, "|", rd, gd, bd, "|", pixeldifference)

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


with picamera.PiCamera() as camera:
    with picamera.array.PiRGBArray(camera, size=(width, height)) as output:

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

        check()
