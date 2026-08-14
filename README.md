# Projeto Integrador - Sistema de Gerenciamento de Clientes

Projeto desenvolvido como aplicação prática de conceitos de desenvolvimento web, programação em Python e banco de dados.

O sistema permite realizar o gerenciamento de clientes por meio de uma interface web integrada a um banco de dados MySQL.

## Funcionalidades

O sistema possui as operações de CRUD:

- Cadastrar clientes
- Listar clientes cadastrados
- Atualizar dados de clientes
- Excluir clientes
- Validar e-mails duplicados
- Confirmar exclusão antes de remover um cliente
- Exibir mensagens de sucesso e erro

## Tecnologias Utilizadas

- Python
- Flask
- MySQL
- HTML5
- CSS3
- JavaScript
- Jinja2
- MySQL Connector/Python
- python-dotenv

## Estrutura do Projeto

```text
projeto_integrador/
│
├── static/
│   ├── script.js
│   └── style.css
│
├── templates/
│   ├── editar.html
│   └── index.html
│
├── app.py
├── app_terminal.py
├── database.sql
├── requirements.txt
├── .gitignore
├── .env
└── README.md
```

## Banco de Dados

O projeto utiliza o MySQL.

O arquivo `database.sql` contém os comandos necessários para criar o banco de dados e a tabela de clientes.

Banco:

```text
projeto_integrador
```

Tabela:

```text
clientes
```

## Instalação das Dependências

Com o ambiente virtual ativado, execute:

```bash
pip install -r requirements.txt
```

## Configuração

Crie um arquivo `.env` na raiz do projeto e informe a senha do MySQL:

```text
MYSQL_PASSWORD=sua_senha_do_mysql
```

O arquivo `.env` não deve ser enviado para repositórios públicos.

## Executando o Projeto

Execute:

```bash
python app.py
```

Depois acesse no navegador:

```text
http://127.0.0.1:5000
```

## Operações CRUD

**Create:** cadastro de novos clientes.

**Read:** visualização dos clientes cadastrados.

**Update:** edição dos dados de um cliente.

**Delete:** exclusão de clientes com confirmação antes da remoção.

## Segurança

As credenciais sensíveis do banco de dados são armazenadas em variável de ambiente utilizando `python-dotenv`.

O arquivo `.env` é ignorado pelo Git por meio do `.gitignore`.

## Autora

Fernanda Silva

Curso: Sistemas de Informação