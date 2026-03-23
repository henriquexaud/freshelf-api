from database import init_db
init_db()
print("DB init: OK")

from produtos import repository
print("Repository import: OK")

from produtos import service
print("Service import: OK")

from produtos.validators import validar_produto
print("Validator import: OK")

result, err = validar_produto(None)
assert err == "Envie um JSON válido no corpo da requisição"
print("Validator (invalid input): OK")

result, err = validar_produto({"nome": "Leite", "quantidade": 5, "data_validade": "2026-04-15"})
assert err is None
assert result["nome"] == "Leite"
print("Validator (valid input): OK")

produto_id = service.cadastrar({"nome": "Teste Refactor", "quantidade": 3, "data_validade": "2026-03-25"})
print("Cadastrar: OK (id=%d)" % produto_id)

todos = service.listar_todos()
produto = [p for p in todos if p["id"] == produto_id][0]
assert "status" in produto
print("Listar todos: OK (status=%s)" % produto["status"])

vencendo = service.listar_vencendo()
print("Listar vencendo: OK (%d itens)" % len(vencendo))

stats = service.obter_estatisticas()
assert "total" in stats and "ok" in stats
print("Estatisticas: OK (%s)" % stats)

removidos = service.remover(produto_id)
assert removidos == 1
print("Remover: OK")

print("")
print("=== TODOS OS TESTES PASSARAM ===")
