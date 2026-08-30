<div align="center">
  <img src="https://i.pinimg.com/originals/7a/74/e0/7a74e0d4bc0b3df2a5105273f5a2e5c8.gif" alt="Banner" width="100%">

  # YamadaBot
  
  *A sua assistente musical definitiva para noites de insônia, playlists enormes e alta performance no Discord.*

  ![Python](https://img.shields.io/badge/PYTHON-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
  ![Discord.py](https://img.shields.io/badge/DISCORD.PY-2.X-5865F2?style=for-the-badge&logo=discord&logoColor=white)
  ![yt-dlp](https://img.shields.io/badge/YT--DLP-2023+-FF0000?style=for-the-badge&logo=youtube&logoColor=white)
  ![FFmpeg](https://img.shields.io/badge/FFMPEG-AUDIO-007808?style=for-the-badge&logo=ffmpeg&logoColor=white)
  <br>
  ![Status](https://img.shields.io/badge/STATUS-ESTÁVEL-success?style=for-the-badge)

</div>

<hr>

## 🖤 O que é a YamadaBot?

Chega de bots de música que travam, engasgam ou caem do nada no meio da melhor música. A **YamadaBot** é um ecossistema completo para reprodução de áudio construído para gerenciar o som do seu servidor de forma **automatizada, isolada por contexto e altamente responsiva**.

Desenvolvida com foco extremo em performance e qualidade de áudio, ela serve perfeitamente para qualquer grupo de amigos que não aguenta mais perder o ritmo da call por causa de bots mal otimizados.

<br>

## ✨ O que há de novo? (Atualização 1.0)

Nosso código foi desenhado do zero focado em **escalabilidade**, **Código Limpo** (Clean Code) e Padrões de Projeto (Orientação a Objetos):

- **Integração NATIVA (Slash Commands `/`)**: Esqueça o antigo `!`. A bot está totalmente integrada na UI oficial do Discord.
- **Isolamento de Estado de Alta Fidelidade**: O sistema permite que o bot toque playlists completamente diferentes em 50 servidores ao mesmo tempo sem que uma fila atropele a outra.
- **Desconexão Inteligente (Smart Disconnect)**: A Yamada monitora o canal. Se ela for deixada sozinha por mais de 3 minutos, ela para tudo, sai de mansinho e limpa a memória para economizar seus recursos.
- **Extração Flat (Ultra Rápida)**: Carrega playlists do YouTube com 300 vídeos quase instantaneamente usando requisições rasas (bypass de download de metadados de vídeo).

<hr>

## 🛠️ Como Instalar e Rodar na sua Máquina

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

3. **Instale as dependências essenciais:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configuração de Segurança e Chaves:**
   - Renomeie o arquivo `.env.example` para `.env`.
   - Adicione o **Token de Desenvolvedor** do seu bot dentro do `.env`.

5. **Inicie a Assistente:**
   ```bash
   python main.py
   ```

<hr>

## 💻 Comandos e Interações

| Comando | Função e Descrição |
| :--- | :--- |
| `/play` | Toca uma música (busca por nome ou link direto) ou carrega uma Playlist completa. |
| `/skip` | Interrompe o fluxo de áudio atual e injeta a próxima música da fila. |
| `/queue` | Retorna um Embed customizado exibindo a fila atual e a música tocando. Possui suporte a paginação. |
| `/stop` | Limpa completamente a fila, destroi a tarefa de fundo e remove o bot do canal. |

<hr>
<div align="center">
Desenvolvido com 🖤 e foco em código limpo.
</div>
