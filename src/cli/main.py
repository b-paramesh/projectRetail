# src/cli/main.py
import argparse
import json
from src.services.product_service import product_service # , order_service  <-- commented out to avoid import error
from src.dao.product_dao import product_dao 
from  src.dao.customer_dao import customer_dao# <-- keep commented as in original
from src.services.customer_service import customer_service
from src.services.order_service import order_service  # Uncomment if using order commands
from src.dao.customer_dao import customer_dao
from src.services.payment_service import payment_service
from src.services.report_service import report_service
class retail:
    def cmd_product_add(self,args):
        try:
            p = product_service.add_product(args.name, args.sku, args.price, args.stock, args.category)
            print("Created product:")
            print(json.dumps(p, indent=2, default=str))
        except Exception as e:
            print("Error:", e)

    def cmd_product_list(self,args):
        ps = product_dao.list_products(limit=100)
        print(json.dumps(ps, indent=2, default=str))
    
    def cmd_product_update_stock(self, args):
        try:
            p = product_service.update_stock(args.prod_id, args.stock)
            print("Updated product stock:")
            print(json.dumps(p, indent=2, default=str))
        except Exception as e:
            print("Error:", e)


    def cmd_customer_add(self,args):
        try:
            c = customer_service.add_customer(args.name, args.email, args.phone, args.city)
            print("Created customer:")
            print(json.dumps(c, indent=2, default=str))
        except Exception as e:
            print("Error:", e)
            customer_dao.list_customers()

    def cmd_order_create(self,args):
        # items provided as prod_id:qty strings
        items = []
        for item in args.item:
            try:
                pid, qty = item.split(":")
                items.append({"prod_id": int(pid), "quantity": int(qty)})
            except Exception:
                print("Invalid item format:", item)
                return
        try:
            ord = order_service.create_order(args.customer, items)
            print("Order created:")
            print(json.dumps(ord, indent=2, default=str))
        except Exception as e:
            print("Error:", e)

    def cmd_order_show(self,args):
        try:
            o = order_service.get_order_details(args.order)
            print(json.dumps(o, indent=2, default=str))
        except Exception as e:
            print("Error:", e)

    def cmd_order_cancel(self,args):
        try:
            o = order_service.cancel_order(args.order)
            print("Order cancelled (updated):")
            print(json.dumps(o, indent=2, default=str))
        except Exception as e:
            print("Error:", e)

    
    def cmd_payment_process(self, args):
        try:
            p = payment_service.process_payment(args.order, args.method)
            print("Payment processed:")
            print(json.dumps(p, indent=2, default=str))
        except Exception as e:
            print("Error:", e)

    def cmd_payment_show(self, args):
        try:
            from src.dao.payment_dao import payment_dao
            p = payment_dao.get_payment_by_order(args.order)
            print(json.dumps(p, indent=2, default=str))
        except Exception as e:
            print("Error:", e)

    def cmd_report_top(self, args):
        print(json.dumps(report_service.top_products(), indent=2, default=str))

    def cmd_report_revenue(self, args):
        print("Revenue last month:", report_service.total_revenue_last_month())

    def cmd_report_orders_by_customer(self, args):
        print(json.dumps(report_service.orders_by_customer(), indent=2, default=str))

    def cmd_report_active_customers(self, args):
        print("Customers with >2 orders:", report_service.customers_with_more_than_two_orders())




    def build_parser(self):
        parser = argparse.ArgumentParser(prog="retail-cli")
        sub = parser.add_subparsers(dest="cmd")

        # product add/list
        p_prod = sub.add_parser("product", help="product commands")
        pprod_sub = p_prod.add_subparsers(dest="action")
        addp = pprod_sub.add_parser("add")
        addp.add_argument("--name", required=True)
        addp.add_argument("--sku", required=True)
        addp.add_argument("--price", type=float, required=True)
        addp.add_argument("--stock", type=int, default=0)
        addp.add_argument("--category", default=None)
        addp.set_defaults(func=self.cmd_product_add)

        listp = pprod_sub.add_parser("list")
        listp.set_defaults(func=self.cmd_product_list)


        update_stock_parser = pprod_sub.add_parser("update-stock")
        update_stock_parser.add_argument("--prod_id", type=int, required=True)
        update_stock_parser.add_argument("--stock", type=int, required=True)
        update_stock_parser.set_defaults(func=self.cmd_product_update_stock)


        # customer add
        pcust = sub.add_parser("customer")
        pcust_sub = pcust.add_subparsers(dest="action")
        addc = pcust_sub.add_parser("add")
        addc.add_argument("--name", required=True)
        addc.add_argument("--email", required=True)
        addc.add_argument("--phone", required=True)
        addc.add_argument("--city", default=None)
        addc.set_defaults(func=self.cmd_customer_add)

        # order
        porder = sub.add_parser("order")
        porder_sub = porder.add_subparsers(dest="action")

        createo = porder_sub.add_parser("create")
        createo.add_argument("--customer", type=int, required=True)
        createo.add_argument("--item", required=True, nargs="+", help="prod_id:qty (repeatable)")
        createo.set_defaults(func=self.cmd_order_create)

        showo = porder_sub.add_parser("show")
        showo.add_argument("--order", type=int, required=True)
        showo.set_defaults(func=self.cmd_order_show)

        cano = porder_sub.add_parser("cancel")
        cano.add_argument("--order", type=int, required=True)
        cano.set_defaults(func=self.cmd_order_cancel)


        # payments
        ppay = sub.add_parser("payment")
        ppay_sub = ppay.add_subparsers(dest="action")

        proc = ppay_sub.add_parser("process")
        proc.add_argument("--order", type=int, required=True)
        proc.add_argument("--method", choices=["Cash","Card","UPI"], required=True)
        proc.set_defaults(func=self.cmd_payment_process)

        showp = ppay_sub.add_parser("show")
        showp.add_argument("--order", type=int, required=True)
        showp.set_defaults(func=self.cmd_payment_show)

        # reports
        prep = sub.add_parser("report")
        prep_sub = prep.add_subparsers(dest="action")

        topr = prep_sub.add_parser("top-products")
        topr.set_defaults(func=self.cmd_report_top)

        revr = prep_sub.add_parser("revenue")
        revr.set_defaults(func=self.cmd_report_revenue)

        ordc = prep_sub.add_parser("orders-by-customer")
        ordc.set_defaults(func=self.cmd_report_orders_by_customer)

        actc = prep_sub.add_parser("active-customers")
        actc.set_defaults(func=self.cmd_report_active_customers)





        return parser

    def main(self):
        parser = self.build_parser()
        args = parser.parse_args()
        if not hasattr(args, "func"):
            parser.print_help()
            return
        args.func(args)

if __name__ == "__main__":
    p=retail()
    p.main()