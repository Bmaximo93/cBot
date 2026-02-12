# 📅 Cbot — Robô Agendador de Eventos

> **Nota:** Este projeto foi desenvolvido principalmente como exercício prático de automação com **Selenium**. Uma versão futura utilizando a **Google Calendar API** oficial está planejada, o que tornará o processo significativamente mais rápido e robusto.

Cbot é um assistente de linha de comando que lê o conteúdo da sua área de transferência (texto ou imagem), extrai informações de eventos usando GPT-4.1-mini e cria automaticamente o evento no Google Calendar via automação de navegador com Selenium.

---

## ✨ Funcionalidades

###  Leitura inteligente do clipboard
O bot lê automaticamente o que estiver na sua área de transferência no momento da execução:
- **Texto** — qualquer trecho copiado contendo informações de evento
- **Imagem** — screenshots, fotos de convites, flyers digitais, etc. A imagem é enviada para o modelo de visão do GPT para extração

###  Extração flexível de eventos com IA
O GPT analisa o conteúdo e mapeia as informações para um schema estruturado. Alguns destaques da inteligência de extração:

- **Datas implícitas** — o modelo entende referências como "amanhã", "semana que vem", "daqui a três dias", "próxima sexta" e converte para datas absolutas com base na data atual
- **Horários deduzidos** — se o evento não for dia inteiro mas não tiver horário explícito, o modelo tenta inferir horários razoáveis com base no contexto (ex: "almoço de negócios" → horário de almoço)
- **Eventos de dia inteiro** — detectados automaticamente quando não há horário definido
- **Eventos de múltiplos dias** — suporte a eventos que se estendem por mais de um dia, com data de início e fim
- **Validação de datas** — datas impossíveis (ex: `40/13/2200`) ou datas no passado distante são rejeitadas; erros de digitação óbvios são corrigidos antes da invalidação
- **Localização e descrição** — extraídas do contexto quando disponíveis, sem repetir informações já presentes em outros campos (data, hora, local)
- **Conteúdo inválido** — se o conteúdo copiado não representar um evento, o bot informa o motivo de forma concisa e encerra sem abrir o navegador

###  Automação via Selenium
Após a extração, o bot abre o Google Calendar no Chrome e preenche o formulário de criação de evento automaticamente:
- Título do evento
- Data de início (e data de fim, para eventos multi-dia)
- Horário de início e fim
- Marcação de dia inteiro
- Localização
- Descrição

---

## ⚠️ Pré-requisitos importantes

### 1. Esteja logado no Google Calendar
O bot utiliza o seu perfil do Chrome para acessar o Google Calendar. **Você precisa estar logado na sua conta Google** no perfil configurado antes de executar o bot.

### 2. Execute o bot ao menos uma vez para gerar os cookies
Se você criar um **novo diretório de perfil do Chrome**, o navegador ainda não terá os cookies de sessão do Google. Nesse caso:

> 🔑 **Execute o bot ao menos uma vez e faça login manualmente na janela que for aberta.** Após isso, os cookies serão persistidos no perfil e as execuções seguintes não pedirão login novamente.

---

## ⚙️ Instalação e configuração

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd <pasta-do-projeto>
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Configure o arquivo `.env`

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
OPENAI_API_KEY=sua_chave_aqui
CHROME_PROFILE_PATH=/caminho/para/seu/perfil/chrome
```


> Você também pode criar uma pasta dedicada (ex: `./chrome_profile`) para isolar o perfil do bot. Lembre-se de fazer login manualmente na primeira execução.

### 4. Execute

```bash
python main.py
```

---

## 🔄 Fluxo de execução

```
[1/4] Lendo conteúdo do clipboard
        ↓
[2/4] Extraindo dados via GPT (em paralelo com a inicialização do Selenium)
        ↓
[3/4] Preenchendo formulário no Google Calendar
        ↓
[4/4] Confirmando criação do evento
```

---

## 📁 Estrutura do projeto

```
.
├── main.py              # Ponto de entrada, orquestra o fluxo principal
├── calendar_bot.py      # Automação Selenium do Google Calendar
├── gpt_service.py       # Integração com OpenAI para extração de eventos
├── utils.py             # Leitura do clipboard e animação de loading
├── requirements.txt     # Dependências do projeto
└── .env                 # Variáveis de ambiente (não versionar)
```
---
> **Nota:** este projeto foi desenvolvido e testado no macOS.
> No Windows, podem ocorrer problemas estéticos no terminal como cores e caracteres do spinner não renderizando corretamente.
---

## 🛠️ Tecnologias utilizadas

| Tecnologia | Uso |
|---|---|
| [Selenium](https://selenium.dev) | Automação do navegador Chrome |
| [OpenAI GPT-4.1-mini](https://platform.openai.com) | Extração e estruturação de eventos |
| [Pydantic](https://docs.pydantic.dev) | Validação e parsing do schema de evento |
| [Pillow](https://pillow.readthedocs.io) | Captura de imagens da área de transferência |
| [pyperclip](https://pypi.org/project/pyperclip/) | Leitura de texto da área de transferência |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | Gerenciamento de variáveis de ambiente |
