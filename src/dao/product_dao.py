# src/dao/product_dao.py
from typing import Optional, List, Dict
from src.config import get_supabase  # use the config helper

class product_dao:
    @staticmethod
    def _sb():
        return get_supabase()  # helper to get supabase client

    @staticmethod
    def create_product(name: str, sku: str, price: float, stock: int = 0, category: str | None = None) -> Optional[Dict]:
        """
        Insert a product and return the inserted row (two-step: insert then select by unique sku).
        """
        payload = {"name": name, "sku": sku, "price": price, "stock": stock}
        if category:
            payload["category"] = category

        # Insert product
        product_dao._sb().table("products").insert(payload).execute()

        # Fetch inserted row by unique column (sku)
        resp = product_dao._sb().table("products").select("*").eq("sku", sku).limit(1).execute()
        return resp.data[0] if resp.data else None

    @staticmethod
    def get_product(prod_id: int) -> Optional[Dict]:
        """
        Fetch a single product by product ID
        """
        resp = product_dao._sb().table("products").select("*").eq("prod_id", prod_id).single().execute()
        return resp.data

    @staticmethod
    def list_products(limit: int = 100, category: str | None = None) -> List[Dict]:
        """
        List products, optionally filtered by category
        """
        q = product_dao._sb().table("products").select("*").order("prod_id", desc=False).limit(limit)
        if category:
            q = q.eq("category", category)
        resp = q.execute()
        return resp.data or []

    @staticmethod
    def update_product(prod_id: int, fields: Dict) -> Optional[Dict]:
        """
        Update a product and return the updated row
        """
        product_dao._sb().table("products").update(fields).eq("prod_id", prod_id).execute()
        resp = product_dao._sb().table("products").select("*").eq("prod_id", prod_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    @staticmethod
    def delete_product(prod_id: int) -> Optional[Dict]:
        """
        Delete a product and return the deleted row
        """
        resp_before = product_dao._sb().table("products").select("*").eq("prod_id", prod_id).limit(1).execute()
        row = resp_before.data[0] if resp_before.data else None
        product_dao._sb().table("products").delete().eq("prod_id", prod_id).execute()
        return row
