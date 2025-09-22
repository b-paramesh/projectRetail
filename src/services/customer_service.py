from typing import Dict
from src.dao.customer_dao import customer_dao

class CustomerError(Exception):
    pass

class customer_service:
    @staticmethod
    def add_customer(name: str, email: str, phone: str, city: str | None = None) -> Dict:
        # Simple validation example
        if not name or not email or not phone:
            raise CustomerError("Name, email and phone are required")
        existing_customers = customer_dao.list_customers()
        if any(c.get("email") == email for c in existing_customers):
            raise CustomerError(f"Customer with email {email} already exists")
        return customer_dao.create_customer(name, email, phone, city)
