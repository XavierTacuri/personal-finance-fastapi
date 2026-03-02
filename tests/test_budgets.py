def test_budget_status(client, token):
    headers = {"Authorization": f"Bearer {token}"}

    # category rent
    client.post("/categories", json={"name": "rent"}, headers=headers)
    cats = client.get("/categories", headers=headers).json()
    rent_id = next(c["id"] for c in cats if c["name"] == "rent")

    # crea una transacción expense en febrero
    client.post("/transactions/", json={
        "category_id": rent_id,
        "type": "expense",
        "amount": 200,
        "currency": "USD",
        "txn_date": "2026-02-10",
        "note": "rent part",
    }, headers=headers)

    # upsert budget
    r = client.post("/budgets", json={
        "category_id": rent_id,
        "month": "2026-02-01",
        "limit_amount": 900
    }, headers=headers)
    assert r.status_code in (201, 200)

    # status
    r = client.get("/budgets", params={"month": "2026-02-01"}, headers=headers)
    assert r.status_code == 200
    status = r.json()
    assert isinstance(status, list)
    rent_budget = next(x for x in status if x["category_id"] == rent_id)
    assert rent_budget["limit_amount"] == 900
    assert rent_budget["spent"] >= 200
    assert rent_budget["remaining"] <= 900