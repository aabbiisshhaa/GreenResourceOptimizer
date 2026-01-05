import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# 1. Load the data previously collected
df = pd.read_csv("system_data.csv")

# 2. Create labels (to be used by the model)
def label_usage(row):
    if row['cpu_usage'] < 10:
        return 'Idle'
    elif row['cpu_usage'] > 70:
        return 'Heavy Load'
    else:
        return 'Productive'
    
df['state'] = df.apply(label_usage, axis=1)

# 3. Features (Inputs) and Target (Output)
X = df[['cpu_usage', 'memory_usage', 'process_count']]
y = df['state']

# 4. Split data (80% for training, 20% for testing)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. Train the Model
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# 6. Check Accuracy
predictions = model.predict(X_test)
print(f"Model Accuracy: {accuracy_score(y_test, predictions) * 100:.2f}%")

# 7. Save the "Brain"
joblib.dump(model, 'resource_model.pkl')
print("Model saved as resource_model.pkl")