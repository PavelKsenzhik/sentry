import datetime

from flask import Flask, request, Response, jsonify

from models import Room, Order, init_db, add_new_room, get_rooms, get_all_rooms, get_room_not_free, add_order

app: Flask = Flask(__name__)


@app.route('/add-room', methods=['POST'])
def add_room() -> Response:
    data = request.get_json()
    room = Room(
        id=None,
        floor=data["floor"],
        beds=data["beds"],
        guest_num=data["guestNum"],
        price=data["price"]
    )

    new_id = add_new_room(room)

    return jsonify({"id": new_id}), 200


@app.route('/room', methods=['GET'])
def get_room() -> Response:
    check_in = request.args.get('checkIn')
    check_out = request.args.get('checkOut')
    guests_num = request.args.get('guestsNum')

    if check_in and check_out and guests_num:
        rooms = get_rooms(
            datetime.datetime.strptime(check_in, "%Y%m%d"),
            datetime.datetime.strptime(check_out, "%Y%m%d"),
            int(guests_num))
    else:
        rooms = get_all_rooms()

    result: dict = {
        "rooms": []
    }
    for room in rooms:
        result["rooms"].append({
            "roomId": room.id,
            "floor": room.floor,
            "guestNum": room.guest_num,
            "beds": room.beds,
            "price": room.price,
        })
    return jsonify(result)


@app.route('/booking', methods=['POST'])
def booking():
    data = request.get_json()
    order = Order(
        id=None,
        check_in=datetime.datetime.strptime(str(data["bookingDates"]["checkIn"]), "%Y%m%d"),
        check_out=datetime.datetime.strptime(str(data["bookingDates"]["checkOut"]), "%Y%m%d"),
        first_name=data["firstName"],
        last_name=data["lastName"],
        room_id=data["roomId"]
    )

    if get_room_not_free(order.check_in, order.check_out, order.room_id):
        return Response(status=409)

    order_id = add_order(order)
    return jsonify({"roomId": order_id}), 200


if __name__ == '__main__':
    init_db()
    app.config["WTF_CSRF_ENABLED"] = False
    app.run(debug=True, port=5000, host="localhost")
