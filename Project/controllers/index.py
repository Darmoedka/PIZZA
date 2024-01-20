from app import app
from flask import render_template, request, session
from utils import get_db_connection
from models.index_model import get_customer, get_order_buy_customer, get_new_customer, get_order_buy, set_return_date


@app.route('/', methods=['GET'])
def index():
    conn = get_db_connection()

    if request.values.get('customer'):
        customer_id = int(request.values.get('customer'))
        session['customer_id'] = customer_id
    elif request.values.get('new_customer'):
        new_customer = request.values.get('new_customer')
        session['customer_id'] = get_new_customer(conn, new_customer)
        print("get_new_customer(conn, new_customer) = ", get_new_customer(conn, new_customer))
    elif request.values.get('order_buy'):
        order_buy_id = int(request.values.get('order_buy'))
        get_order_buy(conn, order_buy_id, session['customer_id'])
    elif request.values.get('return_val'):
        order_buy_customer_id = request.values.get("return_val")
        set_return_date(conn, order_buy_customer_id)
    else:
        if "customer_id" in session.keys():
            session['customer_id'] = session['customer_id']
        else:
            session['customer_id'] = 1


    df_customer = get_customer(conn)
    df_order_buy_customer = get_order_buy_customer(conn, session['customer_id'])

    html = render_template(
        'index.html',
        customer_id=session['customer_id'],
        combo_box=df_customer,
        order_buy_customer=df_order_buy_customer,
        len=len,
    )
    return html
