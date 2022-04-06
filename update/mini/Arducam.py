import time
import os

try:
    import v4l2
except Exception as e:
    print(e)
    print("Try to install v4l2-fix")
    try:
        from pip import main as pipmain
    except ImportError:
        from pip._internal import main as pipmain
    pipmain(['install', 'v4l2-fix'])
    print("\nTry to run the focus program again.")
    exit(0)

import fcntl
import errno

# # Type
# v4l2.V4L2_CTRL_TYPE_INTEGER
# v4l2.V4L2_CTRL_TYPE_BOOLEAN
# v4l2.V4L2_CTRL_TYPE_MENU
# v4l2.V4L2_CTRL_TYPE_BUTTON
# v4l2.V4L2_CTRL_TYPE_INTEGER64
# v4l2.V4L2_CTRL_TYPE_CTRL_CLASS
# # Flags
# v4l2.V4L2_CTRL_FLAG_DISABLED
# v4l2.V4L2_CTRL_FLAG_GRABBED
# v4l2.V4L2_CTRL_FLAG_READ_ONLY
# v4l2.V4L2_CTRL_FLAG_UPDATE
# v4l2.V4L2_CTRL_FLAG_INACTIVE
# v4l2.V4L2_CTRL_FLAG_SLIDER

def assert_valid_queryctrl(queryctrl):
    return queryctrl.type & (
        v4l2.V4L2_CTRL_TYPE_INTEGER
        | v4l2.V4L2_CTRL_TYPE_BOOLEAN
        | v4l2.V4L2_CTRL_TYPE_MENU
        | v4l2.V4L2_CTRL_TYPE_BUTTON
        | v4l2.V4L2_CTRL_TYPE_INTEGER64
        | v4l2.V4L2_CTRL_TYPE_CTRL_CLASS
        | 7
        | 8
        | 9
    ) and queryctrl.flags & (
        v4l2.V4L2_CTRL_FLAG_DISABLED
        | v4l2.V4L2_CTRL_FLAG_GRABBED
        | v4l2.V4L2_CTRL_FLAG_READ_ONLY
        | v4l2.V4L2_CTRL_FLAG_UPDATE
        | v4l2.V4L2_CTRL_FLAG_INACTIVE
        | v4l2.V4L2_CTRL_FLAG_SLIDER
    )

def get_device_controls_menu(fd, queryctrl):
    querymenu = v4l2.v4l2_querymenu(queryctrl.id, queryctrl.minimum)
    while querymenu.index <= queryctrl.maximum:
        fcntl.ioctl(fd, v4l2.VIDIOC_QUERYMENU, querymenu)
        yield querymenu
        querymenu.index += 1

def get_device_controls_by_class(fd, control_class):
    # enumeration by control class
    queryctrl = v4l2.v4l2_queryctrl(control_class | v4l2.V4L2_CTRL_FLAG_NEXT_CTRL)
    while True:
        try:
            fcntl.ioctl(fd, v4l2.VIDIOC_QUERYCTRL, queryctrl)
        except IOError as e:
            assert e.errno == errno.EINVAL
            break
        if v4l2.V4L2_CTRL_ID2CLASS(queryctrl.id) != control_class:
            break
        yield queryctrl
        queryctrl = v4l2.v4l2_queryctrl(queryctrl.id | v4l2.V4L2_CTRL_FLAG_NEXT_CTRL)

def getdict(struct):
    val = dict((field, getattr(struct, field)) for field, _ in struct._fields_)
    val.pop("reserved")
    return val

def get_device_controls(fd):
    # original enumeration method
    queryctrl = v4l2.v4l2_queryctrl(v4l2.V4L2_CID_BASE)
    while queryctrl.id < v4l2.V4L2_CID_LASTP1:
        try:
            fcntl.ioctl(fd, v4l2.VIDIOC_QUERYCTRL, queryctrl)
            print(queryctrl.name)
        except IOError as e:
            # this predefined control is not supported by this device
            assert e.errno == errno.EINVAL
            queryctrl.id += 1
            continue
        queryctrl = v4l2.v4l2_queryctrl(queryctrl.id + 1)

