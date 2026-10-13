# Poké Tower — Front-end + API de IA

Projeto da disciplina de Front-End baseado no MVP **Poké Tower** desenvolvido para a CP5. A entrega foi organizada em dois projetos: o jogo web (HTML/CSS/JavaScript) e uma API em FastAPI que recebe a solicitação tática do jogo e faz a chamada ao LLM local via Ollama.

## Integrantes do grupo

> **Antes de publicar, preencher com os nomes completos e RMs oficiais do grupo:**
> - `[Rickelmy Omine] — RM [563286]`
> - `[Davi Barboza] — RM [562370]`

## Estrutura

```text
poke_tower_frontend_api/
├── frontend/
│   └── index.html        # jogo original; chamada ao LLM direcionada à API
├── backend/
│   ├── main.py           # API FastAPI e rota protegida
│   ├── requirements.txt  # dependências Python
│   └── .env.example      # exemplo de configuração
├── .gitignore
└── README.md
```

## Requisitos

- Python 3.10 ou superior.
- [Ollama](https://ollama.com/) instalado e em execução.
- Modelo `llama3.2` baixado no Ollama.
- Navegador atualizado.

## 1. Preparar o modelo de IA

Abra um terminal e execute:

```bash
ollama pull llama3.2
ollama serve
```

Se o Ollama já estiver executando como serviço, basta confirmar que o modelo está disponível:

```bash
ollama list
```

## 2. Instalar e iniciar a API

Abra um terminal na pasta `backend`.

### Windows (PowerShell)

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Se o PowerShell bloquear a ativação do ambiente virtual, use o terminal CMD e execute `.venv\Scripts\activate.bat`.

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

A API ficará disponível em `http://127.0.0.1:8000`. A documentação interativa do FastAPI está em `http://127.0.0.1:8000/docs` e o teste de saúde em `http://127.0.0.1:8000/health`.

## 3. Executar o front-end

Com a API e o Ollama em execução, abra `frontend/index.html` no navegador. Inicie uma partida e use a análise do Rotom-A1. O navegador envia o prompt de contexto da batalha para `POST http://127.0.0.1:8000/api/analyze`; a API encaminha a solicitação ao Ollama e devolve o texto ao jogo.

## Rota da API

`POST /api/analyze`

Header obrigatório:

```http
X-API-Key: poke-tower-dev-key
Content-Type: application/json
```

Corpo de exemplo:

```json
{
  "prompt": "Analise a batalha e recomende uma ação em até 28 palavras.",
  "model": "llama3.2"
}
```

Resposta de exemplo:

```json
{
  "response": "O tipo do Pokémon ativo tem vantagem; use um golpe desse tipo.",
  "model": "llama3.2",
  "provider": "ollama"
}
```

A rota exige a chave no header. A chave padrão de demonstração é `poke-tower-dev-key`, configurada em `backend/.env.example` e no front-end. Se alterar `API_KEY` no arquivo `backend/.env`, altere também o valor `X-API-Key` no `frontend/index.html` para que ambos coincidam.

> **Nota de segurança:** como o front-end é HTML público, uma chave embutida nele pode ser vista por qualquer pessoa. Essa autenticação por header atende a uma demonstração acadêmica/local, mas não deve ser tratada como proteção forte para um sistema publicado. Em produção, a chave não deve ficar no código entregue ao navegador.

## Testar a API sem abrir o jogo

Com a API em execução, acesse `http://127.0.0.1:8000/docs`, abra `POST /api/analyze`, informe o header `X-API-Key` e envie um prompt. Também é possível testar o endpoint de saúde em `http://127.0.0.1:8000/health`.

## Problemas comuns

- **401 — API key ausente ou inválida:** confira se o header `X-API-Key` corresponde ao `API_KEY` do `.env`.
- **503 — não conecta ao Ollama:** inicie o Ollama e confirme que ele responde em `http://127.0.0.1:11434`.
- **Modelo não encontrado:** execute `ollama pull llama3.2`.
- **A análise não aparece no jogo:** confirme que o terminal do Uvicorn não mostra erros e que a API está na porta 8000.
- **A API funciona, mas o jogo está sem imagem gerada:** a geração visual do cenário é uma integração separada e depende do serviço de imagem externo; a análise textual é que passou a usar a API FastAPI.

## Vídeo curto de demonstração (1–3 minutos)

Grave a tela mostrando, nesta ordem:
1. O repositório e a divisão `frontend/` / `backend/`.
2. A instalação/execução da API e a rota `POST /api/analyze` na documentação `/docs`.
3. O jogo aberto no navegador e uma batalha iniciada.
4. A análise do Rotom-A1 aparecendo no jogo.
5. Se possível, mostre rapidamente o header `X-API-Key` e a resposta da API.

Sugestão de nome: `demo-poke-tower-front-end.mp4`. O vídeo deve ser gravado pelo grupo; este repositório contém o roteiro, não uma gravação real.

## Tecnologias

- Front-end: HTML, CSS e JavaScript.
- Back-end: Python, FastAPI e Uvicorn.
- LLM local: Ollama com `llama3.2`.
- Comunicação: HTTP/JSON com autenticação simples via header.
