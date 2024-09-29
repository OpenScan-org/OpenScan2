import csv

class ScanStatistics:
    def __init__(self, filename="/home/pi/OpenScan/statistics/statistics.csv"):
        self.filename = filename
        self.header = ["arch", "openscan version", "openscan branch", "shield", "date_init", "date_end", "num_photos", "done-photos", "camera", "aborted"]

    def write_statistics(self, arch, openscan_version, openscan_branch, shield, date_init, date_end, num_photos, done_photos, camera, aborted):
        data = [arch, openscan_version, openscan_branch, shield, date_init, date_end, num_photos, done_photos, camera, aborted]
        
        with open(self.filename, "a", newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=';')
            
            # Write header if file is empty
            if csv_file.tell() == 0:
                csv_writer.writerow(self.header)
            
            csv_writer.writerow(data)
