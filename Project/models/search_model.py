import pandas

def get_pizza_count(conn):
    return pandas.read_sql(
        '''
            WITH cte (pizza_name, pizza_count) AS (
                SELECT
                    pizza_name,
                    COUNT(order_buy_id)
                FROM
                    pizza
                    JOIN order_buy USING (pizza_id)
                GROUP BY
                    pizza_name
            )
            SELECT * FROM cte
        ''',
        conn
    )

def get_doping_count(conn):
    return pandas.read_sql(
        '''
            WITH cte (doping_name, doping_count) AS (
                SELECT
                    doping_name,
                    COUNT(order_buy_id)
                FROM
                    doping
                    JOIN order_buy USING (doping_id)
                GROUP BY
                    doping_name
            )
            SELECT * FROM cte
        ''',
        conn
    )

def get_all_pizza(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT pizza_name FROM pizza")
    genres = [row[0] for row in cursor.fetchall()]
    cursor.close()
    return genres

def get_all_doping(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT doping_name FROM doping")
    publishers = [row[0] for row in cursor.fetchall()]
    cursor.close()
    return publishers


def get_filtered_order_buy(conn, selected_pizza, selected_doping):
    return pandas.read_sql(
        '''
            WITH get_order_buy AS (
                SELECT
                    pizza_name,
                    doping_name,
                    hour_delivery,
                    order_buy_date,
                    order_buy_id
                FROM
                    order_buy
                    JOIN doping USING (doping_id)
                    JOIN pizza USING (pizza_id)
                WHERE
                    doping_name IN {}
                    AND pizza_name IN {}
            )
            SELECT
                *
            FROM get_order_buy
        '''.format(
                '({})'.format(', '.join([f'"{elem}"' for elem in selected_doping])),
                '({})'.format(', '.join([f'"{elem}"' for elem in selected_pizza]))
            ),
        conn
    )