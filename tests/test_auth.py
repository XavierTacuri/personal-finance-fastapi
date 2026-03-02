def test_me(client, token):
    r = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    me = r.json()
    assert "id" in me
    assert "email" in me