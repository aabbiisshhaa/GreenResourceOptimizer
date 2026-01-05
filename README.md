# Green Resource Optimizer 🔋

A Software Engineering project designed to monitor system resource usage and use Machine Learning to predict and optimize power consumption.

## 🚀 Project Goals

**Phase 1: Data Collection** - Python script to gather CPU, RAM, and Process metrics.

- **Data Source:** Real-time system calls via `psutil` library.
- **Sampling Rate:** 1 sample every 5-10 seconds.
- **Data Dictionary:**| Variable          | Unit                | Description                                 |
  | :---------------- | :------------------ | :------------------------------------------ |
  | `timestamp`     | YYYY-MM-DD HH:MM:SS | Local system time of capture.               |
  | `cpu_usage`     | Percentage (%)      | Aggregate CPU utilization across all cores. |
  | `memory_usage`  | Percentage (%)      | Percent of total RAM currently in use.      |
  | `process_count` | Integer             | Total number of active PIDs (Process IDs).  |

**Phase 2: AI Integration** - Training a model to recognize "Idle" vs "High Load" states.

- **Algorithm:** Random Forest Classifier (Scikit-Learn)
- **Features:** CPU Usage, Memory Usage, Process Count
- **Target Labels:** Idle, Productive, Heavy Load
- **Validation:** 80/20 Train-Test Split

**Phase 3: Optimization** - Automated system adjustments to save energy.

## 🏗️ System Architecture

```mermaid
graph LR
    A[System Metrics] --> B(monitor.py)
    B --> C[(system_data.csv)]
    C --> D(train_model.py)
    D --> E[resource_model.pkl]
    E --> F(optimizer.py)
    F --> G[User Notifications]
```

## 🛠️ Tech Stack

- **Language:** Python
- **Libraries:** `psutil`, `csv`, `time`
- **Tools:** Git, VS Code

## 🚀 Installation & Usage

1. **Clone the repository:**
   `git clone https://github.com/yourusername/GreenResourceOptimizer.git`
2. **Install dependencies:**
   `pip install -r requirements.txt`
3. **Start monitoring:**
   `python monitor.py`
