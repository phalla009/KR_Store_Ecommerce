=========
KR_Store_Ecommerce 
=========

1. DESCRIPTION
--------------
A Python-based e-commerce platform featuring integrated 
KHQR payment functionality.

Live Demo: https://krecomstore.phalla.lol/


2. PROJECT STRUCTURE
--------------------
- static/           : CSS, JavaScript, and Image assets.
- templates/        : HTML templates (Flask/Jinja2).
- app.py            : Main application entry point.
- checkout.py       : Checkout and order processing logic.
- config.py         : Configuration settings and API keys.
- qr.py             : KHQR generation and payment logic.
- requirements.txt  : Python dependencies list.


3. KEY FEATURES
---------------
* Product Catalog: Dynamic rendering via Flask.
* KHQR Integration: Secure QR code generation for payments.
* Checkout System: Streamlined user flow for purchases.
* Vercel Ready: Optimized for cloud deployment.


4. INSTALLATION & SETUP
-----------------------
Step 1: Clone the repository
   git clone https://github.com/phalla009/KR_Store_Ecommerce.git
   cd KR_Store_Ecommerce

Step 2: Install dependencies
   pip install -r requirements.txt

Step 3: Run the application
   python app.py

The application will start locally at: http://127.0.0.1:5000


5. CONFIGURATION
----------------
Ensure you edit 'config.py' before deployment to set your:
- Merchant IDs
- API Secret Keys
- Flask Security Keys


6. CONTACT & REPOSITORY
-----------------------
Author: phalla009
GitHub: https://github.com/phalla009/KR_Store_Ecommerce

============================================================
