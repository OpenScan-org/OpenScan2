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
    
    def get_statistics_from_file(self):
        '''
        get the required statistics as a dictionary
        '''
        statistics = {}
        file_path = self.filename
        
        # Check if the file exists
        if not os.path.exists(file_path):
            return statistics
        
        # Read all lines from the file
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        # Process each line (each JSON object)
        for line in lines:
            try:
                data = json.loads(line.strip())
                for key, value in data.items():
                    if key not in statistics:
                        statistics[key] = {}
                    if value not in statistics[key]:
                        statistics[key][value] = 0
                    statistics[key][value] += 1
            except json.JSONDecodeError:
                continue  # Skip invalid JSON lines
        
        # Find the most common value for each field
        for key in statistics:
            statistics[key] = max(statistics[key], key=statistics[key].get)
        
        return statistics