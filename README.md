# 🛒 Loja Online em Flask

Este é um projeto de loja virtual desenvolvido em **Python + Flask**, com sistema de carrinho, checkout, login, cadastro e detecção automática de bandeira do cartão.

O objetivo é oferecer uma estrutura simples e funcional para estudos ou pequenos projetos.

---

## 🚀 Tecnologias utilizadas

- Python 3
- Flask
- Flask SQLAlchemy
- HTML + CSS
- JavaScript
- Banco SQLite (`loja.db`)

---

## 📁 Estrutura do projeto

---

## ⚙️ Como rodar o projeto localmente

### 1. Instale as dependências:
pip install -r requirements.txt

### 2. Execute o servidor Flask:
python app.py

### 3. Acesse no navegador:
http://127.0.0.1:5000 (127.0.0.1 in Bing)

---

## 🌐 Como hospedar no Render

1. Crie um repositório no GitHub  
2. Envie todos os arquivos do projeto  
3. No Render, crie um **Web Service**  
4. Configure:

**Build Command:**
pip install -r requirements.txt

**Start Command:**
gunicorn app:app

5. Aguarde o deploy  
6. O Render vai gerar um link como:

https://seuloja.onrender.com
---

## 🔐 Login e Cadastro

O sistema permite:

- Criar conta  
- Fazer login  
- Manter sessão ativa  
- Finalizar compra  

Os dados são armazenados no banco SQLite (`loja.db`).

---

## 💳 Detecção de bandeira do cartão

O checkout identifica automaticamente:

- Visa  
- Mastercard  
- Nubank  
- Itaú  
- Caixa  
- Santander  
- Mercado Pago  
- Desconhecido  

As imagens ficam em:
static/img/bandeiras/

---

## 📦 Funcionalidades principais

- Listagem de produtos  
- Carrinho de compras  
- Remoção de itens  
- Cálculo automático do total  
- Checkout completo  
- Pagamento com cartão (simulado)  
- Pagamento via Pix (simulado)  
- Login e cadastro  
- Layout responsivo  

---

## 👨‍💻 Autor

Projeto desenvolvido por **Gustavo**.

---

## 📜 Licença

Uso livre para estudos e projetos pessoais.
