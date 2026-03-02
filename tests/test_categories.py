import uuid

def test_create_category(client, token):
    headers = {"Authorization": f"Bearer {token}"}
    name = f"Salary_{uuid.uuid4().hex[:6]}"
    r = client.post("/categories", json={"name": name}, headers=headers)
    assert r.status_code in (201, 400, 409), r.text


def test_list_categories(client, token):
    headers = {"Authorization": f"Bearer {token}"}

    r = client.get("/categories/", headers=headers)  # <-- CAMBIO AQUÍ
    assert r.status_code == 200, r.text

    cats = r.json()
    assert isinstance(cats, list)