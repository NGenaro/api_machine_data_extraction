import json

def atualizar_links_imagem(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if key == "img" and isinstance(value, str) and value.startswith("https://www.baldor.com/"):
                final = value.replace("https://www.baldor.com/", "")
                data[key] = f"https://www.baldor.com/api/images/{final}"
            else:
                atualizar_links_imagem(value)
    elif isinstance(data, list):
        for item in data:
            atualizar_links_imagem(item)

# Carregar como dict
with open("app/data/products.json", "r", encoding="utf-8") as f:
    dados = json.load(f)

# Atualizar os links
atualizar_links_imagem(dados)

# Salvar o resultado no mesmo arquivo (ou em outro, se preferir)
with open("app/data/products.json", "w", encoding="utf-8") as f:
    json.dump(dados, f, indent=2, ensure_ascii=False)

# Apenas para visualização no console
print(json.dumps(dados, indent=2, ensure_ascii=False))
