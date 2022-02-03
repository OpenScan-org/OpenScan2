from flask import Flask, make_response, jsonify, request, abort
from PIL import Image
import gphoto2 as gp
from time import sleep
import shutil
from OpenScan import load_int, load_float, load_bool
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

app = Flask(__name__)

basedir = '/home/pi/OpenScan/'

###################################################################################################################
@app.route('/gphoto_init', methods=['get'])
def gphoto_init():
    global camera
    camera = gp.Camera()
    camera.init()
    return ({}, 200)
###################################################################################################################
@app.route('/gphoto_preview', methods=['get'])
def gphoto_preview():
    filepath = str(request.args.get('filepath'))
    camera_file = gp.gp_camera_capture_preview(camera)[1]
    target = basedir + filepath
    camera_file.save(target)
    return ({}, 200)
###################################################################################################################
@app.route('/gphoto_capture', methods=['get'])
def gphoto_capture():
    filepath = str(request.args.get('filepath'))
    file_path = camera.capture(gp.GP_CAPTURE_IMAGE)
    camera_file = camera.file_get(file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL)
    camera_file.save(basedir + filepath)
    return ({}, 200)
###################################################################################################################
@app.route('/gphoto_test', methods=['get'])
def gphoto_test():
    text = camera.get_summary()
    return ({}, 200)
###################################################################################################################
@app.route('/gphoto_exit', methods=['get'])
def gphoto_exit():
    global camera
    camera.exit()
    return ({}, 200)
###################################################################################################################
@app.route('/crop', methods=['get'])
def crop():
    filepath_in = basedir + str(request.args.get('filepath_in'))
    filepath_out = basedir + str(request.args.get('filepath_out'))
    cropx = int(request.args.get('cropx'))/200
    cropy = int(request.args.get('cropy'))/200
    rotation = int(request.args.get('rotation'))
    if cropx == 0 and cropy == 0 and rotation ==  0:
        shutil.copy(filepath_in, filepath_out)
    else:
        with Image.open(filepath_in) as img:
            w, h = img.size
            if cropx != 0 or cropy != 0:
                img = img.crop((w*cropx, h*cropy, w * (1-cropx), h * (1-cropy)))
            if rotation == 90:
                img  = img.transpose(Image.ROTATE_90)
            elif rotation == 180:
                img= img.transpose(Image.ROTATE_180)
            elif rotation == 270:
                img= img.transpose(Image.ROTATE_270)
            img.save(filepath_out, quality=95, subsampling=0)
    return ({}, 200)

###################################################################################################################
@app.route('/external_capture', methods=['get'])
def external_capture():
    pin = load_int('pin_external')
    delay_before = load_float('cam_delay_before')
    timeout = load_float('cam_timeout')/1000
    delay_after = load_float('cam_delay_after')
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    sleep(delay_before)
    GPIO.output(pin, GPIO.HIGH)
    sleep(timeout)
    GPIO.output(pin, GPIO.LOW)
    sleep(delay_after)
    return ({}, 200)




if __name__ == '__main__':
#    app.run(host='127.0.0.1', port=1312, debug=False, threaded=True)
    app.run(host='0.0.0.0', port=1312, debug=False, threaded=True)
