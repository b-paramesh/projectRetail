from datetime import datetime

class PaymentDAO:
    def __init__(self):
        self.payments = {}   # {payment_id: {...}}
        self.counter = 1

    def create_payment(self, order_id, amount):
        pid = self.counter
        self.counter += 1
        payment = {
            "id": pid,
            "order_id": order_id,
            "amount": amount,
            "status": "PENDING",
            "method": None,
            "created_at": datetime.now()
        }
        self.payments[pid] = payment
        return payment

    def update_payment(self, payment_id, status, method=None):
        if payment_id not in self.payments:
            raise ValueError("Payment not found")
        self.payments[payment_id]["status"] = status
        if method:
            self.payments[payment_id]["method"] = method
        return self.payments[payment_id]

    def get_payment_by_order(self, order_id):
        for p in self.payments.values():
            if p["order_id"] == order_id:
                return p
        return None

payment_dao = PaymentDAO()
