from app import app
from flask import render_template, request
from utils import get_db_connection
from models.search_model import get_pizza_count, get_doping_count, get_filtered_order_buy,  get_all_pizza, get_all_doping

@app.route('/search', methods=['GET', 'POST'])
def search():
    conn = get_db_connection()

    selected_pizza = []
    selected_doping = []

    df_pizza = get_pizza_count(conn)
    df_doping = get_doping_count(conn)
    df_order_buy = get_filtered_order_buy(
            conn,
            get_all_pizza(conn),
            get_all_doping(conn)
        )
    
    if request.method == 'POST':
        if 'confirm' in request.form:
            selected_pizza = request.form.getlist("pizza")
            selected_doping = request.form.getlist("doping")

        if 'reset' in request.form:
            selected_pizza = []
            selected_doping = []
        
        df_order_buy = get_filtered_order_buy(
            conn,
            get_all_pizza(conn) if not selected_pizza else selected_pizza,
            get_all_doping(conn) if not selected_doping else selected_doping
        )

    html = render_template(
        'search.html',
        selected_pizza=selected_pizza,
        df_pizza=df_pizza,
        selected_doping=selected_doping,
        df_doping=df_doping,
        df_order_buy=df_order_buy
    )
    return html
