from flask import Flask, jsonify, request
from celery1 import process_images, restore

app = Flask(__name__)

subscribers = []


@app.route('/blur', methods=['POST'])
def blur_image():
    if not request.files:
        return jsonify({'message': 'No file part'})

    task_id = process_images(request.files, subscribers)

    return jsonify({'task_id': task_id})


@app.route('/status/<task_id>', methods=['GET'])
def task_status(task_id):
    result = restore(task_id)

    if result:
        progress = result.completed_count() / len(result)
        return jsonify({'progress': progress, "status": ", ".join(i.status for i in result)}), 200
    else:
        return jsonify({'error': 'Invalid group_id'}), 404

    return jsonify({'task_id': task.id, 'status': task.status, 'info': task.info})


@app.route('/subscribe', methods=['POST'])
def subscribe():
    data = request.get_json()
    email = data.get('email')

    if email not in subscribers:
        subscribers.append(email)
        return jsonify({'message': 'Subscribed successfully'})
    else:
        return jsonify({'message': 'Already subscribed'})


@app.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    data = request.get_json()
    email = data.get('email')

    if email in subscribers:
        subscribers.remove(email)
        return jsonify({'message': 'Unsubscribed successfully'})
    else:
        return jsonify({'message': 'Email not found in subscribers list'})


if __name__ == '__main__':
    app.run(debug=False)
