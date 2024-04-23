"""
Напишите эндпоинт, который принимает на вход код на Python (строка)
и тайм-аут в секундах (положительное число не больше 30).
Пользователю возвращается результат работы программы, а если время, отведённое на выполнение кода, истекло,
то процесс завершается, после чего отправляется сообщение о том, что исполнение кода не уложилось в данное время.
"""
import subprocess
from subprocess import Popen, TimeoutExpired

from flask import Flask, Response
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired, NumberRange

app = Flask(__name__)


class CodeForm(FlaskForm):
    code = StringField(validators=[InputRequired(message="Ожидалась строка")])
    timeout = IntegerField(validators=[InputRequired(), NumberRange(min=0, max=30, message='Ожидалось пооложительное число не больше 30')])


def run_python_code_in_subproccess(code: str, timeout: int):
    cmd = f"prlimit --nproc=1:1 python -c '{code}'"
    proc = Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        outs, errs = proc.communicate(timeout=timeout)
        return f"Python code successfully run\nouts: {outs}\nerrs: {errs}"
    except TimeoutExpired:
        proc.kill()
        outs, errs = proc.communicate()
        return f"Timeout ended\nouts: {outs}\nerrs: {errs}"


@app.route('/run_code', methods=['POST'])
def run_code():
    code_form = CodeForm()
    if code_form.validate_on_submit():
        res = run_python_code_in_subproccess(code_form.data["code"], code_form.data["timeout"])
        return Response(res, status=200)
    else:
        errors = code_form.errors
        error_output = ""

        for key in errors:
            error_output += f"{key}: "
            for err_message in errors[key]:
                error_output += f"{err_message}; "
            error_output += "\n"

        return Response(error_output, status=400)


if __name__ == '__main__':
    app.config["WTF_CSRF_ENABLED"] = False
    app.run(debug=True)
