from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
from mysql.connector import IntegrityError
import os
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "chave-local-desenvolvimento")


def conectar_banco():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        port=int(os.getenv("MYSQL_PORT", 3306)),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE", "projeto_integrador")
    )

@app.route("/")
def inicio():
    return redirect(url_for("login"))

@app.route("/cadastro")
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

    if len(senha) < 6:
       flash("Erro: a senha deve ter no mínimo 6 caracteres.", "erro")
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
        return redirect(url_for("login"))

    except IntegrityError:
        conexao.rollback()
        flash("Erro: este e-mail já está cadastrado.", "erro")
        return redirect(url_for("index"))

    finally:
        cursor.close()
        conexao.close()

    
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        senha = request.form.get("senha", "").strip()

        if email == "" or senha == "":
            flash("Preencha o e-mail e a senha.", "erro")
            return redirect(url_for("login"))

        conexao = conectar_banco()
        cursor = conexao.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT id_cliente, nome, email
            FROM clientes
            WHERE email = %s
              AND senha = %s
            LIMIT 1
            """,
            (email, senha)
        )

        cliente = cursor.fetchone()

        cursor.close()
        conexao.close()

        if cliente:
            session["id_cliente"] = cliente["id_cliente"]
            session["nome_cliente"] = cliente["nome"]

            flash("Login realizado com sucesso!", "success")
            return redirect(url_for("cardapio"))

        flash("E-mail ou senha inválidos.", "erro")
        return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Logout realizado com sucesso!", "success")
    return redirect(url_for("login"))

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

@app.route("/cardapio")
def cardapio():
    if "id_cliente" not in session:
        flash("Faça login para acessar o cardápio.", "error")
        return redirect(url_for("login"))
    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            p.id_produto,
            p.nome,
            p.descricao,
            p.preco,
            p.imagem,
            p.estoque,
            p.ativo,
            c.nome AS categoria
        FROM produtos p
        LEFT JOIN categorias c
            ON p.id_categoria = c.id_categoria
        WHERE p.ativo = TRUE
        AND p.estoque > 0
        ORDER BY c.id_categoria, p.id_produto
    """)

    produtos = cursor.fetchall()

    cursor.close()
    conexao.close()

    return render_template("cardapio.html", produtos=produtos)

@app.route("/adicionar-carrinho/<int:id_produto>", methods=["POST"])
def adicionar_carrinho(id_produto):
    id_cliente = session.get("id_cliente")

    if not id_cliente:
        flash("Faça login para adicionar produtos ao carrinho.", "error")
        return redirect(url_for("login"))

    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT id_carrinho
        FROM carrinhos
        WHERE id_cliente = %s
          AND status = 'Aberto'
        LIMIT 1
        """,
        (id_cliente,)
    )

    carrinho = cursor.fetchone()

    if carrinho:
        id_carrinho = carrinho["id_carrinho"]
    else:
        cursor.execute(
            """
            INSERT INTO carrinhos (id_cliente, status)
            VALUES (%s, 'Aberto')
            """,
            (id_cliente,)
        )

        conexao.commit()
        id_carrinho = cursor.lastrowid

    cursor.execute(
        """
        SELECT id_item_carrinho, quantidade
        FROM itens_carrinho
        WHERE id_carrinho = %s
          AND id_produto = %s
        """,
        (id_carrinho, id_produto)
    )

    item = cursor.fetchone()
    cursor.execute(
        """
        SELECT estoque
        FROM produtos
        WHERE id_produto = %s
        """,
        (id_produto,)
    )

    produto = cursor.fetchone()
    if not produto or produto["estoque"] <= 0:
        cursor.close()
        conexao.close()
        flash("Produto sem estoque!", "error")
        return redirect(url_for("cardapio"))

    if item and item["quantidade"] >= produto["estoque"]:
        cursor.close()
        conexao.close()
        flash("Quantidade máxima disponível em estoque atingida!", "error")
        return redirect(url_for("carrinho"))
    if item:
        cursor.execute(
            """
            UPDATE itens_carrinho
            SET quantidade = quantidade + 1
            WHERE id_item_carrinho = %s
            """,
            (item["id_item_carrinho"],)
        )
    else:
        cursor.execute(
            """
            INSERT INTO itens_carrinho
                (id_carrinho, id_produto, quantidade)
            VALUES (%s, %s, 1)
            """,
            (id_carrinho, id_produto)
        )

    conexao.commit()

    cursor.close()
    conexao.close()

    flash("Produto adicionado ao carrinho!", "success")

    return redirect(url_for("cardapio"))

@app.route("/carrinho")
def carrinho():
    if "id_cliente" not in session:
        flash("Faça login para acessar o carrinho.", "error")
        return redirect(url_for("login"))
    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            ic.id_item_carrinho,
            p.id_produto,
            p.nome,
            p.imagem,
            p.preco,
            ic.quantidade,
            (p.preco * ic.quantidade) AS subtotal
        FROM itens_carrinho ic
        INNER JOIN produtos p
            ON ic.id_produto = p.id_produto
        INNER JOIN carrinhos c
            ON ic.id_carrinho = c.id_carrinho
        WHERE c.id_cliente = %s
          AND c.status = 'Aberto'
        ORDER BY ic.id_item_carrinho
    """, (session["id_cliente"],))

    itens = cursor.fetchall()

    total = sum(item["subtotal"] for item in itens)

    cursor.close()
    conexao.close()

    return render_template(
        "carrinho.html",
        itens=itens,
        total=total
    )

