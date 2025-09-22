# src/services/order_service.py
from typing import List, Dict
from src.dao.order_dao import order_dao
from src.dao.product_dao import product_dao

class OrderError(Exception):
    pass

class order_service:
    @staticmethod
    def create_order(customer_id: int, items: List[Dict]) -> Dict:
        if not items:
            raise OrderError("Order must contain at least one item")
        
        # Validate each item product exists and stock is sufficient
        for item in items:
            prod = product_dao.get_product_by_id(item["prod_id"])
            if not prod:
                raise OrderError(f"Product not found: {item['prod_id']}")
            if (prod.get("stock") or 0) < item["quantity"]:
                raise OrderError(f"Insufficient stock for product {prod['sku']} (requested {item['quantity']}, available {prod.get('stock')})")
        
        # Reduce stock for each product
        for item in items:
            prod = product_dao.get_product_by_id(item["prod_id"])
            new_stock = (prod.get("stock") or 0) - item["quantity"]
            product_dao.update_product(item["prod_id"], {"stock": new_stock})

        # Create order record and items
        return order_dao.create_order(customer_id, items)

    @staticmethod
    def get_order_details(order_id: int) -> Dict:
        order = order_dao.get_order_details(order_id)
        if not order:
            raise OrderError("Order not found")
        return order

    @staticmethod
    def cancel_order(order_id: int) -> Dict:
        order = order_dao.get_order_details(order_id)
        if not order:
            raise OrderError("Order not found")
        if order.get("status") == "cancelled":
            raise OrderError("Order already cancelled")
        
        # Re-stock products in order items
        for item in order.get("items", []):
            prod = product_dao.get_product_by_id(item["prod_id"])
            new_stock = (prod.get("stock") or 0) + item["quantity"]
            product_dao.update_product(item["prod_id"], {"stock": new_stock})

        return order_dao.cancel_order(order_id)
