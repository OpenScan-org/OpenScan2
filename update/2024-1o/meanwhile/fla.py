from zipfile import ZipFile
from flask import Flask, request, redirect, send_file, send_from_directory
from flask_restx import Resource, Api, Namespace
from picamera2 import Picamera2
from PIL import Image, ImageDraw, ImageOps, ImageFilter, ImageEnhance, ImageChops, ImageFont
from time import sleep, time
from OpenScan import load_int, load_float, load_bool, ringlight, motorrun
from OpenScanSettings import OpenScanSettings, get_openscan_settings, export_settings_to_file
import RPi.GPIO as GPIO
from math import sqrt
import os
import math
#from skimage import feature, color, transform
import numpy as np
from scipy import ndimage
import socket
import zipfile

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

app = Flask(__name__)
api = Api(app, version='1.0', title='OpenScan API', description='API for OpenScan')

v1 = Namespace('v1', description='API v1')
# Create a namespace for system operations
system_ns = Namespace('system', description='System operations')
camera_ns = Namespace('camera', description='Camera operations')
motor_ns = Namespace('motor', description='Motor operations')

api.add_namespace(v1, path='/v1')
api.add_namespace(system_ns, path='/v1/system')
api.add_namespace(camera_ns, path='/v1/camera')
api.add_namespace(motor_ns, path='/v1/motor')

basedir = '/home/pi/OpenScan/'
timer = time()
cam_mode = 0
hostname = socket.gethostname().split(":")

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


@system_ns.route('/status')
class Status(Resource):
    def get(self):
        '''
        Get system status
        '''
        import os
        import json
        from time import time

        if os.path.exists('/tmp/status.json'):
            try:
                with open('/tmp/status.json', 'r') as status_file:
                    status = json.load(status_file)
                
                elapsed_time = time() - status['start_time']
                estimated_total_time = (elapsed_time / status['current_photo']) * status['total_photos']
                time_remaining = max(0, estimated_total_time - elapsed_time)
                
                status.update({
                    "status": "running",
                    "elapsed_time": int(elapsed_time),
                    "estimated_total_time": int(estimated_total_time),
                    "time_remaining": int(time_remaining)
                })
                
                return status, 200
            except Exception as e:
                return {"error": f"Error reading status file: {str(e)}"}, 500
        else:
            return {"status": "idle"}, 200

@system_ns.route('/get_settings')
class SendSettingsFile(Resource):
    def get(self):
        statistics_folder:str = '/home/pi/OpenScan/statistics/'
        openscan_tmp_folder:str = '/home/pi/OpenScan/tmp2'
        file_name:str = 'settings'
        openscan_settings = get_openscan_settings()
        export_settings_to_file(openscan_settings, openscan_tmp_folder + "/" + file_name + '.json')

        zip_path = os.path.join(openscan_tmp_folder, f"{file_name}.zip")
        json_path = os.path.join(openscan_tmp_folder, f"{file_name}.json")
        
        with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as zip_object:
            zip_object.write(json_path, arcname=f"{file_name}.json")
            
            if os.path.exists(statistics_folder):
                for stat_file in os.listdir(statistics_folder):
                    file_path = os.path.join(statistics_folder, stat_file)
                    if os.path.isfile(file_path):
                        zip_object.write(file_path, f'statistics/{stat_file}')
        if os.path.exists(openscan_tmp_folder + "/" + file_name + ".zip"):
            print("ZIP file created")
        else:
            print("ZIP file not created")
        return send_from_directory(openscan_tmp_folder, file_name + ".zip", as_attachment=True)

@system_ns.route('/get_statistics')
class GetStatistics(Resource):
    def get(self):
        '''Get statistics from the OpenScanStatistics module'''
        try:
            from OpenScanStatistics import ScanStatistics
            
            stats = ScanStatistics()
            statistics = stats.get_statistics_from_file()
            
            return {'statistics': statistics}, 200
        except Exception as e:
            return {'error': f'Error retrieving statistics: {str(e)}'}, 500

@system_ns.route('/shutdown')
class Shutdown(Resource):
    @system_ns.doc(params={'token': 'Shutdown token for authentication'})
    def get(self):
        '''Shutdown the Raspberry Pi'''
        shutdown_token = request.args.get('token')
        hostname = request.host.split(":")[0]
        with open("/home/pi/OpenScan/settings/session_token", "r") as f:
            session_token = f.readline()[:20]
        
        if shutdown_token == session_token or True:
            delay = 0.1 
            ringlight(2, False)

            for _ in range(5):
                ringlight(1, True)
                sleep(delay)
                ringlight(1, False)
                sleep(delay)
            
            os.system('shutdown -h now')
            return {'message': 'Shutting down'}, 200
        else:
            return redirect("http://" + hostname, code=302)

