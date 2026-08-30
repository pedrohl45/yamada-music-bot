# Discord Music Bot 🎵

Um Bot de Música para Discord robusto e pronto para produção, construído com `discord.py` e `yt-dlp`. 
Possui Comandos Slash modernos (`/`), extração de playlists otimizada, e streaming de áudio confiável sem travar o bot.

## 🚀 Funcionalidades

- **Comandos Slash:** Integração nativa com a interface do Discord (`/play`, `/skip`, `/queue`, `/stop`).
- **Alta Performance:** Utiliza `extract_flat` para carregar playlists do YouTube instantaneamente, sem gargalos.
- **Concorrência Robusta:** Gerenciamento de eventos com `asyncio` à prova de falhas, garantindo que as músicas toquem sem atropelamentos.
- **Desconexão Inteligente:** Sai automaticamente do canal de voz para economizar recursos se ficar inativo ou se todos os usuários saírem por mais de 3 minutos.
- **Arquitetura Limpa:** Design modular Profissional, separando a lógica em Cogs e usando gerenciadores de estado (POO).

## 📋 Requisitos

- Python 3.10 ou superior
- [FFmpeg](https://ffmpeg.org/) instalado na sua máquina/servidor.

## 🛠️ Instalação e Configuração

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio
   ```

2. **Crie o ambiente virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configuração de Segurança:**
   - Renomeie o arquivo `.env.example` para `.env`.
   - Abra o `.env` e cole o Token de Desenvolvedor do seu Bot do Discord.

## 🏃 Como Rodar

Inicie o bot com o comando abaixo. Ele sincronizará os comandos Slash no Discord de forma automática:
```bash
python main.py
```

## 📂 Estrutura do Projeto

- `main.py`: Ponto de entrada do sistema e inicializador de extensões.
- `cogs/music.py`: O coração do bot. Contém os comandos de reprodução, fila e a tarefa paralela (background task) responsável pelo streaming contínuo.
- `core/state.py`: Gerenciador de estado global isolado, garantindo que o bot funcione perfeitamente em múltiplos servidores simultaneamente sem misturar as filas.

## 📄 Licença
Licença MIT
