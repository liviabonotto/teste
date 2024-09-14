## Execução do projeto

#### 1. Atualizar credenciais da AWS:

- Certifique-se de que as credenciais da AWS (chave de acesso e chave secreta) estejam atualizadas no arquivo .env. As credenciais devem ter permissões adequadas para acessar o bucket S3 e interagir com outros serviços AWS necessários.

#### 2. Configurar o bucket S3:

- Crie um bucket no Amazon S3 se ainda não existir e anote o nome dele.
- Adicione o nome do bucket criado ao arquivo .env na variável BUCKET_NAME.
- Certifique-se de que os arquivos CSV necessários estejam armazenados na pasta correta dentro do bucket S3 especificado.

#### 3. Configurar variáveis de ambiente:

- Verifique o arquivo .env para garantir que todas as variáveis de ambiente necessárias estejam configuradas corretamente, como segue no exemplo a seguir com as variáveis necessárias para o projeto funcionar corretamente:

```bash
CLICKHOUSE_HOST=localhost
CLICKHOUSE_PORT=8123
CLICKHOUSE_USER=default
CLICKHOUSE_PASSWORD=admin
AWS_ACCESS_KEY_ID='example'
AWS_SECRET_KEY_ID='example'
AWS_SESSION_TOKEN='example'
BUCKET_NAME = 'lake-example'
PREFIX = 'dataset/'
```

#### 4. Construir e executar os contêineres Docker:

- Na raiz do projeto (data_app), execute o comando para criar e iniciar os contêineres Docker:

```bash
docker-compose up --build
```

#### 5. Rodar o endpoint para processamento de dados:

- Antes de executar o endpoint da pipeline, certifique-se de ter criado o bucket S3 na AWS, armazenado uma ou mais bases de dados nele e inserido seu nome e prefixo (pasta a qual as bases de dados foram armazenadas) corretamente no .env.
- Acesse o endpoint de processamento de dados via browser ou ferramenta como Postman para iniciar o pipeline:

```bash
GET http://localhost:5000/pipeline/s3
```

#### 6. Acessar o dashboard

```bash
http://localhost:8501
```

#### 7. Rodar os testes automatizados

```bash
cd src/data_app

poetry run pytest
```


