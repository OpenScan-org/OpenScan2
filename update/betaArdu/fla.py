
from flask import Flask, make_response, jsonify, request, abort
from picamera2 import Picamera2
from PIL import Image, ImageDraw, ImageOps, ImageFilter, ImageEnhance, ImageChops
from time import sleep, time
import shutil
from OpenScan import load_int, load_float, load_bool, ringlight
import RPi.GPIO as GPIO
from math import sqrt
import os
import math

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

app = Flask(__name__)

basedir = '/home/pi/OpenScan/'
timer = time()
cam_mode = 0

###################################################################################################################
@app.route('/shutdown', methods=['get'])
def shutdown():
    delay = 0.1
    ringlight(2,False)

    for i in range (5):
        ringlight(1,True)
        sleep(delay)
        ringlight(1,False)
        sleep(delay)
    os.system('shutdown -h now')
###################################################################################################################
@app.route('/reboot', methods=['get'])
def reboot():
    delay = 0.1
    ringlight(2,False)

    for i in range (5):
        ringlight(1,True)
        sleep(delay)
        ringlight(1,False)
        sleep(delay)

    os.system('reboot -h')
###################################################################################################################
@app.route('/ping', methods=['get'])
def ping():
    global timer
    cmd = str(request.args.get('cmd'))
    if cmd == 'set':
        timer = time()
    inactive = time() - timer
    return ({'inactive':inactive}, 200)

