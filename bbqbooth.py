from jam_picamera import JamPiCamera
from auth import CON_KEY, CON_SEC, ACC_TOK, ACC_SEC
from gpiozero import Button
from time import sleep
from PIL import Image
import logging

logger = logging.getLogger('photobooth')
logging.basicConfig(level=logging.INFO)
logger.info("starting")

camera = JamPiCamera()
button = Button(14, hold_time=5)
camera.resolution = (1024, 768)
camera.start_preview()
camera.hflip = True
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

def _pad(resolution, width=32, height=16):
    # A little utility routine which pads the specified resolution
    # up to the nearest multiple of *width* and *height*; this is
    # needed because overlays require padding to the camera's
    # block size (32x16)
    return (
        ((resolution[0] + (width - 1)) // width) * width,
        ((resolution[1] + (height - 1)) // height) * height,
    )

photo = None

while True:
    if photo:
        #camera.annotate_text = "Press button to take your photo"
        #logger.info("waiting for button press")
	overlay_image = Image.open(photo).convert('RGBA')
	pad = Image.new('RGB', _pad(camera.resolution))
        pad.paste(overlay_image, (0, 0))
        #overlay = camera.add_overlay(pad.tobytes(), alpha=100, layer=3)
        overlay = camera.add_overlay(pad.tobytes())
        camera.preview.alpha = 0

        #overlay = camera.add_overlay(overlay_image.tobytes())
        #button.wait_for_press()
        #logger.info("button pressed")
        sleep(5)
        camera.remove_overlay(overlay)
        camera.preview.alpha = 255
        
    camera.annotate_text = "Press button to take photo"
    button.wait_for_press()
    logger.info("button pressed")
    button.wait_for_release()
    logger.info("button released")
    #sleep(1)
    countdown(3)
    logger.info("capturing photo")
    photo = camera.capture()
    logger.info("captured photo: {}".format(photo))
    camera.annotate_text = None
