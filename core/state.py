import asyncio
from collections import deque

class GuildMusicState:
    """Representa o estado da música para um servidor específico do Discord."""
    def __init__(self, guild_id: int):
        self.guild_id = guild_id
        self.queue = deque()
        self.is_playing = False
        self.current_song = None
        
        self.song_added = asyncio.Event()
        self.song_finished = asyncio.Event()
        
        self.stopped = False
        self.text_channel = None

    def clear(self):
        """Limpa a fila e prepara a parada da tarefa de fundo."""
        self.queue.clear()
        self.stopped = True
        self.song_added.set()


class MusicManager:
    """Gerencia os estados de música de múltiplos servidores simultaneamente."""
    def __init__(self):
        self._states = {}

    def get_state(self, guild_id: int) -> GuildMusicState:
        if guild_id not in self._states:
            self._states[guild_id] = GuildMusicState(guild_id)
        return self._states[guild_id]

    def remove_state(self, guild_id: int):
        self._states.pop(guild_id, None)

# Instância global (Singleton)
manager = MusicManager()
