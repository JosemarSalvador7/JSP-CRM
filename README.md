# Django CRM

Este projeto é um CRM simples desenvolvido com Django para gerenciar contatos, usuários e operações básicas de um painel administrativo.

## Funcionalidades

- Autenticação de usuários com login, logout e cadastro
- Gestão de contatos com cadastro, listagem e exclusão
- Filtros e contagem de contatos por status e presença de e-mail/empresa
- Interface com Bootstrap e Font Awesome
- Suporte básico a internacionalização

## Tecnologias

- Python 3.12+
- Django 6+
- Django Crispy Forms
- Django Filter
- FPDF
- Pillow
- pandas

## Instalação com UV

1. Crie e ative o ambiente virtual com UV:
   ```bash
   uv venv
   source .venv/bin/activate
   ```

2. Instale as dependências do projeto:
   ```bash
   uv sync
   ```

3. Aplique as migrações:
   ```bash
   uv run python manage.py migrate
   ```

4. Crie um superusuário:
   ```bash
   uv run python manage.py createsuperuser
   ```

5. Inicie o servidor:
   ```bash
   uv run python manage.py runserver
   ```

## Acesso

- Login: http://127.0.0.1:8000/accounts/
- Cadastro: http://127.0.0.1:8000/accounts/register/
- Lista de contatos: http://127.0.0.1:8000/contactos/list/
- Painel: http://127.0.0.1:8000/dashboard/

## Estrutura principal

- accounts: autenticação e perfis de usuários
- contacts: gerenciamento de contatos
- dashboard: páginas principais do painel
- core: configuração do projeto Django

## Observações

O projeto ainda está em evolução e pode ser expandido com novas funcionalidades como tarefas, oportunidades e integração com outros sistemas.
