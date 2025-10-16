import json
import os
from flask import Flask, render_template, request, jsonify,redirect,url_for,flash
from flask_mail import Mail,Message
from checkout import process_checkout
import requests
from bakong_khqr import KHQR
import qrcode
from qr import token
app = Flask(__name__)
app.config.from_object('config')
app.secret_key = os.urandom(24)
mail = Mail(app)

products =  [
    {
      "id": 1,
      "title": "Essence Mascara Lash Princess",
      "description": "The Essence Mascara Lash Princess is a popular mascara known for its volumizing and lengthening effects. Achieve dramatic lashes with this long-lasting and cruelty-free formula.",
      "category": "beauty",
      "price": 0.1,
      "discountPercentage": 10.48,
      "rating": 2.56,
      "stock": 99,
      "tags": [
        "beauty",
        "mascara"
      ],
      "brand": "Essence",
      "sku": "BEA-ESS-ESS-001",
      "weight": 4,
      "dimensions": {
        "width": 15.14,
        "height": 13.08,
        "depth": 22.99
      },
      "warrantyInformation": "1 week warranty",
      "shippingInformation": "Ships in 3-5 business days",
      "availabilityStatus": "In Stock",
      "reviews": [
        {
          "rating": 3,
          "comment": "Would not recommend!",
          "date": "2025-04-30T09:41:02.053Z",
          "reviewerName": "Eleanor Collins",
          "reviewerEmail": "eleanor.collins@x.dummyjson.com"
        },
        {
          "rating": 4,
          "comment": "Very satisfied!",
          "date": "2025-04-30T09:41:02.053Z",
          "reviewerName": "Lucas Gordon",
          "reviewerEmail": "lucas.gordon@x.dummyjson.com"
        },
        {
          "rating": 5,
          "comment": "Highly impressed!",
          "date": "2025-04-30T09:41:02.053Z",
          "reviewerName": "Eleanor Collins",
          "reviewerEmail": "eleanor.collins@x.dummyjson.com"
        }
      ],
      "returnPolicy": "No return policy",
      "minimumOrderQuantity": 48,
      "meta": {
        "createdAt": "2025-04-30T09:41:02.053Z",
        "updatedAt": "2025-04-30T09:41:02.053Z",
        "barcode": "5784719087687",
        "qrCode": "https://cdn.dummyjson.com/public/qr-code.png"
      },
      "images": [
        "https://cdn.dummyjson.com/product-images/beauty/essence-mascara-lash-princess/1.webp"
      ],
      "thumbnail": "https://cdn.dummyjson.com/product-images/beauty/essence-mascara-lash-princess/thumbnail.webp"
    }
  ]


def get_filtered_products():
  response = requests.get('https://dummyjson.com/products?limit=100')
  data = response.json()
  excluded = ['furniture', 'groceries', 'beauty']
  products = [p for p in data['products'] if p['category'] not in excluded]

  # Priority categories first
  priority = ['mens-watches', 'mens-shirts', 'laptops']
  products.sort(key=lambda x: (priority.index(x['category'])
                               if x['category'] in priority else len(priority)))
  return products
@app.get('/')
@app.get('/home')
def home():
    module = 'home'
    products = get_filtered_products()
    return render_template('front/home.html', products=products)
@app.get('/cart')
def cart():
    return render_template('front/cart.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')  # Customer's email
        subject = request.form.get('subject')
        message = request.form.get('message')

        # Email to shop owner
        shop_body = f"From: {name} <{email}>\n\n{message}"

        # Confirmation email to customer
        customer_subject = "Thank you for contacting us!"
        customer_body = f"Hi {name},\n\nThank you for reaching out. We have received your message:\n\nSubject: {subject}\nMessage: {message}\n\nWe will get back to you shortly.\n\nBest regards,\nKR STORE"

        try:
            # Email to shop
            msg_shop = Message(subject=subject,
                               recipients=['hphalla3@gmail.com'],
                               body=shop_body)
            mail.send(msg_shop)

            # Confirmation email to customer
            msg_customer = Message(subject=customer_subject,
                                   recipients=[email],
                                   body=customer_body)
            mail.send(msg_customer)

            flash('Message sent successfully! Confirmation email sent to you.', 'success')
        except Exception as e:
            flash(f'Failed to send message: {e}', 'danger')

        return redirect(url_for('contact'))

    return render_template('front/contact.html')

@app.get('/product')
def product():
  products = get_filtered_products()
  return render_template('front/product.html', products=products, module='product')

@app.route('/Category/<category_name>')
def category_page(category_name):
    filtered_products = [p for p in products if p['category'].lower() == category_name.lower()]
    return render_template('front/category.html', products=filtered_products, category=category_name.title())

@app.get('/about')
def about():
    return render_template('front/about.html')
@app.route('/product/<int:id>')
def product_detail(id):
    product = next((p for p in products if p['id'] == id), None)
    if product is None:
        return "Product not found", 404
    return render_template('front/product_detail.html', product=product)

@app.route("/checkout", methods=["GET"])
def checkout_page():
    return render_template("front/checkout.html")

@app.route("/checkout", methods=["POST"])
def checkout():
    data = request.json
    try:
        result = process_checkout(app, mail, data)
        return jsonify(result)
    except Exception as e:
        print("Exception in /checkout:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

@app.post('/buy_now')
def buy_now():
    try:
        cart = json.loads(request.form.get('cart', '[]'))
        price = sum(float(item['price']) * int(item['qty']) for item in cart)
        currency = 'USD'
        # Generate KHQR (you already have KHQR token)
        khqr = KHQR(token)
        qr_str = khqr.create_qr(
            bank_account='phallaheang@aclb',
            merchant_name='PHALLA',
            merchant_city='Phnom Penh',
            amount=price,
            currency=currency,
            store_label='KRShop',
            phone_number='855964775515',
            bill_number='TRX01234567',
            terminal_label='Cashier-01',
            static=False
        )

        md5 = khqr.generate_md5(qr_str)

        # Save QR image
        qr_object = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr_object.add_data(qr_str)
        qr_object.make(fit=True)
        img = qr_object.make_image(fill_color="black", back_color="white")
        qr_path = "./static/image/qrcode.png"
        img.save(qr_path)

        return jsonify({
            "status": "success",
            "amount": price,
            "currency": currency,
            "md5": md5,
            "merchant_name": "PHALLA HEANG",
            "qr_url": "/static/image/qrcode.png"

        })
    except Exception as e:
        print("Buy Now Error:", e)
        return jsonify({"status": "error", "message": str(e)})

@app.post('/check-payment')
def check_payment():
    json_data = request.get_json()
    md5 = json_data.get('md5')
    res = requests.post(
        'https://api-bakong.nbc.gov.kh/v1/check_transaction_by_md5',
        json={
            'md5': md5
        },
        headers={
            'authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
    )

    return res.json()
@app.get('/customer_thanks')
def customer_thanks():
    return render_template('khqr/customer_thanks.html')



if __name__ == "__main__":
    app.run(debug=True)

