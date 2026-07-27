import pytest

from backend.app import create_app, db


@pytest.fixture()
def client(tmp_path):
    app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": f"sqlite:///{tmp_path / 'test.db'}", "WTF_CSRF_ENABLED": False})
    with app.test_client() as client:
        yield client
    with app.app_context():
        db.drop_all()


@pytest.mark.parametrize("path", ["/", "/products", "/categories", "/offers", "/about", "/contact", "/privacy", "/terms", "/api/v1/health", "/robots.txt", "/sitemap.xml"])
def test_public_routes(client, path):
    assert client.get(path).status_code == 200


def test_product_api(client):
    response = client.get("/api/v1/products")
    assert response.status_code == 200
    assert response.json["count"] >= 8
    assert response.json["pagination"]["page"] == 1
    assert len(response.json["data"]) <= response.json["pagination"]["per_page"]


def test_enterprise_crm_workflow_and_audit(client):
    from backend.app import AuditEvent, CRMLead, CRMTask
    client.post("/login", data={"email":"admin@shield.test","password":"ShieldAdmin123!"})
    response=client.post("/admin/crm/leads",data={"name":"Nairobi Family Clinic","company":"Nairobi Family Clinic","email":"procurement@nfc.test","source":"Corporate outreach","opportunity_value":"75000"},follow_redirects=True)
    assert response.status_code==200
    lead=CRMLead.query.filter_by(email="procurement@nfc.test").one()
    client.post(f"/admin/crm/leads/{lead.id}/stage",data={"stage":"Qualified"})
    response=client.post("/admin/crm/tasks",data={"lead_id":lead.id,"title":"Prepare corporate pricing","assigned_to":"Admin User","priority":"High","due_at":"2026-08-01"},follow_redirects=True)
    assert response.status_code==200
    assert CRMTask.query.filter_by(lead_id=lead.id,status="Open").count()==1
    assert AuditEvent.query.filter_by(entity_type="CRMLead",entity_id=str(lead.id)).count()>=2


def test_order_workflow_rejects_invalid_transition(client):
    client.post("/cart/add/1",data={"quantity":1})
    client.post("/checkout", data={"name":"Amina Kamau","email":"amina@example.com","phone":"0712345678","address":"Westlands Road","town":"Nairobi","county":"Nairobi","payment_method":"cash","terms":"on"})
    client.post("/login", data={"email":"admin@shield.test","password":"ShieldAdmin123!"})
    response=client.post("/admin/orders/1/status",data={"status":"Completed"},follow_redirects=True)
    assert b"cannot move from Pending to Completed" in response.data


def test_cart_and_checkout(client):
    response = client.post("/cart/add/1", data={"quantity": 2}, follow_redirects=True)
    assert b"Shopping bag" in response.data
    assert b"Panadol Advance" in response.data
    response = client.post("/checkout", data={"name":"Amina Kamau","email":"amina@example.com","phone":"0712345678","address":"Westlands Road","town":"Nairobi","county":"Nairobi","payment_method":"cash","terms":"on"}, follow_redirects=True)
    assert b"Order confirmed" in response.data


def test_registration_and_account(client):
    response = client.post("/register", data={"name":"Amina Kamau","email":"amina@example.com","phone":"0712345678","password":"a-secure-password"}, follow_redirects=True)
    assert b"Hello, Amina" in response.data


def test_contact_form_is_stored_and_visible_to_admin(client):
    response = client.post("/contact", data={"name":"Amina Kamau","email":"amina@example.com","subject":"Order support","message":"Please help me with my delivery."}, follow_redirects=True)
    assert b"Message received" in response.data
    client.post("/login", data={"email":"admin@shield.test","password":"ShieldAdmin123!"})
    response = client.get("/admin")
    assert response.status_code == 200
    assert b"Please help me with my delivery" in response.data


def test_contact_api_validates_and_stores_message(client):
    invalid=client.post("/api/v1/contact",json={"name":"Amina","email":"invalid","message":"short"})
    assert invalid.status_code==400
    response=client.post("/api/v1/contact",json={"name":"Amina","email":"amina@example.com","subject":"Product question","message":"Please help me understand this product."})
    assert response.status_code==201
    assert response.json["data"]["status"]=="received"


def test_readiness_reports_test_database(client):
    response=client.get("/api/v1/readiness")
    assert response.status_code==200
    assert response.json["checks"]["database"] is True


def test_customer_can_update_profile(client):
    client.post("/register", data={"name":"Amina Kamau","email":"amina@example.com","phone":"0712345678","password":"a-secure-password"})
    response = client.post("/account", data={"name":"Amina Njeri","phone":"0799999999"}, follow_redirects=True)
    assert b"Profile updated" in response.data
    assert b"Amina Njeri" in response.data


def test_admin_can_create_product_and_update_order(client):
    client.post("/login", data={"email":"admin@shield.test","password":"ShieldAdmin123!"})
    response = client.post("/admin/products/save", data={"name":"Digital Thermometer","sku":"SH-MED-999","brand":"Shield","category_id":"5","price":"950","stock":"12","description":"Fast digital temperature reading.","benefits":"Easy home monitoring.","usage":"Follow the supplied guide.","ingredients":"Thermometer and battery.","warnings":"Clean after use."}, follow_redirects=True)
    assert b"Product saved" in response.data
    assert b"Digital Thermometer" in response.data
    client.post("/logout")
    client.post("/cart/add/1", data={"quantity":1})
    client.post("/checkout", data={"name":"Amina Kamau","email":"amina@example.com","phone":"0712345678","address":"Westlands Road","town":"Nairobi","county":"Nairobi","payment_method":"cash","terms":"on"})
    client.post("/login", data={"email":"admin@shield.test","password":"ShieldAdmin123!"})
    response = client.post("/admin/orders/1/status", data={"status":"Dispatched"}, follow_redirects=True)
    assert b"Dispatched" in response.data
