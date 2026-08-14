from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import IntegrityError
import os
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)
app.secret_key = "projeto-integrador"


def conectar_banco():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.getenv("MYSQL_PASSWORD"),
        database="projeto_integrador"
    )


@app.route("/")
def index():
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id_cliente, nome, email, senha, telefone, data_cadastro
        FROM clientes
        ORDER BY id_cliente
    """)

    clientes = cursor.fetchall()

    cursor.close()
    conexao.close()

    return render_template("index.html", clientes=clientes)


@app.route("/cadastrar", methods=["POST"])
def cadastrar():
    nome = request.form["nome"].strip()
    email = request.form["email"].strip()
    senha = request.form["senha"].strip()
    telefone = request.form["telefone"].strip()

    if nome == "" or email == "" or senha == "" or telefone == "":
        flash("Erro: todos os campos são obrigatórios.", "erro")
        return redirect(url_for("index"))

    if "@" not in email or "." not in email:
        flash("Erro: e-mail inválido.", "erro")
        return redirect(url_for("index"))

    conexao = conectar_banco()
    cursor = conexao.cursor()

    try:
        sql = """
        INSERT INTO clientes (nome, email, senha, telefone)
        VALUES (%s, %s, %s, %s)
        """

        valores = (nome, email, senha, telefone)

        cursor.execute(sql, valores)
        conexao.commit()

        flash("Cliente cadastrado com sucesso!", "sucesso")

    except IntegrityError:
        conexao.rollback()
        flash("Erro: este e-mail já está cadastrado.", "erro")

    finally:
        cursor.close()
        conexao.close()

    return redirect(url_for("index"))


@app.route("/editar/<int:id_cliente>", methods=["GET", "POST"])
def editar(id_cliente):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    if request.method == "POST":
        nome = request.form["nome"].strip()
        email = request.form["email"].strip()
        senha = request.form["senha"].strip()
        telefone = request.form["telefone"].strip()

        if nome == "" or email == "" or senha == "" or telefone == "":
            cursor.close()
            conexao.close()

            flash("Erro: todos os campos são obrigatórios.", "erro")
            return redirect(url_for("editar", id_cliente=id_cliente))

        if "@" not in email or "." not in email:
            cursor.close()
            conexao.close()

            flash("Erro: e-mail inválido.", "erro")
            return redirect(url_for("editar", id_cliente=id_cliente))

        try:
            sql = """
            UPDATE clientes
            SET nome = %s,
                email = %s,
                senha = %s,
                telefone = %s
            WHERE id_cliente = %s
            """

            valores = (
                nome,
                email,
                senha,
                telefone,
                id_cliente
            )

            cursor.execute(sql, valores)
            conexao.commit()

            if cursor.rowcount > 0:
                flash("Cliente atualizado com sucesso!", "sucesso")
            else:
                flash("Cliente não encontrado.", "erro")

        except IntegrityError:
            conexao.rollback()
            flash("Erro: este e-mail já está cadastrado.", "erro")

        finally:
            cursor.close()
            conexao.close()

        return redirect(url_for("index"))

    cursor.execute("""
        SELECT id_cliente, nome, email, senha, telefone
        FROM clientes
        WHERE id_cliente = %s
    """, (id_cliente,))

    cliente = cursor.fetchone()

    cursor.close()
    conexao.close()

    if cliente is None:
        flash("Cliente não encontrado.", "erro")
        return redirect(url_for("index"))

    return render_template("editar.html", cliente=cliente)


@app.route("/excluir/<int:id_cliente>", methods=["POST"])
def excluir(id_cliente):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute(
        "DELETE FROM clientes WHERE id_cliente = %s",
        (id_cliente,)
    )

    linhas_afetadas = cursor.rowcount

    conexao.commit()
    cursor.close()
    conexao.close()

    if linhas_afetadas > 0:
        flash("Cliente excluído com sucesso!", "sucesso")
    else:
        flash("Cliente não encontrado.", "erro")

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)