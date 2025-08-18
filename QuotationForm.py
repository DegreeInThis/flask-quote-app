form_template = """
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
    input[type="date"],
    select,
    textarea {
      width: 100%;
      padding: 10px;
      margin-top: 6px;
      margin-bottom: 20px;
      border: 1px solid #ccc;
      border-radius: 4px;
      box-sizing: border-box;
      font-size: 16px;
    }
    input[type="checkbox"] {
      margin-right: 10px;
    }
    textarea {
      resize: vertical;
    }
    input[type="submit"] {
      background-color: #3498db;
      color: white;
      padding: 12px 20px;
      border: none;
      border-radius: 4px;
      cursor: pointer;
      font-size: 16px;
      transition: background 0.3s ease;
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
    Name: <input type="text" name="name" required>
    Email: <input type="email" name="email" required>
    Website Type:
    <select name="website_type">
      <option>Portfolio</option>
      <option>Blog</option>
      <option>Business</option>
      <option>E-commerce</option>
      <option>Booking</option>
    </select>
    Number of Pages:
    <select name="pages">
      <option>1–5</option>
      <option>6–10</option>
      <option>11–20</option>
      <option>20+</option>
    </select>
    <label><input type="checkbox" name="ecommerce"> E-commerce Functionality</label><br>
    <label><input type="checkbox" name="apps"> Custom Web Apps Needed</label><br>
    <label><input type="checkbox" name="images"> Stock Images Required</label><br>
    <label><input type="checkbox" name="seo"> SEO Optimization</label><br>
    <label><input type="checkbox" name="hosting"> Hosting & Domain Setup</label><br><br>
    Deadline: <input type="date" name="deadline">
    Additional Notes:<br>
    <textarea name="notes" rows="4" cols="40"></textarea><br>
    <input type="submit" value="Get Quote">
  </form>

  {% if quote %}
    <div class="quote-box">
      <h3>Quotation for {{ name }}</h3>
      <p>Estimated Price: <strong>£{{ quote }}</strong></p>
      <p>We'll follow up via: <strong>{{ email }}</strong></p>
    </div>
  {% endif %}
</body>
</html>
"""