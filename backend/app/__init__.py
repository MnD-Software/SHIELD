import os
import base64
import json
import re
import secrets
import urllib.error
import urllib.request
from datetime import datetime, timedelta
from decimal import Decimal
from pathlib import Path

from flask import Flask, abort, flash, jsonify, redirect, render_template, request, session, url_for
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(30))
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="customer")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False, index=True)
    icon = db.Column(db.String(12), default="✦")
    description = db.Column(db.String(240), nullable=False)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(180), nullable=False, index=True)
    slug = db.Column(db.String(180), unique=True, nullable=False, index=True)
    brand = db.Column(db.String(100), nullable=False, index=True)
    sku = db.Column(db.String(60), unique=True, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    category = db.relationship("Category", backref="products")
    price = db.Column(db.Numeric(10, 2), nullable=False)
    sale_price = db.Column(db.Numeric(10, 2))
    stock = db.Column(db.Integer, nullable=False, default=0)
    description = db.Column(db.Text, nullable=False)
    benefits = db.Column(db.Text, nullable=False)
    usage = db.Column(db.Text, nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    warnings = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(500), nullable=False)
    featured = db.Column(db.Boolean, default=False, nullable=False)
    popularity = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    @property
    def effective_price(self):
        return self.sale_price if self.sale_price is not None else self.price


class Coupon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(32), unique=True, nullable=False)
    percent_off = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.String(30), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    customer = db.relationship("User", backref="orders")
    customer_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    town = db.Column(db.String(100), nullable=False)
    county = db.Column(db.String(100), nullable=False)
    payment_method = db.Column(db.String(30), nullable=False)
    status = db.Column(db.String(30), default="Pending", nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
    delivery_fee = db.Column(db.Numeric(10, 2), nullable=False)
    discount = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), nullable=False)
    order = db.relationship("Order", backref=db.backref("items", cascade="all, delete-orphan"))
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    name = db.Column(db.String(180), nullable=False)
    sku = db.Column(db.String(60), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)


class WishlistItem(db.Model):
    __table_args__ = (db.UniqueConstraint("user_id", "product_id"),)
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    product = db.relationship("Product")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    body = db.Column(db.String(500), nullable=False)
    verified = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(30), default="New", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class CRMLead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    company = db.Column(db.String(160))
    email = db.Column(db.String(255), nullable=False, index=True)
    phone = db.Column(db.String(30))
    source = db.Column(db.String(60), nullable=False, default="Website")
    stage = db.Column(db.String(30), nullable=False, default="New")
    owner = db.Column(db.String(100), nullable=False, default="Pharmacy team")
    opportunity_value = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    next_follow_up = db.Column(db.Date)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class CRMActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lead_id = db.Column(db.Integer, db.ForeignKey("crm_lead.id"), nullable=False, index=True)
    lead = db.relationship("CRMLead", backref=db.backref("activities", cascade="all, delete-orphan"))
    activity_type = db.Column(db.String(40), nullable=False, default="Note")
    details = db.Column(db.String(500), nullable=False)
    created_by = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class CRMTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lead_id = db.Column(db.Integer, db.ForeignKey("crm_lead.id"), nullable=False, index=True)
    lead = db.relationship("CRMLead", backref=db.backref("tasks", cascade="all, delete-orphan"))
    title = db.Column(db.String(180), nullable=False)
    assigned_to = db.Column(db.String(100), nullable=False)
    priority = db.Column(db.String(20), nullable=False, default="Normal")
    due_at = db.Column(db.DateTime)
    status = db.Column(db.String(20), nullable=False, default="Open")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    completed_at = db.Column(db.DateTime)


class AuditEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    actor_id = db.Column(db.Integer, db.ForeignKey("user.id"), index=True)
    actor = db.relationship("User")
    action = db.Column(db.String(80), nullable=False, index=True)
    entity_type = db.Column(db.String(60), nullable=False, index=True)
    entity_id = db.Column(db.String(80), index=True)
    summary = db.Column(db.String(500), nullable=False)
    metadata_json = db.Column(db.Text, nullable=False, default="{}")
    ip_address = db.Column(db.String(64))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)


class PaymentAttempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), nullable=False)
    order = db.relationship("Order", backref="payment_attempts")
    provider = db.Column(db.String(30), nullable=False, default="mpesa")
    merchant_request_id = db.Column(db.String(100))
    checkout_request_id = db.Column(db.String(100), index=True)
    status = db.Column(db.String(30), nullable=False, default="Pending")
    response_message = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


def slugify(value):
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def require_admin():
    if not current_user.is_authenticated or current_user.role != "admin":
        abort(403)


ROLE_PERMISSIONS = {
    "admin": {"*"},
    "manager": {"dashboard.read", "orders.manage", "catalogue.manage", "crm.manage", "reports.read"},
    "pharmacist": {"dashboard.read", "orders.read", "prescriptions.manage", "crm.manage"},
    "marketer": {"dashboard.read", "crm.manage", "marketing.manage"},
    "fulfilment": {"dashboard.read", "orders.manage", "stock.manage"},
}


def require_permission(permission):
    permissions=ROLE_PERMISSIONS.get(getattr(current_user,"role",None),set())
    if "*" not in permissions and permission not in permissions:
        abort(403)


def record_audit(action, entity_type, entity_id, summary, metadata=None):
    db.session.add(AuditEvent(
        actor_id=current_user.id if current_user.is_authenticated else None,
        action=action,entity_type=entity_type,entity_id=str(entity_id) if entity_id is not None else None,
        summary=summary,metadata_json=json.dumps(metadata or {},default=str),
        ip_address=request.headers.get("X-Forwarded-For",request.remote_addr),
    ))


