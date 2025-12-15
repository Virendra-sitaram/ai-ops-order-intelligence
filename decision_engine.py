import pandas as pd
from collections import defaultdict
from datetime import datetime

# -----------------------------
# Load CSV files safely
# -----------------------------
orders = pd.read_csv("orders.csv", encoding="utf-8-sig")
inventory = pd.read_csv("inventory.csv", encoding="utf-8-sig")

# Normalize column names
orders.columns = orders.columns.str.strip().str.lower()
inventory.columns = inventory.columns.str.strip().str.lower()

# Clean inventory
inventory["productcode"] = inventory["productcode"].astype(str).str.strip()
inventory["availablestock"] = inventory["availablestock"].astype(int)

stock = dict(zip(inventory["productcode"], inventory["availablestock"]))

# Production rules
MAX_DAILY_CAPACITY = 200
daily_capacity_used = defaultdict(int)

# Create log file
log_file = open("output.log", "w")
log_file.write("AI Ops Assistant Log\n")
log_file.write("=" * 40 + "\n")

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_file.write(f"[{timestamp}] {message}\n")

# -----------------------------
# Order processing
# -----------------------------
def process_order(order):
    order_id = str(order["orderid"]).strip()
    product = str(order["productcode"]).strip()
    qty = int(order["quantity"])
    date = str(order["orderdate"]).strip()
    priority = str(order["priority"]).strip()

    available_stock = stock.get(product, 0)
    remaining_capacity = MAX_DAILY_CAPACITY - daily_capacity_used[date]

    if available_stock >= qty and remaining_capacity >= qty:
        decision = "APPROVE"
        reason = "Sufficient stock and production capacity"
        stock[product] -= qty
        daily_capacity_used[date] += qty

    elif available_stock > 0:
        decision = "SPLIT"
        reason = f"Only {available_stock} units available"
        produced = min(available_stock, remaining_capacity)
        stock[product] -= produced
        daily_capacity_used[date] += produced

    elif remaining_capacity < qty:
        decision = "DELAY"
        reason = "Daily capacity exceeded"

    else:
        decision = "ESCALATE"
        reason = "No inventory available"

    log(f"Order {order_id} | {decision} | {reason}")

    return {
        "OrderID": order_id,
        "Decision": decision,
        "Reason": reason
    }

# -----------------------------
# Run assistant
# -----------------------------
print("\n--- AI Ops Assistant Decisions ---\n")

for _, order in orders.iterrows():
    result = process_order(order)
    print(result)

log_file.write("=" * 40 + "\n")
log_file.write("Processing completed successfully\n")
log_file.close()

print("\n✅ Processing completed successfully.")
print("📄 Log file created: output.log")
