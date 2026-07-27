# Django CRM

Projeto CRM simples em Django para gerenciar usuários, contactos e recursos básicos de um painel administrativo.

## Funcionalidades

- Autenticação: login, logout e registro
- Gestão de contactos: criar, listar, editar e eliminar
- Gestão de utilizadores: listagem com filtros por username, email, cargo, estado e permissões
- Relatórios em PDF (FPDF)
- Interface com Bootstrap e Font Awesome
- Suporte básico a internacionalização (pt / en)

## Tecnologias

- Python 3.12+
- Django 6+
- django-crispy-forms
- django-filter
- fpdf
- pillow
- pandas

## Instalação

Recomenda-se usar um ambiente virtual. Exemplos com ferramentas comuns:

Usando venv + pip:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Se usa a ferramenta `uv` no seu fluxo (opcional):

```bash
uv venv
source .venv/bin/activate
uv sync
```

## Configuração e execução

```bash
uv run manage.py migrate
uv run manage.py createsuperuser
uv run manage.py runserver
```

## URLs úteis

- Lista de utilizadores: `/accounts/list/`
- Cadastro: `/accounts/register/`
- Login: `/accounts/login/`

## Licença

Consulte o ficheiro `LICENSE` no repositório.
