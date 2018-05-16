from jam_picamera import JamPiCamera
from auth import CON_KEY, CON_SEC, ACC_TOK, ACC_SEC
from gpiozero import Button
from time import sleep
import logging

logger = logging.getLogger('photobooth')
logging.basicConfig(level=logging.INFO)
logger.info("starting")

camera = JamPiCamera()
button = Button(14, hold_time=5)
camera.resolution = (1024, 768)
camera.start_preview()
camera.vflip = True
camera.annotate_text_size = 70

def quit():
    logger.info("quitting")
    camera.close()

def countdown(n):
    logger.info("running countdown")
    for i in reversed(range(n)):
        camera.annotate_text = '{}...'.format(i + 1)
        sleep(1)
    camera.annotate_text = None

button.when_held = quit

while True:
    camera.annotate_text = "Press button to start"
    logger.info("waiting for button press")
    button.wait_for_press()
    logger.info("button pressed")
    camera.annotate_text = "Press button to take photo"
    button.wait_for_press()
    logger.info("button pressed")
    button.wait_for_release()
    logger.info("button released")
    sleep(1)
    countdown(3)
    logger.info("capturing photo")
    photo = camera.capture()
    logger.info("captured photo: {}".format(photo))
    camera.annotate_text = None
