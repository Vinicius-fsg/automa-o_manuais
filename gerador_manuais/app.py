import streamlit as st
import streamlit.components.v1 as components
import os
import markdown
from bs4 import BeautifulSoup
from core.database import salvar_manual
from core.conversor import processar_conteudo_com_alertas

# 1. Configuração da Página
st.set_page_config(page_title="Gerador de Manuais Intelbras", layout="wide")

# 2. CSS da Interface (Dashboard)
st.markdown("""
    <style>
    .main { background-color: #f0f2f5; }
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #e0e0e0; }
    div.stButton > button {
        background-color: #00A94D !important;
        color: white !important;
        border-radius: 12px;
        font-weight: 600;
        height: 3em;
    }
    .stTextInput input, .stTextArea textarea {
        border-radius: 8px !important;
        border: 1px solid #dee2e6 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar
with st.sidebar:
    st.image("https://www.intelbras.com/sites/default/files/logo-intelbras.png") 
    st.title("Configurações")
    setor = st.text_input("Setor", value="Redes Empresariais")
    st.info("Configurações aplicadas ao layout final.")

# 4. Área Principal
st.title("📄 Gerador de Documentação Técnica")

col_editor, col_acoes = st.columns([2, 1])

with col_editor:
    st.header("Edição e Preview")
    
    tab_edit, tab_vis_real, tab_vis_cod, tab_guia = st.tabs([
        "📝 Editor", 
        "🎨 Visualização Real", 
        "🔍 Código Identado", 
        "📖 Guia de Uso"
    ])
    
    with tab_edit:
        titulo = st.text_input("Título do Equipamento", placeholder="Ex: S1105F-HP")
        conteudo_md = st.text_area("Conteúdo (Markdown)", height=500, placeholder="Use # para títulos e | para tabelas")

    with tab_vis_real:
        if titulo and conteudo_md:
            html_final_preview = processar_conteudo_com_alertas(conteudo_md)
            
            # Preview usando o estilo simplificado do Dashboard
            preview_html = f"""
            <html>
                <head>
                    <style>
                        :root {{ --color-green: #00A94D; --color-text: #2d3436; }}
                        body {{ background: #f4f7f6; padding: 30px; font-family: 'Segoe UI', sans-serif; display: flex; justify-content: center; }}
                        .folha-conteudo {{ background: white; padding: 60px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); width: 100%; max-width: 850px; }}
                        h1 {{ color: #333; font-size: 32px; margin: 10px 0 20px 0; }}
                        .tag-guia {{ color: var(--color-green); font-weight: bold; text-transform: uppercase; font-size: 12px; }}
                        .alert {{ padding: 15px; border-radius: 8px; margin: 20px 0; border-left: 5px solid; }}
                        .alert-info {{ background: #e7f3ff; border-color: var(--color-green); color: #007d3a; }}
                        .alert-warning {{ background: #fff4e5; border-color: #ffa000; color: #856404; }}
                        .intelbras-table {{ width: 100%; border-collapse: collapse; margin: 25px 0; }}
                        .intelbras-table th {{ background-color: #f8f9fb; color: #888; text-align: left; padding: 12px 15px; border-bottom: 2px solid #eee; }}
                        .intelbras-table td {{ padding: 15px; border-bottom: 1px solid #f0f0f0; }}
                        tr td:first-child {{ font-weight: bold; }}
                    </style>
                </head>
                <body>
                    <div class="folha-conteudo">
                        <span class="tag-guia">{setor}</span>
                        <h1>{titulo}</h1>
                        <div class="conteudo-renderizado">{html_final_preview}</div>
                    </div>
                </body>
            </html>
            """
            components.html(preview_html, height=800, scrolling=True)
        else:
            st.info("Preencha o título e o conteúdo para visualizar o manual.")

    with tab_vis_cod:
        if conteudo_md:
            soup_p = BeautifulSoup(markdown.markdown(conteudo_md, extensions=['tables', 'fenced_code']), 'html.parser')
            st.code(soup_p.prettify().replace('  ', '    '), language="html")

    with tab_guia:
        st.markdown("""
        ### 📘 Manual de Uso
        * **Info (Verde)**: `> info: Seu texto aqui`
        * **Aviso (Laranja)**: `> aviso: Seu texto aqui`
        * **Tabelas**: Use o padrão Markdown para gerar tabelas.
        """)

# Função de Montagem do Template Oficial (Fora dos botões para ser acessível)
def montar_template_oficial(titulo_equipamento, conteudo_md):
    corpo_renderizado = processar_conteudo_com_alertas(conteudo_md)
    return f"""<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="utf-8" />
    <meta content="width=device-width, initial-scale=1.0" name="viewport">
    <title>{titulo_equipamento} | Guia de Instalação</title>
    <link href="/res/img/favicon.ico" rel="shortcut icon" />
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="/gerador_manuais/templates/estilo.css">
    <script src="kit.fontawesome.com" crossorigin="anonymous"></script>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
    <script src="/gerador_manuais/templates/funcoes.js"></script>
</head>
<body>
    <header class="header">
        <div class="header-left">
            <button class="open_btn" onclick="toggleSidebar()"><i class="fas fa-bars fa-lg"></i></button>
            <img src="/res/img/intelbras_marca.svg" alt="Intelbras" class="logo-header">
        </div>
        <div class="header-right">
            <button onclick="window.print()" class="btn-header btn-outline"><i class="fas fa-print"></i> <span>PDF</span></button>
            <a href="/" class="btn-header"><i class="fas fa-home"></i> Início</a>
        </div>
    </header>
    <nav class="scrollbar" id="mySidebar">
        <ul><li id="falecom">Fale com a gente</li></ul>
    </nav>
    <main class="content" id="mainContent">
       <section id="inicio">
            <span style="color: #00A94D; font-weight: bold; text-transform: uppercase; font-size: 12px;">Guia de instalação</span>
            <h1>{titulo_equipamento}</h1>
            {corpo_renderizado}
            <div id="faleCom" class="fale-com-a-gente">
                <div class="div-logo-fale-com-a-gente"><img src="/res/img/intelbras_marca.svg" class="logo-itb-fale-com-a-gente"></div>
                <hr class="divider">
                <div class="div-info-fale-com-a-gente">
                    <p><strong>Suporte a clientes:</strong> (48) 2106 0006</p>
                    <p>Intelbras S/A – Rodovia SC 281, km 4,5 – São José/SC</p>
                </div>
            </div>      
        </section>
    </main>
</body>
</html>"""

# Bloco de Ações
with col_acoes:
    st.header("Ações")
    
    if st.button("💾 Salvar Rascunho"):
        if titulo and conteudo_md:
            salvar_manual({"titulo": titulo, "setor": setor, "conteudo": conteudo_md})
            st.success("Salvo no banco de dados!")
        else:
            st.warning("Preencha o título e o conteúdo.")

    if st.button("🚀 GERAR MANUAL OFICIAL"):
        if titulo and conteudo_md:
            try:
                # Gera o conteúdo com a estrutura oficial
                html_oficial = montar_template_oficial(titulo, conteudo_md)
                nome_arq = f"{titulo.replace(' ', '_').lower()}.html"
                
                # Botão de Download
                st.download_button(
                    label="📥 Baixar Arquivo HTML Oficial",
                    data=html_oficial,
                    file_name=nome_arq,
                    mime="text/html"
                )
                st.success("Estrutura oficial preparada para download!")
            except Exception as e:
                st.error(f"Erro técnico: {e}")
        else:
            st.error("Preencha os campos antes de gerar.")