from flask import Flask, make_response, jsonify, request, abort
from picamera2 import Picamera2
from PIL import Image, ImageDraw, ImageOps, ImageFilter, ImageEnhance, ImageChops, ImageFont
from time import sleep, time
import shutil
from OpenScan import load_int, load_float, load_bool, ringlight
import RPi.GPIO as GPIO
from math import sqrt
import os
import math
from skimage import io, feature, color, transform
import numpy as np
from scipy import ndimage

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

app = Flask(__name__)

basedir = '/home/pi/OpenScan/'
timer = time()
cam_mode = 0

def overlay_mask(image, mask_image):
    # Ensure image is in RGB mode
    image_rgb = image.convert('RGB')
    # Create an empty image with RGBA channels
    overlay = Image.new('RGBA', image_rgb.size)

    # Prepare a red image of the same size
    red_image = Image.new('RGB', image_rgb.size, (255, 0, 0))
    # Prepare a mask where the condition is met (mask_image pixels == 255)
    mask_condition = np.array(mask_image) > 0
    overlay_mask = Image.fromarray(np.uint8(mask_condition) * 255)
    # Paste the red image onto the overlay using the condition mask
    overlay.paste(red_image, mask=overlay_mask)
    # Combine the original image with the overlay
    combined = Image.alpha_composite(image_rgb.convert('RGBA'), overlay)
    # Convert the final image to RGB
    combined_rgb = combined.convert('RGB')
    return combined_rgb



def highlight_sharpest_areas(image, threshold=load_int('cam_sharpness'), dilation_size=5):
    # Convert PIL image to grayscale
    image_gray = image.convert('L')

    # Convert grayscale image to numpy array
    image_array = np.array(image_gray)

    # Calculate the gradient using a Sobel filter
    dx = ndimage.sobel(image_array, 0)  # horizontal derivative
    dy = ndimage.sobel(image_array, 1)  # vertical derivative
    mag = np.hypot(dx, dy)  # magnitude

    # Threshold the gradient to create a mask of the sharpest areas
    mask = np.where(mag > threshold, 255, 0).astype(np.uint8)

    dilated_mask = ndimage.binary_dilation(mask, structure=np.ones((dilation_size,dilation_size)))
    # Create a PIL image from the mask
    mask_image = Image.fromarray(dilated_mask)

    return mask_image




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

def plot_orb_keypoints(pil_image):
    downscale = 2
    # Read the image from the given image path
    image = np.array(pil_image)
    #image = io.imread(image_path)
    image = transform.resize(image, (image.shape[0] // downscale, image.shape[1] // downscale), anti_aliasing=True)

    # Convert the image to grayscale
    gray_image = color.rgb2gray(image)

    try:
        orb = feature.ORB(n_keypoints=10000, downscale=1.2, fast_n=2, fast_threshold=0.2 , n_scales=3, harris_k=0.001)
        orb.detect_and_extract(gray_image)
        keypoints = orb.keypoints
    except:
        return pil_image

    # Convert the image back to the range [0, 255]
    display_image = (image * 255).astype(np.uint8)

    # Draw the keypoints on the image
    draw = ImageDraw.Draw(pil_image)
    size = max(2,int(image.shape[0]*downscale*0.005))
    for i, (y, x) in enumerate(keypoints):
        draw.ellipse([(downscale*x-size, downscale*y-size), (downscale*x+size, downscale*y+size)], fill = (0,255,0))
    # Save the image with keypoints to the given output path
    return pil_image

def add_histo(img):
    histo_size = 241

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

    text = ""
    if min(histogram[235:238])>0:
        text = "overexposed"
    if sum(histogram[190:192])<8:
        text = "underexposed"
    font = ImageFont.truetype("DejaVuSans.ttf", 30)

    bbox = draw.textbbox((0, 0), text, font=font)

    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]


    x = (hist_image.width - text_width )/2
    y = hist_image.height - text_height - 10
    draw.text((x, y), text, font=font, fill=(255,0,0))

    scale = 0.25
    width1, height1 = hist_image.size
    width2 = img.size[0]
    new_width1 = int(width2 * scale)
    new_height1 = int((height1 / width1) * new_width1)
    hist_image = hist_image.convert('RGB')

    hist_image = hist_image.resize((new_width1, new_height1))
    x = hist_image.width - text_width - 10
    y = hist_image.height - text_height - 10


    img.paste(hist_image, (img.size[0]-new_width1-int(0.01*img.size[0]),img.size[1]-new_height1-int(0.01*img.size[0])))

    return img

def create_mask(image: Image, scale: float = 0.1, threshold: int = 45) -> Image:
    threshold = load_int("cam_mask_threshold")
    if threshold <= 1:
        return image
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

#    preview_config = picam2.create_preview_configuration(main={"size": (2328, 1748)})
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

    if load_bool("cam_features") and not load_bool("cam_sharparea"):
        img = plot_orb_keypoints(img)

    if load_bool("cam_sharparea") and not load_bool("cam_features"):
        img2 = highlight_sharpest_areas(img)
        img = overlay_mask(img, img2)

    if cam_mode != 1 and not  load_bool("cam_sharparea") and not load_bool("cam_features"):
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