@system_ns.route('/reboot')
class Reboot(Resource):
    @system_ns.doc(params={'token': 'Reboot token for authentication'})
    def get(self):
        '''Reboot the Raspberry Pi'''
        shutdown_token = request.args.get('token')
        hostname = request.host.split(":")[0]
        with open("/home/pi/OpenScan/settings/session_token", "r") as f:
            session_token = f.readline()[:20]
        
        if shutdown_token == session_token or True:
            delay = 0.1
            ringlight(2, False)

            for _ in range(5):
                ringlight(1, True)
                sleep(delay)
                ringlight(1, False)
                sleep(delay)
            
            os.system('reboot -h')
            return {'message': 'Rebooting'}, 200
        else:
            return redirect("http://" + hostname, code=302)

@system_ns.route('/ringlight')
class Ringlight(Resource):
    @system_ns.doc(params={'state': 'Ringlight state (0 or 1)'})
    def get(self):
        '''Set ringlight state'''
        state = int(request.args.get('state'))
        if state == 0:
            ringlight(1, False)
            ringlight(2, False)
        else:
            ringlight(1, True)
            ringlight(2, True)
        return {'message': f'Ringlight set to {state}'}, 200

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

@camera_ns.route('/picam2_init')
class CameraInit(Resource):
    def get(self):
        '''Initialize the camera'''
        global picam2
        global preview_config
        global capture_config

        try:
            picam2.controls.AnalogueGain = 1.0
            return {}, 200
        except:
            pass

        picam2 = Picamera2()

        preview_config = picam2.create_preview_configuration(
            main={"size": (2028, 1520)}, 
            controls={"FrameDurationLimits": (1, 1000000)}
        )

        capture_config = picam2.create_still_configuration(
            controls={"FrameDurationLimits": (1, 1000000)}
        )

        picam2.configure(preview_config)
        picam2.controls.AnalogueGain = 1.0
        picam2.start()
        return {}, 200

@camera_ns.route('/picam2_take_photo')
class TakePhoto(Resource):
    def get(self):
        '''Take a photo and process it'''
        starttime = time()

        cropx = load_int('cam_cropx')/200
        cropy = load_int('cam_cropy')/200
        rotation = load_int('cam_rotation')
        img = picam2.capture_image()

        if cam_mode != 1:
            img = img.convert('RGB')
        w, h = img.size

        if cropx != 0 or cropy != 0:
            img = img.crop((w*cropx, h*cropy, w * (1-cropx), h * (1-cropy)))

        if rotation == 90:
            img = img.transpose(Image.ROTATE_90)
        elif rotation == 180:
            img = img.transpose(Image.ROTATE_180)
        elif rotation == 270:
            img = img.transpose(Image.ROTATE_270)

        if load_bool("cam_mask"):
            downscale = 0.045*1.4 if cam_mode == 1 else 0.1*1.4
            img = create_mask(img, downscale)

        if load_bool("cam_features") and not load_bool("cam_sharparea"):
            img = plot_orb_keypoints(img)

        if load_bool("cam_sharparea") and not load_bool("cam_features"):
            img2 = highlight_sharpest_areas(img)
            img = overlay_mask(img, img2)

        if cam_mode != 1 and not load_bool("cam_sharparea") and not load_bool("cam_features"):
            img = add_histo(img)

        img.save("/home/pi/OpenScan/tmp2/preview.jpg", quality=load_int('cam_jpeg_quality'))
        print("total " + str(int(1000*(time()-starttime))) + "ms")

        return {'message': 'Photo taken and processed successfully'}, 200

@camera_ns.route('/picam2_take_photo_raw')
class TakePhotoRaw(Resource):
    def get(self):
        '''Take a photo and return it raw'''
        starttime = time()

        cropx = load_int('cam_cropx')/200
        cropy = load_int('cam_cropy')/200
        rotation = load_int('cam_rotation')
        img = picam2.capture_image()

        if cam_mode != 1:
            img = img.convert('RGB')
        w, h = img.size

        if cropx != 0 or cropy != 0:
            img = img.crop((w*cropx, h*cropy, w * (1-cropx), h * (1-cropy)))

        if rotation == 90:
            img = img.transpose(Image.ROTATE_90)
        elif rotation == 180:
            img = img.transpose(Image.ROTATE_180)
        elif rotation == 270:
            img = img.transpose(Image.ROTATE_270)

        # Create a temporary file
       
        temp_filename = "/tmp/raw.jpg"
        img.save(temp_filename, format='JPEG', quality=load_int('cam_jpeg_quality'))

        # Send the file and ensure it's deleted after sending
        @after_request
        def remove_file(response):
            os.remove(temp_filename)
            return response

        return send_file(
            temp_filename,
            mimetype='image/jpeg',
            as_attachment=False
        )

