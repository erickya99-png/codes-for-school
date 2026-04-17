import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import IsolationForest

# Load the dataset (replace this with your actual dataset filename)
dataset_path = 'your_dataset.csv'
df = pd.read_csv(dataset_path)

# Display the first few rows
print("First few rows of the dataset:")
print(df.head())

# Show dataset info
print("\nDataset Info:")
print(df.info())

# Basic statistics
print("\nDescriptive Statistics:")
print(df.describe())

# Check for missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Create a simple distribution plot for a numeric feature
feature_column = 'feature_column'
if feature_column not in df.columns:
    numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
    if numeric_columns:
        feature_column = numeric_columns[0]
        print(f"Using numeric column '{feature_column}' for the distribution plot.")
    else:
        raise ValueError('No numeric column found for plotting.')

plt.figure(figsize=(10, 6))
sns.histplot(df[feature_column], bins=30, kde=True)
plt.title(f'Distribution of {feature_column}')
plt.xlabel(feature_column)
plt.ylabel('Count')
plt.tight_layout()
plt.show()

# Save a simple summary report
with open('data_summary.txt', 'w') as f:
    f.write("First few rows of the dataset:\n")
    f.write(str(df.head()))
    f.write("\n\nDataset Info:\n")
    f.write(str(df.info()))
    f.write("\n\nMissing Values:\n")
    f.write(str(df.isnull().sum()))
    f.write("\n\nDescriptive Statistics:\n")
    f.write(str(df.describe()))

print("Data profiling completed and summary saved to 'data_summary.txt'")

# Anomaly Detection (Isolation Forest)
numeric_df = df.select_dtypes(include=['number']).dropna()
print("\nNumeric columns used for anomaly detection:")
print(numeric_df.columns.tolist())

if numeric_df.empty:
    raise ValueError('No numeric data available for anomaly detection after dropping missing values.')

if len(numeric_df) < 2:
    raise ValueError('Not enough rows in numeric data for IsolationForest.')

iso = IsolationForest(contamination=0.02, random_state=42)
iso.fit(numeric_df)

df['anomaly_score'] = iso.decision_function(numeric_df)
df['anomaly_label'] = iso.predict(numeric_df)

anomalies = df[df['anomaly_label'] == -1]
print("\nDetected anomalies:")
print(anomalies.head())
print(f"Total anomalies detected: {len(anomalies)}")

plt.figure(figsize=(10, 6))
sns.histplot(df['anomaly_score'], bins=50, kde=True)
plt.title('Anomaly Score Distribution')
plt.xlabel('Anomaly Score')
plt.ylabel('Frequency')
plt.tight_layout()
plt.show()

# Export anomalies if any are found
anomalies.to_csv('anomalies.csv', index=False)
print("Anomaly results saved to 'anomalies.csv'")


 