@app.route("/diminuir-carrinho/<int:id_item>", methods=["POST"])
def diminuir_carrinho(id_item):
    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT quantidade
        FROM itens_carrinho
        WHERE id_item_carrinho = %s
        """,
        (id_item,)
    )

    item = cursor.fetchone()

    if item:
        if item["quantidade"] > 1:
            cursor.execute(
                """
                UPDATE itens_carrinho
                SET quantidade = quantidade - 1
                WHERE id_item_carrinho = %s
                """,
                (id_item,)
            )
        else:
            cursor.execute(
                """
                DELETE FROM itens_carrinho
                WHERE id_item_carrinho = %s
                """,
                (id_item,)
            )

        conexao.commit()

    cursor.close()
    conexao.close()

    return redirect(url_for("carrinho"))

@app.route("/aumentar-carrinho/<int:id_item>", methods=["POST"])
def aumentar_carrinho(id_item):
    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            ic.quantidade,
            p.estoque
        FROM itens_carrinho ic
        INNER JOIN produtos p
            ON ic.id_produto = p.id_produto
        WHERE ic.id_item_carrinho = %s
        """,
        (id_item,)
    )

    item = cursor.fetchone()

    if not item:
        cursor.close()
        conexao.close()
        return redirect(url_for("carrinho"))

    if item["quantidade"] >= item["estoque"]:
        cursor.close()
        conexao.close()
        flash("Quantidade máxima disponível em estoque atingida!", "error")
        return redirect(url_for("carrinho"))

    cursor.execute(
        """
        UPDATE itens_carrinho
        SET quantidade = quantidade + 1
        WHERE id_item_carrinho = %s
        """,
        (id_item,)
    )

    conexao.commit()

    cursor.close()
    conexao.close()

    return redirect(url_for("carrinho"))

@app.route("/remover-carrinho/<int:id_item>", methods=["POST"])
def remover_carrinho(id_item):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute(
        """
        DELETE FROM itens_carrinho
        WHERE id_item_carrinho = %s
        """,
        (id_item,)
    )

    conexao.commit()

    cursor.close()
    conexao.close()

    return redirect(url_for("carrinho"))

