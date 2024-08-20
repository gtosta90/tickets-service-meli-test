# Sistema de Gerenciamento de Tickets
Descrição
Este projeto é um backend desenvolvido em Python utilizando o Django para criar uma plataforma robusta de gerenciamento de tickets. O sistema oferece uma API poderosa para a criação e gerenciamento de tickets, permitindo que cada ticket seja classificado detalhadamente com informações sobre Categoria, Subcategoria e Severidade. O objetivo é otimizar o rastreamento e a resolução de problemas de forma eficiente e organizada.

# Funcionalidades
Criação de Tickets: Registre novos tickets com informações detalhadas e específicas.

Categoria e Subcategoria: Atribua categoria e subcategoria aos tickets para uma organização mais eficaz.

Severidade: Classifique o nível de gravidade dos tickets para uma melhor priorização.

Consulta e Filtragem: Utilize endpoints da API para buscar tickets por Categoria, Subcategoria, Severidade e outros critérios.

Atualização e Exclusão: Permita a modificação e remoção de tickets conforme necessário.

Usuários: É possível consultar e listar usuários do sistema através das rotas de users.

# Tecnologias Utilizadas
Python: Linguagem principal.

Django: Framework web que proporciona uma base sólida para a criação de APIs e gerenciamento de dados.

Django REST Framework: Biblioteca para facilitar a construção de APIs RESTful.

Pytest: Framework de testes que bibliotecas para a criação de testes untitários e de integração.

PostgreSQL: Sistema de gerenciamento de banco de dados para armazenar e consultar dados dos tickets (ajuste conforme sua escolha).

# Estrutura do Projeto
src/: Contém a estrutura principal de código fonte do projeto.

src/django_project: Contém a estrutura principal da camada de Adapters, os projetos Django e arquivos de configuração dos mesmos, cada entidade do sistema possui um projeto próprio. Possui arquivos de testes unitários e de integração.

src/core: Contém toda a estrtura de Entidades e Casos de Uso totalmente desacoplada da camada de Adapters. Possui arquivos de testes unitários e de integração.

# Instalação

Clone o repositório:

```bash
git clone https://github.com/seuusuario/seuprojeto.git
```
Navegue até o diretório do projeto:

```bash
cd seuprojeto
```
Crie e ative um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```
Instale as dependências:

```bash
pip install -r requirements.txt
```

Configure o banco de dados e aplique as migrações:

```bash
python manage.py migrate
```

Inicie o servidor:

```bash
python manage.py runserver
```

Uso
A API estará disponível em http://localhost:8000. Consulte a documentação da API para explorar os endpoints e obter exemplos de uso.

Documentações:
http://localhost:8000/swagger/
http://localhost:8000/redoc/


Contato
Para dúvidas e suporte, entre em contato com gabriel.tosta90@gmail.com.
