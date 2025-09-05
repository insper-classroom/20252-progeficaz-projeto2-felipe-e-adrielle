from db import get_db_connection

cnx = get_db_connection()
cursor = cnx.cursor()

# SQL para criar a tabela no MySQL
sql_script = """
CREATE TABLE IF NOT EXISTS imoveis (
    id INT AUTO_INCREMENT PRIMARY KEY,
    logradouro VARCHAR(255) NOT NULL,
    tipo_logradouro VARCHAR(255),
    bairro VARCHAR(255),
    cidade VARCHAR(255) NOT NULL,
    cep VARCHAR(20),
    tipo VARCHAR(50),
    valor DECIMAL(10, 2),
    data_aquisicao DATE
);
"""

cursor.execute(sql_script)
cnx.commit()

with open("imoveis.sql", "r") as file:
    cursor.execute(file.read())

cursor.close()
cnx.close()