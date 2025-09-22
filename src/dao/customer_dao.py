from typing import Optional, List, Dict
from src.config import get_supabase

class customer_dao:
    @staticmethod
    def _sb():
        return get_supabase()

    @staticmethod
    def create_customer(name: str, email: str, phone: str, city: str | None = None) -> Optional[Dict]:
        payload = {"name": name, "email": email, "phone": phone}
        if city:
            payload["city"] = city
        
        # Insert customer
        customer_dao._sb().table("customers").insert(payload).execute()

        # Fetch inserted row by unique email (assuming email unique)
        resp = customer_dao._sb().table("customers").select("*").eq("email", email).limit(1).execute()
        return resp.data[0] if resp.data else None

    @staticmethod
    def get_customer_by_id(cust_id: int) -> Optional[Dict]:
        resp = customer_dao._sb().table("customers").select("*").eq("cust_id", cust_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    @staticmethod
    def list_customers(limit: int = 100) -> List[Dict]:
        resp = customer_dao._sb().table("customers").select("*").order("cust_id", desc=False).limit(limit).execute()
        return resp.data or []
