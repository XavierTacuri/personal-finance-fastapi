def test_print_routes(client):
    schema = client.get("/openapi.json").json()
    paths = schema["paths"].keys()
    print("\n".join(sorted(paths)))
    assert True