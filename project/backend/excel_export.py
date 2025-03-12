from openpyxl import Workbook
import psycopg2

def export_orders():
    # Connect to PostgreSQL database
    conn = psycopg2.connect(
        dbname="your_dbname",
        user="your_user",
        password="your_password",
        host="your_host",
        port="your_port"
    )
    cursor = conn.cursor()

    # Fetch orders from the database
    cursor.execute("SELECT user_email, product_name, quantity, unit_price, total_price FROM orders")
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