def test_dashboard(client, token):
    headers = {"Authorization": f"Bearer {token}"}

    # crea categorías
    client.post("/categories", json={"name": "salary"}, headers=headers)
    client.post("/categories", json={"name": "food"}, headers=headers)

    cats = client.get("/categories", headers=headers).json()
    salary_id = next(c["id"] for c in cats if c["name"] == "salary")
    food_id = next(c["id"] for c in cats if c["name"] == "food")

    # crea transacciones en febrero
    client.post("/transactions/", json={
        "category_id": salary_id, "type": "income", "amount": 2000,
        "currency": "USD", "txn_date": "2026-02-01", "note": "salary"
    }, headers=headers)

    client.post("/transactions/", json={
        "category_id": food_id, "type": "expense", "amount": 50,
        "currency": "USD", "txn_date": "2026-02-03", "note": "groceries"
    }, headers=headers)

    r = client.get("/dashboard", params={"month": "2026-02-01"}, headers=headers)
    assert r.status_code == 200
    d = r.json()

    assert "summary" in d
    assert d["summary"]["month"] == "2026-02-01"
    assert d["summary"]["income"] >= 2000
    assert d["summary"]["expense"] >= 50
    assert "recent_transactions" in d