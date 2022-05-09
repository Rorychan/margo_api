from flask import Flask, request, jsonify, make_response
import uuid
import hashlib
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
        nickname = user_info["nickname"]
        user_id = hashlib.sha256(user_info["nickname"].encode("utf-8")).hexdigest()
        if user_id in users:
            resp = make_response(jsonify({"msg": "user already exists"}),403)
            return resp
        else:
            users[user_id] = {
                "nickname": user_info["nickname"],
                "name": user_info["name"],
                "pass": hashlib.sha256(user_info["pass"].encode("utf-8")).hexdigest(),
                "orders": {}
            }
            resp = make_response(jsonify({"msg":"created"}),200)
            resp.set_cookie("UserId", user_id)
            return resp
@app.route("/api/v1/login", methods = ["POST"])
def login():
    global users
    if request.method == "POST":
        user_info = request.get_json()
        user_id = hashlib.sha256(user_info["nickname"].encode("utf-8")).hexdigest()
        if user_id in users:
            if hashlib.sha256(user_info["pass"].encode("utf-8")).hexdigest() == users[user_id]["pass"]:
                resp = make_response({"msg":"logged in"}, 200)
                resp.set_cookie("UserId", user_id)
                return resp
            else:
                resp = make_response(jsonify({"msg":"password incorrect"}), 401)
                return resp
        else:
            resp = make_response(jsonify({"msg": "user is not exisiting"}), 401)
            return resp
    else:
        return 400

@app.route("/api/v1/orders", methods = ["POST"])
def orders_processor():
    global orders
    if request.method == "POST":
        if request.cookies.get("UserId") == None:
            resp = make_response({"msg": "User is not authorised"}, 401)
            return resp
        else:
            user_id = request.cookies.get("UserId")
        order_data = request.get_json()
        print(order_data)
        order_id = uuid.uuid4()
        order_id_str = str(order_id)
        print(user_id)
        users[user_id]["orders"].update({order_id_str: order_data})
        resp = make_response(users[user_id]["orders"][order_id_str],200)
        resp.set_cookie("UserId",user_id)
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
@app.route("/api/v1/users", methods = ["GET"])
def get_users():
    resp = make_response(users, 200)
    return resp
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5001, debug = True)