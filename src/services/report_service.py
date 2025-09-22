"""
report_service.py

Reporting Service using Supabase Python client.
Features:
- Top products by quantity sold
- Total revenue last month
- Orders by customer
- Customers with more than 2 orders
"""

import os
from collections import Counter
from datetime import datetime, timedelta
from dotenv import load_dotenv
from supabase import create_client, Client

# Load Supabase credentials
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Import product DAO if needed for product names
from src.dao.product_dao import product_dao

class ReportService:
    def top_products(self, n=5):
        # Fetch all order items
        result = supabase.table("order_items").select("prod_id, quantity").execute()
        counts = Counter()
        for row in result.data:
            counts[row["prod_id"]] += row["quantity"]
        top = counts.most_common(n)
        return [
            {"product": product_dao.get_product(pid)["name"], "quantity": qty}
            for pid, qty in top
        ]

    def total_revenue_last_month(self):
        cutoff = datetime.now() - timedelta(days=30)
        result = supabase.table("orders").select("total_amount, status, order_date").execute()
        total = 0
        for o in result.data:
            if o["status"] == "COMPLETED" and o["order_date"] and datetime.fromisoformat(o["order_date"][:-1]) >= cutoff:
                total += o["total_amount"] or 0
        return total

    def orders_by_customer(self):
        result = supabase.table("orders").select("customer_id").execute()
        counts = Counter([o["customer_id"] for o in result.data if o["customer_id"]])
        return dict(counts)

    def customers_with_more_than_two_orders(self):
        c = self.orders_by_customer()
        return [cid for cid, cnt in c.items() if cnt > 2]

report_service = ReportService()
