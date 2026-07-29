# Django CRM

Projeto CRM simples em Django para gerenciar utilizadores, contactos, interações, tarefas e oportunidades.

## Autor

- João Salvador Paulo

## Descrição

Aplicação web desenvolvida em Django com painel administrativo, autenticação, relatórios em PDF e suporte a português e inglês. O projeto segue os princípios do padrão MVT, separação de responsabilidades e busca reduzir duplicação de código (DRY).

## Funcionalidades principais

- Autenticação de utilizadores: login, logout, registo e edição de perfil
- Gestão de utilizadores: listagem, edição, eliminação e geração de PDF
- Gestão de contactos: criação, listagem, edição, visualização, eliminação e PDF por contacto
- Gestão de interações: listagem, criação, actualização, eliminação e exportação em PDF
- Gestão de tarefas: listagem, criação, actualização, eliminação e exportação em PDF
- Gestão de oportunidades: listagem, kanban, criação, actualização, eliminação, alteração de fase e PDF
- Suporte a internacionalização: `pt` / `en`
- Utilização de templates com Bootstrap 5 e Crispy Forms

## Requisitos funcionais

- O sistema deve permitir registo e autenticação de utilizadores
- Utilizadores autenticados devem poder gerir contactos, interações, tarefas e oportunidades
- Deve ser possível gerar relatórios em PDF para utilizadores, contactos, interações, tarefas e oportunidades
- Deve existir uma vista de perfil com estatísticas do utilizador autenticado
- As rotas devem estar organizadas por apps (`accounts`, `contacts`, `interations`, `task`, `opportunities`, `dashboard`)

## Requisitos não funcionais

- Utilizar Python 3.12+ e Django 6.x
- Banco de dados SQLite para desenvolvimento local
- Separação de responsabilidades entre modelos, views, forms e templates
- UI responsiva com Bootstrap 5 e templates reutilizáveis
- Código organizado para facilitar manutenção e testes unitários
- Configuração local simples via `manage.py`

## Tecnologias e dependências

- Python 3.12+
- Django 6.0.4+
- django-crispy-forms
- crispy-bootstrap5
- django-filter
- fpdf
- pillow
- pandas
- python-decouple
- django-rich
- django-rql
- djangorestframework
- djangorestframework-simplejwt
- drf-spectacular

## Instalação

Recomenda-se usar um ambiente virtual.

Usando `venv` e `pip`:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Se usar o utilitário `uv`:

```bash
uv venv
source .venv/bin/activate
uv sync
```

## Configuração e execução

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Rotas principais

- `GET /accounts/list/`
- `GET /accounts/register/`
- `GET /accounts/login/`
- `GET /accounts/logout/`
- `GET /accounts/profile/`
- `GET /accounts/profile/edit/`
- `GET /contacts/list/`
- `GET /contacts/add/`
- `GET /contacts/retrieve/<id>/`
- `GET /contacts/update/<id>/`
- `GET /contacts/delete/<id>/`
- `GET /contacts/pdf/`
- `GET /interactions/list/`
- `GET /interactions/post/`
- `GET /interactions/retrieve/<id>/`
- `GET /interactions/put/<id>/`
- `GET /interactions/delete/<id>/`
- `GET /interactions/pdf/`
- `GET /task/list/`
- `GET /task/post/`
- `GET /task/retrieve/<id>/`
- `GET /task/put/<id>/`
- `GET /task/delete/<id>/`
- `GET /task/pdf/`
- `GET /opportunities/list/`
- `GET /opportunities/kanban/`
- `GET /opportunities/post/`
- `GET /opportunities/retrieve/<id>/`
- `GET /opportunities/put/<id>/`
- `GET /opportunities/delete/<id>/`
- `GET /opportunities/update-stage/<id>/`
- `GET /opportunities/pdf/`
- `GET /dashboard/home/`
- `GET /dashboard/sobre/`

> Nota: O projeto usa rotas internacionais com prefixos como `/pt/` e `/en/` quando a internacionalização está activa.

## Considerações de arquitetura

- MVT: models, views e templates separados por app
- DRY: reutilização de formulários, templates e componentes de interface
- Separação de concerns: cada app trata de uma área do domínio (contas, contactos, interacções, tarefas, oportunidades, dashboard)

## Licença

Consulte o ficheiro `LICENSE` no repositório.