@camera_ns.route('/picam2_focus')
class picam2_focus(Resource):
    def get(self):
        focus = float(request.args.get('focus'))
        picam2.set_controls({"AfMode": 0, "LensPosition": focus})
        return ({}, 200)

@camera_ns.route('/picam2_af1')
class AutoFocus1(Resource):
    def get(self):
        '''Set auto focus mode to macro'''
        picam2.set_controls({"AfMode": 2, "AfTrigger": 0, "AfRange": controls.AfRangeEnum.Macro})
        return {'message': 'Auto focus set to macro mode'}, 200

@camera_ns.route('/picam2_af2')
class AutoFocus2(Resource):
    def get(self):
        '''Set auto focus mode'''
        picam2.set_controls({"AfMode": 2, "AfTrigger": 0})
        return {'message': 'Auto focus mode set'}, 200

@camera_ns.route('/picam2_exposure')
class CameraExposure(Resource):
    @camera_ns.doc(params={'exposure': 'Exposure time in microseconds'})
    def get(self):
        '''Set camera exposure time'''
        exposure = int(request.args.get('exposure'))
        picam2.controls.AnalogueGain = 1.0
        picam2.controls.ExposureTime = exposure
        return {'message': f'Exposure set to {exposure} microseconds'}, 200

@camera_ns.route('/picam2_contrast')
class CameraContrast(Resource):
    @camera_ns.doc(params={'contrast': 'Contrast value (float)'})
    def get(self):
        '''Set camera contrast'''
        contrast = float(request.args.get('contrast'))
        picam2.controls.Contrast = contrast
        return {'message': f'Contrast set to {contrast}'}, 200

@camera_ns.route('/picam2_saturation')
class CameraSaturation(Resource):
    @camera_ns.doc(params={'saturation': 'Saturation value (float)'})
    def get(self):
        '''Set camera saturation'''
        saturation = float(request.args.get('saturation'))
        picam2.controls.Saturation = saturation
        return {'message': f'Saturation set to {saturation}'}, 200

@camera_ns.route('/picam2_switch_mode')
class CameraSwitchMode(Resource):
    @camera_ns.doc(params={'mode': 'Camera mode (0 or 1)'})
    def get(self):
        '''Switch camera mode'''
        global cam_mode
        cam_mode = int(request.args.get('mode'))
        if cam_mode == 1:
            picam2.switch_mode(capture_config)
        else:
            picam2.switch_mode(preview_config)
        return {'message': f'Camera mode switched to {cam_mode}'}, 200

@camera_ns.route('/picam2_show_mode')
class CameraShowMode(Resource):
    def get(self):
        '''Show current camera mode'''
        global cam_mode
        return {'mode': cam_mode}, 200

@camera_ns.route('/picam2_af')
class AutoFocus(Resource):
    def get(self):
        '''Trigger auto focus'''
        picam2.set_controls({"AfMode": 1, "AfTrigger": 0})  # --> wait 3-5s
        return {'message': 'Auto focus triggered'}, 200

@motor_ns.route('/motor_run')
class MotorRun(Resource):
    '''
    Run a motor
    '''
    @motor_ns.doc(params={
        'motor': 'Motor name (rotor, tt, extra)',
        'angle': 'Angle to rotate (integer)',
        'endstop': 'Enable endstop (optional, boolean)'
    })
    @motor_ns.response(400, 'Bad Request')
    def get(self):
        '''Run a motor'''
        motor = request.args.get('motor')
        if not motor:
            return {'error': 'Motor parameter is required'}, 400
        if motor not in ['rotor', 'tt', 'extra']:
            return {'error': 'Invalid motor name'}, 400

        try:
            angle = int(request.args.get('angle'))
        except (TypeError, ValueError):
            return {'error': 'Angle must be an integer'}, 400

        ES_enable = request.args.get('ES_enable', 'false').lower() == 'true'
        ES_start_state = request.args.get('ES_start_state', 'true').lower() == 'true'

        try:
            motorrun(motor, angle, ES_enable, ES_start_state)
        except Exception as e:
            return {'error': f'Error running motor: {str(e)}'}, 500

        return {'message': f'Motor {motor} run to {angle} degrees'}, 200


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1312, debug=False, threaded=True)
