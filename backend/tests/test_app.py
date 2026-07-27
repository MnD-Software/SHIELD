import pytest

from backend.app import create_app, db


@pytest.fixture()
def client(tmp_path):
    app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": f"sqlite:///{tmp_path / 'test.db'}", "WTF_CSRF_ENABLED": False})
    with app.test_client() as test_client:
        yield test_client
    with app.app_context():
        db.drop_all()


def login_admin(client):
    response = client.post("/api/v1/auth/login", json={"email": "admin@shield.test", "password": "ShieldAdmin123!"})
    assert response.status_code == 200
    assert response.json["data"]["role"] == "admin"


@pytest.mark.parametrize("path", ["/", "/products", "/categories", "/offers", "/about", "/contact", "/privacy", "/terms", "/sitemap.xml"])
def test_legacy_pages_redirect_to_next(client, path):
    response = client.get(path)
    assert response.status_code == 302
    assert response.location.startswith("http://localhost:3000")


def test_health_catalogue_and_readiness_apis(client):
    assert client.get("/api/v1/health").status_code == 200
    response = client.get("/api/v1/products")
    assert response.status_code == 200
    assert response.json["count"] >= 8
    assert client.get("/api/v1/categories").status_code == 200
    readiness = client.get("/api/v1/readiness")
    assert readiness.status_code == 200
    assert readiness.json["checks"]["database"] is True


def test_json_registration_session_and_account(client):
    response = client.post("/api/v1/auth/register", json={"name":"Amina Kamau","email":"amina@example.com","phone":"0712345678","password":"a-secure-password"})
    assert response.status_code == 201
    assert client.get("/api/v1/auth/me").json["data"]["name"] == "Amina Kamau"
    assert client.get("/api/v1/account").status_code == 200
    assert client.post("/api/v1/auth/logout").status_code == 200
    assert client.get("/api/v1/account").status_code == 401


def test_contact_api_validates_and_surfaces_message_in_admin(client):
    invalid = client.post("/api/v1/contact", json={"name":"Amina","email":"invalid","message":"short"})
    assert invalid.status_code == 400
    response = client.post("/api/v1/contact", json={"name":"Amina","email":"amina@example.com","subject":"Product question","message":"Please help me understand this product."})
    assert response.status_code == 201
    login_admin(client)
    overview = client.get("/api/v1/admin/overview")
    assert overview.status_code == 200
    assert overview.json["data"]["messages"][0]["subject"] == "Product question"


def test_order_api_recalculates_stock_and_admin_controls_transition(client):
    order = client.post("/api/v1/orders", json={"customer":{"name":"Amina Kamau","email":"amina@example.com","phone":"0712345678","address":"Westlands Road","town":"Nairobi","county":"Nairobi","payment_method":"cash"},"items":[{"product_id":1,"quantity":1}]})
    assert order.status_code == 201
    login_admin(client)
    rejected = client.patch("/api/v1/admin/orders/1", json={"status":"Completed"})
    assert rejected.status_code == 409
    accepted = client.patch("/api/v1/admin/orders/1", json={"status":"Processing"})
    assert accepted.status_code == 200
    assert accepted.json["data"]["status"] == "Processing"


def test_admin_overview_requires_admin_session(client):
    assert client.get("/api/v1/admin/overview").status_code == 403
    login_admin(client)
    response = client.get("/api/v1/admin/overview")
    assert response.status_code == 200
    assert {"orders","revenue","products","low_stock","open_leads","open_tasks"} <= response.json["data"]["metrics"].keys()


def test_crm_stage_update_writes_audit(client):
    from backend.app import AuditEvent, CRMLead
    login_admin(client)
    lead = CRMLead(name="Nairobi Family Clinic", company="Nairobi Family Clinic", email="procurement@nfc.test", source="Corporate outreach", opportunity_value=75000)
    db.session.add(lead)
    db.session.commit()
    response = client.patch(f"/api/v1/admin/crm/leads/{lead.id}", json={"stage":"Qualified"})
    assert response.status_code == 200
    assert CRMLead.query.get(lead.id).stage == "Qualified"
    assert AuditEvent.query.filter_by(entity_type="CRMLead", entity_id=str(lead.id)).count() == 1
