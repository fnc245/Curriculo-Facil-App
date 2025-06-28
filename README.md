# Currículo Fácil V2.0

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0-lightgrey.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

Assistente inteligente para criação de currículos profissionais, potencializado pela API do Google Gemini e construído com Flask. Distribuído como uma aplicação de desktop para Windows com instalador.

---

### Tabela de Conteúdos
1. [Descrição do Projeto](#descrição-do-projeto)
2. [Features Principais](#features-principais)
3. [Demonstração em Vídeo (Opcional)](#demonstração)
4. [Tecnologias Utilizadas](#tecnologias-utilizadas)
5. [Como Instalar (Usuário Final)](#como-instalar-usuário-final)
6. [Como Executar (Desenvolvedores)](#como-executar-desenvolvedores)
7. [Estrutura do Projeto](#estrutura-do-projeto)
8. [Licença](#licença)
9. [Contato](#contato)

---

### Descrição do Projeto
O **Currículo Fácil** é uma aplicação de desktop para Windows que oferece uma interface de chat para ajudar usuários a criarem currículos de forma rápida e intuitiva. A aplicação utiliza um modelo de linguagem avançado (Google Gemini) para coletar as informações do usuário em uma conversa natural e, ao final, gera um arquivo HTML bem formatado e pronto para ser impresso ou compartilhado.

Este projeto foi desenvolvido com uma arquitetura modular em Python, utilizando o microframework Flask para o backend e uma interface web simples para o chat, empacotado como uma aplicação de desktop autônoma.

### Features Principais
- **Chat Inteligente:** Conversa guiada para coleta de dados pessoais, objetivos, experiência, escolaridade e habilidades.
- **Geração de HTML:** Cria um arquivo de currículo `.html` com um layout limpo e profissional, com link direto para visualização.
- **Configuração no App:** Solicita a chave de API do Gemini na primeira execução, com validação instantânea e armazenamento seguro (criptografado) no computador do usuário.
- **Acesso em Rede Local:** A IA é informada sobre o endereço de IP local para que possa orientar o usuário sobre como acessar a aplicação de outros dispositivos na mesma rede.
- **Bandeja de Sistema (System Tray):** Roda em segundo plano com um ícone na bandeja do sistema para fácil acesso (abrir no navegador) e controle (fechar a aplicação).
- **Instalador para Windows:** Distribuído como um `.exe` com um instalador profissional criado com Inno Setup para uma experiência de usuário familiar.
- **Sessões no Lado do Servidor:** Utiliza `Flask-Session` para armazenar o histórico da conversa no servidor, permitindo chats longos e complexos sem os limites de tamanho de cookies.

### Demonstração
*(Opcional: Se você gravar um pequeno vídeo ou GIF mostrando a aplicação em funcionamento, pode adicioná-lo aqui. É uma ótima maneira de demonstrar o projeto.)*
`[Link para o vídeo ou GIF aqui]`

### Tecnologias Utilizadas
- **Backend:** Python, Flask, Flask-Session
- **IA:** Google Gemini API (`google-generativeai`)
- **Frontend:** HTML, CSS, JavaScript (com `marked.js` e `DOMPurify`)
- **Interface de Desktop:** `pystray`, `Pillow`
- **Empacotamento:** PyInstaller
- **Instalador:** Inno Setup
- **Outras Bibliotecas:** `netifaces`, `cryptography`, `python-dotenv`

### Como Instalar (Usuário Final)
1. Vá para a seção **[Releases](https://github.com/fnc245/Curriculo-Facil-App/releases)** deste repositório.
2. Baixe o arquivo `CurriculoFacil-v2.0-setup.exe`.
3. Execute o instalador e siga as instruções do assistente.
4. Após a instalação, um ícone do "Currículo Fácil" será criado na sua área de trabalho e/ou Menu Iniciar.
5. Execute a aplicação. Um ícone aparecerá na bandeja do sistema (ao lado do relógio). Clique com o botão esquerdo nele para abrir a interface do chat no seu navegador.

### Como Executar (Desenvolvedores)
1. **Clone o repositório:**
   ```bash
   git clone https://github.com/fnc245/Curriculo-Facil-App.git
   cd Curriculo-Facil-App
   ```
2. **Crie e ative um ambiente virtual:**
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```
3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure suas chaves:**
   - Renomeie o arquivo `.env.example` para `.env`.
   - Abra o `.env` e insira uma `FLASK_SECRET_KEY` (pode ser qualquer string aleatória). A `GEMINI_API_KEY` pode ser deixada em branco para testar o fluxo de configuração inicial.
5. **Inicialize o banco de dados (apenas na primeira vez):**
   ```bash
   # Define a aplicação para o Flask (exemplo para Windows CMD)
   set FLASK_APP=run.py
   # Executa o comando de inicialização
   flask init-db
   ```
6. **Execute a aplicação:**
   ```bash
   python run.py
   ```
   Acesse `http://localhost:5001/app_chat` no seu navegador.

### Estrutura do Projeto
```
/Curriculo-Facil-App/
|-- app/                # Módulo principal da aplicação Flask
|   |-- services/       # Lógica de negócio (IA, prompts)
|   |-- utils/          # Funções utilitárias (detecção de IP)
|   |-- models.py       # Interação com o banco de dados
|   |-- routes.py       # Definição dos endpoints
|   |-- static/         # Arquivos CSS e JS
|   |-- templates/      # Arquivos HTML
|
|-- run.py              # Ponto de entrada para iniciar a aplicação (System Tray)
|-- config.py           # Configurações da aplicação
|-- setup_script.iss    # Script do Inno Setup para o instalador
|-- requirements.txt    # Lista de dependências Python
|-- .gitignore          # Arquivos e pastas a serem ignorados pelo Git
|-- app_icon.ico        # Ícone da aplicação
|...
```

### Licença
Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

### Contato
Francisco Neves Carvalho Filho - fnc245@gmail.com
