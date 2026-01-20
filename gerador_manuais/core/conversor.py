import json
import os
import markdown
from bs4 import BeautifulSoup

def processar_conteudo_com_alertas(conteudo_md):
    """Converte Markdown e aplica classes de alerta e tabelas Intelbras."""
    html_raw = markdown.markdown(conteudo_md, extensions=['tables', 'fenced_code'])
    soup = BeautifulSoup(html_raw, 'html.parser')
    
    # Processa os alertas (Blockquotes)
    for bq in soup.find_all('blockquote'):
        texto_full = bq.get_text().strip()
        texto_lower = texto_full.lower()
        
        alerta_div = soup.new_tag('div')
        
        if texto_lower.startswith('info:'):
            alerta_div['class'] = 'alert alert-info'
            bq.string = texto_full[5:].strip()
            bq.wrap(alerta_div)
        elif texto_lower.startswith('aviso:'):
            alerta_div['class'] = 'alert alert-warning'
            bq.string = texto_full[6:].strip()
            bq.wrap(alerta_div)
            
    # Retorna o HTML com a classe de tabela aplicada
    return str(soup).replace('<table>', '<table class="intelbras-table">')

def gerar_html_do_json():
    caminho_json = 'data/manuais.json'
    caminho_template = 'templates/layout.html'
    pasta_output = 'output'
    
    if not os.path.exists(pasta_output):
        os.makedirs(pasta_output)

    with open(caminho_template, 'r', encoding='utf-8') as f:
        template_html = f.read()

    if not os.path.exists(caminho_json):
        return "Erro: Base de dados não encontrada."

    with open(caminho_json, 'r', encoding='utf-8') as f:
        manuais = json.load(f)

    for manual in manuais:
        # 1. USA A FUNÇÃO DE ALERTAS PARA GERAR O CORPO
        corpo_processado = processar_conteudo_com_alertas(manual['conteudo'])
        soup = BeautifulSoup(corpo_processado, 'html.parser')
        
        # 2. Construção do Menu Dinâmico
        menu_html = '<ul id="menu-dinamico">'
        titulos = soup.find_all(['h1', 'h2'])
        
        for i, tag in enumerate(titulos):
            tag_id = f"secao_{i}"
            tag['id'] = tag_id
            
            if tag.name == 'h1':
                menu_html += f'<li><a href="#{tag_id}">{tag.get_text()}</a>'
                if i + 1 < len(titulos) and titulos[i+1].name == 'h2':
                    menu_html += '<ul class="nav-subitens">'
                else:
                    menu_html += '</li>'
            elif tag.name == 'h2':
                menu_html += f'<li><a href="#{tag_id}">{tag.get_text()}</a></li>'
                if i + 1 == len(titulos) or titulos[i+1].name == 'h1':
                    menu_html += '</ul></li>'
        
        menu_html += '</ul>'

        # 3. Injeção no Layout
        pagina_final = template_html.replace("{{TITULO}}", manual['titulo'])
        pagina_final = pagina_final.replace("{{MENU_LATERAL}}", menu_html)
        pagina_final = pagina_final.replace("{{CONTEUDO}}", str(soup))

        # 4. IDENTAÇÃO ULTRA EXPLÍCITA (Padrão ADS - 4 espaços)
        soup_final = BeautifulSoup(pagina_final, 'html.parser')
        linhas = soup_final.prettify().splitlines()
        html_explícito = ""
        
        for linha in linhas:
            nivel_recuo = len(linha) - len(linha.lstrip())
            html_explícito += ("    " * nivel_recuo) + linha.lstrip() + "\n"

        # 5. Salvamento do arquivo
        nome_arquivo = manual['titulo'].replace(" ", "_").lower() + ".html"
        caminho_final = os.path.join(pasta_output, nome_arquivo)
        
        with open(caminho_final, "w", encoding="utf-8") as f:
            f.write(html_explícito)