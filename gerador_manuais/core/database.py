import json
import os

def salvar_manual(novo_conteudo):
    caminho_arquivo = 'data/manuais.json'
    
    # Garante que a pasta data existe
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # Tenta ler o arquivo se ele existir
    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            try:
                lista_manuais = json.load(f)
            except json.JSONDecodeError:
                lista_manuais = []
    else:
        lista_manuais = []

    lista_manuais.append(novo_conteudo)

    with open(caminho_arquivo, 'w', encoding='utf-8') as f:
        json.dump(lista_manuais, f, indent=4, ensure_ascii=False)