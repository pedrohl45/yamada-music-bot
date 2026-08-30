import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

class MusicBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        """Loads extensions and syncs slash commands."""
        await self.load_extension("cogs.music")
        
        # Sincroniza os comandos (/) com o Discord
        await self.tree.sync()
        print("✅ Comandos (Slash Commands) sincronizados com sucesso.")

    async def on_ready(self):
        print(f"🤖 Bot online como {self.user}!")
        print("Pronto para tocar música.")

if __name__ == "__main__":
    if not TOKEN:
        print("❌ Erro: DISCORD_TOKEN não encontrado. Renomeie o .env.example para .env e coloque seu token.")
    else:
        bot = MusicBot()
        bot.run(TOKEN)

