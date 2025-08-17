from flask import Flask, request, render_template_string

app = Flask(__name__)

# Define service area (you can expand this list)
SERVICE_AREA = ['Gloucester', 'Cheltenham', 'Stroud', 'Tewkesbury']

# HTML form template
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

@app.route("/", methods=["GET", "POST"])
def quote():
    if request.method == "POST":
        name = request.form["name"]
        location = request.form["location"].strip().title()
        bedrooms = int(request.form["bedrooms"])
        floors = int(request.form["floors"])
        packing = "packing" in request.form
        assembly = "assembly" in request.form
        special_items = request.form["special_items"].split(",") if request.form["special_items"] else []

        # Check jurisdiction
        in_area = any(area in location for area in SERVICE_AREA)

        # Pricing logic
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

if __name__ == "__main__":
    app.run(debug=True)

