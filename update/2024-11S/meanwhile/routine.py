# The contents of this file are embedded in the OpenScan app (Node-RED)
from OpenScan import load_bool, load_str, load_int, load_float, motorrun, sort_spherical_coordinates_deg, create_coordinates, take_photo, save, \
    load_bool, camera
from time import sleep, strftime, time
from subprocess import getoutput, run

from zipfile import ZipFile, ZIP_DEFLATED
from os import system, uname
from os.path import isfile, getsize
import math
import threading
import numpy as np
import json

if load_str("status_internal_cam") == "no camera found" or load_str("status_internal_cam")[:5] == "Featu":
    return

save('status_internal_cam', 'Routine-preparing')
camera('/v1/camera/picam2_switch_mode?mode=1')

save('cam_sharparea', False)
save('cam_features', False)

projectname = load_str("routine_projectname")
angle_max = load_int('rotor_anglemax')
angle_min = load_int('rotor_anglemin')
if load_bool('rotor_enable_endstop'):
    angle_start = load_int('rotor_endstop_angle')
    motorrun('rotor',angle_start/abs(angle_start) * 130, True, False)

else:
    angle_start = load_int('rotor_anglestart')


photocount = load_int('routine_photocount')

focus_min = load_float('cam_focus_min')
focus_max = load_float('cam_focus_max')
stacksize = load_int('cam_stacksize')
group_stack_photos = load_bool('group_stack_photos')

telegram_enable = load_bool('telegram_enable')
if telegram_enable:
    telegram_api_token = load_str('telegram_api_token')
    telegram_client_id = load_str('telegram_client_id')

if focus_min == focus_max:
    stacksize = 1

focuslist = []
if stacksize == 1:
    steps = 3 + int(abs(focus_max-focus_min)*0.8)
else:
    steps = stacksize

for i in range (steps):
    focuslist.append(min(focus_min,focus_max) + i * abs(focus_max-focus_min)/(steps-1))

msg['focuslist'] = focuslist
msg['payload2'] = []
counter = 0

basepath = '/home/pi/OpenScan/'
temppath = basepath + 'tmp2/preview.jpg'
zippath = basepath + 'tmp.zip'

projectcode = strftime('20%y-%m-%d_%H.%M.%S-') + projectname

if isfile(zippath):
    system('rm ' + zippath)
sleep(1)

coordinates = create_coordinates(angle_min, angle_max, photocount)
coordinates = sort_spherical_coordinates_deg(coordinates)

msg['payload'] = coordinates

position_last = (angle_start, 0)

zip = ZipFile(zippath, "a", ZIP_DEFLATED, allowZip64=True)

hostname = str(uname()[1])

starttime = time()

def get_eta(starttime, photocounter, count):
    return str(int((photocount / counter - 1) * (time() - starttime))) + '/' + str(
        int(photocount / counter * (time() - starttime))) + 's'

def photo(counter2):
    camera('/v1/camera/picam2_take_photo')
    returning[0] = focus(returning[0])
    zip.write(temppath, projectname + '_' + str(counter) + ".jpg")

def stack_photo(i):
    
    camera('/v1/camera/picam2_take_photo')
    if group_stack_photos:
        name = projectname + '_' + str(counter) + "/" + projectname + '_' + str(counter) + '-' + str(i) + '.jpg'
    else:
        name = projectname + '_' + str(counter) + '-' + str(i) + '.jpg'
    zip.write(temppath, name)
    
def stack_focus(i):
    sleep(load_float('cam_shutter')/1000000*2)
    if i < len(focuslist)-1:
        camera('/v1/camera/picam2_focus?focus=' + str(focuslist[i+1]))
    else:
        camera('/v1/camera/picam2_focus?focus=' + str(focuslist[0]))
    sleep(1.7)

def photo_stack():
    camera('/v1/camera/picam2_focus?focus=' + str(focuslist[0]))
    for i in range(len(focuslist)):
        if load_str('status_internal_cam') == "Routine-stopping":
            break
        save('status_internal_cam', 'Routine-Photo ' + str(counter) + '/' + str(photocount) + "-F"+ str(i+1))
        
        focus_thread = threading.Thread(target=stack_focus, args=(i,))
        photo_thread = threading.Thread(target=stack_photo, args=(i,))
        
        focus_thread.start()
        photo_thread.start()
        
        focus_thread.join()
        photo_thread.join()



