import pandas as pd
import matplotlib.pyplot as plt
import os

def generate_research_viz():
    # Maasin Lab R&D Path
    raw_data_path = "input_data/raw/creditcard.csv"
    output_path = "reports/fraud_imbalance.png"
    
    print("LOG: Initializing R&D Phase: Data Visualization...")
    
    if not os.path.exists(raw_data_path):
        print(f"ERROR: Target file not found at {raw_data_path}")
        return

    # 1. Loading the Big Data
    df = pd.read_csv(raw_data_path)
    
    # 2. Calculating Class Distribution
    class_counts = df['Class'].value_counts()
    
    # 3. Generating Plot
    plt.figure(figsize=(10, 6))
    class_counts.plot(kind='bar', color=['blue', 'red'])
    plt.title('R&D Phase: Transaction Class Distribution (Fraud vs Normal)')
    plt.xlabel('Class (0: Normal, 1: Fraud)')
    plt.ylabel('Number of Transactions')
    plt.xticks(rotation=0)
    
    # Ensure the reports directory exists
    os.makedirs('reports', exist_ok=True)
    
    # 4. Saving the Insight
    plt.savefig(output_path)
    print(f"LOG: Visual report saved successfully to {output_path}")
    print("LOG: Visualization complete.")

if __name__ == "__main__":
    generate_research_viz()