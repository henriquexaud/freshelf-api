from app import app

client = app.test_client()

r = client.get("/health")
assert r.status_code == 200
print("GET /health: OK")

r = client.post("/produtos", json={"nome": "HTTP Test", "quantidade": 2, "data_validade": "2026-05-01"})
assert r.status_code == 201
data = r.get_json()
pid = data["id"]
print("POST /produtos: OK (id=%d)" % pid)

r = client.post("/produtos", json={"nome": "", "quantidade": 2, "data_validade": "2026-05-01"})
assert r.status_code == 400
assert "erro" in r.get_json()
print("POST /produtos (invalid): OK")

r = client.get("/produtos")
assert r.status_code == 200
produtos = r.get_json()
p = [x for x in produtos if x["id"] == pid][0]
assert "status" in p
print("GET /produtos: OK (status=%s)" % p["status"])

r = client.get("/produtos/vencendo")
assert r.status_code == 200
print("GET /produtos/vencendo: OK")

r = client.get("/produtos/estatisticas")
assert r.status_code == 200
s = r.get_json()
assert all(k in s for k in ["total", "ok", "vencendo", "vencidos"])
print("GET /produtos/estatisticas: OK")

r = client.delete("/produtos/%d" % pid)
assert r.status_code == 200
print("DELETE /produtos/%d: OK" % pid)

r = client.delete("/produtos/999999")
assert r.status_code == 404
print("DELETE /produtos/999999: OK (404)")

print("")
print("=== TODOS OS TESTES HTTP PASSARAM ===")
