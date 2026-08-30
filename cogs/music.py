import math
import asyncio
import discord
from discord.ext import commands
from discord import app_commands
import yt_dlp

from core.state import manager

YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': True,
    'no_warnings': True,
}

YDL_QUEUE_OPTIONS = {
    'extract_flat': True,
    'quiet': True,
    'no_warnings': True,
}

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}


class Music(commands.Cog):
    """Módulo responsável por todos os comandos de música e controle de áudio."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def _audio_player_task(self, interaction: discord.Interaction, state):
        """Tarefa paralela que processa a fila de músicas e transmite o áudio."""
        guild = interaction.guild
        while not state.stopped:
            if not state.queue:
                state.song_added.clear()
                try:
                    await asyncio.wait_for(state.song_added.wait(), timeout=120)
                except asyncio.TimeoutError:
                    if guild.voice_client and guild.voice_client.is_connected():
                        await guild.voice_client.disconnect()
                        if state.text_channel:
                            await state.text_channel.send("💤 Desconectado por inatividade (2 minutos sem músicas).")
                    manager.remove_state(guild.id)
                    break
            
            if state.stopped:
                break
                
            if not state.queue:
                continue

            item = state.queue.popleft()
            state.current_song = item

            loop = asyncio.get_event_loop()
            try:
                data = await loop.run_in_executor(
                    None, 
                    lambda: yt_dlp.YoutubeDL(YDL_OPTIONS).extract_info(item['url'], download=False)
                )
                audio_url = data['url']
            except Exception:
                if state.text_channel:
                    await state.text_channel.send(f"⚠️ Não foi possível reproduzir **{item['title']}**. Pulando...")
                state.current_song = None
                continue

            if state.stopped:
                break

            state.song_finished.clear()

            def after_playing(error):
                if error:
                    print(f"[Music] Playback error: {error}")
                state.is_playing = False
                state.current_song = None
                loop.call_soon_threadsafe(state.song_finished.set)

            try:
                player = discord.FFmpegPCMAudio(audio_url, **FFMPEG_OPTIONS)
                guild.voice_client.play(player, after=after_playing)
                state.is_playing = True
                
                if state.text_channel:
                    embed = discord.Embed(
                        description=f"🎵 Tocando agora: **[{item['title']}]({item['url']})**", 
                        color=discord.Color.green()
                    )
                    await state.text_channel.send(embed=embed)
            except Exception as e:
                print(f"[Music] Playback start error: {e}")
                state.is_playing = False
                continue

            await state.song_finished.wait()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        """Gerencia a desconexão automática quando o bot fica sozinho no canal de voz."""
        if member.id == self.bot.user.id:
            return

        for vc in self.bot.voice_clients:
            if before.channel and vc.channel and vc.channel.id == before.channel.id:
                # Verifica se sobraram apenas bots no canal
                non_bot_members = [m for m in vc.channel.members if not m.bot]
                if not non_bot_members:
                    await asyncio.sleep(180)  # Aguarda 3 minutos
                    
                    if vc.is_connected():
                        current_non_bots = [m for m in vc.channel.members if not m.bot]
                        if not current_non_bots:
                            state = manager.get_state(vc.guild.id)
                            text_channel = state.text_channel
                            
                            state.clear()
                            await vc.disconnect()
                            manager.remove_state(vc.guild.id)
                            
                            if text_channel:
                                await text_channel.send("👋 Fiquei sozinho no canal de voz por mais de 3 minutos, então saí para economizar recursos.")

    @app_commands.command(name="play", description="Toca uma música ou playlist do YouTube")
    @app_commands.describe(query="Nome da música ou link do YouTube")
    async def play(self, interaction: discord.Interaction, query: str):
        if not interaction.user.voice:
            return await interaction.response.send_message("❌ Você precisa estar em um canal de voz!", ephemeral=True)

        await interaction.response.defer()

        state = manager.get_state(interaction.guild.id)
        state.text_channel = interaction.channel

        if not interaction.guild.voice_client:
            await interaction.user.voice.channel.connect()
            state.stopped = False
            self.bot.loop.create_task(self._audio_player_task(interaction, state))

        is_url = query.startswith(('http://', 'https://'))
        search_query = query if is_url else f"ytsearch1:{query}"

        loop = asyncio.get_event_loop()
        try:
            data = await loop.run_in_executor(
                None, 
                lambda: yt_dlp.YoutubeDL(YDL_QUEUE_OPTIONS).extract_info(search_query, download=False)
            )
        except Exception:
            return await interaction.followup.send("❌ Erro ao buscar a música.")

        if not data or ('entries' in data and not data['entries']):
            return await interaction.followup.send("❌ Nenhum resultado encontrado.")

        if 'entries' in data:
            if is_url:
                added = 0
                for entry in data['entries']:
                    if entry:
                        url = entry.get('url') or (f"https://www.youtube.com/watch?v={entry['id']}" if entry.get('id') else None)
                        if url:
                            state.queue.append({'url': url, 'title': entry.get('title', 'Desconhecido')})
                            added += 1
                await interaction.followup.send(f"📚 Playlist: **{added}** músicas adicionadas à fila!")
            else:
                entry = data['entries'][0]
                url = entry.get('url') or (f"https://www.youtube.com/watch?v={entry['id']}" if entry.get('id') else None)
                title = entry.get('title', 'Desconhecido')
                state.queue.append({'url': url, 'title': title})
                await interaction.followup.send(f"✅ Adicionado à fila: **{title}**")
        else:
            url = data.get('original_url', query)
            title = data.get('title', 'Desconhecido')
            state.queue.append({'url': url, 'title': title})
            await interaction.followup.send(f"✅ Adicionado à fila: **{title}**")

        if not state.is_playing:
            state.song_added.set()

    @app_commands.command(name="skip", description="Pula a música atual")
    async def skip(self, interaction: discord.Interaction):
        vc = interaction.guild.voice_client
        if vc and vc.is_playing():
            vc.stop()
            await interaction.response.send_message("⏭️ Música pulada!")
        else:
            await interaction.response.send_message("❌ Não há nenhuma música tocando no momento.", ephemeral=True)

    @app_commands.command(name="stop", description="Para a música, limpa a fila e desconecta o bot")
    async def stop(self, interaction: discord.Interaction):
        state = manager.get_state(interaction.guild.id)
        vc = interaction.guild.voice_client
        
        state.clear()
        
        if vc:
            if vc.is_playing():
                vc.stop()
            await vc.disconnect()
            await interaction.response.send_message("🛑 Reprodução parada, fila limpa e bot desconectado.")
        else:
            await interaction.response.send_message("❌ Eu não estou conectado a um canal de voz.", ephemeral=True)
            
        manager.remove_state(interaction.guild.id)

    @app_commands.command(name="queue", description="Mostra a fila atual de músicas")
    @app_commands.describe(page="Página da fila (padrão: 1)")
    async def queue(self, interaction: discord.Interaction, page: int = 1):
        state = manager.get_state(interaction.guild.id)
        
        if not state.current_song and not state.queue:
            return await interaction.response.send_message("A fila está vazia e nada está tocando.", ephemeral=True)

        items_per_page = 10
        total_pages = max(1, math.ceil(len(state.queue) / items_per_page))
        page = max(1, min(page, total_pages))

        embed = discord.Embed(
            title=f"Fila de Reprodução - {interaction.guild.name}",
            color=discord.Color.blurple()
        )

        if state.is_playing and state.current_song:
            embed.add_field(name="🎵 Tocando Agora:", value=f"**[{state.current_song['title']}]({state.current_song['url']})**", inline=False)

        if state.queue:
            start = (page - 1) * items_per_page
            queue_slice = list(state.queue)[start:start + items_per_page]
            
            queue_text = "\n".join(
                f"**{i}.** [{item['title']}]({item['url']})" 
                for i, item in enumerate(queue_slice, start + 1)
            )
            embed.add_field(name="A Seguir:", value=queue_text, inline=False)
            embed.set_footer(text=f"Página {page}/{total_pages} | Total na fila: {len(state.queue)}")
        else:
            embed.add_field(name="A Seguir:", value="Nenhuma música na fila.", inline=False)

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Music(bot))

