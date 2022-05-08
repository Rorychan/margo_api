from flask import Flask, request, jsonify, make_response
import uuid
users = {}
orders = {}
app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World'
@app.route("/api/v1/register",methods = ["POST"])
def register():
    global users
    if request.method == "POST":
        user_info = request.get_json()
        if user_info["nickname"] in users:
            resp = make_response(jsonify({"error": "user already exists"}),400)
            return resp
        else:
            users[user_info["nickname"]] = {
                "name": user_info["name"],
                "pass": user_info["pass"],
                "orders": []
            }
            resp = make_response
@app.route("/api/v1/orders", methods = ["POST"])
def orders_processor():
    global orders
    if request.method == "POST":
        if request.cookies.get("UserId") == None:
            user_id = uuid.uuid4()
            orders.update({str(user_id): {}})
        else:
            user_id = request.cookies.get("UserId")
        user_id_str = str(user_id)
        order_data = request.get_json()
        print(order_data)

        order_id = uuid.uuid4()
        order_id_str = str(order_id)
        print(order_id)
        orders[user_id_str].update({order_id_str: order_data})
        resp = make_response(jsonify(orders[user_id_str]),200)
        resp.set_cookie("UserId",user_id_str)
        print(orders)
    return resp
@app.route("/api/v1/orders", methods = ["GET"])
def get_orders():
    global orders
    if request.method == "GET":
        if request.cookies.get("UserId") == None:
            resp = make_response({"Message": "User not found"}, 404)
            return resp
        else:
            resp = make_response(orders[request.cookies.get("UserId")], 200)
            return resp

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5001, debug = True)