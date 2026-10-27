import json
import random
from datetime import datetime, timedelta

def generate_mock_transactions(num_records=10):
    """
    Generates mock financial transaction records for testing the PySpark ETL pipeline.
    This acts as a data source simulator for local development.
    """
    customers = ["CUST101", "CUST102", "CUST103", "CUST104", "CUST105"]
    statuses = ["COMPLETED", "COMPLETED", "COMPLETED", "FAILED", "PENDING"]
    
    events = []
    base_time = datetime.utcnow()
    
    for i in range(1, num_records + 1):
        event = {
            "transaction_id": f"TXN{i:03d}",
            "customer_id": random.choice(customers),
            "amount": round(random.uniform(-20.0, 1500.0), 2), # Includes some negative/invalid amounts for testing data cleaning
            "status": random.choice(statuses),
            "timestamp": (base_time - timedelta(minutes=random.randint(1, 60))).isoformat() + "Z"
        }
        events.append(event)
        
    return events

if __name__ == "__main__":
    records = generate_mock_transactions(5)
    print(json.dumps(records, indent=4))
    
    # Optional: Automatically write it to your data directory for the pipeline to consume
    with open("data/generated_transactions.json", "w") as f:
        json.dump(records, f, indent=4)
    print("--- Successfully generated and saved mock raw transactions to data/generated_transactions.json ---")