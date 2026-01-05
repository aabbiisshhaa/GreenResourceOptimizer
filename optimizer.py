import os
import psutil
import joblib
import pandas as pd
import time
import logging
from windows_toasts import WindowsToaster, Toast

# GUIDs
BALANCED_GUID = "381b4222-f694-41f0-9685-ff5bb260df2e"
POWER_SAVER_GUID = "0f3869e4-2868-4a37-9ba0-21e3368c89d9"

# To prevent redundant OS calls
current_active_plan = None
toaster = WindowsToaster('Green Optimizer')

def set_power_plan(plan_grid, plan_name):
    global current_active_plan
    if current_active_plan != plan_grid:
        try:
            os.system(f'powercfg /setactive {plan_grid}')
            logging.info(f"Switched to {plan_name} power plan.")
            current_active_plan = plan_grid
            
            # Notify the user of the hardware changes
            new_toast = Toast()
            new_toast.text_fields = [f"Mode: {plan_name}", f"AI adjusted power settings for efficiency."]
            toaster.show_toast(new_toast)
        
        except Exception as e:
            logging.error(f"Failed to set power plan: {e}")

# 1. Setup Logging and Notification
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
toaster = WindowsToaster('Green Optimizer')
# 2. Load the 'Brain'
try:
    model = joblib.load('resource_model.pkl')
    logging.info("AI Model loaded successfully. Optimizer is active.")
except:
    logging.error("Model file not found! Run train_model.py first.")
    exit()

def monitor_and_optimize():
    sleep_time = 15     # Check every 15 seconds

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
        
        # 6. Logic : Variable Polling & Notification
        if prediction == "Idle" or current_metrics['cpu_usage'] < 10.0:
            set_power_plan(POWER_SAVER_GUID, "Power Saver")
            sleep_time = 60  # Slow down when idle
            logging.info(f"State: IDLE. Sleeping for 60s to save energy.")
            
            # Notification logic
            new_toast = Toast()
            new_toast.body_text = "System is Idle. Optimizer entering low-power polling mode."
            toaster.show_toast(new_toast)
            
            sleep_time = 60  # Slow down when idle
        else:
            set_power_plan(BALANCED_GUID, "Balanced")
            logging.info(f"State: ACTIVE (CPU: {current_metrics['cpu_usage']}), Checking again in 15s.")
            sleep_time = 15  # Normal polling interval
        
        time.sleep(sleep_time)

if __name__ == "__main__":
    monitor_and_optimize()