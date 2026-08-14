import mysql.connector


def conectar_banco():
    conexao = mysql.connector.connect(
        host= "localhost",
        user= "root",
        password= "Meliflua@2605",
        database= "projeto_integrador"
    )

    return conexao


def cadastrar_cliente(nome, email, senha, telefone):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    sql = """
    INSERT INTO clientes (nome, email, senha, telefone)
    VALUES (%s, %s, %s, %s)
    """

    valores = (nome, email, senha, telefone)

    try:
        cursor.execute(sql, valores)
        linhas_afetadas = cursor.rowcount

        conexao.commit()
        cursor.close()
        conexao.close()

        return linhas_afetadas

    except mysql.connector.IntegrityError:
        print("Erro: este e-mail já está cadastrado.")

        cursor.close()
        conexao.close()

        return 0


def listar_clientes():
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM clientes")

    clientes = cursor.fetchall()

    for cliente in clientes:
        print(
            f"ID: {cliente[0]} | "
            f"Nome: {cliente[1]} | "
            f"E-mail: {cliente[2]} | "
            f"Telefone: {cliente[4]}"
        )

    cursor.close()
    conexao.close()


def atualizar_cliente(
    id_cliente,
    novo_nome,
    novo_email,
    nova_senha,
    novo_telefone
):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    sql = """
    UPDATE clientes
    SET nome = %s, email = %s, senha = %s, telefone = %s
    WHERE id_cliente = %s
    """

    valores = (
        novo_nome,
        novo_email,
        nova_senha,
        novo_telefone,
        id_cliente
    )

    cursor.execute(sql, valores)
    linhas_afetadas = cursor.rowcount

    conexao.commit()
    cursor.close()
    conexao.close()

    return linhas_afetadas


def excluir_cliente(id_cliente):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    sql = "DELETE FROM clientes WHERE id_cliente = %s"

    cursor.execute(sql, (id_cliente,))
    linhas_afetadas = cursor.rowcount

    conexao.commit()
    cursor.close()
    conexao.close()

    return linhas_afetadas


while True:
    print("===== PROJETO INTEGRADOR =====")
    print("1 - Cadastrar cliente")
    print("2 - Listar clientes")
    print("3 - Atualizar cliente")
    print("4 - Excluir cliente")
    print("5 - Sair")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        nome = input("Digite o nome: ")
        email = input("Digite o e-mail: ")
        senha = input("Digite a senha: ")
        telefone = input("Digite o telefone: ")

        if nome == "" or email == "" or senha == "" or telefone == "":
            print("Erro: todos os campos são obrigatórios.")
            continue

        if "@" not in email or "." not in email:
            print("Erro: e-mail inválido.")
            continue

        linhas_afetadas = cadastrar_cliente(
            nome,
            email,
            senha,
            telefone
        )

        if linhas_afetadas > 0:
            print("Cliente cadastrado com sucesso!")
        else:
            print("Não foi possível cadastrar o cliente.")

    elif opcao == "2":
        print("\n--- CLIENTES CADASTRADOS ---")
        listar_clientes()

    elif opcao == "3":
        id_cliente = input("Digite o ID do cliente: ")
        novo_nome = input("Digite o novo nome: ")
        novo_email = input("Digite o novo e-mail: ")
        nova_senha = input("Digite a nova senha: ")
        novo_telefone = input("Digite o novo telefone: ")

        linhas_afetadas = atualizar_cliente(
            id_cliente,
            novo_nome,
            novo_email,
            nova_senha,
            novo_telefone
        )

        if linhas_afetadas > 0:
            print("Cliente atualizado com sucesso!")
        else:
            print("Cliente não encontrado.")

    elif opcao == "4":
        id_cliente = input(
            "Digite o ID do cliente que deseja excluir: "
        )

        confirmacao = input(
            "Tem certeza que deseja excluir este cliente? (s/n): "
        )
        if confirmacao.lower() not in ["s", "n"]:
             print("Opção inválida. Digite apenas s ou n.")
             continue

        if confirmacao.lower() == "s":
            linhas_afetadas = excluir_cliente(id_cliente)

            if linhas_afetadas > 0:
                print("Cliente excluído com sucesso!")
            else:
                print("Cliente não encontrado.")

        else:
            print("Exclusão cancelada.")

    elif opcao == "5":
        print("Programa encerrado.")
        break

    else:
        print("Opção inválida. Tente novamente.")
