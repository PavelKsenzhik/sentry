from flask import Flask

app = Flask(__name__)


@app.route("/max_number/<path:nums>")
def max_number(nums):
    nums = nums.split('/')
    nums_list = []
    for num in nums:

        if num.isdigit():
            nums_list.append(int(num))
        else:
            try:
                num = float(num)
                nums_list.append(num)
            except ValueError:
                return 'Необходимо вводить только числа'
    return f'Максимальное числло: <i>{max(nums_list)}</i>'


if __name__ == "__main__":
    app.run(debug=True)