@app.route("/finalizar-pedido", methods=["POST"])
def finalizar_pedido():
    id_cliente = session.get("id_cliente")

    if not id_cliente:
        flash("Faça login para finalizar o pedido.", "error")
        return redirect(url_for("login"))

    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT id_carrinho
        FROM carrinhos
        WHERE id_cliente = %s
          AND status = 'Aberto'
        LIMIT 1
        """,
        (id_cliente,)
    )

    carrinho = cursor.fetchone()

    if not carrinho:
        cursor.close()
        conexao.close()

        flash("Nenhum carrinho aberto encontrado.", "erro")
        return redirect(url_for("carrinho"))

    id_carrinho = carrinho["id_carrinho"]

    cursor.execute(
        """
        SELECT
            SUM(p.preco * ic.quantidade) AS total
        FROM itens_carrinho ic
        INNER JOIN produtos p
            ON ic.id_produto = p.id_produto
        WHERE ic.id_carrinho = %s
        """,
        (id_carrinho,)
    )

    resultado = cursor.fetchone()
    total = resultado["total"]

    if total is None:
        cursor.close()
        conexao.close()

        flash("O carrinho está vazio.", "erro")
        return redirect(url_for("carrinho"))

    cursor.execute(
        """
        INSERT INTO pedidos
            (id_cliente, status_pedido, valor_total)
        VALUES (%s, 'Em preparo', %s)
        """,
        (id_cliente, total)
    )

    id_pedido = cursor.lastrowid

    cursor.execute(
        """
        INSERT INTO itens_pedido
            (id_pedido, id_produto, quantidade, preco_unitario)
        SELECT
            %s,
            ic.id_produto,
            ic.quantidade,
            p.preco
        FROM itens_carrinho ic
        INNER JOIN produtos p
            ON ic.id_produto = p.id_produto
        WHERE ic.id_carrinho = %s
        """,
        (id_pedido, id_carrinho)
    )

    cursor.execute(
        """
        UPDATE carrinhos
        SET status = 'Finalizado'
        WHERE id_carrinho = %s
        """,
        (id_carrinho,)
    )

    conexao.commit()

    cursor.close()
    conexao.close()

   
    return redirect(url_for("pagamento", id_pedido=id_pedido))

@app.route("/pagamento/<int:id_pedido>", methods=["GET", "POST"])
def pagamento(id_pedido):
    if "id_cliente" not in session:
        flash("Faça login para acessar o pagamento.", "error")
        return redirect(url_for("login"))
    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT id_pedido
        FROM pedidos
        WHERE id_pedido = %s
        AND id_cliente = %s
        LIMIT 1
        """,
        (id_pedido, session["id_cliente"])
    )

    pedido_do_cliente = cursor.fetchone()

    if not pedido_do_cliente:
        cursor.close()
        conexao.close()
        flash("Pedido não encontrado ou não pertence a este cliente.", "error")
        return redirect(url_for("cardapio"))

    cursor.execute(
        """
        SELECT id_pagamento
        FROM pagamentos
        WHERE id_pedido = %s
        LIMIT 1
        """,
        (id_pedido,)
    )

    pagamento_existente = cursor.fetchone()

    if pagamento_existente:
        cursor.close()
        conexao.close()

        flash("Este pedido já foi pago.", "error")
        return redirect(url_for("cardapio"))

    if request.method == "POST":
        forma_pagamento = request.form.get("forma_pagamento")

        
        cursor.execute(
            """
            INSERT INTO pagamentos
                (id_pedido, forma_pagamento, status_pagamento)
            VALUES (%s, %s, 'Aprovado')
            """,
            (id_pedido, forma_pagamento)
        )

        cursor.execute(
            """
            UPDATE pedidos
            SET status_pedido = 'Em preparo'
            WHERE id_pedido = %s
            """,
            (id_pedido,)
        )

        cursor.execute("""UPDATE produtos p INNER JOIN itens_pedido ip ON p.id_produto = ip.id_produto SET p.estoque = p.estoque - ip.quantidade WHERE ip.id_pedido = %s""", (id_pedido,))

        conexao.commit()
                        
    cursor.execute(
        """
       SELECT id_pedido, valor_total
FROM pedidos
WHERE id_pedido = %s
AND id_cliente = %s
""",
(id_pedido, session["id_cliente"])
    )

    pedido = cursor.fetchone()

    cursor.close()
    conexao.close()

    if request.method == "POST":
        return render_template(
            "confirmacao.html",
            pedido=pedido,
            forma_pagamento=forma_pagamento
        )
        
    return render_template("pagamento.html", pedido=pedido)

if __name__ == "__main__":
    app.run(debug=True)