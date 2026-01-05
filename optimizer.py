import psutil
import joblib
import pandas as pd
import time
import logging
from win10toast import ToastNotifier

# 1. Setup Logging and Notification
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
toaster = ToastNotifier()

# 2. Load the 'Brain'
try:
    model = joblib.load('resource_model.pkl')
    logging.info("AI Model loaded successfully. Optimizer is active.")
except:
    logging.error("Model file not found! Run train_model.py first.")
    exit()

def monitor_and_optimize():
    while True:
        
        # 3. Capture current system state
        current_metrics = {
            "cpu_usage": psutil.cpu_percent(interval=1),
            "memory_usage": psutil.virtual_memory().percent,
            "process_count": len(psutil.pids())
        }
        
        # 4. Prepare data for the AI
        input_df = pd.DataFrame([current_metrics])
        
        # 5. Predict the state
        prediction = model.predict(input_df)[0]
        logging.info(f"Predicted State: {prediction} | CPU: {current_metrics['cpu_usage']}%")

        # 6. Logic: If Idle, suggest optimization
        if prediction == "Idle":
            toaster.show_toast(
                "Green Optimizer",
                "System is Idle. AI suggests switching to Power Saver mode.",
                duration=5,
                threaded=True
            )
        
        time.sleep(15) # Check every 15 seconds

if __name__ == "__main__":
    monitor_and_optimize()