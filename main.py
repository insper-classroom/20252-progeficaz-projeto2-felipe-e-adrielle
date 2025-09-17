from flask import Flask, jsonify, request, url_for
from db import get_db_connection
import math

app = Flask(__name__)
conn = get_db_connection()

# API Version
API_VERSION = "v1"
BASE_URL = f"/api/{API_VERSION}"


@app.route("/")
def home():
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM imoveis;")
    count = cursor.fetchone()[0]
    return jsonify(
        {
            "message": "API is running",
            "version": API_VERSION,
            "imoveis_count": count,
            "_links": {
                "self": url_for("home", _external=True),
                "imoveis": url_for("get_imoveis", _external=True),
                "docs": url_for("api_docs", _external=True),
            },
        }
    )


@app.route(f"{BASE_URL}/docs")
def api_docs():
    """Documentação da API"""
    return jsonify(
        {
            "title": "API Imóveis",
            "version": API_VERSION,
            "description": "API RESTful para gerenciamento de imóveis",
            "endpoints": {
                "GET /api/v1/imoveis": "Lista todos os imóveis com paginação e filtros",
                "GET /api/v1/imoveis/{id}": "Busca um imóvel específico",
                "POST /api/v1/imoveis": "Cria um novo imóvel",
                "PUT /api/v1/imoveis/{id}": "Atualiza um imóvel existente",
                "DELETE /api/v1/imoveis/{id}": "Remove um imóvel",
            },
            "query_parameters": {
                "page": "Número da página (padrão: 1)",
                "per_page": "Itens por página (padrão: 10, máximo: 100)",
                "tipo": "Filtrar por tipo de imóvel",
                "cidade": "Filtrar por cidade",
                "sort": "Campo para ordenação (id, valor, data_aquisicao)",
                "order": "Direção da ordenação (asc, desc)",
            },
        }
    )


@app.route(f"{BASE_URL}/imoveis", methods=["GET"])
def get_imoveis():
    """
    Lista todos os imóveis com paginação, filtros e ordenação.
    Ex:
        /api/v1/imoveis?tipo=casa&page=1&per_page=10
        /api/v1/imoveis?cidade=São Paulo&sort=valor&order=desc
    """
    # Parâmetros de paginação
    page = int(request.args.get("page", 1))
    per_page = min(int(request.args.get("per_page", 10)), 100)  # Máximo 100 por página

    # Parâmetros de filtro
    tipo = request.args.get("tipo")
    cidade = request.args.get("cidade")

    # Parâmetros de ordenação
    sort = request.args.get("sort", "id")
    order = request.args.get("order", "asc")

    # Validar campos de ordenação
    valid_sort_fields = ["id", "valor", "data_aquisicao", "cidade", "tipo"]
    if sort not in valid_sort_fields:
        return jsonify(
            {
                "error": f"Campo de ordenação inválido. Use: {', '.join(valid_sort_fields)}"
            }
        ), 400

    if order not in ["asc", "desc"]:
        return jsonify(
            {"error": "Direção de ordenação inválida. Use: asc ou desc"}
        ), 400

    cursor = conn.cursor(dictionary=True)

    # Construir query base
    where_conditions = []
    params = []

    if tipo:
        where_conditions.append("LOWER(tipo) = LOWER(%s)")
        params.append(tipo)

    if cidade:
        where_conditions.append("cidade = %s")
        params.append(cidade)

    where_clause = (
        " WHERE " + " AND ".join(where_conditions) if where_conditions else ""
    )

    # Contar total de registros
    count_query = f"SELECT COUNT(*) as total FROM imoveis{where_clause}"
    cursor.execute(count_query, params)
    total = cursor.fetchone()["total"]

    # Calcular paginação
    total_pages = math.ceil(total / per_page)
    offset = (page - 1) * per_page

    # Query principal com paginação e ordenação
    query = f"""
    SELECT * FROM imoveis{where_clause}
    ORDER BY {sort} {order.upper()}
    LIMIT %s OFFSET %s
    """
    cursor.execute(query, params + [per_page, offset])
    imoveis = cursor.fetchall()

    # Adicionar links HATEOAS
    for imovel in imoveis:
        imovel["_links"] = {
            "self": url_for("get_imovel", id=imovel["id"], _external=True),
            "update": url_for("update_imovel", id=imovel["id"], _external=True),
            "delete": url_for("delete_imovel", id=imovel["id"], _external=True),
        }

    # Resposta com metadados de paginação
    response = {
        "data": imoveis,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_prev": page > 1,
        },
        "_links": {
            "self": url_for("get_imoveis", _external=True, **request.args),
            "first": url_for(
                "get_imoveis",
                _external=True,
                page=1,
                **{k: v for k, v in request.args.items() if k != "page"},
            ),
            "last": url_for(
                "get_imoveis",
                _external=True,
                page=total_pages,
                **{k: v for k, v in request.args.items() if k != "page"},
            )
            if total_pages > 0
            else None,
            "next": url_for(
                "get_imoveis",
                _external=True,
                page=page + 1,
                **{k: v for k, v in request.args.items() if k != "page"},
            )
            if page < total_pages
            else None,
            "prev": url_for(
                "get_imoveis",
                _external=True,
                page=page - 1,
                **{k: v for k, v in request.args.items() if k != "page"},
            )
            if page > 1
            else None,
        },
    }

    return jsonify(response)


