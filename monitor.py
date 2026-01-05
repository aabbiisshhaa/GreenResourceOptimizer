import psutil
import time
import csv
import os
import logging
from datetime import datetime

import logging

# Configure logging to both console and a file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app_log.txt"),
        logging.StreamHandler()
    ]
)

class ResourceMonitor:
    def __init__(self, file_name="system_data.csv"):
        self.file_name = file_name
        self.headers = ['timestamp', 'cpu_usage', 'memory_usage', 'process_count']
        self._prepare_csv()

    def _prepare_csv(self):
            if not os.path.exists(self.file_name):
                with open(self.file_name, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(self.headers)

    def collect_metrics(self):
        # Capture usage over a 1-second interval
        return {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'cpu_usage': psutil.cpu_percent(interval=1),
            'memory_usage': psutil.virtual_memory().percent,
            'process_count': len(psutil.pids())
        }
        
    def start_logging(self, interval=5):
        print(f"--- GreenMonitor Active ---")
        print(f"Logging system metrics to {self.file_name} every {interval} seconds.")
        print("Action: Go about your normal study day. Press Ctrl + C to stop this event.")
        
        try:
            while True:
                data = self.collect_metrics()
                with open(self.file_name, mode='a', newline='') as file:
                    writer = csv.DictWriter(file, fieldnames=self.headers)
                    writer.writerow(data)
                logging.info(f"Logged data at {data['timestamp']}: CPU {data['cpu_usage']}% | RAM {data['memory_usage']}%, | Processes {data['process_count']}")
                time.sleep(interval)
        except KeyboardInterrupt:
            logging.info("\n GreenMonitor Stopped. Data is ready for tomorrow!")
if __name__ == "__main__":
    monitor = ResourceMonitor()
    monitor.start_logging(interval=10)