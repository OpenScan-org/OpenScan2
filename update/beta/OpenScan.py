basepath = '/home/pi/OpenScan/'
from os.path import isfile

def load_bool(name):
    filename = basepath+'settings/'+name
    if not isfile(filename):
        return
    with open(filename, 'r') as file:
        value = file.read().replace('\n','')
    if value == '1' or value == 'True' or value =='true':
        value = True
    else:
        value = False
    return value

def load_str(name):
    filename = basepath+'settings/'+name
    if not isfile(filename):
        return
    with open(filename, 'r') as file:
        value = file.read().replace('\n','')
    return value

def load_int(name):
    filename = basepath+'settings/'+name
    if not isfile(filename):
        return
    with open(filename, 'r') as file:
        value = int(file.read().replace('\n',''))
    return value

def load_float(name):
    filename = basepath+'settings/'+name
    if not isfile(filename):
        return
    with open(filename, 'r') as file:
        value = float(file.read().replace('\n',''))
    return value

def save(name, value):
    filename = basepath+'settings/'+name
    with open(filename, 'w+') as file:
        file.write(str(value))
    return

def OpenScanCloud(cmd, msg):
    from requests import get
    osc_user = 'openscan'
    osc_pw = 'free'
    osc_server = 'http://openscanfeedback.dnsuser.de:1334/'

    try:
        r = get(osc_server + cmd, auth=(osc_user, osc_pw), params=msg)
    except:
        r = type('obj', (object,), {'status_code' : 404, 'text':None})
    return r

def camera(cmd, msg = {}):
    from requests import get
    flask = 'http://127.0.0.1:1312/'
    try:
        r = get(flask + cmd, params=msg)
        return r.status_code
    except:
        return 400

def motorrun(motor,angle):
    import RPi.GPIO as GPIO
    from time import sleep
    from math import cos
    msg = {'cmd':'set'}
    camera('/ping', msg)

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    spr = load_int(motor + '_stepsperrotation')
    dirpin = load_int('pin_' + motor + '_dir')
    steppin = load_int('pin_' + motor +'_step')
    dir = load_int(motor + '_dir')
    ramp = load_int(motor + '_accramp')
    acc = load_float(motor + '_acc')
    delay_init = load_float(motor + '_delay')
    delay = delay_init

    step_count=int(angle*spr/360) * dir
    GPIO.setup(dirpin, GPIO.OUT)
    GPIO.setup(steppin, GPIO.OUT)
    if (step_count>0):
        GPIO.output(dirpin, GPIO.HIGH)
    if(step_count<0):
        GPIO.output(dirpin, GPIO.LOW)
        step_count=-step_count
    for x in range(step_count):
        GPIO.output(steppin, GPIO.HIGH)
        if x<=ramp and x<=step_count/2:
            delay = delay_init * (1 + -1/acc*cos(1*(ramp-x)/ramp)+1/acc)
            #delay=delay_init+(ramp-x)*(delay_init)/acc
        elif step_count-x<=ramp and x>step_count/2:
            delay = delay_init * (1-1/acc*cos(1*(ramp+x-step_count)/ramp)+1/acc)
            #delay=delay_init+(ramp-step_count+x)*(delay_init)/acc
        else:
            delay = delay_init
        sleep(delay)
        GPIO.output(steppin, GPIO.LOW)
        sleep(delay)

def ringlight(number,state):
    import RPi.GPIO as GPIO
    msg = {'cmd':'set'}
    camera('/ping', msg)
    pin = load_int('pin_ringlight' + str(number))
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, state)

def take_photo(file):
    from os import system
    filepath = basepath + file

    model=load_str('model')



    shutter = str(load_int('cam_shutter'))
    saturation = load_str('cam_saturation')
    contrast = load_str('cam_contrast')
    awbg_red = load_str('cam_awbg_red')
    awbg_blue = load_str('cam_awbg_blue')
    gain = load_str('cam_gain')
    quality = load_int('cam_jpeg_quality')
    filepath2 = '/home/pi/OpenScan/tmp/tmp.jpg'
    #width = load_str('cam_resx')
    #height = load_str('cam_resy')
    timeout = load_str('cam_timeout')
    cropx = load_int('cam_cropx')/200
    cropy = load_int('cam_cropy')/200
    rotation = load_int('cam_rotation')
    AF = load_bool('cam_AFmode')
    camera = load_str('camera')


    if camera == 'imx519' and AF == True:
        autofocus = ' --autofocus '
    else:
        autofocus = ''

    if camera  == "usb_webcam":
        cmd = 'fswebcam -i 0 -r "1280x720" -F 5 --no-banner --jpeg 95 --save ' + filepath2
    else:
        cmd = 'libcamera-still -n --denoise off --sharpness 0 -o ' + filepath2 + ' -t ' + timeout  +' --shutter ' + shutter + ' --saturation ' + saturation + ' --contrast ' + contrast + ' --awbgains '+awbg_red + "," + awbg_blue + ' --gain ' + gain + ' -q ' + str(quality) + autofocus + ' >/dev/null 2>&1'
    #    cmd = 'libcamera-still -n --denoise off --sharpness 0 -o ' + filepath2 + ' -t ' + timeout  +' --shutter ' + shutter + ' --saturation ' + saturation + ' --contrast ' + contrast + ' --awbgains '+awbg_red + "," + awbg_blue + ' --gain ' + gain + ' -q ' + str(quality) + autofocus
        
    system(cmd)
    return cmd

def get_points(samples=1):
    from math import pi, sqrt, acos, atan2, cos, sin

    points = []
    phi = pi * (3. - sqrt(5.))
    for i in range(int(samples)):
        y = 1 - (i / float(samples - 1)) * 2
        radius = sqrt(1 - y * y)
        theta = phi * i
        x = cos(theta) * radius
        z = sin(theta) * radius
        r=sqrt(x*x+y*y+z*z)
        theta_neu=acos(z/r)*180/pi
        phi_neu=atan2(y,x)*180/pi
        points.append((theta_neu-90,phi_neu))
    points.sort()
    return points

def create_coordinates(angle_min, angle_max,point_count):
    point_count_final=point_count
    if angle_max < angle_min:
        a = angle_min
        angle_min = angle_max
        angle_max = a
    point_count=point_count*90/(angle_max-angle_min)
    actual_points=0
    while actual_points<point_count_final:
        points=get_points(point_count)
        filtered=[]
        for x,y in points:
            if x>angle_min and x<angle_max and len(filtered)<point_count_final:
                filtered.append((x,y))
        actual_points=len(filtered)

        if point_count-actual_points>20:
            point_count=point_count+3
        else:
            point_count=point_count+1
    return filtered

