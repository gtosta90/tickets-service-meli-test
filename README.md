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

PostgreSQL: Sistema de gerenciamento de banco de dados para armazenar e consultar dados dos tickets.

Keycloak: Sistema de autenticação e autorização.


# Estrutura do Projeto

./: Contém todos arquivos de configuração do projeto bem o arquivo manage.py responsável pela inicialização da aplicação.

src/: Contém a estrutura principal de código fonte do projeto.

src/django_project: Contém a estrutura principal da camada de Adapters, os projetos Django e arquivos de configuração dos mesmos, cada entidade do sistema possui um projeto próprio. Possui arquivos de testes unitários e de integração.

src/core: Contém toda a estrtura de Entidades e Casos de Uso totalmente desacoplada da camada de Adapters. Possui arquivos de testes unitários e de integração.

# Instalação do ambiente de Desenvolvimento

Instalar a docker engine na sua máquina:
https://docs.docker.com/engine/install/


Clone o repositório:

```bash
git clone https://github.com/gtosta90/tickets-service-meli-test/
```

Navegue até o diretório do projeto:

```bash
cd {your-workspace}/tickets-service-meli-test/
```

Execute o Docker Compose para criar os conteineres do ambiente de Dev completo:
OBS: Verifique o apontamento dos volumes do Postgres e do Keycloak no arquivo docker-compose.yml, altere caso necessário. 

```bash
docker-compose up -d --build
```

Entre no Container tickets-service

```bash
docker exec -it tickets-service bash
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

Na raiz do projeto (pelo próprio VSCode) crie um arquivo .env e insira os dados a seguir:

```bash
DB_ENGINE="django.db.backends.postgresql"
DB_NAME="tickets_db"
DB_USER="postgres"
DB_PASSWORD="postgres"
DB_HOST="postgres"
DB_PORT=5432


AUTH_PUBLIC_KEY=""
```

Configure o banco de dados e aplique as migrações:

```bash
python manage.py makemigrations
```

```bash
python manage.py migrate
```

Inicie o servidor:

```bash
python manage.py runserver 0.0.0.0:8000
```
O Docker Compose sobe uma instância de Keycloak local, a mesma não estará configurada na primeira execução, será preciso configurar um realm, criar um user e um client, visite o site do keycloak para obter ajuda: https://www.keycloak.org/getting-started/getting-started-docker

Caso haja uma intância de Keycloak de uso geral em abiente de desenvolvimento basta configurar o parâmetro AUTH_PUBLIC_KEY em sua .env.

As configurações são necessárias apenas na primeira execução. Ao finalizar você terá 3 contêineres rodando o Postgres, Keycloack e a API Tickets-Service.

Os volumes estão mapeados na sua máquina localmente, isso quer dizer que alterações não serão perdidas caso os contêineres sejam destruídos.

Repare que não é necessário instalar o pyhon localmente, a única instalação necessária foi o docker engine, isso se dá pois a aplicação Tickets-Service está com todo seu conteúdo mapeado como volume, isso quer dizer que todas as alterações efetuadas no código serão compartilhadas com o contêiner e você poderá seguir o desenvolvimento sem maiores problemas e garantindo que o ambiente será exatamente o mesmo em todos os contextos da aplicação.       

# Ambiente de Produção

A imagem de ambiente produtivo será construída pelo arquivo Dockerfile.prod e executado o deploy via GitHub Actions após commit executado na branch master.

## Monitoramento NewRelic

* Latência no tempo de resposta das rotas;
* Latência no tempo de resposta do Potgres;
* Latência no tempo de resposta do serviço de Users -> https://jsonplaceholder.typicode.com/users/;
* Quantidade de erros;
* Taxa média de erros;

## Uso
A API estará disponível em http://localhost:8000. Consulte a documentação da API para explorar os endpoints e obter exemplos de uso.

## Documentações:
http://localhost:8000/swagger/
http://localhost:8000/redoc/


## Contato
Para dúvidas e suporte, entre em contato com gabriel.tosta90@gmail.com.
