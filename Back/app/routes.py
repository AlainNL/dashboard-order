from flask import Blueprint, request, jsonify
from .models import Order
from . import db
from sqlalchemy import and_

api = Blueprint('api', __name__)

@api.route('/orders')
def get_orders():
    page = int(request.args.get('page', 1))
    limit = request.args.get('limit', 100)

    status = request.args.get('status')
    user = request.args.get('user')
    min_amount = request.args.get('min_amount', type=float)
    max_amount = request.args.get('max_amount', type=float)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    query = Order.query

    if status:
        query = query.filter(Order.status == status)

    if user:
        query = query.filter(Order.user.ilike(f'%{user}'))

    if min_amount is not None:
        query = query.filter(Order.amount <= max_amount)

    if start_date:
        query = query.filter(Order.created_at >= start_date)

    if end_date:
        query = query.filter(Order.created_at <= end_date)

    query = query.order_by(Order.created_at.desc())

    try:
        limit = int(limit)
    except ValueError:
        return jsonify({"error": "The 'limit' parameter must be a valid integer."}), 400

    query = Order.query.order_by(Order.created_at.desc())
    orders = query.paginate(page=page, per_page=limit, error_out=False)

    results = [{
        "id": order.id,
        'user': order.user,
        "amount": order.amount,
        "status": order.status,
        "created_at": order.created_at.isoformat()
    } for order in orders.items]

    return jsonify({
        "data": results,
        "total": orders.total,
        "page": page,
        "pages": orders.pages
    })
