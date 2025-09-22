# 📌 Retail Inventory Management System

**Technologies:** Python | Supabase | PostgreSQL  

This project demonstrates a **real-world Retail Inventory Management System** using Python and Supabase/Postgres.  
It simulates retail operations such as managing products, customers, orders, payments, and generating reports.

---

## 🚀 Features

### 👕 Product Management
- Add new products with SKU, price, stock, and category  
- Update, list, and view products  
- Check low-stock products and restock  

### 👥 Customer Management
- Add, update, delete, and list customers  
- Search customers by email or city  

### 🛒 Order Management
- Create orders with multiple items  
- Show order details  
- Cancel orders (restores stock and refunds payment)  
- Complete orders (marks as completed and processes payment)  

### 💳 Payment Management
- Process payments via Cash, Card, or UPI  
- Refund payments for cancelled orders  
- Handles datetime serialization for JSON output  

### 📊 Reporting
- Top-selling products  
- Total revenue last month  
- Orders per customer  
- Frequent customers based on order count  

### 🗄 Database
- Persistent relational data storage using **Supabase/Postgres**  

### 🖥 Command-Line Interface (CLI)
- Fully menu-driven CLI for easy interaction  

---

## 🛠 How to Run

### Clone the repository
```bash
git clone https://github.com/AnveshAnnepaga/Retail-Inventory-Management-System.git
cd Retail-Inventory-Management-System


python -m venv venv

# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate

pip install -r requirements.txt

# Add a product
python -m src.cli.main product add --name "Laptop" --sku "LP100" --price 1200 --stock 10 --category "Electronics"

# List products
python -m src.cli.main product list


# Add a customer
python -m src.cli.main customer add --name "John Doe" --email "john@example.com" --phone "1234567890" --city "NY"

# Update a customer
python -m src.cli.main customer update --customer 1 --phone "9876543210" --city "LA"

# Delete a customer
python -m src.cli.main customer delete --customer 1

# List customers
python -m src.cli.main customer list

# Search customers
python -m src.cli.main customer search --email "john" --city "NY"


# Create an order (format: item_id:quantity)
python -m src.cli.main order create --customer 1 --item 2:3 4:1

# Show order details
python -m src.cli.main order show --order 3

# Complete an order
python -m src.cli.main order complete --order 3

# Cancel an order
python -m src.cli.main order cancel --order 3


# Process payment
python -m src.cli.main payment process --order 3 --method UPI

# Refund payment
python -m src.cli.main payment refund --order 3


# Top-selling products
python -m src.cli.main report top_products

# Revenue last month
python -m src.cli.main report revenue_last_month

# Orders per customer
python -m src.cli.main report orders_per_customer

# Frequent customers (min_orders defines the threshold)
python -m src.cli.main report frequent_customers --min_orders 5
