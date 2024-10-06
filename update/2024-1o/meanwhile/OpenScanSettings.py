import json
import os
from datetime import datetime
from dataclasses import dataclass, asdict
from unicodedata import decimal

@dataclass
class OpenScanSettings:
    advanced_settings: bool
    cam_awbg_blue: int
    cam_awbg_red: int
    cam_contrast: int
    cam_cropx: int
    cam_cropy: int
    cam_delay_after: int
    cam_delay_before: int
    camera: str
    cam_features: bool
    cam_focus_max: float
    cam_focus_min: float
    cam_focuspeak: bool
    cam_gain: int
    cam_histogram: bool
    cam_jpeg_quality: int
    cam_mask: bool
    cam_mask_threshold: int
    cam_output_downscale: bool
    cam_output_resolution: int
    cam_preview_resolution: int
    cam_rotation: int
    cam_saturation: int
    cam_sharparea: bool
    cam_sharpness: int
    cam_shutter: int
    cam_stacksize: int
    cam_timeout: int
    datadog_enable: bool
    delete_aborted: bool
    diskspace_threshold: int
    extra_acc: float
    extra_accramp: int
    extra_angle: int
    extra_delay: int
    extra_dir: int
    extra_stepsperrotation: int
    group_stack_photos: bool
    hostname: str
    interface_color: str
    model: str
    object_size: float
    openscan_uuid: str
    osc_credit: int
    osc_limit_filesize: int
    osc_limit_photos: int
    osc_splitsize: int
    pin_external: int
    pin_extra_dir: int
    pin_extra_enable: int
    pin_extra_endstop: int
    pin_extra_step: int
    pin_ringlight1: int
    pin_ringlight2: int
    pin_rotor_dir: int
    pin_rotor_enable: int
    pin_rotor_endstop: int
    pin_rotor_step: int
    pin_tt_dir: int
    pin_tt_step: int
    raspberry_model: str
    raspbian_codename: str
    rotate_tt_first: bool
    rotor_acc: int
    rotor_accramp: int
    rotor_angle: int
    rotor_anglemax: int
    rotor_anglemin:int
    rotor_anglestart: int
    rotor_delay: int
    rotor_dir: int
    rotor_enable_endstop: bool
    rotor_endstop_angle: int
    rotor_endstop_enable: bool
    rotor_stepsperrotation: int
    routine_photocount: int
    routine_projectname: str
    routine_secondpass: bool
    sdcard_manfid: str
    sdcard_name: str
    shield_type: str
    smb_enable: bool
    ssh_enable: bool
    status_cloud: str
    status_internal_cam: str
    telegram_client_id: str
    telegram_enable: bool
    terms: bool
    tt_acc: float
    tt_accramp: int
    tt_angle: int
    tt_delay: int
    tt_dir: int
    tt_stepsperrotation: int
    turntable_mode: bool
    updateable: bool
    update_auto: bool
    uploadprogress: str
    
    @classmethod
    def get_openscan_settings(cls):
        settings = {}
        blacklist = [
            'architecture',
            'openscan_version',
            'openscan_branch',
            'token',
            'session_token',
            'telegram_api_token',
            'telegram_client_id',
            'status_uploadprogress',
            'raspberry_model',
            'sdcard_name',
            'sdcard_manfid',
            'uploadprogress'
             ]  # Add more keywords as needed
        for field in cls.__dataclass_fields__:
            if field not in blacklist:
                try:
                    with open(f"/home/pi/OpenScan/settings/{field}", "r") as file:
                        value = file.read().strip()
                        field_type = cls.__annotations__[field]
                        if field_type == bool:
                            settings[field] = value.lower() == 'true'
                        elif field_type == int:
                            settings[field] = int(value)
                        elif field_type == float:
                            settings[field] = float(value)
                        else:
                            settings[field] = value
                except FileNotFoundError:
                    print(f"Warning: File {field} not found. Skipping this field.")
                except ValueError:
                    print(f"Warning: Could not convert value for {field}. Skipping this field.")
        
        return {
            "version": "1.0",
            "settings": settings
        }

    @staticmethod
    def export_settings_to_file(settings, file_path=None):
        from datetime import datetime
        
        if file_path is None:
            current_date = datetime.now().strftime("%Y-%m-%d")
            file_path = f"openscan-settings-{current_date}.json"
        
        with open(file_path, "w") as json_file:
            json.dump(settings, json_file, indent=4)

def get_openscan_settings():
    return OpenScanSettings.get_openscan_settings()

def export_settings_to_file(settings, file_path=None):
    OpenScanSettings.export_settings_to_file(settings, file_path)

def persist_settings_from_file(settings):
    for field, value in settings.items():
        if field in OpenScanSettings.__dataclass_fields__:
            field_type = OpenScanSettings.__annotations__[field]
            try:
                if field_type == bool:
                    value = str(value).lower()
                elif field_type in (int, float):
                    value = str(field_type(value))
                else:
                    value = str(value)
                
                with open(f"/home/pi/OpenScan/settings/{field}", "w") as file:
                    file.write(value)
            except ValueError:
                print(f"Warning: Could not convert value for {field}. Skipping this field.")
            except IOError:
                print(f"Warning: Could not write to file for {field}. Skipping this field.")
