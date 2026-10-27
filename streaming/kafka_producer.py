import json
import time
import random

def simulate_cdc_stream():
    """Simulates real-time CDC financial webhook events coming into a stream."""
    customers = ["CUST101", "CUST102", "CUST103", "CUST104"]
    statuses = ["COMPLETED", "COMPLETED", "COMPLETED", "FAILED"]
    
    print("--- STARTING REAL-TIME FINTECH CDC STREAM SIMULATION ---")
    for i in range(5):
        event = {
            "transaction_id": f"TXN_STREAM_{random.randint(1000, 9999)}",
            "customer_id": random.choice(customers),
            "amount": round(random.uniform(10.0, 500.0), 2),
            "status": random.choice(statuses),
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
        }
        print(f"Produced Event -> {json.dumps(event)}")
        time.sleep(1)

if __name__ == "__main__":
    simulate_cdc_stream()