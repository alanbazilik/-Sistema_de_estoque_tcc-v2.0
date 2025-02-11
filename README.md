﻿# -Sistema_de_estoque_tcc-v2.0
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Cadastro de Produtos - Sistema de Estoque

Este é um sistema simples para cadastro, alteração, deleção e leitura de produtos em estoque, utilizando Python, CustomTkinter para a interface gráfica, OpenCV para o scanner de código de barras e PostgreSQL como banco de dados.

## Funcionalidades

- **Cadastro de Produtos**: Permite adicionar novos produtos com descrição, quantidade, valor e código de barras.
- **Alteração de Produtos**: Permite alterar as informações de um produto já cadastrado.
- **Deletar de Produtos**: Permite remover um produto do estoque.
- **Scanner de Código de Barras**: Usa a câmera do celular (via DroidCam) para escanear códigos de barras e verificar se o produto já está cadastrado no banco de dados.
- **Tabela de Produtos**: Exibe uma tabela com todos os produtos cadastrados, com possibilidade de editar ou deletar produtos ao clicar na linha correspondente.

## Tecnologias Utilizadas

- **Python**: Linguagem de programação principal.
- **CustomTkinter**: Biblioteca para criar interfaces gráficas modernas e customizáveis.
- **OpenCV**: Usado para capturar o vídeo da câmera e decodificar os códigos de barras.
- **pyzbar**: Biblioteca para ler e decodificar códigos de barras.
- **PostgreSQL**: Banco de dados relacional para armazenar as informações dos produtos.

## Como Executar

### Requisitos

- Python 3.x
- Bibliotecas Python:
  - `customtkinter`
  - `opencv-python`
  - `pyzbar`
  - `psycopg2`
  - `tkinter` (já incluída no Python)
  - `ttk` (já incluída no Python)

### Instalação das Dependências

Instale as dependências necessárias utilizando o `pip`:

```bash
pip install customtkinter opencv-python pyzbar psycopg2
