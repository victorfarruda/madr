# Projeto final do curso de FastAPI do Dunossauro 
[Link do teste](https://fastapidozero.dunossauro.com/14/)

Este serviço é responsável por gerenciar livros e fazer o relacionamento com seus autores.


### Clone o Repositório:
```shell script
git clone git@github.com:victorfarruda/madr.git
```

### Configurando projeto

#### Dependências

1. [Install docker](https://docs.docker.com/get-started/get-docker//)
2. [Install docker-compose](https://docs.docker.com/compose/install/)

Entre na pasta do projeto:
```shell script
cd madr/
```
Agora vamos buildar o projeto:
```shell script
docker build . -t madr
ou
docker-compose build
```

Você pode rodar o projeto:
```shell script
docker-compose up -d madr
```

O projeto está rodando em:
```shell script
http://127.0.0.1:8000
```

Dê uma olhada nos endpoints em:
```shell script
http://127.0.0.1:8000/docs/
http://127.0.0.1:8000/redoc/
```


Para rodar os testes utilizando testcontainers você pode usar os comandos 
(não se esqueça de copiar o env-sample para um arquivo .env):
```shell script
uv sync
uv run task test
```
