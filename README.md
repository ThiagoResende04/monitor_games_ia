🎮 GameScout AI - Monitor Inteligente de Mercado de Games com IA

O **GameScout AI** é um robô automatizado de inteligência de mercado focado no ecossistema de videogames. Desenvolvido em Python, o script realiza a extração de dados reais (**Web Scraping**) diretamente do e-commerce da **Amazon Brasil**, captura títulos e preços atualizados de jogos (PS5 e Xbox) e utiliza Inteligência Artificial generativa (**Google Gemini**) para enriquecer e analisar esses dados, exportando um relatório analítico consolidado em Excel.

---

## 🚀 Funcionalidades Clave

* **Coleta de Dados Comercial:** Raspagem assíncrona/síncrona utilizando **Playwright** mapeando elementos estruturais em e-commerce real.
* **Análise Preditiva com IA:** Integração com a API do **Google Gemini (Modelo `gemini-2.5-flash`)** utilizando o novo SDK `google-genai` para inferir gênero, avaliar o preço e gerar recomendações de compra personalizadas.
* **Arquitetura Resiliente (Modo Fallback):** Sistema de tratamento de erros avançado que intercepta esgotamento de cotas da API (Erro `429 RESOURCE_EXHAUSTED` / `UNAVAILABLE`) e chaveia automaticamente para uma inteligência algorítmica local baseada em heurísticas, garantindo que o robô nunca quebre.
* **Cadenciamento de Requisições:** Implementação de controle de fluxo (*rate-limiting* mecânico com `time.sleep`) para mitigar bloqueios de infraestrutura e respeitar as políticas de uso dos servidores.
* **Exportação Estruturada:** Geração de planilhas formatadas (`.xlsx`) via **OpenPyXL** prontas para uso por equipes de negócios.

---

## 🛠️ Tecnologias e Ferramentas

* **Python 3.12+**
* **Playwright** (Navegação e raspagem de dados dinâmicos)
* **Google GenAI SDK** (Integração com LLM Gemini 2.5 Flash)
* **OpenPyXL** (Manipulação de planilhas Excel)
* **Plataforma Alvo:** Amazon Brasil (Seção de Games de Console)

---

## 📊 Arquitetura de Dados do Robô

O fluxo de dados do projeto segue uma linha de processamento inteligente e resiliente:

1. **Extração:** O robô abre a instância do navegador e isola os seletores semânticos dos produtos (`div[data-component-type='s-search-result']`).
2. **Sanitização:** Filtra palavras-chave indesejadas (como acessórios) e limpa as strings de preço, tipando-as como `float`.
3. **Enriquecimento Dinâmico:** * *Fluxo Principal:* Envia o contexto do anúncio para o Gemini classificar via Prompt Engineering.
   * *Fluxo de Contingência:* Se o limite de tokens diários da API for atingido, a lógica local assume o processamento das linhas restantes.
4. **Carga (Load):** Consolida os dados e insights em uma estrutura tabular.

---
## 📂Prints

<img width="1292" height="404" alt="Código iniciando no terminal" src="https://github.com/user-attachments/assets/d211a260-ea73-4f4e-8278-7a8aab66cf06" />
<img width="1342" height="627" alt="Navegador aberto" src="https://github.com/user-attachments/assets/856c7774-8f75-445e-8980-fe2809dcd548" />
<img width="1261" height="545" alt="Código reiniciando após abertura do navegador" src="https://github.com/user-attachments/assets/ae615b0a-938e-4cbb-bced-ebe0c7597ba7" />
<img width="1271" height="387" alt="Planilha" src="https://github.com/user-attachments/assets/4c534ec6-4931-46fa-9a28-03b5817ffa0a" />




---

## 📦 Como Instalar e Rodar o Projeto

### 1. Clonar o Repositório
```bash
git clone [https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO_GAMES.git](https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO_GAMES.git)
cd NOME_DO_REPOSITORIO_GAMES´´´

---







