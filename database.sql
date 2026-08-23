CREATE DATABASE IF NOT EXISTS projeto_integrador;

USE projeto_integrador;


-- =====================================================
-- TABELA DE CLIENTES
-- HU01 - Cadastro de Cliente
-- HU02 - Autenticação de Usuário
-- =====================================================

CREATE TABLE IF NOT EXISTS clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    telefone VARCHAR(20),
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP
);


-- =====================================================
-- TABELA DE ADMINISTRADORES
-- HU12 - Cadastro de Produtos
-- HU13 - Controle de Estoque
-- HU14 - Relatórios
-- =====================================================

CREATE TABLE IF NOT EXISTS administradores (
    id_admin INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL
);


-- =====================================================
-- TABELA DE PRODUTOS
-- HU04 - Visualizar Cardápio
-- HU05 - Filtrar Produtos
-- HU12 - Cadastro de Produtos
-- HU13 - Controle de Estoque
-- =====================================================

CREATE TABLE IF NOT EXISTS produtos (
    id_produto INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(255),
    sabor VARCHAR(100),
    preco DECIMAL(10,2) NOT NULL,
    imagem VARCHAR(255),
    estoque INT NOT NULL DEFAULT 0,
    ativo BOOLEAN DEFAULT TRUE,
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP
);


-- =====================================================
-- TABELA DE CARRINHO
-- HU06 - Adicionar ao Carrinho
-- HU07 - Remover do Carrinho
-- =====================================================

CREATE TABLE IF NOT EXISTS carrinhos (
    id_carrinho INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (id_cliente)
        REFERENCES clientes(id_cliente)
        ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS itens_carrinho (
    id_item_carrinho INT AUTO_INCREMENT PRIMARY KEY,
    id_carrinho INT NOT NULL,
    id_produto INT NOT NULL,
    quantidade INT NOT NULL DEFAULT 1,

    FOREIGN KEY (id_carrinho)
        REFERENCES carrinhos(id_carrinho)
        ON DELETE CASCADE,

    FOREIGN KEY (id_produto)
        REFERENCES produtos(id_produto)
);


-- =====================================================
-- TABELA DE CUPONS
-- HU15 - Aplicação de Cupom de Desconto
-- =====================================================

CREATE TABLE IF NOT EXISTS cupons (
    id_cupom INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(50) NOT NULL UNIQUE,
    percentual_desconto DECIMAL(5,2) NOT NULL,
    data_validade DATE NOT NULL,
    limite_utilizacao INT,
    quantidade_utilizada INT DEFAULT 0,
    ativo BOOLEAN DEFAULT TRUE
);


-- =====================================================
-- TABELA DE PEDIDOS
-- HU08 - Finalizar Pedido
-- HU10 - Acompanhamento de Pedido
-- =====================================================

CREATE TABLE IF NOT EXISTS pedidos (
    id_pedido INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    id_cupom INT NULL,

    valor_total DECIMAL(10,2) NOT NULL,

    status_pedido ENUM(
        'Em preparo',
        'Em rota de entrega',
        'Entregue'
    ) DEFAULT 'Em preparo',

    data_pedido DATETIME DEFAULT CURRENT_TIMESTAMP,
    previsao_entrega DATETIME NULL,

    FOREIGN KEY (id_cliente)
        REFERENCES clientes(id_cliente),

    FOREIGN KEY (id_cupom)
        REFERENCES cupons(id_cupom)
);


-- =====================================================
-- ITENS DO PEDIDO
-- =====================================================

CREATE TABLE IF NOT EXISTS itens_pedido (
    id_item_pedido INT AUTO_INCREMENT PRIMARY KEY,
    id_pedido INT NOT NULL,
    id_produto INT NOT NULL,
    quantidade INT NOT NULL,
    preco_unitario DECIMAL(10,2) NOT NULL,

    FOREIGN KEY (id_pedido)
        REFERENCES pedidos(id_pedido)
        ON DELETE CASCADE,

    FOREIGN KEY (id_produto)
        REFERENCES produtos(id_produto)
);


-- =====================================================
-- PAGAMENTOS
-- HU09 - Seleção de Forma de Pagamento
-- =====================================================

CREATE TABLE IF NOT EXISTS pagamentos (
    id_pagamento INT AUTO_INCREMENT PRIMARY KEY,
    id_pedido INT NOT NULL,

    forma_pagamento ENUM(
        'Cartão',
        'Pix',
        'Dinheiro'
    ) NOT NULL,

    status_pagamento ENUM(
        'Pendente',
        'Aprovado',
        'Recusado'
    ) DEFAULT 'Pendente',

    data_pagamento DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (id_pedido)
        REFERENCES pedidos(id_pedido)
        ON DELETE CASCADE
);


-- =====================================================
-- AVALIAÇÕES
-- HU11 - Avaliação de Produto
-- =====================================================

CREATE TABLE IF NOT EXISTS avaliacoes (
    id_avaliacao INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    id_produto INT NOT NULL,
    id_pedido INT NOT NULL,

    nota INT NOT NULL,
    comentario VARCHAR(500),

    data_avaliacao DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (id_cliente)
        REFERENCES clientes(id_cliente),

    FOREIGN KEY (id_produto)
        REFERENCES produtos(id_produto),

    FOREIGN KEY (id_pedido)
        REFERENCES pedidos(id_pedido),

    CHECK (nota BETWEEN 1 AND 5)
);


-- =====================================================
-- RECUPERAÇÃO DE SENHA
-- HU03 - Recuperação de Senha
-- =====================================================

CREATE TABLE IF NOT EXISTS recuperacoes_senha (
    id_recuperacao INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    token VARCHAR(255) NOT NULL,
    data_expiracao DATETIME NOT NULL,
    utilizado BOOLEAN DEFAULT FALSE,

    FOREIGN KEY (id_cliente)
        REFERENCES clientes(id_cliente)
        ON DELETE CASCADE
);


-- =====================================================
-- PRODUTOS INICIAIS PARA O CARDÁPIO
-- =====================================================

INSERT INTO produtos
    (nome, descricao, sabor, preco, estoque)
VALUES
    (
        'Cupcake de Chocolate',
        'Cupcake de chocolate com cobertura cremosa',
        'Chocolate',
        8.50,
        20
    ),
    (
        'Cupcake de Morango',
        'Cupcake de baunilha com cobertura de morango',
        'Morango',
        9.00,
        20
    ),
    (
        'Cupcake de Baunilha',
        'Cupcake tradicional com cobertura de baunilha',
        'Baunilha',
        8.00,
        20
    ),
    (
        'Cupcake Red Velvet',
        'Cupcake red velvet com cobertura de cream cheese',
        'Red Velvet',
        10.00,
        15
    );