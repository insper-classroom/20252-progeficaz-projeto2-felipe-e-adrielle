from main import app
import pytest


class TestImoveisAPI:
    @pytest.fixture
    def client(self):
        app.testing = True
        with app.test_client() as client:
            yield client

    def test_get_imoveis(self, client):
        response = client.get("/api/v1/imoveis")
        assert response.status_code == 200
        data = response.get_json()
        assert "data" in data
        assert "pagination" in data
        assert "_links" in data
        assert isinstance(data["data"], list)
        if data["data"]:
            assert "id" in data["data"][0]
            assert "logradouro" in data["data"][0]
            assert "tipo_logradouro" in data["data"][0]
            assert "bairro" in data["data"][0]
            assert "cidade" in data["data"][0]
            assert "cep" in data["data"][0]
            assert "tipo" in data["data"][0]
            assert "valor" in data["data"][0]
            assert "data_aquisicao" in data["data"][0]

    def test_add_imovel(self, client):
        new_imovel = {
            "logradouro": "Rua Teste",
            "tipo_logradouro": "Rua",
            "bairro": "Bairro Teste",
            "cidade": "Cidade Teste",
            "cep": "12345-678",
            "tipo": "Venda",
            "valor": 250000.00,
            "data_aquisicao": "2023-01-01",
        }
        response = client.post("/api/v1/imoveis", json=new_imovel)
        assert response.status_code == 201
        data = response.get_json()
        assert data["message"] == "Imóvel adicionado com sucesso"
        assert "id" in data

        client.delete(f"/api/v1/imoveis/{data['id']}")

    def test_get_imovel_by_id(self, client):
        new_imovel = {
            "logradouro": "Rua GetById",
            "tipo_logradouro": "Rua",
            "bairro": "Bairro Get",
            "cidade": "Cidade Get",
            "cep": "55555-000",
            "tipo": "Venda",
            "valor": 100000.00,
            "data_aquisicao": "2023-05-01",
        }
        post_resp = client.post("/api/v1/imoveis", json=new_imovel)
        imovel_id = post_resp.get_json()["id"]

        get_resp = client.get(f"/api/v1/imoveis/{imovel_id}")
        assert get_resp.status_code == 200
        data = get_resp.get_json()
        assert data["id"] == imovel_id
        assert data["logradouro"] == "Rua GetById"
        assert data["tipo_logradouro"] == "Rua"
        assert data["bairro"] == "Bairro Get"
        assert data["cidade"] == "Cidade Get"
        assert data["cep"] == "55555-000"
        assert data["tipo"] == "Venda"
        assert data["valor"] == 100000.00
        assert data["data_aquisicao"] == "2023-05-01"

        # Cleanup
        client.delete(f"/imoveis/{imovel_id}")

    def test_delete_imovel(self, client):
        new_imovel = {
            "logradouro": "Rua Delete",
            "tipo_logradouro": "Rua",
            "bairro": "Bairro Delete",
            "cidade": "Cidade Delete",
            "cep": "98765-432",
            "tipo": "Aluguel",
            "valor": 1500.00,
            "data_aquisicao": "2023-02-01",
        }
        post_response = client.post("/api/v1/imoveis", json=new_imovel)
        imovel_id = post_response.get_json()["id"]

        # Deleta
        delete_response = client.delete(f"/api/v1/imoveis/{imovel_id}")
        assert delete_response.status_code == 204

        # Tenta deletar de novo (não existe mais)
        delete_response = client.delete(f"/api/v1/imoveis/{imovel_id}")
        assert delete_response.status_code == 404
        assert delete_response.get_json()["error"] == "Imóvel não encontrado"

    def test_update_imovel(self, client):
        new_imovel = {
            "logradouro": "Rua Update",
            "tipo_logradouro": "Rua",
            "bairro": "Bairro Update",
            "cidade": "Cidade Update",
            "cep": "54321-098",
            "tipo": "Venda",
            "valor": 300000.00,
            "data_aquisicao": "2023-03-01",
        }
        post_response = client.post("/api/v1/imoveis", json=new_imovel)
        imovel_id = post_response.get_json()["id"]

        updated_imovel = {
            "logradouro": "Rua Updated",
            "tipo_logradouro": "Avenida",
            "bairro": "Bairro Updated",
            "cidade": "Cidade Updated",
            "cep": "54321-000",
            "tipo": "Aluguel",
            "valor": 2000.00,
            "data_aquisicao": "2023-04-01",
        }
        put_response = client.put(f"/api/v1/imoveis/{imovel_id}", json=updated_imovel)
        assert put_response.status_code == 200
        assert put_response.get_json()["message"] == "Imóvel atualizado com sucesso"

        # Atualiza um inexistente
        put_response = client.put("/api/v1/imoveis/999999", json=updated_imovel)
        assert put_response.status_code == 404
        assert put_response.get_json()["error"] == "Imóvel não encontrado"

        # Cleanup
        client.delete(f"/imoveis/{imovel_id}")

    def test_get_imoveis_by_tipo(self, client):
        imovel_casa = {
            "logradouro": "Rua Casa",
            "tipo_logradouro": "Rua",
            "bairro": "Bairro A",
            "cidade": "Cidade A",
            "cep": "11111-111",
            "tipo": "casa",
            "valor": 300000.00,
            "data_aquisicao": "2023-06-01",
        }
        imovel_apartamento = {
            "logradouro": "Rua Apartamento",
            "tipo_logradouro": "Avenida",
            "bairro": "Bairro B",
            "cidade": "Cidade B",
            "cep": "22222-222",
            "tipo": "Apartamento",
            "valor": 200000.00,
            "data_aquisicao": "2023-07-01",
        }

        resp_casa = client.post("/api/v1/imoveis", json=imovel_casa)
        resp_apt = client.post("/api/v1/imoveis", json=imovel_apartamento)
        id_casa = resp_casa.get_json()["id"]
        id_apt = resp_apt.get_json()["id"]

        get_resp = client.get("/api/v1/imoveis?tipo=casa&per_page=100")
        assert get_resp.status_code == 200
        data = get_resp.get_json()
        assert "data" in data
        assert all("casa" in item["tipo"].lower() for item in data["data"])

        # Verifica se o imóvel específico foi criado corretamente
        get_specific = client.get(f"/api/v1/imoveis/{id_casa}")
        assert get_specific.status_code == 200
        specific_data = get_specific.get_json()
        assert specific_data["tipo"].lower() == "casa"

        client.delete(f"/api/v1/imoveis/{id_casa}")
        client.delete(f"/api/v1/imoveis/{id_apt}")

    def test_get_imoveis_by_cidade(self, client):
        imovel_cidade_a = {
            "logradouro": "Rua Cidade A",
            "tipo_logradouro": "Rua",
            "bairro": "Bairro A",
            "cidade": "Cidade A",
            "cep": "33333-333",
            "tipo": "casa",
            "valor": 250000.00,
            "data_aquisicao": "2023-08-01",
        }
        imovel_cidade_b = {
            "logradouro": "Rua Cidade B",
            "tipo_logradouro": "Avenida",
            "bairro": "Bairro B",
            "cidade": "Cidade B",
            "cep": "44444-444",
            "tipo": "Apartamento",
            "valor": 350000.00,
            "data_aquisicao": "2023-09-01",
        }

        resp_a = client.post("/api/v1/imoveis", json=imovel_cidade_a)
        resp_b = client.post("/api/v1/imoveis", json=imovel_cidade_b)
        id_a = resp_a.get_json()["id"]
        id_b = resp_b.get_json()["id"]

        get_resp = client.get("/api/v1/imoveis?cidade=Cidade A")
        assert get_resp.status_code == 200
        data = get_resp.get_json()
        assert "data" in data
        assert all(item["cidade"] == "Cidade A" for item in data["data"])
        assert any(item["id"] == id_a for item in data["data"])

        client.delete(f"/api/v1/imoveis/{id_a}")
        client.delete(f"/api/v1/imoveis/{id_b}")

    def test_get_imovel_not_found(self, client):
        response = client.get("/api/v1/imoveis/9999999999999999999999999")
        assert response.status_code == 404
        assert response.get_json()["error"] == "Imóvel não encontrado"

    def test_delete_imovel_false_positive(self, client):
        # Adiciona imóvel
        new_imovel = {
            "logradouro": "Rua False Positive",
            "tipo_logradouro": "Rua",
            "bairro": "Bairro FP",
            "cidade": "Cidade FP",
            "cep": "99999-999",
            "tipo": "Venda",
            "valor": 123456.78,
            "data_aquisicao": "2023-10-10",
        }
        post_response = client.post("/api/v1/imoveis", json=new_imovel)
        imovel_id = post_response.get_json()["id"]

        # Simula falso positivo: responde sucesso mas não deleta realmente
        # Aqui, deletamos, mas depois checamos se ainda existe
        delete_response = client.delete(f"/api/v1/imoveis/{imovel_id}")
        assert delete_response.status_code == 204

        # Se o delete não funcionou, o imóvel ainda existe
        get_response = client.get(f"/api/v1/imoveis/{imovel_id}")
        # O correto seria 404, mas se for 200, é falso positivo
        assert (
            get_response.status_code == 404
            or get_response.get_json().get("error") == "Imóvel não encontrado"
        )

    def test_update_imovel_partial_fields(self, client):
        # Adiciona imóvel completo
        new_imovel = {
            "logradouro": "Rua Parcial",
            "tipo_logradouro": "Rua",
            "bairro": "Bairro Parcial",
            "cidade": "Cidade Parcial",
            "cep": "11111-222",
            "tipo": "Venda",
            "valor": 12345.67,
            "data_aquisicao": "2023-11-11",
        }
        post_response = client.post("/api/v1/imoveis", json=new_imovel)
        imovel_id = post_response.get_json()["id"]

        # Atualiza só alguns campos (o backend espera todos, então deve atualizar tudo)
        partial_update = {
            "logradouro": "Rua Parcial Atualizada",
            "tipo_logradouro": "Avenida",
            "bairro": "Bairro Parcial",
            "cidade": "Cidade Parcial",
            "cep": "11111-222",
            "tipo": "Venda",
            "valor": 54321.00,
            "data_aquisicao": "2023-12-12",
        }
        put_response = client.put(f"/api/v1/imoveis/{imovel_id}", json=partial_update)
        assert put_response.status_code == 200
        assert put_response.get_json()["message"] == "Imóvel atualizado com sucesso"

        # Confirma atualização
        get_response = client.get(f"/api/v1/imoveis/{imovel_id}")
        data = get_response.get_json()
        assert data["logradouro"] == "Rua Parcial Atualizada"
        assert data["valor"] == 54321.00

        # Cleanup
        client.delete(f"/imoveis/{imovel_id}")

    def test_get_imoveis_empty_result(self, client):
        # Busca por tipo/cidade que não existe
        response = client.get("/api/v1/imoveis?tipo=tipo_inexistente")
        assert response.status_code == 200
        data = response.get_json()
        assert "data" in data
        assert isinstance(data["data"], list)
        assert len(data["data"]) == 0

        response = client.get("/api/v1/imoveis?cidade=Cidade Inexistente")
        assert response.status_code == 200
        data = response.get_json()
        assert "data" in data
        assert isinstance(data["data"], list)
        assert len(data["data"]) == 0

    def test_add_and_get_multiple_imoveis(self, client):
        imoveis = [
            {
                "logradouro": "Rua 1",
                "tipo_logradouro": "Rua",
                "bairro": "Bairro 1",
                "cidade": "Cidade 1",
                "cep": "10101-101",
                "tipo": "Venda",
                "valor": 100000.00,
                "data_aquisicao": "2023-01-01",
            },
            {
                "logradouro": "Rua 2",
                "tipo_logradouro": "Avenida",
                "bairro": "Bairro 2",
                "cidade": "Cidade 2",
                "cep": "20202-202",
                "tipo": "Aluguel",
                "valor": 2000.00,
                "data_aquisicao": "2023-02-02",
            },
        ]
        ids = []
        for imovel in imoveis:
            resp = client.post("/api/v1/imoveis", json=imovel)
            assert resp.status_code == 201
            ids.append(resp.get_json()["id"])

        # Verifica se os imóveis foram criados corretamente
        for imovel_id in ids:
            get_resp = client.get(f"/api/v1/imoveis/{imovel_id}")
            assert get_resp.status_code == 200
            data = get_resp.get_json()
            assert "id" in data
            assert data["id"] == imovel_id

        # Cleanup
        for id_ in ids:
            client.delete(f"/api/v1/imoveis/{id_}")

    def test_sql_injection_attempt(self, client):
        # Tenta SQL injection no parâmetro tipo
        response = client.get("/api/v1/imoveis?tipo=casa'; DROP TABLE imoveis; --")
        assert response.status_code == 200
        # Se a tabela sumiu, os outros testes vão falhar, então só verifica que não retorna erro grave
        data = response.get_json()
        assert "data" in data
        assert isinstance(data["data"], list)

    def test_pagination(self, client):
        """Testa funcionalidade de paginação"""
        # Testa primeira página
        response = client.get("/api/v1/imoveis?page=1&per_page=5")
        assert response.status_code == 200
        data = response.get_json()
        assert "pagination" in data
        assert data["pagination"]["page"] == 1
        assert data["pagination"]["per_page"] == 5
        assert len(data["data"]) <= 5

        # Testa segunda página
        response2 = client.get("/api/v1/imoveis?page=2&per_page=5")
        assert response2.status_code == 200
        data2 = response2.get_json()
        assert data2["pagination"]["page"] == 2

        # Verifica que as páginas são diferentes
        if data["data"] and data2["data"]:
            assert data["data"][0]["id"] != data2["data"][0]["id"]

    def test_sorting(self, client):
        """Testa funcionalidade de ordenação"""
        # Testa ordenação por valor crescente
        response = client.get("/api/v1/imoveis?sort=valor&order=asc&per_page=10")
        assert response.status_code == 200
        data = response.get_json()
        assert "data" in data
        if len(data["data"]) > 1:
            valores = [
                item["valor"] for item in data["data"] if item["valor"] is not None
            ]
            assert valores == sorted(valores)

        # Testa ordenação por valor decrescente
        response2 = client.get("/api/v1/imoveis?sort=valor&order=desc&per_page=10")
        assert response2.status_code == 200
        data2 = response2.get_json()
        if len(data2["data"]) > 1:
            valores2 = [
                item["valor"] for item in data2["data"] if item["valor"] is not None
            ]
            assert valores2 == sorted(valores2, reverse=True)

    def test_invalid_sort_field(self, client):
        """Testa validação de campo de ordenação inválido"""
        response = client.get("/api/v1/imoveis?sort=campo_inexistente")
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data
        assert "Campo de ordenação inválido" in data["error"]

    def test_invalid_sort_order(self, client):
        """Testa validação de direção de ordenação inválida"""
        response = client.get("/api/v1/imoveis?sort=valor&order=invalid")
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data
        assert "Direção de ordenação inválida" in data["error"]

    def test_validation_missing_fields(self, client):
        """Testa validação de campos obrigatórios"""
        imovel_incompleto = {
            "logradouro": "Rua Teste",
            # Faltam campos obrigatórios: cidade, tipo, valor
        }
        response = client.post("/api/v1/imoveis", json=imovel_incompleto)
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data
        assert "Campos obrigatórios ausentes" in data["error"]
        assert "missing_fields" in data

    def test_validation_invalid_value(self, client):
        """Testa validação de valor inválido"""
        imovel_valor_invalido = {
            "logradouro": "Rua Teste",
            "cidade": "Cidade Teste",
            "tipo": "casa",
            "valor": "não é um número",
        }
        response = client.post("/api/v1/imoveis", json=imovel_valor_invalido)
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data
        assert "Valor deve ser um número válido" in data["error"]

    def test_validation_negative_value(self, client):
        """Testa validação de valor negativo"""
        imovel_valor_negativo = {
            "logradouro": "Rua Teste",
            "cidade": "Cidade Teste",
            "tipo": "casa",
            "valor": -1000,
        }
        response = client.post("/api/v1/imoveis", json=imovel_valor_negativo)
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data
        assert "Valor deve ser positivo" in data["error"]

    def test_api_docs(self, client):
        """Testa endpoint de documentação da API"""
        response = client.get("/api/v1/docs")
        assert response.status_code == 200
        data = response.get_json()
        assert "title" in data
        assert "version" in data
        assert "endpoints" in data
        assert "query_parameters" in data
        assert data["version"] == "v1"

    def test_home_endpoint_with_version(self, client):
        """Testa endpoint home com informação de versão"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.get_json()
        assert "version" in data
        assert data["version"] == "v1"
        assert "docs" in data["_links"]
