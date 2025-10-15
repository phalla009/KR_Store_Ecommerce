
import qrcode
import hashlib
from flask import Flask, render_template, request, url_for, redirect
from bakong_khqr import KHQR
import requests

app = Flask(__name__)

# Your Bakong API token
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7ImlkIjoiYzAzMTJjMDE2NDQwNDNhNiJ9LCJpYXQiOjE3NTk5ODE4MzEsImV4cCI6MTc2Nzc1NzgzMX0.TA0uZ8y6JRcmTvM8VFTqJbERtinoU76DVo3Wvp1T4ts"

@app.route('/')
def home():
    return render_template('index.html')


@app.post('/buy_now')
def buy_now():
    price = request.form.get('price')
    product = request.form.get('name')
    currency = 'USD'

    khqr = KHQR(token)
    qr = khqr.create_qr(
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
    md5 = khqr.generate_md5(qr)
    # generate qr code image

    # Create QR code instance
    qr_object = qrcode.QRCode(
        version=1,  # controls size (1 = smallest)
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,  # pixel size of each box
        border=4,  # thickness of the border
    )
    qr_object.add_data(qr)
    qr_object.make(fit=True)
    img = qr_object.make_image(fill_color="black", back_color="white")
    img.save("./static/qrcode.png")

    # Redirect to show QR page
    return render_template('payment.html', amount=price, currency=currency, md5=md5, merchant_name="PHALLA HEANG")

# @app.post('/check-payment')
# def check_payment():
#     json_data = request.get_json()
#     md5 = json_data.get('md5')
#     res = requests.post(
#         'https://api-bakong.nbc.gov.kh/v1/check_transaction_by_md5',
#         json={
#             'md5': md5
#         },
#         headers={
#             'authorization': f'Bearer {token}',
#             'Content-Type': 'application/json'
#         }
#     )
#
#     return res.json()
#
# @app.get('/customer_thanks')
# def customer_thanks():
#     return render_template('customer_thanks.html')
# if __name__ == '__main__':
#     app.run(debug=True)
