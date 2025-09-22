# src/dao/order_dao.py
from typing import Optional, List, Dict
from src.config import get_supabase

class order_dao:
    @staticmethod
    def _sb():
        return get_supabase()

    @staticmethod
    def create_order(customer_id: int, items: List[Dict]) -> Optional[Dict]:
        """
        Insert an order and its items.
        Items: list of {"prod_id": int, "quantity": int}
        """
        # Insert order header
        payload = {"customer_id": customer_id, "status": "created"}
        resp = order_dao._sb().table("orders").insert(payload).execute()
        order = resp.data[0] if resp.data else None
        if not order:
            return None
        
        order_id = order.get("order_id")
        
        # Insert order items
        for item in items:
            item_payload = {
                "order_id": order_id,
                "prod_id": item["prod_id"],
                "quantity": item["quantity"]
            }
            order_dao._sb().table("order_items").insert(item_payload).execute()
        
        return order_dao.get_order_details(order_id)

    @staticmethod
    def get_order_details(order_id: int) -> Optional[Dict]:
        """
        Fetch order and its items.
        """
        resp_order = order_dao._sb().table("orders").select("*").eq("order_id", order_id).limit(1).execute()
        order = resp_order.data[0] if resp_order.data else None
        if not order:
            return None
        
        resp_items = order_dao._sb().table("order_items").select("*").eq("order_id", order_id).execute()
        items = resp_items.data or []
        
        order["items"] = items
        return order

    @staticmethod
    def cancel_order(order_id: int) -> Optional[Dict]:
        """
        Update order status to cancelled and return updated order.
        """
        order_dao._sb().table("orders").update({"status": "cancelled"}).eq("order_id", order_id).execute()
        return order_dao.get_order_details(order_id)
