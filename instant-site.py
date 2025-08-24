from flask import Flask, render_template, request, redirect
import random

app = Flask(__name__)

# Template preview URLs (can be IONOS or your own hosted previews)
TEMPLATES = {
    "modern": "https://www.levelasolutions.co.uk/templates/modern-preview",
    "bold": "https://www.levelasolutions.co.uk/templates/bold-preview",
    "minimal": "https://www.levelasolutions.co.uk/templates/minimal-preview"
}

@app.route('/', methods=['GET', 'POST'])
def instant_site():
    if request.method == 'POST':
        data = request.form.to_dict()

        # Handle "Surprise Me" logic
        if data.get('surprise_me'):
            data['template'] = random.choice(list(TEMPLATES.keys()))

        # Calculate pricing
        base_price = {
            "starter": 9900,
            "pro": 19900,
            "premium": 29900
        }.get(data.get("package"), 9900)

        add_ons = 0
        if data.get("add_logo"): add_ons += 4900
        if data.get("add_seo"): add_ons += 7900
        if data.get("add_email"): add_ons += 2900

        total_price = base_price + add_ons

        preview_url = TEMPLATES.get(data.get("template"), "")

        return render_template("confirmation.html", data=data, preview_url=preview_url, total_price=total_price)

    return render_template("form.html", templates=TEMPLATES)