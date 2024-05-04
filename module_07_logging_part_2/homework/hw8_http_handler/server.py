from flask import Flask, request

app = Flask(__name__)


@app.route('/log', methods=['POST'])
def log():
    """
    Записываем полученные логи которые пришли к нам на сервер
    return: текстовое сообщение об успешной записи, статус код успешной работы

    """
    log_data = request.form
    if log_data is None:
        return 'Пустое тело запроса.', 400

    with open('server.log', 'a') as log_file:
        log_file.write(f'{log_data.to_dict(flat=False)}\n')

    return 'Успех!'


@app.route('/logs', methods=['GET'])
def logs():
    """
    Рендерим список полученных логов
    return: список логов обернутый в тег HTML <pre></pre>
    """
    with open('server.log', 'r') as log_file:
        log_items = log_file.read().replace('\n', '</br>')
    return f"<pre>{log_items}</pre>"


if __name__ == '__main__':
    app.run(debug=True)
