
# PROJETO: Automação da Coleta de Dados de Maquinário via API

Este projeto consiste em uma API desenvolvida para centralizar e automatizar o processo de coleta de dados de maquinário a partir de sites específicos. 

O objetivo é garantir que o processo de coleta ocorra de forma eficiente, programável e sustentável a longo prazo, permitindo atualizações automáticas sempre que necessário, desse modo, sempre que for necessario realizar uma atualizacao desses mesmos dados basta acessar por aqui.

**Site atualmente suportado**

- [BALDOR](https://www.baldor.com/): a coleta de dados deste site já está implementada e funcionando através da API.

## DESENVOLVIMENTO

O projeto foi desenvolvido de forma modular, considerando possíveis futuras alterações, tanto na estrutura dos sites quanto no formato de retorno dos dados ou outros requisitos.

Todo o desenvolvimento foi realizado em `Python`, utilizando as seguintes tecnologias:

Para a API foi utilizado:

- `FastAPI`: escolhido por sua performance, simplicidade e suporte nativo à documentação interativa via Swagger.

Para a coleta de dados foram utilizadas:

- `Playwright`: utilizado para automatizar a navegação em páginas com conteúdo dinâmico, simulando a interação humana de forma eficiente.
- `Requests`: empregado em páginas cujo conteúdo pode ser acessado diretamente por requisições HTTP, agilizando o processo de extração.

Para o pré-processamento foi utilizado:

- `NLTK`: usado para tratamento e limpeza de dados textuais, como tokenização e remoção de ruídos, quando necessário.

Essas ferramentas foram integradas para garantir uma extração de dados eficiente, robusta e facilmente adaptável a diferentes cenários de coleta.

### ESTRUTURA DAS PASTAS

Os arquivos nas pastas encontram-se na seguinte distribuição: 

```bash
project/
├── app/
│   ├── utils/
│   │   ├── config.py                 # Variáveis globais, caminhos, constantes
│   │   └── data_dictionary.py   # Dicionários com rotas ou mapeamentos
│   ├── services/                    # Lógica de negócio (scraping, etc)
│   │   ├── scraping_functions.py
│   │   └── base64_converter.py
│   ├── main.py                      # FastAPI app e inclusão das rotas
│   └── __init__.py
├── output/                          # Arquivos gerados pelo sistema
│   └── assets/
├── Dockerfile
├── requirements.txt
└── README.md
```

### Retorno

A API conta com dois endpoints `POST`, ambos executam o mesmo processo de coleta por site, com a diferença principal no formato de resposta:

- **/coleta**: retorna um arquivo `.zip` contendo os dados extraídos (metadados em JSON + arquivos brutos como imagens, PDFs e CADs).
- **/coleta_base64**: retorna um objeto JSON contendo os mesmos dados, mas com os arquivos incorporados no formato Base64.

#### Exemplo de retorno do endpoint `/coleta` (ZIP)

O retorno será um arquivo `.zip` contendo:

- `metadados.json`: informações estruturadas do produto;
- `assets/`: pasta com arquivos relacionados (imagem, manual, CAD etc.).

Estrutura dos arquivos na pasta ZIP de saida:

```bash
output/
├── assets/
│   ├── M123456/
│   │   ├── manual.pdf
│   │   ├── cad.dwg
│   │   └── img.jpg
│   ├── ...
│   └── M123459/
│       ├── manual.pdf
│       ├── cad.dwg
│       └── img.jpg
├── M123456.json
├── ...
└── M123459.json
```

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
  }
}
```

#### Exemplo de retorno do endpoint `/coleta_base64` (JSON com arquivos em Base64)

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
  "docs_base64": {
    "manual": "SLJKDHFKHGA/.../SKA20935423H/KJB42352342/2342;5EÇRWÉ",
    "cad": "SLJKDHFKHGA/.../SKA20935423H/KJB42352342/2342;5EÇRWÉ",
    "image": "SLJKDHFKHGA/.../SKA20935423H/KJB42352342/2342;5EÇRWÉ"
  }
}
```
Exemplo do retorno referente ao post "**COLETA EM ZIP**"




python -m uvicorn main:app --reload

url = f"https://www.baldor.com/catalog/{product_id}#tab=%22parts%22"
f"https://www.baldor.com/AssetImage.axd?id={image_id}"


url = f"https://www.baldor.com/api/products/{product_id}/drawings"
f"https://www.baldor.com/api/products/{product_id}/drawings/{number}"