def add_histo(img):
    histo_size = 200

    img_gray = ImageOps.grayscale(img)
    histogram = img_gray.histogram()
    histogram_log = [math.log10(h + 1) for h in histogram]
    histogram_max = max(histogram_log)
    histogram_normalized = [float(h) / histogram_max for h in histogram_log]
    hist_image = Image.new("RGBA", (histo_size, histo_size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(hist_image)

    for i in range(0, 256):
        x = i
        y = 256 - int(histogram_normalized[i] * 256)
        draw.line((x, 256, x, y), fill=(0, 0, 0, 255))

    img.paste(hist_image, (img.size[0] - histo_size, img.size[1] - histo_size))
    return img

def create_mask(image: Image, scale: float = 0.1, threshold: int = 45) -> Image:
    threshold = load_int("cam_mask_threshold")
    orig = image
    image = image.resize((int(image.width*scale),int(image.height*scale)))
    image = image.convert("L")
    reduced = image
    image = image.filter(ImageFilter.EDGE_ENHANCE)
    image = image.filter(ImageFilter.BLUR)
    reduced = reduced.filter(ImageFilter.EDGE_ENHANCE_MORE)
    mask = ImageChops.difference(image, reduced)
    mask = ImageEnhance.Brightness(mask).enhance(2.5)
    mask = mask.filter(ImageFilter.MaxFilter(9))
    mask = mask.filter(ImageFilter.MinFilter(5))
    mask = mask.point(lambda x: 255 if x <threshold else 0)
    mask = mask.filter(ImageFilter.MaxFilter(5))
    mask = mask.convert(orig.mode)
    mask = mask.resize((orig.width,orig.height), resample=Image.BOX)
    result = ImageChops.subtract(orig, mask)

    return result

###################################################################################################################
@app.route('/picam2_init', methods=['get'])
def picam2_init():
    global picam2
    global preview_config
    global capture_config

    try:
        picam2.controls.AnalogueGain = 1.0
        return ({}, 200)
    except:
        pass
    picam2 = Picamera2()

#    preview_config = picam2.create_preview_configuration(main={"size": (1280, 720)}) #--> wrong aspect ratio!
#    preview_config = picam2.create_preview_configuration(main={"size": (2028, 1520)})
    preview_config = picam2.create_preview_configuration(main={"size": (2028, 1520)}, controls ={"FrameDurationLimits": (1, 1000000)})

#   preview_config = picam2.create_preview_configuration(main={"size": (2328, 1748)})
    capture_config = picam2.create_still_configuration(controls ={"FrameDurationLimits": (1, 1000000)})
    picam2.configure(preview_config)
    picam2.controls.AnalogueGain = 1.0
    picam2.start()
    return ({}, 200)
###################################################################################################################
@app.route('/picam2_take_photo', methods=['get'])
def picam2_take_photo():
    starttime = time()

    cropx = load_int('cam_cropx')/200
    cropy = load_int('cam_cropy')/200
    rotation = load_int('cam_rotation')
    img = picam2.capture_image()

    if cam_mode !=1:
        img = img.convert('RGB')
    w,h = img.size

    if cropx != 0 or cropy != 0:
        img = img.crop((w*cropx, h*cropy, w * (1-cropx), h * (1-cropy)))

    if rotation == 90:
        img  = img.transpose(Image.ROTATE_90)
    elif rotation == 180:
        img= img.transpose(Image.ROTATE_180)
    elif rotation == 270:
        img= img.transpose(Image.ROTATE_270)

    if load_bool("cam_mask"):
        if cam_mode == 1:
            downscale = 0.045*1.4
        else:
            downscale = 0.1*1.4
        img = create_mask(img, downscale)

    if cam_mode != 1:
        img = add_histo(img)

    img.save("/home/pi/OpenScan/tmp2/preview.jpg", quality=load_int('cam_jpeg_quality'))
    print("total " + str(int(1000*(time()-starttime))) + "ms")
    starttime = time()




    return ({}, 200)
###################################################################################################################
@app.route('/picam2_focus', methods=['get'])
def picam2_focus():
    focus = float(request.args.get('focus'))
    picam2.set_controls({"AfMode": 0, "LensPosition": focus})
    return ({}, 200)
###################################################################################################################
@app.route('/picam2_af1', methods=['get'])
def picam2_af1():
    from libcamera import controls

    picam2.set_controls({"AfMode": 2 ,"AfTrigger": 0, "AfRange":controls.AfRangeEnum.Macro})
    return ({}, 200)
###################################################################################################################
@app.route('/picam2_af2', methods=['get'])
def picam2_af2():
    picam2.set_controls({"AfMode": 2 ,"AfTrigger": 0})
    return ({}, 200)





###################################################################################################################
@app.route('/picam2_exposure', methods=['get'])
def picam2_exposure():
    exposure = int(request.args.get('exposure'))
    picam2.controls.AnalogueGain = 1.0
    picam2.controls.ExposureTime = exposure
    return ({}, 200)
###################################################################################################################
@app.route('/picam2_contrast', methods=['get'])
def picam2_contrast():
    contrast = float(request.args.get('contrast'))
    picam2.controls.Contrast = contrast
    return ({}, 200)
###################################################################################################################
@app.route('/picam2_saturation', methods=['get'])
def picam2_saturation():
    saturation = float(request.args.get('saturation'))
    picam2.controls.Saturation = saturation
    return ({}, 200)
###################################################################################################################
@app.route('/picam2_switch_mode', methods=['get'])
def picam2_switch_mode():
    global cam_mode
    cam_mode = int(request.args.get('mode'))
    if cam_mode == 1:
        picam2.switch_mode(capture_config)
    else:
        picam2.switch_mode(preview_config)
    return ({}, 200)
###################################################################################################################
@app.route('/picam2_show_mode', methods=['get'])
def picam2_show_mode():
    global cam_mode
    return({"mode":cam_mode},200)
###################################################################################################################
@app.route('/picam2_af', methods=['get'])
def picam2_af():
    picam2.set_controls({"AfMode": 1 ,"AfTrigger": 0}) # --> wait 3-5s
    return ({}, 200)

if __name__ == '__main__':
#    app.run(host='127.0.0.1', port=1312, debug=False, threaded=True)
    app.run(host='0.0.0.0', port=1312, debug=False, threaded=True)
