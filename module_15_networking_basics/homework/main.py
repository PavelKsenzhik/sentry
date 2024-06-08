import datetime

from flask import Flask, request, Response, jsonify, url_for, abort, make_response

from models import Room, Order, init_db, add_new_room, get_rooms, get_all_rooms, get_room_not_free, add_order, \
    get_room_by_id, update_room_by_id, delete_room_by_id

app: Flask = Flask(__name__)


def add_public_urls(room):
    room.url = url_for('get_room', id=room['id'], _external=True)
    room.urlRooms = url_for('get_rooms', _external=True)
    return room


# @app.route('/add-room', methods=['POST'])
# def add_room() -> Response:
#     data = request.get_json()
#     room = Room(
#         id=None,
#         floor=data["floor"],
#         beds=data["beds"],
#         guest_num=data["guestNum"],
#         price=data["price"]
#     )
#
#     new_id = add_new_room(room)
#
#     return jsonify({"id": new_id}), 200


@app.route('/room/<id>', methods=['GET'])
def get_room(id: str) -> Response:
    room = get_room_by_id(id)
    if room:
        room = add_public_urls(room)
        return room.to_json()
    else:
        return abort(404)


@app.route('/room', methods=['GET'])
def get_rooms() -> Response:
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
        room = add_public_urls(room)
        result["rooms"].append({
            "roomId": room.id,
            "floor": room.floor,
            "guestNum": room.guest_num,
            "beds": room.beds,
            "price": room.price,
            "url": room.url,
            "urlRooms": room.urlRooms
        })
    return jsonify(result)


@app.route("/room/<id>", methods=["PUT"])
def update_room(id):
    rooms = get_all_rooms()

    room = dict()
    for i_room in rooms:
        if str(i_room['id']) == str(id):
            room = i_room
            break

    if not request.json:
        abort(400)


    try:
        updated_room = update_room_by_id(
            id,
            request.json.get('floor', room.floor),
            request.json.get('beds', room['beds']),
            request.json.get('guest_num', room['guest_num']),
            request.json.get('price', room['price'])
        )
        updated_room = add_public_urls(updated_room)
        return updated_room.to_json()
    except:
        abort(404)


@app.route("/room/<id>", methods=["DELETE"])
def delete_room(id):
    result = {
        "status": True,
        "urlRooms": url_for('get_rooms', _external=True)
    }
    if delete_room_by_id(id):
        result["status"] = True
        return jsonify({'result': result})
    else:
        return abort(404)


@app.route("/room", methods=["POST"])
def add_room():
    if not request.json:
        abort(400)

    data = request.get_json()
    room = Room(
        id=None,
        floor=data["floor"],
        beds=data["beds"],
        guest_num=data["guestNum"],
        price=data["price"]
    )

    new_room = add_new_room(room)
    new_room = add_public_urls(new_room)

    return new_room.to_json(), 200





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



@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    init_db()
    app.config["WTF_CSRF_ENABLED"] = False
    app.run(debug=True, port=5000, host="localhost")