@app.route(f"{BASE_URL}/imoveis/<int:id>", methods=["GET"])
def get_imovel(id):
    """Lista um imóvel específico pelo ID"""
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM imoveis WHERE id = %s;", (id,))
    imovel = cursor.fetchone()
    if imovel:
        imovel["_links"] = {
            "self": url_for("get_imovel", id=id, _external=True),
            "update": url_for("update_imovel", id=id, _external=True),
            "delete": url_for("delete_imovel", id=id, _external=True),
        }
        return jsonify(imovel)
    return jsonify({"error": "Imóvel não encontrado"}), 404


@app.route(f"{BASE_URL}/imoveis", methods=["POST"])
def add_imovel():
    """Adiciona um novo imóvel"""
    data = request.get_json()

    # Validação de campos obrigatórios
    required_fields = ["logradouro", "cidade", "tipo", "valor"]
    missing_fields = [field for field in required_fields if not data.get(field)]

    if missing_fields:
        return jsonify(
            {
                "error": "Campos obrigatórios ausentes",
                "missing_fields": missing_fields,
                "required_fields": required_fields,
            }
        ), 400

    # Validação de tipos de dados
    try:
        valor = float(data.get("valor"))
        if valor < 0:
            return jsonify({"error": "Valor deve ser positivo"}), 400
    except (ValueError, TypeError):
        return jsonify({"error": "Valor deve ser um número válido"}), 400

    cursor = conn.cursor()
    sql = """
    INSERT INTO imoveis (logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """
    values = (
        data.get("logradouro"),
        data.get("tipo_logradouro"),
        data.get("bairro"),
        data.get("cidade"),
        data.get("cep"),
        data.get("tipo"),
        valor,
        data.get("data_aquisicao"),
    )

    cursor.execute(sql, values)
    conn.commit()
    new_id = cursor.lastrowid
    return jsonify(
        {
            "message": "Imóvel adicionado com sucesso",
            "id": new_id,
            "_links": {
                "self": url_for("get_imovel", id=new_id, _external=True),
                "update": url_for("update_imovel", id=new_id, _external=True),
                "delete": url_for("delete_imovel", id=new_id, _external=True),
            },
        }
    ), 201


@app.route(f"{BASE_URL}/imoveis/<int:id>", methods=["PUT"])
def update_imovel(id):
    """Atualiza um imóvel existente"""
    data = request.get_json()

    # Validação de valor se fornecido
    if "valor" in data:
        try:
            valor = float(data.get("valor"))
            if valor < 0:
                return jsonify({"error": "Valor deve ser positivo"}), 400
        except (ValueError, TypeError):
            return jsonify({"error": "Valor deve ser um número válido"}), 400

    cursor = conn.cursor()
    sql = """
    UPDATE imoveis
    SET logradouro = %s, tipo_logradouro = %s, bairro = %s, cidade = %s, cep = %s, tipo = %s, valor = %s, data_aquisicao = %s
    WHERE id = %s;
    """
    values = (
        data.get("logradouro"),
        data.get("tipo_logradouro"),
        data.get("bairro"),
        data.get("cidade"),
        data.get("cep"),
        data.get("tipo"),
        data.get("valor"),
        data.get("data_aquisicao"),
        id,
    )
    cursor.execute(sql, values)
    conn.commit()
    if cursor.rowcount:
        return jsonify(
            {
                "message": "Imóvel atualizado com sucesso",
                "_links": {
                    "self": url_for("get_imovel", id=id, _external=True),
                    "update": url_for("update_imovel", id=id, _external=True),
                    "delete": url_for("delete_imovel", id=id, _external=True),
                },
            }
        ), 200
    return jsonify({"error": "Imóvel não encontrado"}), 404


@app.route(f"{BASE_URL}/imoveis/<int:id>", methods=["DELETE"])
def delete_imovel(id):
    """Remove um imóvel existente"""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM imoveis WHERE id = %s;", (id,))
    conn.commit()
    if cursor.rowcount:
        return "", 204
    return jsonify({"error": "Imóvel não encontrado"}), 404


if __name__ == "__main__":
    app.run(debug=True)