def initiate_mpesa_stk(order):
    required = ["MPESA_CONSUMER_KEY", "MPESA_CONSUMER_SECRET", "MPESA_SHORTCODE", "MPESA_PASSKEY", "MPESA_CALLBACK_URL"]
    if os.getenv("MPESA_ENABLED", "false").lower() != "true" or not all(os.getenv(key) for key in required):
        return {"configured": False, "message": "M-Pesa is awaiting merchant credentials; the order has been saved for follow-up."}
    env = os.getenv("MPESA_ENVIRONMENT", "sandbox").lower()
    host = "https://api.safaricom.co.ke" if env == "production" else "https://sandbox.safaricom.co.ke"
    credentials = base64.b64encode(f"{os.environ['MPESA_CONSUMER_KEY']}:{os.environ['MPESA_CONSUMER_SECRET']}".encode()).decode()
    token_request = urllib.request.Request(f"{host}/oauth/v1/generate?grant_type=client_credentials", headers={"Authorization": f"Basic {credentials}"})
    try:
        with urllib.request.urlopen(token_request, timeout=12) as response:
            token = json.loads(response.read())["access_token"]
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        shortcode = os.environ["MPESA_SHORTCODE"]
        password = base64.b64encode(f"{shortcode}{os.environ['MPESA_PASSKEY']}{timestamp}".encode()).decode()
        phone = re.sub(r"\D", "", order.phone)
        phone = f"254{phone[-9:]}" if len(phone) >= 9 else phone
        payload = {"BusinessShortCode": shortcode, "Password": password, "Timestamp": timestamp, "TransactionType": "CustomerPayBillOnline", "Amount": int(order.total), "PartyA": phone, "PartyB": shortcode, "PhoneNumber": phone, "CallBackURL": os.environ["MPESA_CALLBACK_URL"], "AccountReference": order.reference, "TransactionDesc": "Shield Pharmacy order"}
        stk_request = urllib.request.Request(f"{host}/mpesa/stkpush/v1/processrequest", data=json.dumps(payload).encode(), headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
        with urllib.request.urlopen(stk_request, timeout=15) as response:
            data = json.loads(response.read())
        return {"configured": True, "ok": data.get("ResponseCode") == "0", "data": data, "message": data.get("CustomerMessage", "M-Pesa request submitted.")}
    except (urllib.error.URLError, KeyError, ValueError) as exc:
        return {"configured": True, "ok": False, "message": f"M-Pesa request could not be completed: {exc}"}


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


def cart_details():
    raw = session.get("cart", {})
    products = Product.query.filter(Product.id.in_([int(k) for k in raw] or [0])).all()
    items, subtotal = [], Decimal("0")
    for product in products:
        qty = max(1, min(int(raw.get(str(product.id), 1)), product.stock))
        line = product.effective_price * qty
        subtotal += line
        items.append({"product": product, "quantity": qty, "line_total": line})
    discount = Decimal(str(session.get("discount", 0)))
    delivery = Decimal("0") if subtotal >= 3000 or subtotal == 0 else Decimal("250")
    return items, subtotal, delivery, min(discount, subtotal)


def seed_database():
    if Category.query.first():
        return
    definitions = [
        ("Over-the-counter", "over-the-counter", "✚", "Trusted everyday relief"),
        ("Vitamins & Supplements", "vitamins-supplements", "☀", "Daily nutrition and wellbeing"),
        ("Baby Care", "baby-care", "♡", "Gentle care for little ones"),
        ("Personal Care", "personal-care", "✦", "Dermatologist-inspired care"),
        ("Medical Equipment", "medical-equipment", "⌁", "Reliable home health monitoring"),
        ("First Aid", "first-aid", "+", "Essentials for life's small emergencies"),
    ]
    categories = {}
    for name, slug, icon, description in definitions:
        row = Category(name=name, slug=slug, icon=icon, description=description)
        db.session.add(row); categories[slug] = row
    db.session.flush()
    rows = [
        ("Panadol Advance 500mg", "panadol-advance-500mg", "GSK", "SH-OTC-001", "over-the-counter", 240, 210, 38, "Fast, effective relief from headache and everyday pain.", "Relieves headache, muscle ache, toothache and fever.", "Adults: 1–2 tablets every 4–6 hours. Do not exceed 8 tablets in 24 hours.", "Paracetamol 500mg.", "Do not combine with other paracetamol products. Consult a clinician if symptoms persist.", "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?auto=format&fit=crop&w=900&q=85", True, 98),
        ("Centrum Women Multivitamin", "centrum-women-multivitamin", "Centrum", "SH-VIT-002", "vitamins-supplements", 2450, 2190, 22, "Complete daily multivitamin formulated to support women's health.", "Supports energy, immunity, healthy skin and normal metabolism.", "Take one tablet daily with food.", "Vitamins A–K, calcium, iron, zinc and essential minerals.", "Food supplements do not replace a varied diet. Keep away from children.", "https://images.unsplash.com/photo-1550572017-edd951b55104?auto=format&fit=crop&w=900&q=85", True, 88),
        ("CeraVe Moisturising Cream", "cerave-moisturising-cream", "CeraVe", "SH-PC-003", "personal-care", 2800, None, 15, "Rich, non-greasy moisturiser for dry to very dry skin.", "Helps restore the protective skin barrier with three essential ceramides.", "Apply generously to face or body as often as needed.", "Ceramides, hyaluronic acid and glycerin.", "For external use only. Avoid direct contact with eyes.", "https://images.unsplash.com/photo-1556228578-8c89e6adf883?auto=format&fit=crop&w=900&q=85", True, 92),
        ("Omron M2 Blood Pressure Monitor", "omron-m2-blood-pressure-monitor", "Omron", "SH-MED-004", "medical-equipment", 6750, 6290, 8, "Clinically validated automatic upper-arm blood pressure monitor.", "Simple one-touch measurement with irregular heartbeat detection.", "Rest for five minutes, position cuff at heart level and follow the included guide.", "Monitor, medium cuff, batteries and instruction manual.", "Not a substitute for medical diagnosis. Discuss unusual readings with a clinician.", "https://images.unsplash.com/photo-1615486511484-92e172cc4fe0?auto=format&fit=crop&w=900&q=85", True, 85),
        ("Sudocrem Antiseptic Healing Cream", "sudocrem-antiseptic-cream", "Sudocrem", "SH-BABY-005", "baby-care", 1350, None, 30, "Versatile protective cream for nappy rash and minor skin irritation.", "Soothes sore skin and forms a water-repellent protective barrier.", "Apply a thin, translucent layer to clean, dry skin.", "Zinc oxide, benzyl alcohol and hypoallergenic lanolin.", "External use only. Avoid eyes and mucous membranes.", "https://images.unsplash.com/photo-1601612628452-9e99ced43524?auto=format&fit=crop&w=900&q=85", False, 78),
        ("Shield Essential First Aid Kit", "shield-essential-first-aid-kit", "Shield", "SH-FA-006", "first-aid", 1950, 1750, 18, "A practical 42-piece kit for home, car or office.", "Organised essentials for cuts, grazes, minor burns and sprains.", "Follow the instructions supplied with each item and replenish after use.", "Dressings, plasters, antiseptic wipes, gloves, tape, scissors and bandage.", "Seek urgent help for severe bleeding, burns, allergic reactions or breathing difficulty.", "https://images.unsplash.com/photo-1603398938378-e54eab446dde?auto=format&fit=crop&w=900&q=85", True, 90),
        ("Seven Seas Cod Liver Oil", "seven-seas-cod-liver-oil", "Seven Seas", "SH-VIT-007", "vitamins-supplements", 1680, 1490, 27, "Omega-3 and vitamin-rich daily capsules.", "Supports heart, brain, vision and immune health.", "Adults take one capsule daily with a cold drink.", "Cod liver oil, omega-3, vitamins A and D.", "Consult your clinician if pregnant, breastfeeding or using anticoagulants.", "https://images.unsplash.com/photo-1577174881658-0f30ed549adc?auto=format&fit=crop&w=900&q=85", False, 76),
        ("Dettol Antiseptic Liquid 500ml", "dettol-antiseptic-liquid-500ml", "Dettol", "SH-FA-008", "first-aid", 690, 625, 46, "Concentrated antiseptic disinfectant for first aid and hygiene.", "Helps protect minor wounds from infection when correctly diluted.", "Always dilute exactly as directed on the product label.", "Chloroxylenol 4.8% w/v.", "Never swallow. Do not use undiluted on skin. Keep out of children's reach.", "https://images.unsplash.com/photo-1583947581924-860bda6a26df?auto=format&fit=crop&w=900&q=85", False, 82),
    ]
    for values in rows:
        name, slug, brand, sku, cat, price, sale, stock, desc, benefits, usage, ingredients, warnings, image, featured, popularity = values
        db.session.add(Product(name=name, slug=slug, brand=brand, sku=sku, category=categories[cat], price=price, sale_price=sale, stock=stock, description=desc, benefits=benefits, usage=usage, ingredients=ingredients, warnings=warnings, image=image, featured=featured, popularity=popularity))
    db.session.add(Coupon(code="WELCOME10", percent_off=10))
    db.session.add(User(name="Shield Administrator", email="admin@shield.test", password_hash=generate_password_hash("ShieldAdmin123!"), role="admin"))
    db.session.commit()
    reviews = [
        (1, "Wanjiku M.", 5, "Fast delivery and the sealed pack arrived in perfect condition."),
        (1, "David O.", 5, "Straightforward ordering and clear usage information."),
        (3, "Njeri K.", 5, "Genuine product and excellent for my dry skin."),
        (4, "Peter A.", 4, "Simple to use and thoughtfully packed."),
    ]
    for product_id, customer_name, rating, body in reviews:
        db.session.add(Review(product_id=product_id, customer_name=customer_name, rating=rating, body=body))
    db.session.commit()


def sync_jamieson_catalog():
    """Keep the supplied Jamieson price list available in existing and new databases."""
    category = Category.query.filter_by(slug="vitamins-supplements").first()
    if category is None:
        return
    image = "https://images.unsplash.com/photo-1550572017-edd951b55104?auto=format&fit=crop&w=900&q=85"
    rows = [
        ("5-HTP 100mg Caplets 90's", "5-htp-100mg-caplets-90", 3330, 3000),
        ("Apple Cider Vinegar + Chromium Caplets 120's", "apple-cider-vinegar-chromium-caplets-120", 2995, 2700),
        ("Ashwagandha Capsules 60's", "ashwagandha-capsules-60", 3030, 2730),
        ("B6 + B12 and Folic Acid Tablets 110's", "b6-b12-folic-acid-tablets-110", 1450, 1300),
        ("Calcium Magnesium + D3 Caplets 200's", "calcium-magnesium-d3-caplets-200", 2150, 1930),
        ("Calcium Magnesium + Zinc Caplets 200's", "calcium-magnesium-zinc-caplets-200", 2150, 1930),
        ("Collagen Anti-Wrinkle Capsules 60's", "collagen-anti-wrinkle-capsules-60", 4410, 4000),
        ("Vitamin D3 1000 IU Tablets 100's", "vitamin-d3-1000-iu-tablets-100", 2590, 2330),
        ("Vitamin D3 2500 IU Chewable Tablets 75's", "vitamin-d3-2500-iu-chewable-75", 2020, 1820),
        ("Evening Primrose Oil 1000mg Softgels 85's", "evening-primrose-oil-1000mg-85", 3200, 2900),
        ("Gentle Iron 28mg Capsules 90's", "gentle-iron-28mg-capsules-90", 3130, 2820),
        ("Lutein 20mg Softgels 45's", "lutein-20mg-softgels-45", 1490, 1250),
        ("Maca 1000mg Capsules 45's", "maca-1000mg-capsules-45", 1850, 1665),
        ("Magnesium 250mg Caplets 90's", "magnesium-250mg-caplets-90", 2995, 2700),
        ("Melatonin 10mg Caplets 60's", "melatonin-10mg-caplets-60", 3390, 3050),
        ("Melatonin 3mg Capsules 30's", "melatonin-3mg-capsules-30", 1890, 1700),
        ("Saw Palmetto 1000mg Softgels 60's", "saw-palmetto-1000mg-softgels-60", 4110, 3700),
        ("Selenium Extra Strength 100mcg Tablets 100's", "selenium-100mcg-tablets-100", 2060, 1850),
        ("Zinc 50mg Tablets 100's", "zinc-50mg-tablets-100", 2330, 2100),
    ]
    for index, (name, slug, price, sale_price) in enumerate(rows, start=1):
        product = Product.query.filter_by(slug=f"jamieson-{slug}").first()
        if product is None:
            product = Product(
                slug=f"jamieson-{slug}",
                sku=f"SH-JAM-{index:03d}",
                stock=24,
                featured=index <= 4,
                popularity=84 - index,
            )
            db.session.add(product)
        product.name = f"Jamieson {name}"
        product.brand = "Jamieson"
        product.category = category
        product.price = Decimal(str(price))
        product.sale_price = Decimal(str(sale_price))
        product.description = f"Jamieson {name}, supplied through approved pharmacy channels."
        product.benefits = "A convenient addition to a balanced daily wellness routine."
        product.usage = "Use only as directed on the product label or by your healthcare professional."
        product.ingredients = "See the product label for the complete active and inactive ingredient list."
        product.warnings = "Food supplements do not replace a varied diet. Consult a healthcare professional if pregnant, breastfeeding, taking medication or managing a health condition."
        product.image = image
    db.session.commit()


def create_app(test_config=None):
    root = Path(__file__).resolve().parents[2]
    app = Flask(__name__, template_folder=str(root / "templates"), static_folder=str(root / "static"))
    app.config.update(SECRET_KEY=os.getenv("SECRET_KEY", "development-key-change-before-deploy"), SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL", f"sqlite:///{root / 'shield.db'}"), SQLALCHEMY_TRACK_MODIFICATIONS=False, SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE="Lax", SESSION_COOKIE_SECURE=os.getenv("SESSION_COOKIE_SECURE","false").lower()=="true", MAX_CONTENT_LENGTH=8 * 1024 * 1024)
    if test_config: app.config.update(test_config)
    db.init_app(app); login_manager.init_app(app); csrf.init_app(app)
    login_manager.login_view = "login"; login_manager.login_message_category = "info"

    @app.after_request
    def security_headers(response):
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "SAMEORIGIN")
        response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
        response.headers.setdefault("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
        response.headers.setdefault("Content-Security-Policy", "default-src 'self'; img-src 'self' data: https://images.unsplash.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; script-src 'self' 'unsafe-inline'; frame-src https://www.google.com; connect-src 'self'")
        return response

    @app.context_processor
    def inject_globals():
        wishlist_ids = set()
        if current_user.is_authenticated:
            wishlist_ids = {row.product_id for row in WishlistItem.query.filter_by(user_id=current_user.id).all()}
        return {"cart_count": sum(session.get("cart", {}).values()), "year": datetime.utcnow().year, "categories_nav": Category.query.order_by(Category.name).all(), "wishlist_ids": wishlist_ids}

    @app.get("/")
    def home(): return render_template("home.html", featured=Product.query.filter_by(featured=True).limit(4).all(), categories=Category.query.all(), popular=Product.query.order_by(Product.popularity.desc()).limit(4).all())

    @app.get("/products")
    def products():
        query = Product.query; q=request.args.get("q","").strip(); category=request.args.get("category",""); brand=request.args.get("brand",""); availability=request.args.get("availability",""); sort=request.args.get("sort","popular"); price=request.args.get("price","")
        if q: query=query.filter(or_(Product.name.ilike(f"%{q}%"),Product.brand.ilike(f"%{q}%"),Product.description.ilike(f"%{q}%")))
        if category: query=query.join(Category).filter(Category.slug==category)
        if brand: query=query.filter(Product.brand==brand)
        if availability=="in-stock": query=query.filter(Product.stock>0)
        if price=="under-1000": query=query.filter(Product.price<1000)
        elif price=="1000-3000": query=query.filter(Product.price>=1000,Product.price<=3000)
        elif price=="over-3000": query=query.filter(Product.price>3000)
        query=query.order_by({"newest":Product.created_at.desc(),"price-low":Product.price.asc(),"price-high":Product.price.desc()}.get(sort,Product.popularity.desc()))
        return render_template("products.html",products=query.all(),categories=Category.query.all(),brands=[r[0] for r in db.session.query(Product.brand).distinct().order_by(Product.brand)],selected={"q":q,"category":category,"brand":brand,"availability":availability,"sort":sort,"price":price},title="Shop all products")

    @app.get("/products/<slug>")
    def product_detail(slug):
        product=Product.query.filter_by(slug=slug).first_or_404(); related=Product.query.filter(Product.category_id==product.category_id,Product.id!=product.id).limit(4).all()
        recent=session.get("recent",[]); recent=[product.id]+[item for item in recent if item!=product.id]; session["recent"]=recent[:6]
        recently_viewed=Product.query.filter(Product.id.in_(recent[1:])).limit(4).all() if len(recent)>1 else []
        reviews=Review.query.filter_by(product_id=product.id).order_by(Review.created_at.desc()).all()
        return render_template("product.html",product=product,related=related,recently_viewed=recently_viewed,reviews=reviews)

    @app.post("/wishlist/toggle/<int:product_id>")
    @login_required
    def toggle_wishlist(product_id):
        db.get_or_404(Product,product_id)
        item=WishlistItem.query.filter_by(user_id=current_user.id,product_id=product_id).first()
        if item: db.session.delete(item); message="Removed from saved items."
        else: db.session.add(WishlistItem(user_id=current_user.id,product_id=product_id)); message="Saved to your wishlist."
        db.session.commit(); flash(message,"success"); return redirect(request.referrer or url_for("products"))

    @app.post("/cart/add/<int:product_id>")
    def add_cart(product_id):
        product=db.get_or_404(Product,product_id); cart=session.get("cart",{}); key=str(product.id); cart[key]=min(product.stock,int(cart.get(key,0))+max(1,int(request.form.get("quantity",1)))); session["cart"]=cart
        flash(f"{product.name} added to your basket.","success"); return redirect(request.referrer or url_for("cart"))

    @app.route("/cart",methods=["GET","POST"])
    def cart():
        if request.method=="POST":
            data=session.get("cart",{})
            for key in list(data):
                qty=int(request.form.get(f"qty_{key}",data[key])); data.pop(key,None) if qty<=0 else data.update({key:qty})
            session["cart"]=data; flash("Basket updated.","success")
        items,subtotal,delivery,discount=cart_details(); return render_template("cart.html",items=items,subtotal=subtotal,delivery=delivery,discount=discount,total=subtotal+delivery-discount)

    @app.post("/cart/remove/<int:product_id>")
    def remove_cart(product_id):
        data=session.get("cart",{}); data.pop(str(product_id),None); session["cart"]=data; flash("Item removed.","info"); return redirect(url_for("cart"))

    @app.post("/cart/coupon")
    def apply_coupon():
        row=Coupon.query.filter(db.func.upper(Coupon.code)==request.form.get("code","").strip().upper(),Coupon.active.is_(True)).first()
        if row:
            _,subtotal,_,_=cart_details(); session["discount"]=float(subtotal*Decimal(row.percent_off)/100); flash(f"{row.percent_off}% discount applied.","success")
        else: flash("That coupon is not valid.","error")
        return redirect(url_for("cart"))

    @app.route("/checkout",methods=["GET","POST"])
    def checkout():
        items,subtotal,delivery,discount=cart_details()
        if not items: flash("Your basket is empty.","info"); return redirect(url_for("products"))
        if request.method=="POST":
            fields=["name","email","phone","address","town","county","payment_method"]
            if any(not request.form.get(x,"").strip() for x in fields) or request.form.get("terms")!="on": flash("Complete all fields and accept the terms.","error")
            else:
                order=Order(reference=f"SHP-{datetime.utcnow():%y%m%d}-{Order.query.count()+1:05d}",user_id=current_user.id if current_user.is_authenticated else None,customer_name=request.form["name"],email=request.form["email"],phone=request.form["phone"],address=request.form["address"],town=request.form["town"],county=request.form["county"],payment_method=request.form["payment_method"],subtotal=subtotal,delivery_fee=delivery,discount=discount,total=subtotal+delivery-discount)
                db.session.add(order)
                for item in items:
                    product=item["product"]; product.stock-=item["quantity"]; db.session.add(OrderItem(order=order,product_id=product.id,name=product.name,sku=product.sku,quantity=item["quantity"],unit_price=product.effective_price))
                db.session.commit()
                payment_notice = None
                if order.payment_method == "mpesa":
                    result = initiate_mpesa_stk(order); data = result.get("data", {})
                    attempt = PaymentAttempt(order=order, merchant_request_id=data.get("MerchantRequestID"), checkout_request_id=data.get("CheckoutRequestID"), status="Prompt sent" if result.get("ok") else "Pending", response_message=result["message"])
                    db.session.add(attempt); db.session.commit(); payment_notice = result["message"]
                session.pop("cart",None); session.pop("discount",None); return render_template("order_success.html",order=order,payment_notice=payment_notice)
        return render_template("checkout.html",items=items,subtotal=subtotal,delivery=delivery,discount=discount,total=subtotal+delivery-discount)

    @app.route("/login",methods=["GET","POST"])
    def login():
        if request.method=="POST":
            user=User.query.filter(db.func.lower(User.email)==request.form.get("email","").strip().lower()).first()
            if user and check_password_hash(user.password_hash,request.form.get("password","")): login_user(user,remember=request.form.get("remember")=="on"); return redirect(url_for("admin" if user.role=="admin" else "account"))
            flash("Email or password is incorrect.","error")
        return render_template("auth.html",mode="login")

    @app.route("/register",methods=["GET","POST"])
    def register():
        if request.method=="POST":
            email=request.form.get("email","").strip().lower(); password=request.form.get("password","")
            if User.query.filter_by(email=email).first(): flash("An account already uses that email.","error")
            elif len(password)<10: flash("Use at least 10 characters for your password.","error")
            else:
                user=User(name=request.form.get("name","").strip(),email=email,phone=request.form.get("phone","").strip(),password_hash=generate_password_hash(password)); db.session.add(user); db.session.commit(); login_user(user); return redirect(url_for("account"))
        return render_template("auth.html",mode="register")

    @app.route("/forgot-password",methods=["GET","POST"])
    def forgot_password():
        if request.method=="POST": flash("If that email is registered, a secure reset link will be sent.","success")
        return render_template("auth.html",mode="forgot")

    @app.get("/logout")
    @login_required
    def logout(): logout_user(); return redirect(url_for("home"))

    @app.route("/account", methods=["GET", "POST"])
    @login_required
    def account():
        if request.method == "POST":
            name=request.form.get("name","").strip(); phone=request.form.get("phone","").strip()
            if not name: flash("Your name is required.","error")
            else: current_user.name=name; current_user.phone=phone; db.session.commit(); flash("Profile updated.","success")
        return render_template("account.html",orders=Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all(),saved=WishlistItem.query.filter_by(user_id=current_user.id).order_by(WishlistItem.created_at.desc()).all())

    @app.get("/admin", defaults={"section":"overview"})
    @app.get("/admin/<section>")
    @login_required
    def admin(section):
        require_admin()
        allowed_sections={"overview","orders","catalogue","stock","purchasing","prescriptions","customers","crm","marketing","payments","settings","audit"}
        if section not in allowed_sections: abort(404)
        products=Product.query.order_by(Product.stock).all()
        orders=Order.query.order_by(Order.created_at.desc()).all()
        users=User.query.order_by(User.created_at.desc()).all()
        messages=ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
        leads=CRMLead.query.order_by(CRMLead.updated_at.desc()).all()
        crm_activities=CRMActivity.query.order_by(CRMActivity.created_at.desc()).limit(12).all()
        crm_tasks=CRMTask.query.order_by(CRMTask.status,CRMTask.due_at).all()
        audit_events=AuditEvent.query.order_by(AuditEvent.created_at.desc()).limit(100).all()
        revenue=db.session.query(db.func.coalesce(db.func.sum(Order.total),0)).scalar()
        sales_days=[]
        for offset in range(6,-1,-1):
            day=(datetime.utcnow()-timedelta(days=offset)).date()
            total=sum((order.total for order in orders if order.created_at.date()==day),Decimal("0"))
            sales_days.append({"label":day.strftime("%a"),"total":float(total)})
        max_daily=max([day["total"] for day in sales_days] or [1]) or 1
        status_counts={status:sum(1 for order in orders if order.status==status) for status in ["Pending","Processing","Ready","Dispatched","Completed","Cancelled"]}
        top_products=db.session.query(
            OrderItem.name,
            db.func.sum(OrderItem.quantity).label("quantity"),
            db.func.sum(OrderItem.unit_price*OrderItem.quantity).label("sales"),
        ).group_by(OrderItem.name).order_by(db.desc("quantity")).limit(6).all()
        return render_template(
            "admin.html",products=products,orders=orders,users=users,
            categories=Category.query.order_by(Category.name).all(),messages=messages,
            leads=leads,crm_activities=crm_activities,crm_tasks=crm_tasks,audit_events=audit_events,
            coupons=Coupon.query.order_by(Coupon.code).all(),
            payments=PaymentAttempt.query.order_by(PaymentAttempt.created_at.desc()).limit(10).all(),
            revenue=revenue,sales_days=sales_days,max_daily=max_daily,
            status_counts=status_counts,top_products=top_products,admin_section=section,
        )

    @app.post("/admin/crm/leads")
    @login_required
    def admin_crm_lead_create():
        require_admin()
        name=request.form.get("name","").strip()
        email=request.form.get("email","").strip().lower()
        if not name or not email:
            flash("Lead name and email are required.","error")
            return redirect(url_for("admin",section="crm"))
        follow_up=None
        if request.form.get("next_follow_up"):
            try: follow_up=datetime.strptime(request.form["next_follow_up"],"%Y-%m-%d").date()
            except ValueError: pass
        lead=CRMLead(
            name=name,email=email,company=request.form.get("company","").strip(),
            phone=request.form.get("phone","").strip(),source=request.form.get("source","Website"),
            owner=request.form.get("owner","").strip() or current_user.name,
            opportunity_value=Decimal(request.form.get("opportunity_value") or "0"),
            next_follow_up=follow_up,notes=request.form.get("notes","").strip(),
        )
        db.session.add(lead); db.session.flush()
        db.session.add(CRMActivity(lead=lead,activity_type="Lead created",details=f"Added from {lead.source}.",created_by=current_user.name))
        record_audit("crm.lead.created","CRMLead",lead.id,f"Created lead {lead.name}",{"source":lead.source,"owner":lead.owner})
        db.session.commit(); flash(f"{lead.name} added to the CRM pipeline.","success")
        return redirect(url_for("admin",section="crm"))

    @app.post("/admin/crm/leads/<int:lead_id>/stage")
    @login_required
    def admin_crm_lead_stage(lead_id):
        require_admin(); lead=db.get_or_404(CRMLead,lead_id)
        stage=request.form.get("stage","New")
        if stage not in {"New","Qualified","Opportunity","Converted","Lost"}: abort(400)
        old_stage=lead.stage; lead.stage=stage
        db.session.add(CRMActivity(lead=lead,activity_type="Stage changed",details=f"{old_stage} → {stage}",created_by=current_user.name))
        record_audit("crm.stage.changed","CRMLead",lead.id,f"Moved {lead.name} from {old_stage} to {stage}")
        db.session.commit(); flash("Pipeline stage updated.","success")
        return redirect(url_for("admin",section="crm"))

    @app.post("/admin/crm/leads/<int:lead_id>/activities")
    @login_required
    def admin_crm_activity_create(lead_id):
        require_admin(); lead=db.get_or_404(CRMLead,lead_id)
        details=request.form.get("details","").strip()
        if details:
            db.session.add(CRMActivity(lead=lead,activity_type=request.form.get("activity_type","Note"),details=details,created_by=current_user.name))
            record_audit("crm.activity.logged","CRMLead",lead.id,f"Logged activity for {lead.name}",{"type":request.form.get("activity_type","Note")})
            db.session.commit(); flash("CRM activity recorded.","success")
        return redirect(url_for("admin",section="crm"))

    @app.post("/admin/crm/tasks")
    @login_required
    def admin_crm_task_create():
        require_permission("crm.manage"); lead=db.get_or_404(CRMLead,request.form.get("lead_id",type=int))
        title=request.form.get("title","").strip()
        if not title: abort(400)
        due_at=None
        if request.form.get("due_at"):
            try: due_at=datetime.strptime(request.form["due_at"],"%Y-%m-%d")
            except ValueError: pass
        task=CRMTask(lead=lead,title=title,assigned_to=request.form.get("assigned_to","").strip() or current_user.name,priority=request.form.get("priority","Normal"),due_at=due_at)
        db.session.add(task); db.session.flush()
        record_audit("crm.task.created","CRMTask",task.id,f"Created task for {lead.name}",{"priority":task.priority})
        db.session.commit(); flash("Follow-up task created.","success")
        return redirect(url_for("admin",section="crm"))

    @app.post("/admin/crm/tasks/<int:task_id>/complete")
    @login_required
    def admin_crm_task_complete(task_id):
        require_permission("crm.manage"); task=db.get_or_404(CRMTask,task_id)
        task.status="Completed"; task.completed_at=datetime.utcnow()
        record_audit("crm.task.completed","CRMTask",task.id,f"Completed task: {task.title}")
        db.session.commit(); flash("Task completed.","success")
        return redirect(url_for("admin",section="crm"))

    @app.post("/admin/products/save")
    @login_required
    def admin_product_save():
        require_admin(); product_id=request.form.get("product_id",type=int); product=db.session.get(Product,product_id) if product_id else Product()
        category=db.get_or_404(Category,request.form.get("category_id",type=int)); name=request.form.get("name","").strip(); sku=request.form.get("sku","").strip()
        if not name or not sku: flash("Product name and SKU are required.","error"); return redirect(url_for("admin",section="catalogue"))
        requested_slug=request.form.get("slug","").strip() or slugify(name)
        sku_owner=Product.query.filter_by(sku=sku).first()
        slug_owner=Product.query.filter_by(slug=requested_slug).first()
        if sku_owner and sku_owner.id!=product_id:
            flash(f"SKU {sku} already belongs to {sku_owner.name}. Open that product to edit it, or use a unique SKU.","error")
            return redirect(url_for("admin",section="catalogue"))
        if slug_owner and slug_owner.id!=product_id:
            flash(f"The product URL '{requested_slug}' is already in use. Choose a unique slug.","error")
            return redirect(url_for("admin",section="catalogue"))
        product.name=name; product.slug=requested_slug; product.sku=sku; product.brand=request.form.get("brand","").strip(); product.category=category
        product.price=Decimal(request.form.get("price") or "0"); product.sale_price=Decimal(request.form["sale_price"]) if request.form.get("sale_price") else None; product.stock=max(0,request.form.get("stock",type=int) or 0)
        product.description=request.form.get("description","").strip(); product.benefits=request.form.get("benefits","").strip(); product.usage=request.form.get("usage","").strip(); product.ingredients=request.form.get("ingredients","").strip(); product.warnings=request.form.get("warnings","").strip(); product.featured=request.form.get("featured")=="on"
        image=request.files.get("image_file"); image_url=request.form.get("image","").strip()
        if image and image.filename:
            filename=f"{secrets.token_hex(6)}-{secure_filename(image.filename)}"; image.save(Path(app.static_folder)/"uploads"/filename); image_url=url_for("static",filename=f"uploads/{filename}")
        product.image=image_url or product.image or "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?auto=format&fit=crop&w=900&q=80"
        try:
            db.session.add(product); db.session.flush()
            record_audit("catalogue.product.saved","Product",product.id,f"Saved product {product.name}",{"sku":product.sku,"stock":product.stock})
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("This product could not be saved because its SKU or product URL is already in use.","error")
            return redirect(url_for("admin",section="catalogue"))
        flash("Product saved.","success"); return redirect(url_for("admin",section="catalogue"))

    @app.post("/admin/products/<int:product_id>/delete")
    @login_required
    def admin_product_delete(product_id):
        require_admin(); product=db.get_or_404(Product,product_id)
        if OrderItem.query.filter_by(product_id=product.id).first(): product.stock=0; flash("Product has order history, so it was archived as out of stock.","info")
        else: WishlistItem.query.filter_by(product_id=product.id).delete(); Review.query.filter_by(product_id=product.id).delete(); db.session.delete(product); flash("Product deleted.","success")
        db.session.commit(); return redirect(url_for("admin"))

    @app.post("/admin/categories")
    @login_required
    def admin_category_save():
        require_admin(); name=request.form.get("name","").strip()
        if name and not Category.query.filter_by(slug=slugify(name)).first(): db.session.add(Category(name=name,slug=slugify(name),icon=request.form.get("icon") or "+",description=request.form.get("description") or "Pharmacy essentials")); db.session.commit(); flash("Category created.","success")
        return redirect(url_for("admin"))

    @app.post("/admin/orders/<int:order_id>/status")
    @login_required
    def admin_order_status(order_id):
        require_permission("orders.manage"); order=db.get_or_404(Order,order_id); status=request.form.get("status")
        transitions={"Pending":{"Processing","Cancelled"},"Processing":{"Ready","Cancelled"},"Ready":{"Dispatched","Cancelled"},"Dispatched":{"Completed"},"Completed":set(),"Cancelled":set()}
        if status not in transitions.get(order.status,set()):
            flash(f"Order cannot move from {order.status} to {status}.","error")
            return redirect(url_for("admin",section="orders"))
        previous=order.status; order.status=status
        record_audit("order.status.changed","Order",order.id,f"{order.reference}: {previous} → {status}")
        db.session.commit(); flash("Order status updated.","success")
        return redirect(url_for("admin",section="orders"))

    @app.post("/admin/messages/<int:message_id>/resolve")
    @login_required
    def admin_message_resolve(message_id):
        require_admin(); row=db.get_or_404(ContactMessage,message_id); row.status="Resolved"
        record_audit("care.message.resolved","ContactMessage",row.id,f"Resolved message from {row.name}")
        db.session.commit(); return redirect(url_for("admin"))

    @app.get("/api/v1/products")
    def api_products():
        page=max(1,request.args.get("page",1,type=int)); per_page=min(100,max(1,request.args.get("per_page",24,type=int)))
        query=Product.query
        if request.args.get("q"):
            term=f"%{request.args['q'].strip()}%"; query=query.filter(or_(Product.name.ilike(term),Product.brand.ilike(term),Product.sku.ilike(term)))
        if request.args.get("category"): query=query.join(Category).filter(Category.slug==request.args["category"])
        if request.args.get("brand"): query=query.filter(Product.brand==request.args["brand"])
        result=query.order_by(Product.id).paginate(page=page,per_page=per_page,error_out=False)
        return jsonify({"data":[serialize_product(p) for p in result.items],"count":result.total,"pagination":{"page":page,"per_page":per_page,"pages":result.pages,"has_next":result.has_next}})

    @app.get("/api/v1/products/<slug>")
    def api_product(slug):
        product=Product.query.filter_by(slug=slug).first_or_404()
        related=Product.query.filter(Product.category_id==product.category_id,Product.id!=product.id).limit(4).all()
        reviews=Review.query.filter_by(product_id=product.id).order_by(Review.created_at.desc()).all()
        group, _ = product_variation_meta(product)
        variations = [p for p in Product.query.filter_by(brand=product.brand).all() if product_variation_meta(p)[0] == group] if group else []
        return jsonify({"data":serialize_product(product,True),"variations":[serialize_product(p) for p in variations],"related":[serialize_product(p) for p in related],"reviews":[{"id":r.id,"customer_name":r.customer_name,"rating":r.rating,"body":r.body,"verified":r.verified} for r in reviews]})

    @app.get("/api/v1/categories")
    def api_categories():
        rows=Category.query.order_by(Category.name).all()
        return jsonify({"data":[{"id":c.id,"name":c.name,"slug":c.slug,"icon":c.icon,"description":c.description,"product_count":len(c.products)} for c in rows]})

    @app.post("/api/v1/contact")
    @csrf.exempt
    def api_contact():
        payload=request.get_json(silent=True) or {}
        if str(payload.get("website","")).strip():
            return jsonify({"error":"invalid_request","message":"The message could not be accepted."}),400
        fields={key:str(payload.get(key,"")).strip() for key in ("name","email","subject","message")}
        if not fields["name"] or "@" not in fields["email"] or len(fields["message"])<10:
            return jsonify({"error":"invalid_request","message":"Please provide your name, a valid email and a message of at least 10 characters."}),400
        db.session.add(ContactMessage(**fields)); db.session.commit()
        return jsonify({"data":{"status":"received"},"message":"Our care team will reply within one working day."}),201

    @app.post("/api/v1/orders")
    @csrf.exempt
    def api_create_order():
        payload=request.get_json(silent=True) or {}; customer=payload.get("customer",{}); requested=payload.get("items",[])
        required=["name","email","phone","address","town","county","payment_method"]
        if any(not str(customer.get(field,"")).strip() for field in required) or not requested:
            return jsonify({"error":"invalid_request","message":"Complete delivery details and include at least one item."}),400
        product_ids=[int(item.get("product_id",0)) for item in requested]
        products={p.id:p for p in Product.query.filter(Product.id.in_(product_ids)).all()}; subtotal=Decimal("0"); lines=[]
        for item in requested:
            product=products.get(int(item.get("product_id",0))); quantity=max(1,int(item.get("quantity",1)))
            if not product or quantity>product.stock: return jsonify({"error":"stock_unavailable","message":"One or more products are unavailable."}),409
            subtotal+=product.effective_price*quantity; lines.append((product,quantity))
        delivery=Decimal("0") if subtotal>=3000 else Decimal("250")
        order=Order(reference=f"SHP-{datetime.utcnow():%y%m%d}-{Order.query.count()+1:05d}",customer_name=customer["name"],email=customer["email"],phone=customer["phone"],address=customer["address"],town=customer["town"],county=customer["county"],payment_method=customer["payment_method"],subtotal=subtotal,delivery_fee=delivery,discount=0,total=subtotal+delivery)
        db.session.add(order)
        for product,quantity in lines:
            product.stock-=quantity; db.session.add(OrderItem(order=order,product_id=product.id,name=product.name,sku=product.sku,quantity=quantity,unit_price=product.effective_price))
        db.session.commit(); return jsonify({"data":{"reference":order.reference,"total":float(order.total),"status":order.status}}),201

    @app.post("/api/v1/payments/mpesa/callback")
    @csrf.exempt
    def mpesa_callback():
        payload=request.get_json(silent=True) or {}; callback=payload.get("Body",{}).get("stkCallback",{}); checkout_id=callback.get("CheckoutRequestID")
        attempt=PaymentAttempt.query.filter_by(checkout_request_id=checkout_id).first()
        if attempt:
            attempt.status="Paid" if callback.get("ResultCode")==0 else "Failed"; attempt.response_message=callback.get("ResultDesc"); attempt.order.status="Processing" if callback.get("ResultCode")==0 else attempt.order.status; db.session.commit()
        return jsonify({"ResultCode":0,"ResultDesc":"Accepted"})

    @app.get("/api/v1/health")
    def health(): return jsonify({"status":"healthy","service":"shield-pharmacy-api"})

    @app.get("/api/v1/readiness")
    def readiness():
        checks={
            "database": bool(db.session.execute(db.text("SELECT 1")).scalar()),
            "secret_key": app.config["SECRET_KEY"]!="development-key-change-before-deploy",
            "secure_cookie": bool(app.config["SESSION_COOKIE_SECURE"]),
            "mpesa": os.getenv("MPESA_ENABLED","false").lower()=="true" and all(os.getenv(key) for key in ("MPESA_CONSUMER_KEY","MPESA_CONSUMER_SECRET","MPESA_SHORTCODE","MPESA_PASSKEY","MPESA_CALLBACK_URL")),
            "mail": all(os.getenv(key) for key in ("MAIL_SERVER","MAIL_USERNAME","MAIL_PASSWORD","MAIL_DEFAULT_SENDER")),
        }
        ready=checks["database"] and (app.config.get("TESTING") or (checks["secret_key"] and checks["secure_cookie"]))
        return jsonify({"status":"ready" if ready else "configuration_required","checks":checks}),200 if ready else 503

    @app.get("/sitemap.xml")
    def sitemap():
        urls=[url_for("home",_external=True),url_for("products",_external=True),url_for("about",_external=True),url_for("contact",_external=True)]+[url_for("product_detail",slug=p.slug,_external=True) for p in Product.query.all()]
        return app.response_class(render_template("sitemap.xml",urls=urls),mimetype="application/xml")

    @app.get("/robots.txt")
    def robots(): return app.response_class("User-agent: *\nAllow: /\nDisallow: /admin\nSitemap: "+url_for("sitemap",_external=True),mimetype="text/plain")

    @app.get("/about")
    def about(): return render_template("about.html",title="About Shield")
    @app.route("/contact",methods=["GET","POST"])
    def contact():
        if request.method=="POST":
            honeypot=request.form.get("website","")
            if honeypot: abort(400)
            fields={key:request.form.get(key,"").strip() for key in ("name","email","subject","message")}
            if not fields["name"] or "@" not in fields["email"] or not fields["message"]: flash("Please complete the contact form.","error")
            else: db.session.add(ContactMessage(**fields)); db.session.commit(); flash("Message received. Our care team will reply shortly.","success"); return redirect(url_for("contact"))
        return render_template("contact.html",title="Contact us")
    @app.get("/categories")
    def categories(): return render_template("categories.html",categories=Category.query.all(),title="Shop categories")
    @app.get("/offers")
    def offers(): return render_template("products.html",products=Product.query.filter(Product.sale_price.isnot(None)).all(),categories=Category.query.all(),brands=[],selected={"q":"","category":"","brand":"","availability":"","sort":"popular","price":""},title="Current offers")
    @app.get("/privacy")
    def privacy(): return render_template("legal.html",page="privacy",title="Privacy policy")
    @app.get("/terms")
    def terms(): return render_template("legal.html",page="terms",title="Terms & conditions")

    @app.errorhandler(404)
    def not_found(error): return render_template("404.html"),404
    @app.errorhandler(403)
    def forbidden(error): return render_template("404.html",forbidden=True),403

    with app.app_context():
        (Path(app.static_folder)/"uploads").mkdir(parents=True,exist_ok=True); db.create_all(); seed_database(); sync_jamieson_catalog()
        if not Review.query.first() and Product.query.count() >= 4:
            for product_id, customer_name, rating, body in [(1,"Wanjiku M.",5,"Fast delivery and the sealed pack arrived in perfect condition."),(1,"David O.",5,"Straightforward ordering and clear usage information."),(3,"Njeri K.",5,"Genuine product and excellent for my dry skin."),(4,"Peter A.",4,"Simple to use and thoughtfully packed.")]:
                db.session.add(Review(product_id=product_id,customer_name=customer_name,rating=rating,body=body))
            db.session.commit()
    return app


def product_variation_meta(product):
    groups = {
        "jamieson-melatonin-": ("Jamieson Melatonin", product.name.removeprefix("Jamieson Melatonin ").replace(" Caplets", " ·").replace(" Capsules", " ·")),
        "jamieson-vitamin-d3-": ("Jamieson Vitamin D3", product.name.removeprefix("Jamieson Vitamin D3 ").replace(" Tablets", " ·").replace(" Chewable", " · Chewable")),
        "jamieson-calcium-magnesium-": ("Jamieson Calcium Magnesium", product.name.removeprefix("Jamieson Calcium Magnesium + ").replace(" Caplets", " ·")),
    }
    for prefix, meta in groups.items():
        if product.slug.startswith(prefix):
            return meta
    return None, None


def serialize_product(product, detailed=False):
    data={"id":product.id,"name":product.name,"slug":product.slug,"brand":product.brand,"sku":product.sku,"category":{"name":product.category.name,"slug":product.category.slug},"price":float(product.price),"sale_price":float(product.sale_price) if product.sale_price is not None else None,"effective_price":float(product.effective_price),"stock":product.stock,"image":product.image,"featured":product.featured,"popularity":product.popularity,"description":product.description}
    group, label = product_variation_meta(product)
    data.update(variation_group=group, variation_label=label)
    if detailed: data.update(benefits=product.benefits,usage=product.usage,ingredients=product.ingredients,warnings=product.warnings)
    return data
