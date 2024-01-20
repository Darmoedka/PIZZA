import pandas

def get_customer(conn):
    return pandas.read_sql(
    '''
            SELECT * FROM customer
        ''',
    conn
    )

def get_order_buy_customer(conn, customer_id):
    return pandas.read_sql('''
        SELECT 
            pizza_name AS Пицца,
            order_buy_date AS Дата_оформления_заказа, 
            hour_delivery AS Ориентировочное_время_доставки_в_часах,
            order_buy_customer_id
        FROM
        customer
        JOIN order_buy_customer USING(customer_id)
        JOIN order_buy USING(order_buy_id)
        
        JOIN pizza USING(pizza_id)
        WHERE customer.customer_id = :id
        ORDER BY 3
    ''',
    conn,
    params={"id": customer_id}
    )

def get_new_customer(conn, new_customer):
    cur = conn.cursor()
    cur.execute(
        '''
            INSERT INTO customer (customer_name)
            VALUES (:new_customer)
        ''',
        {"new_customer": new_customer}
    )
    conn.commit()
    return cur.lastrowid

def get_order_buy(conn, order_buy_id, customer_id):
    cur = conn.cursor()
    cur.executescript(
        f'''
            INSERT INTO order_buy_customer (order_buy_id, customer_id, getting_date)
            VALUES ({order_buy_id}, {customer_id}, DATE("NOW"));

        ''',
    )
    conn.commit()

def set_return_date(conn, order_buy_customer_id):
    cur = conn.cursor()
    cur.execute(
        f'''
            UPDATE order_buy_customer
            SET getting_date = DATE('NOW')
            WHERE order_buy_customer_id = {order_buy_customer_id}
        '''
    )
    conn.commit()
