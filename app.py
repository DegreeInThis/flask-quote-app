from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello Rueben, your Flask app is running!"

@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    result = None
    error = None
    if request.method == 'POST':
        try:
            num1 = float(request.form['num1'])
            num2 = float(request.form['num2'])
            op = request.form['op']
            if op == '+':
                result = num1 + num2
            elif op == '-':
                result = num1 - num2
            elif op == '*':
                result = num1 * num2
            elif op == '/':
                if num2 != 0:
                    result = num1 / num2
                else:
                    error = "Error: Division by zero"
            else:
                error = "Invalid operation"
        except Exception as e:
            error = str(e)
    return render_template_string('''
        <h2>Simple Calculator</h2>
        <form method="post">
            <input name="num1" type="number" step="any" required>
            <input name="num2" type="number" step="any" required>
            <select name="op">
                <option value="+">+</option>
                <option value="-">-</option>
                <option value="*">*</option>
                <option value="/">/</option>
            </select>
            <button type="submit">Calculate</button>
        </form>
        {% if result is not none %}
            <p>Result: {{ result }}</p>
        {% elif error %}
            <p style="color:red;">{{ error }}</p>
        {% endif %}
    ''', result=result, error=error)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)