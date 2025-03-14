from openpyxl import Workbook
from .database import SQLALCHEMY_DATABASE_URL
import psycopg2

def export_orders():
    # Connect to the database
    conn = psycopg2.connect(SQLALCHEMY_DATABASE_URL)
    cursor = conn.cursor()

    # Fetch orders from the database
    cursor.execute("""
        SELECT users.email as user_email, products.name as product_name, order_items.quantity, products.price as unit_price, orders.total_price
        FROM orders
        JOIN users ON orders.user_id = users.id
        JOIN order_items ON orders.id = order_items.order_id
        JOIN products ON order_items.product_id = products.id
    """)
    orders = cursor.fetchall()

    # Create a new Excel workbook and add a worksheet
    wb = Workbook()
    ws = wb.active
    ws.append(['Пользователь', 'Товар', 'Количество', 'Цена', 'Итого'])

    # Add orders to the worksheet
    for order in orders:
        ws.append(order)

    # Save the workbook to a file
    wb.save('orders.xlsx')

    # Close the database connection
    cursor.close()
    conn.close()