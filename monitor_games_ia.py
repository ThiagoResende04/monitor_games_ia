import os
import time
from openpyxl import Workbook
from playwright.sync_api import sync_playwright
from google import genai


# CONFIGURAÇÃO DA IA (NOVO SDK GEMINI)
# SEGURANÇA: O código agora busca a chave de forma segura no sistema operacional
API_KEY_GEMINI = os.environ.get("GEMINI_API_KEY")

# Inicialização global do cliente do Gemini
client = genai.Client(api_key=API_KEY_GEMINI)
# ==========================================

def simular_analise_local(titulo, preco):
    """Análise de contingência caso a cota do Gemini termine."""
    titulo_lower = titulo.lower()
    
    if any(k in titulo_lower for k in ["soccer", "fifa", "ea sports fc", "futebol", "nba", "f1", "wheels"]):
        genero = "Esportes / Corrida"
    elif any(k in titulo_lower for k in ["duty", "doom", "halo", "gears", "metro", "resident", "fighter", "ninja"]):
        genero = "FPS / Luta / Ação"
    elif any(k in titulo_lower for k in ["minecraft", "among", "lego", "park"]):
        genero = "Casual / Aventura"
    elif any(k in titulo_lower for k in ["cyberpunk", "witcher", "elden", "fantasy", "souls", "monster hunter"]):
        genero = "RPG / Mundo Aberto"
    else:
        genero = "Ação / Aventura"

    if preco > 300:
        avaliacao = "Caro"
        recomendacao = "Jogo recente ou edição Premium. Aguarde uma promoção se puder."
    elif 150 <= preco <= 300:
        avaliacao = "Justo"
        recomendacao = "Preço médio padrão de mercado para consoles."
    else:
        avaliacao = "Barato"
        recomendacao = "Excelente oportunidade física! Vale a compra imediata."

    return {"genero": genero, "avaliacao": avaliacao, "recomendacao": recomendacao}


def analisar_jogo_com_ia(titulo, preco):
    """Usa o Gemini se houver cota disponível, caso contrário ativa a lógica local."""
    print(f"🤖 IA analisando: {titulo[:30]}...")

    prompt = f"""
    Baseado no título do jogo de videogame e no preço fornecido, responda estritamente no formato abaixo, separando por ponto e vírgula (;):
    GÊNERO;AVALIAÇÃO_PREÇO;RECOMENDAÇÃO

    Jogo: {titulo}
    Preço: R$ {preco}

    Regras:
    - GÊNERO: Descubra o gênero do jogo (ex: RPG, Ação, Corrida, FPS, Esportes).
    - AVALIAÇÃO_PREÇO: Avalie se está Caro, Justo ou Barato baseado no mercado de games atual.
    - RECOMENDAÇÃO: Uma frase curta dizendo se vale a pena comprar ou esperar.
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        resposta_texto = response.text.strip()

        partes = resposta_texto.split(";")
        if len(partes) == 3:
            return {
                "genero": partes[0].strip(),
                "avaliacao": partes[1].strip(),
                "recomendacao": partes[2].strip(),
            }
    except Exception as e:
        # 🧠 ENGENHARIA DE RESILIÊNCIA: Se estourar a cota diária (429), entra o modo Fallback
        if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
            print("⚠️ Cota do Gemini esgotada para hoje. Ativando inteligência local de contingência...")
            return simular_analise_local(titulo, preco)
        else:
            print(f"⚠️ Erro temporário na IA ({e}). Usando dados locais.")
            return simular_analise_local(titulo, preco)

    return simular_analise_local(titulo, preco)


def salvar_em_excel(dados_jogos):
    """Salva os dados coletados e as análises no Excel."""
    print("\n[Excel] Criando planilha inteligente de Games...")
    wb = Workbook()
    aba_ativa = wb.active
    aba_ativa.title = "Análise de Games IA"

    aba_ativa.append(
        ["Título do Jogo", "Preço Real (R$)", "Gênero (IA)", "Avaliação de Preço (IA)", "Insight / Recomendação (IA)"])

    for item in dados_jogos:
        aba_ativa.append([
            item["produto"],
            item["preco_reais"],
            item["ia"]["genero"],
            item["ia"]["avaliacao"],
            item["ia"]["recomendacao"],
        ])

    nome_arquivo = "mercado_games_ia.xlsx"
    wb.save(nome_arquivo)
    print(f"✅ [Excel] Planilha inteligente salva com sucesso como: {nome_arquivo}")


def rodar_robo_games_ia():
    print("=== INICIANDO ROBÔ MONITOR DE GAMES COM IA ===")

    with sync_playwright() as p:
        print("Abrindo navegador Chrome...")
        navegador = p.chromium.launch(headless=False, channel="chrome")

        contexto = navegador.new_context(
            viewport={"width": 1366, "height": 768},
            locale="pt-BR",
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, Gecko) Chrome/120.0.0.0 Safari/537.36",
        )
        pagina = contexto.new_page()

        url_alvo = "https://www.amazon.com.br/s?k=jogos+ps5+xbox"
        print(f"Acessando mercado de games: {url_alvo}")
        pagina.goto(url_alvo)

        print("\n" + "=" * 60)
        print("PAUSA DE SEGURANÇA (MODO HÍBRIDO):")
        print("Aguarde a página carregar os jogos completamente.")
        print("Quando os jogos e preços aparecerem, volte ao PyCharm.")
        print("=" * 60)

        input("\n--> Quando a página mostrar os games, aperte ENTER para iniciar a IA: ")

        print("\nIniciando extração e análise preditiva...")

        blocos_produtos = pagina.locator("div[data-component-type='s-search-result']").all()
        lista_jogos = []

        for bloco in blocos_produtos:
            try:
                tag_titulo = bloco.locator("h2")
                titulo = tag_titulo.inner_text().strip()

                if len(titulo) > 15 and not any(
                        k in titulo.lower() for k in ["controle", "headset", "cabo", "carregador", "suporte"]):

                    try:
                        texto_reais = bloco.locator(".a-price-whole").first.inner_text()
                        texto_reais = texto_reais.replace(".", "").replace(",", "").replace("\n", "").strip()

                        try:
                            texto_centavos = bloco.locator(".a-price-fraction").first.inner_text().strip()
                        except Exception:
                            texto_centavos = "00"

                        preco_final = float(f"{texto_reais}.{texto_centavos}")
                    except Exception:
                        continue

                    if not any(j["produto"] == titulo for j in lista_jogos):
                        analise_ia = analisar_jogo_com_ia(titulo, preco_final)

                        lista_jogos.append({
                            "produto": titulo,
                            "preco_reais": preco_final,
                            "ia": analise_ia,
                        })
                        print(f"-> Sucesso: {titulo[:35]}... | R$ {preco_final} | Gênero: {analise_ia['genero']}\n")

                        # Mantemos 4 segundos para evitar picos de chamadas desnecessários
                        time.sleep(4)

                # Coleta 15 jogos para montar uma planilha bem encorpada
                if len(lista_jogos) >= 15:
                    break
            except Exception:
                continue

        if lista_jogos:
            salvar_em_excel(lista_jogos)
        else:
            print("❌ O robô não conseguiu ler os dados de nenhum jogo.")

        print("\n🏁 Processo concluído com sucesso!")
        navegador.close()
        os._exit(0)


if __name__ == "__main__":
    if API_KEY_GEMINI == "SUA_CHAVE_API_AQUI" or API_KEY_GEMINI.strip() == "":
        print("❌ ERRO: Você precisa colocar sua chave API válida do Gemini na linha 8 do código!")
    else:
        rodar_robo_games_ia()