def get_ctrls(vd):
    ctrls = []
    # enumeration by control class
    for class_ in (v4l2.V4L2_CTRL_CLASS_USER, v4l2.V4L2_CTRL_CLASS_MPEG, v4l2.V4L2_CTRL_CLASS_CAMERA):
        for queryctrl in get_device_controls_by_class(vd, class_):
            ctrl = getdict(queryctrl)
            if queryctrl.type == v4l2.V4L2_CTRL_TYPE_MENU:
                ctrl["menu"] = []
                for querymenu in get_device_controls_menu(vd, queryctrl):
                    # print(querymenu.name)
                    ctrl["menu"].append(querymenu.name)

            if queryctrl.type == 9:
                ctrl["menu"] = []
                for querymenu in get_device_controls_menu(vd, queryctrl):
                    ctrl["menu"].append(querymenu.index)
            ctrls.append(ctrl)
    return ctrls

def set_ctrl(vd, id, value):
    ctrl = v4l2.v4l2_control()
    ctrl.id = id
    ctrl.value = value
    try:
        fcntl.ioctl(vd, v4l2.VIDIOC_S_CTRL, ctrl)
    except IOError as e:
        print(e)

def get_ctrl(vd, id):
    ctrl = v4l2.v4l2_control()
    ctrl.id = id
    try:
        fcntl.ioctl(vd, v4l2.VIDIOC_G_CTRL, ctrl)
    except IOError as e:
        print(e)
        return None
    return ctrl.value


class Focuser:
    FOCUS_ID = 0x009a090a
    dev = None

    def __init__(self, dev=0):
        self.focus_value = 0
        self.dev = dev

        if type(dev) == int or (type(dev) == str and dev.isnumeric()):
            self.dev = "/dev/video{}".format(dev)

        self.fd = open(self.dev, 'r')
        self.ctrls = get_ctrls(self.fd)
        self.hasFocus = False
        for ctrl in self.ctrls:
            if ctrl['id'] == Focuser.FOCUS_ID:
                self.hasFocus = True
                self.opts[Focuser.OPT_FOCUS]["MIN_VALUE"] = ctrl['minimum']
                self.opts[Focuser.OPT_FOCUS]["MAX_VALUE"] = ctrl['maximum']
                self.opts[Focuser.OPT_FOCUS]["DEF_VALUE"] = ctrl['default']
                self.focus_value = get_ctrl(self.fd, Focuser.FOCUS_ID)

        if not self.hasFocus:
            raise RuntimeError("Device {} has no focus_absolute control.".format(self.dev))

    def read(self):
        return self.focus_value

    def write(self, value):
        self.focus_value = value
        # os.system("v4l2-ctl -d {} -c focus_absolute={}".format(self.dev, value))
        set_ctrl(self.fd, Focuser.FOCUS_ID, value)

    OPT_BASE    = 0x1000
    OPT_FOCUS   = OPT_BASE | 0x01
    OPT_ZOOM    = OPT_BASE | 0x02
    OPT_MOTOR_X = OPT_BASE | 0x03
    OPT_MOTOR_Y = OPT_BASE | 0x04
    OPT_IRCUT   = OPT_BASE | 0x05
    opts = {
        OPT_FOCUS : {
            "MIN_VALUE": 0,
            "MAX_VALUE": 1000,
            "DEF_VALUE": 0,
        },
    }
    def reset(self,opt,flag = 1):
        info = self.opts[opt]
        if info == None or info["DEF_VALUE"] == None:
            return
        self.set(opt,info["DEF_VALUE"])

    def get(self,opt,flag = 0):
        info = self.opts[opt]
        return self.read()

    def set(self,opt,value,flag = 1):
        info = self.opts[opt]
        if value > info["MAX_VALUE"]:
            value = info["MAX_VALUE"]
        elif value < info["MIN_VALUE"]:
            value = info["MIN_VALUE"]
        self.write(value)
        print("write: {}".format(value))

    def __del__(self):
        self.fd.close()

pass
