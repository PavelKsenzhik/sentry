from flask import Flask

app = Flask(__name__)


@app.route("/max_number/<path:nums>")
def max_number(nums):
    nums = nums.split('/')
    try:
        nums_list = [int(num) for num in nums]
    except ValueError:
        return 'Необходимо вводить только числа'
    return f'Максимальное числло: {max(nums_list)}'


if __name__ == "__main__":
    app.run(debug=True)
