from flask import Blueprint, request, jsonify
from .models import Order
from . import db

api = Blueprint('api', __name__)

@api.route('/orders')
def get_orders():
    page = int(request.args.get('page', 1))
    limit = request.args.get('limit', 100)

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
