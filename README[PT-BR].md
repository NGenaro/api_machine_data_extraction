
# PROJETO: Automação da Coleta de Dados de Maquinário via API

Este projeto consiste em uma API desenvolvida para centralizar e automatizar o processo de coleta de dados de maquinário a partir de sites específicos. 

O objetivo é garantir que o processo de coleta ocorra de forma eficiente, programável e sustentável a longo prazo, permitindo atualizações automáticas sempre que necessário, desse modo, sempre que for necessario realizar uma atualizacao desses mesmos dados basta acessar por aqui.

**Site atualmente suportado**

- [BALDOR](https://www.baldor.com/): a coleta de dados deste site já está implementada e funcionando através da API.

## DESENVOLVIMENTO

Todo o desenvolvimento foi realizado em `Python`, utilizando as seguintes tecnologias:

Para a API foi utilizado:

- `FastAPI`: escolhido por sua performance, simplicidade e suporte nativo à documentação interativa via Swagger.

Para a coleta de dados foram utilizadas:

- `Playwright`: utilizado para automatizar a navegação em páginas com conteúdo dinâmico, simulando a interação humana de forma eficiente.
- `Requests`: empregado em páginas cujo conteúdo pode ser acessado diretamente por requisições HTTP, agilizando o processo de extração.

### ESTRUTURA DAS PASTAS

Os arquivos nas pastas encontram-se na seguinte distribuição: 

```bash
project/
├── app/
│   ├── output/                          # Arquivos que contem os dados gerados pelo sistema 
│   │   └── assets/
│   │
│   ├── scraping/                        # Lógica de scraping
│   │   ├── baldor
│   │   │   ├── baldor_scraping.py       # Arquivo com as funcoes de scraping do site da baldor
│   │   │   ├── baldor_output.py         # Arquivo responsavel por processar e retornar a saida solicitada
│   │   │   └── final_output.py          # Arquivo responsavel por processar e retornar a saida final da apo
│   │   │   
│   │   └── outros sites                 # Local recomendado para futuros sites raspados
│   │
│   ├── utils/
│   │   ├── base64_converter.py          # Arquivo responsável por realizar o code e encode dos dados de base64 
│   │   ├── download_files.py            # Arquivo responsável pelo download dos dados na pasta especificada
│   │   ├── general_utils.py             # Arquivo responsável pelas funcoes basicas como logs, checkpoints entre outras
│   │   └── pre_process.py               # Arquivo responsável pelas funcoes de pre-processamentos
│   │
│   └── main.py                          # FastAPI, arquivo de execução principal
│   
├── Dockerfile
├── startup.sh
├── requirements.txt
├── .gitignore
└── README.md                            # Este arquivo
```

### RETORNO

A API conta com um endpoint `POST`, que executa o processo de coleta por site, com a diferença principal no formato de resposta:

- **/query**: retorna um objeto JSON contendo os mesmos dados, mas com os arquivos incorporados no formato Base64.

#### EXEMPLO DO RETORNO

O retorno será um arquivo `.json` contendo:

- `metadados.json`: informações estruturadas do produto;

Exemplo do retorno do JSON:

```json
{
  "product_id": "M123456",
  "name": "Motor AC Trifásico",
  "description": "TEFC, 2 HP, 1800 RPM",
  "specs": {
    "hp": "2",
    "voltage": "230/460",
    "rpm": "1800",
    "frame": "145T"
  },
  "bom": [
    {
      "part_number": "123-456",
      "description": "Ventilador de resfriamento",
      "quantity": 1
    }
  ],
  "assets": {
    "manual": "assets/M123456/manual.pdf",
    "cad": "assets/M123456/cad.dwg",
    "image": "assets/M123456/img.jpg"
  },
  "docs_base64": {
    "manual": "SLJKDHFKHGA/.../SKA20935423H/KJB42352342/2342;5EÇRWÉ",
    "cad": "SLJKDHFKHGA/.../SKA20935423H/KJB42352342/2342;5EÇRWÉ",
    "image": "SLJKDHFKHGA/.../SKA20935423H/KJB42352342/2342;5EÇRWÉ"
  }
}
```

Visualização do funcionamento da api com o retorno:

<video controls src="app/data/api_example.mp4" title="Title" style="width: 100%;"></video>

## EXECUTANDO O PROJETO

O Projeto foi desenvolivo e estruturada para realizar a raspagem de todos os produtos do site, como o site pode bloquear por execesso no processo de raspagem foi adicionando metodos para tentar resolver isso, sendo esses metodos a limpeza dos cookies e um ponto de espera que aguarda o sistema retornar salvando o processo ate aquele ponto para retornar a partir dali.

Vale lembrar que mesmo que o projeto tenha sido elaborado para coletar todos os dados de maquinario do site foi adicionado uma limitação no processo, fazendo com que ele seja interrompido e passe para a proxima etapa após coletar 15 produtos, caso deseje que essa limitação seja maior ou nao exista basta ir no ´"scraping/baldor_scraping.py"´ e apagar ou comentar o trecho a seguir:

```python
########################################################################

if len(products) >= 15:
    logging.info("  |_ Limit of 15 products reached. Stopping collection.")
    subsubcat["product"] = products
    return data 

########################################################################
```

Para executar o projeto basta instalar o docker e feito isso via wsl no vscode abra seu terminal e execute o seguinte comando: 
```bash
docker build -t scrap .
```
Seguido de 
```bash
docker run -p 5000:5050 scrap
```

Você pode acompanhar o desempenho e erros nos logs, como pode ser visto no exemplo a seguir:

<video controls src="app/data/logs_example.mp4" title="Title" style="width: 100%;"></video>
