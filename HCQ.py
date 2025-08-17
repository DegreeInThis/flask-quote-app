from flask import Flask, request, render_template_string

app = Flask(__name__)

# Define service area
SERVICE_AREA = ['Gloucester', 'Cheltenham', 'Stroud', 'Tewkesbury']

# --- Home Route ---
@app.route('/')
def home():
    return "Hello Rueben, your Flask app is running!"

# --- Calculator Route ---
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

# --- Quotation Route ---
@app.route('/quote', methods=['GET', 'POST'])
def quote():
    form_template = """
    <!doctype html>
    <title>Removal Service Quotation</title>
    <h2>Get Your Quotation</h2>
    <form method="post">
      Name: <input type="text" name="name" required><br><br>
      Location (Town/Postcode): <input type="text" name="location" required><br><br>
      Property Type:
      <select name="property_type">
        <option>Flat</option>
        <option>House</option>
        <option>Bungalow</option>
      </select><br><br>
      Bedrooms: <input type="number" name="bedrooms" min="0" required><br><br>
      Floors: <input type="number" name="floors" min="0" required><br><br>
      Packing Required? <input type="checkbox" name="packing"><br><br>
      Furniture Assembly? <input type="checkbox" name="assembly"><br><br>
      Special Items (comma-separated): <input type="text" name="special_items"><br><br>
      Preferred Date: <input type="date" name="date"><br><br>
      <input type="submit" value="Get Quote">
    </form>

    {% if quote %}
      <h3>Quotation for {{ name }}</h3>
      {% if in_area %}
        <p>Estimated Price: <strong>£{{ quote }}</strong></p>
        <p>We serve your area: {{ location }}</p>
      {% else %}
        <p>Sorry, we currently do not serve your area: {{ location }}</p>
      {% endif %}
    {% endif %}
    """

    if request.method == "POST":
        name = request.form["name"]
        location = request.form["location"].strip().title()
        bedrooms = int(request.form["bedrooms"])
        floors = int(request.form["floors"])
        packing = "packing" in request.form
        assembly = "assembly" in request.form
        special_items = request.form["special_items"].split(",") if request.form["special_items"] else []

        in_area = any(area in location for area in SERVICE_AREA)

        base_price = 100
        price = base_price
        price += bedrooms * 30
        price += floors * 20
        if packing:
            price += 50
        if assembly:
            price += 40
        price += len(special_items) * 25

        return render_template_string(form_template, quote=price, name=name, location=location, in_area=in_area)

    return render_template_string(form_template)

# --- Run App ---
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)