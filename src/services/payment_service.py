from src.dao.payment_dao import payment_dao
from src.services.order_service import order_service

class PaymentService:
    def create_pending_payment(self, order_id, amount):
        return payment_dao.create_payment(order_id, amount)

    def process_payment(self, order_id, method):
        p = payment_dao.get_payment_by_order(order_id)
        if not p:
            raise ValueError("No payment record for order")
        payment_dao.update_payment(p["id"], "PAID", method)
        order_service.update_status(order_id, "COMPLETED")
        return p

    def refund_payment(self, order_id):
        p = payment_dao.get_payment_by_order(order_id)
        if not p:
            raise ValueError("No payment record for order")
        payment_dao.update_payment(p["id"], "REFUNDED")
        return p

payment_service = PaymentService()
