from flask import Flask, jsonify, request, url_for
from db import get_db_connection

app = Flask(__name__)
conn = get_db_connection()


@app.route("/")
def home():
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM imoveis;")
    count = cursor.fetchone()[0]
    return jsonify({
        "message": "API is running",
        "imoveis_count": count,
        "_links": {
            "self": url_for("home", _external=True),
            "imoveis": url_for("get_imoveis", _external=True)
        }
    })


@app.route("/imoveis", methods=["GET"])
def get_imoveis():
    """
    Lista todos os imóveis ou filtra por tipo ou cidade se parâmetros forem fornecidos.
    Ex:
        /imoveis?tipo=casa
        /imoveis?cidade=São Paulo
    """
    tipo = request.args.get("tipo")
    cidade = request.args.get("cidade")
    cursor = conn.cursor(dictionary=True)

    if tipo:
        cursor.execute("SELECT * FROM imoveis WHERE LOWER(tipo) = LOWER(%s);", (tipo,))
    elif cidade:
        cursor.execute("SELECT * FROM imoveis WHERE cidade = %s;", (cidade,))
    else:
        cursor.execute("SELECT * FROM imoveis;")
    
    imoveis = cursor.fetchall()
    for imovel in imoveis:
        imovel["_links"] = {
            "self": url_for("get_imovel", id=imovel["id"], _external=True),
            "update": url_for("update_imovel", id=imovel["id"], _external=True),
            "delete": url_for("delete_imovel", id=imovel["id"], _external=True)
        }
    return jsonify(imoveis)


@app.route("/imoveis/<int:id>", methods=["GET"])
def get_imovel(id):
    """Lista um imóvel específico pelo ID"""
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM imoveis WHERE id = %s;", (id,))
    imovel = cursor.fetchone()
    if imovel:
        imovel["_links"] = {
            "self": url_for("get_imovel", id=id, _external=True),
            "update": url_for("update_imovel", id=id, _external=True),
            "delete": url_for("delete_imovel", id=id, _external=True)
        }
        return jsonify(imovel)
    return jsonify({"error": "Imóvel não encontrado"}), 404


@app.route("/imoveis", methods=["POST"])
def add_imovel():
    """Adiciona um novo imóvel"""
    data = request.get_json()
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
        data.get("valor"),
        data.get("data_aquisicao")
    )
    
    cursor.execute(sql, values)
    conn.commit()
    new_id = cursor.lastrowid
    return jsonify({
        "message": "Imóvel adicionado com sucesso",
        "id": new_id,
        "_links": {
            "self": url_for("get_imovel", id=new_id, _external=True),
            "update": url_for("update_imovel", id=new_id, _external=True),
            "delete": url_for("delete_imovel", id=new_id, _external=True)
        }
    }), 201


@app.route("/imoveis/<int:id>", methods=["PUT"])
def update_imovel(id):
    """Atualiza um imóvel existente"""
    data = request.get_json()
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
        id
    )
    cursor.execute(sql, values)
    conn.commit()
    if cursor.rowcount:
        return jsonify({
            "message": "Imóvel atualizado com sucesso",
            "_links": {
                "self": url_for("get_imovel", id=id, _external=True),
                "update": url_for("update_imovel", id=id, _external=True),
                "delete": url_for("delete_imovel", id=id, _external=True)
            }
        })
    return jsonify({"error": "Imóvel não encontrado"}), 404


@app.route("/imoveis/<int:id>", methods=["DELETE"])
def delete_imovel(id):
    """Remove um imóvel existente"""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM imoveis WHERE id = %s;", (id,))
    conn.commit()
    if cursor.rowcount:
        return jsonify({"message": "Imóvel deletado com sucesso"})
    return jsonify({"error": "Imóvel não encontrado"}), 404


if __name__ == "__main__":
    app.run(debug=True)
