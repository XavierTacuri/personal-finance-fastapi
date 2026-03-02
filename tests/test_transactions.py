def test_create_transaction_and_list_has_category_name(client, token):
    headers = {"Authorization": f"Bearer {token}"}

    # crea categoría
    r = client.post("/categories", json={"name": "rent"}, headers=headers)
    assert r.status_code in (201, 409)

    # saca categories para obtener id de rent
    r = client.get("/categories", headers=headers)
    assert r.status_code == 200
    cats = r.json()
    rent = next(c for c in cats if c["name"] == "rent")
    rent_id = rent.get("id")

    # crea transaction expense
    payload = {
        "category_id": rent_id,
        "type": "expense",
        "amount": 800,
        "currency": "USD",
        "txn_date": "2026-02-02",
        "note": "apartment rent",
    }
    r = client.post("/transactions/", json=payload, headers=headers)
    if r.status_code != 201:
        print("TX STATUS:", r.status_code)
        print("TX BODY:", r.text)
    assert r.status_code == 201, r.text

    # lista y verifica category_name
    r = client.get("/transactions", headers=headers)
    assert r.status_code == 200, r.text

    data = r.json()
    # si ya implementaste paginación, esto será {"items":[...],...}
    items = data["items"] if isinstance(data, dict) and "items" in data else data
    assert len(items) >= 1
    assert items[0]["category_name"] is not None