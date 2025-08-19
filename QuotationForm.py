from flask import Flask, request, render_template_string, send_file
import pdfkit
from io import BytesIO

app = Flask(__name__)

# Base prices by page count
BASE_PRICES = {
    'starter': 249,
    'pro': 469,
    'elite': 925
}

# Website type multipliers
TYPE_MULTIPLIERS = {
    'personal': 1.0,
    'business': 1.3,
    'ecommerce': 1.8
}

# Add-on prices
ADD_ONS = {
    'seo': 150,
    'social_media': 300,
    'hosting': 99,
    'stock_images': 100,
    'blog': 120,
    'custom_app': 400,
    'business_app': 750
}

HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Website Design Quotation</title>
  <style>
    body {
      font-family: 'Segoe UI', sans-serif;
      background: #f4f7f8;
      color: #333;
      padding: 40px;
    }
    h2 {
      text-align: center;
      color: #2c3e50;
    }
    form {
      max-width: 600px;
      margin: auto;
      background: #fff;
      padding: 30px;
      border-radius: 8px;
      box-shadow: 0 0 15px rgba(0,0,0,0.1);
    }
    input[type="text"],
    input[type="email"],
    select {
      width: 100%;
      padding: 10px;
      margin-top: 6px;
      margin-bottom: 20px;
      border: 1px solid #ccc;
      border-radius: 4px;
      font-size: 16px;
    }
    input[type="checkbox"] {
      margin-right: 10px;
    }
    input[type="submit"] {
      background-color: #3498db;
      color: white;
      padding: 12px 20px;
      border: none;
      border-radius: 4px;
      cursor: pointer;
      font-size: 16px;
    }
    input[type="submit"]:hover {
      background-color: #2980b9;
    }
    .quote-box {
      max-width: 600px;
      margin: 30px auto;
      background: #eaf2f8;
      padding: 20px;
      border-radius: 8px;
      border-left: 5px solid #3498db;
    }
    .quote-box strong {
      font-size: 20px;
      color: #2c3e50;
    }
  </style>
</head>
<body>
  <h2>Get Your Website Quote</h2>
  <form method="post">
    Name: <input type="text" name="name" required value="{{ name or '' }}">
    Email: <input type="email" name="email" required value="{{ email or '' }}">

    Page Count:
    <select name="page_count">
      <option value="starter" {% if page_count == 'starter' %}selected{% endif %}>1–3 Pages (Starter)</option>
      <option value="pro" {% if page_count == 'pro' %}selected{% endif %}>4–6 Pages (Pro)</option>
      <option value="elite" {% if page_count == 'elite' %}selected{% endif %}>7+ Pages (Elite)</option>
    </select>

    Website Type:
    <select name="site_type">
      <option value="personal" {% if site_type == 'personal' %}selected{% endif %}>Personal</option>
      <option value="business" {% if site_type == 'business' %}selected{% endif %}>Business</option>
      <option value="ecommerce" {% if site_type == 'ecommerce' %}selected{% endif %}>E-commerce</option>
    </select>

    <label><input type="checkbox" name="addons" value="seo" {% if 'seo' in selected_addons %}checked{% endif %}> SEO Optimization</label><br>
    <label><input type="checkbox" name="addons" value="social_media" {% if 'social_media' in selected_addons %}checked{% endif %}> Social Media Setup</label><br>
    <label><input type="checkbox" name="addons" value="hosting" {% if 'hosting' in selected_addons %}checked{% endif %}> Hosting & Domain Setup</label><br>
    <label><input type="checkbox" name="addons" value="stock_images" {% if 'stock_images' in selected_addons %}checked{% endif %}> Stock Images</label><br>
    <label><input type="checkbox" name="addons" value="blog" {% if 'blog' in selected_addons %}checked{% endif %}> Blog Creation</label><br>
    <label><input type="checkbox" name="addons" value="custom_app" {% if 'custom_app' in selected_addons %}checked{% endif %}> Custom Web App</label><br>
    <label><input type="checkbox" name="addons" value="business_app" {% if 'business_app' in selected_addons %}checked{% endif %}> Business App</label><br><br>

    <input type="submit" value="Get Quote">
  </form>

  {% if quote %}
    <div class="quote-box">
      <h3>Quotation for {{ name }}</h3>
      <p>Email: <strong>{{ email }}</strong></p>
      <p>Website Type: <strong>{{ site_type.capitalize() }}</strong></p>
      <p>Page Count: <strong>{{ page_count.capitalize() }}</strong></p>
      <p>Add-ons Selected:</p>
      <ul>
        {% for addon in selected_addons %}
          <li>{{ addon.replace('_', ' ').title() }}</li>
        {% endfor %}
      </ul>
      <p>Estimated Price: <strong>£{{ quote }}</strong></p>

      <form method="post" action="/download">
        <input type="hidden" name="name" value="{{ name }}">
        <input type="hidden" name="email" value="{{ email }}">
        <input type="hidden" name="page_count" value="{{ page_count }}">
        <input type="hidden" name="site_type" value="{{ site_type }}">
        {% for addon in selected_addons %}
          <input type="hidden" name="addons" value="{{ addon }}">
        {% endfor %}
        <input type="hidden" name="quote" value="{{ quote }}">
        <input type="submit" value="Download Quote as PDF">
      </form>
    </div>
  {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def quote():
    name = email = page_count = site_type = None
    selected_addons = []
    total_quote = None

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        page_count = request.form["page_count"]
        site_type = request.form["site_type"]
        selected_addons = request.form.getlist("addons")

        base_price = BASE_PRICES.get(page_count, 0)
        multiplier = TYPE_MULTIPLIERS.get(site_type, 1.0)
        adjusted_price = base_price * multiplier
        addons_total = sum(ADD_ONS.get(addon, 0) for addon in selected_addons)
        total_quote = round(adjusted_price + addons_total, 2)

    return render_template_string(
        HTML_TEMPLATE,
        name=name,
        email=email,
        page_count=page_count,
        site_type=site_type,
        selected_addons=selected_addons,
        quote=total_quote
    )

@app.route("/download", methods=["POST"])
def download_pdf():
    name = request.form["name"]
    email = request.form["email"]
    page_count = request.form["page_count"]
    site_type = request.form["site_type"]
    selected_addons = request.form.getlist("addons")
    quote = request.form["quote"]

    html = f"""
    <html>
    <head><meta charset="UTF-8"></head>
    <body style='font-family: Segoe UI; padding: 30px;'>
        <h2>Quotation for {name}</h2>
        <p>Email: <strong>{email}</strong></p>
        <p>Website Type: <strong>{site_type.capitalize()}</strong></p>
        <p>Page Count: <strong>{page_count.capitalize()}</strong></p>
        <p>Add-ons Selected:</p>
        <ul>
            {''.join(f"<li>{addon.replace('_', ' ').title()}</li>" for addon in selected_addons)}
        </ul>
        <p>Estimated Price: <strong>£{quote}</strong></p>
    </body>
    </html>
    """

    pdf = pdfkit.from_string(html, False)
    return send_file(BytesIO(pdf), download_name="quote.pdf", as_attachment=True)

if __name__ == "__