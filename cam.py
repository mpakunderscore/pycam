import time
import picamera
import picamera.array
from PIL import Image

with picamera.PiCamera() as camera:
    with picamera.array.PiRGBArray(camera) as output:

        print ("Init")

        width = 3280/2
        height = 2464/2

        inaccuracy = 10

        ra = []
        ga = []
        ba = []
        for i in range(width):
            ra.append(0)
            ga.append(0)
            ba.append(0)

        camera.resolution = (width, height)

        # camera.hflip = True
        # camera.vflip = True
        # camera.brightness = 70

        # Camera warm-up time
        time.sleep(2)

        n = 0

        training = 5

        print ("Run")

        while True:

            print ("--")

            bias = 0

            start = time.time()

            camera.capture(output, "rgb")

            end1 = time.time()
            print (end1 - start, "camera")

            im = Image.open("foo.jpg")
            rgb_im = im.convert("RGB")

            end2 = time.time()
            print (end2 - end1, "image load")

            if n < training:
                for i in range(0, width):
                    r, g, b = rgb_im.getpixel((i, height / 2))

                    ra[i] += r
                    ga[i] += g
                    ba[i] += b

                print ("R: ", n)
                n = n + 1

            if n == training:
                for i in range(0, width):
                    ra[i] /= training
                    ga[i] /= training
                    ba[i] /= training

                print ("Remembered")
                n = n + 1

            if n > training:
                # for i in range(0, width):

                    i = width / 2

                    r, g, b = rgb_im.getpixel((i, height / 2))

                    # rdifference = ra[i] - r
                    # gdifference = ra[i] - r
                    # bdifference = ra[i] - r

                    print ("RGB center: ", r, g, b, " | ", ra[i], ga[i], ba[i])

                    # if difference > inaccuracy or difference < -1 * inaccuracy:
                    #     bias += 1
                    # else:
                    #     print "."

            # print bias