def move_motor():
    rotor_angle = position[0] - position_last[0]
    msg['payload2'].append(rotor_angle)
    #if abs(rotor_angle) > 180:
    #    rotor_angle = -360 * rotor_angle / abs(rotor_angle) + rotor_angle
    tt_angle = position_last[1] - position[1]
    if tt_angle > 180:
        tt_angle -= 360
    elif tt_angle < -180:
        tt_angle += 360

    motorrun('tt',tt_angle)
    motorrun('rotor',rotor_angle)
    return

    # THE FOLLOWING DOES NOT WORK PROPERLY WITH THREADING ?!

    #tt_thread = threading.Thread(target=motorrun, args=('tt', tt_angle))
    #rotor_thread = threading.Thread(target=motorrun, args=('rotor', rotor_angle))
    #tt_thread.start()
    #rotor_thread.start()
    #tt_thread.join()
    #rotor_thread.join()


counter2 = 0

def check_diskspace():
    diskspace_threshold = load_int('diskspace_threshold')
    diskspace = getoutput('df -h / | awk "{print $5}"').split('\n')[1]
    available = int(float(diskspace.replace(' ','').split('G')[2])*1000)
    if available < diskspace_threshold:
        save('status_internal_cam', 'Routine-stopping')
    return

def focus(i):
    f = focuslist[i]
    camera('/v1/camera/picam2_focus?focus=' + str(f))
    if i < len(focuslist) - 1:
        i += 1
    else:
        i = 0
    return i

def send_telegram_message(message, telegram_api_token, telegram_client_id):
    telegram_bot_path = '/usr/local/bin/send-telegram'
    run([telegram_bot_path,"-a",telegram_api_token,"-c",telegram_client_id,"-m",message])

if telegram_enable:
    telegram_message = "[START] " + hostname + " starting " + projectname + "(" + str(photocount) + " photos) ETA: "
    try:
        send_telegram_message(telegram_message, telegram_api_token, telegram_client_id)
    except Exception as e:
        print(e)
for position in coordinates:
    counter += 1
    filepath = basepath + 'tmp/' + projectname + '_' + str(counter) + ".jpg"
    if load_str('status_internal_cam') == "Routine-stopping":
        break
    if counter < 6:
        ETA = ''

    save('status_internal_cam', 'Routine-Photo ' + str(counter) + '/' + str(photocount) + ETA)
    if counter > 6:
        check_diskspace()

    move_motor()
    sleep(load_float("cam_delay_before"))
    
    if stacksize ==1:
        returning = [counter2]
        photo(returning)
        counter2 = returning[0]

    else:
        photo_stack()

    sleep(load_float("cam_delay_after"))
    ETA = '-ETA:' + str(int((photocount / counter - 1) * (time() - starttime))) + '/' + str(
            int(photocount / counter * (time() - starttime))) + 's'
    
    status = {
        "projectname": projectname,
        "total_photos": photocount,
        "current_photo": counter,
        "stacksize": steps,
        "start_time": int(starttime),
        
    }
    with open('/tmp/status.json', 'w') as status_file:
        json.dump(status, status_file)

    position_last = position

zip.close()
try:
    send_telegram_message("[STOP] " + hostname + " stop " + projectname, telegram_api_token, telegram_client_id)
except Exception as e:
    print(e)
camera('/v1/camera/picam2_switch_mode?mode=0')

save('status_internal_cam', 'Routine-done')

# Delete the status.json file
import os

try:
    os.remove('/tmp/status.json')
except FileNotFoundError:
    pass  # File doesn't exist, so no need to delete
except Exception as e:
    print(f"Error deleting /tmp/status.json: {e}")


motorrun('rotor', -position_last[0] )
motorrun('tt', position_last[1])

save('status_internal_cam', '--READY--')

system('mv ' + zippath + " " + basepath + "scans/" + projectcode + ".zip")

return msg
