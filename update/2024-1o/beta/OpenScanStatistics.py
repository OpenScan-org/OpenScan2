import json
import os
from datetime import datetime
from dataclasses import dataclass

@dataclass
class ScanData:
    arch: str
    openscan_version: str
    openscan_branch: str
    shield: str
    date_init: str  # Format: YYYY-MM-DD HH:MM
    date_end: str   # Format: YYYY-MM-DD HH:MM
    num_photos: int
    done_photos: int
    camera: str
    stack_size: int
    telegram_enabled: bool
    delete_aborted: bool
    endstop_enabled: bool
    group_stack_photos: bool
    aborted: bool

class ScanStatistics:
    def __init__(self, filename: str = "/home/pi/OpenScan/statistics") -> None:
        self.filename: str = filename

    def write_statistics(self, scan_data: ScanData) -> None:
        data: dict = scan_data.__dict__  # Convert dataclass to dictionary

        # Parse date_init to get year and month
        date_object: datetime = datetime.strptime(scan_data.date_init, "%Y-%m-%d %H:%M")
        record_filename: str = os.path.join(self.filename, f"statistics-{date_object.year}-{date_object.month:02d}.json")

        # Append the new data as a new line
        with open(record_filename, "a") as json_file:
            json.dump(data, json_file, separators=(',', ':'), indent=None)  # Collapsed JSON
            json_file.write('\n')  # Add a newline after each entry