import requests
from flask_mail import Message
import config

def to_number(val):
    try:
        return int(val)
    except:
        try:
            return float(val)
        except:
            return 0

def process_checkout(app, mail, data):
    total_usd = sum(to_number(item["qty"]) * to_number(item["price"]) for item in data["cart"])
    total_khr = total_usd * config.USD_TO_KHR

    product_lines = "\n\n".join(
        f"🛒 {i+1}. {item['title']} x{item['qty']} = ${to_number(item['qty']) * to_number(item['price']):.2f}\n🖼️ {item['image']}"
        for i, item in enumerate(data["cart"])
    )

    message = f"""
=====📦 New Order =====

👤 Name: {data['first_name']} {data['last_name']}
🏠 Address: {data['address']}, {data['city']}, {data['country']} {data['zip']}
📧 Email: {data.get('email', 'N/A')}
📱 Phone: {data['phone']}

---- 📦 Order Summary ----
{product_lines}
====================
Total:
💵 USD: ${total_usd:.2f}
🇰🇭 KHR: ៛{total_khr:,.2f}
"""

    # --- Send Telegram ---
    try:
        url = f"https://api.telegram.org/bot{config.BOT_TOKEN}/sendMessage"
        payload = {"chat_id": config.CHAT_ID, "text": message}
        telegram_response = requests.post(url, json=payload)
        telegram_response.raise_for_status()
    except Exception as e:
        return {"status": "error", "message": f"Telegram error: {e}"}

    # --- Send Email ---
    if data.get("email"):
        try:
            msg = Message(
                subject="Your Order Confirmation",
                sender=app.config['MAIL_DEFAULT_SENDER'],
                recipients=[data['email']],
                body=message
            )
            mail.send(msg)
        except Exception as e:
            return {"status": "error", "message": f"Email error: {e}"}

    return {"status": "success"}
