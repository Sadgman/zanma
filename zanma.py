from modulos import *

base = sqlite3.connect('zanma.db')
cursor = base.cursor()
cursor.execute('''
	CREATE TABLE IF NOT EXISTS PLAYERS (
			   id INTEGER PRIMARY KEY,
			   casado TEXT DEFAULT 'Con nadie:(',
			   dinero INTEGER DEFAULT 0,
			   dinero_banco INTEGER DEFAULT 0,
			   rool TEXT DEFAULT 'Vagabundo',
			   nivel INTEGER DEFAULT 0,
			   Bot_waintegracion INTEGER DEFAULT 0   
	)
''')
base.commit()
base.close()

load_dotenv()

Token = os.getenv("DISCORD_TOKEN")

class search:
    def __init__(self, words):
        self.search_words = str(pytube.contrib.search.Search(words).results)
        self.search_words_url = words
        self.result = ""
        self.result1 = ""
        self.num = 0
        self.search1 = ""
    @property
    def search_for(self):
        try:
            if "https://" in self.search_words_url:
                self.search1 = self.search_words_url
            else:
                for _ in self.search_words:
                    self.num += 1
                    if '=' in self.search_words[self.num]:
                        self.num += 1
                        self.result = self.num
                        break
                self.num = 0
                for _ in self.search_words:
                    self.num += 1
                    if '>' in self.search_words[self.num]:
                        self.result1 = self.num
                        break
                self.search1 = "https://www.youtube.com/watch?v=" + self.search_words[self.result:self.result1]
            return self.search1
        except IndexError:
            pass
class Cliente(discord.Client): 
	def __init__(self, intents=None):
		super().__init__(intents=intents)

	async def on_message(self, message):
		if self.jugador_existe(message.author.id) is None:
			self.agregar_jugador(message.author.id)
		print(message.author, message.content)

		if message.content.lower() == 'io':
			datos_jugador = self.datos_jugador(message.author.id)
			if datos_jugador[6] == 0:
				await message.channel.send(f'Hola {message.author.mention}\n casado con: {datos_jugador[1]}\n dinero: {datos_jugador[2]}\n dinero en el banco {datos_jugador[3]}')
			else:
				await message.channel.send(f'Hola {message.author.mention}\n casado con: {datos_jugador[1]}\n dinero: {self.obtener_dato_Wajugador(str(datos_jugador[6]))["dinero"]}\n dinero en el banco: {self.obtener_dato_Wajugador(str(datos_jugador[6]))["banco"]}\n Nivel: {self.obtener_dato_Wajugador(str(datos_jugador[6]))["nivel"]}\n Rool: {self.obtener_dato_Wajugador(str(datos_jugador[6]))["roles"]}')

		if message.content.lower() == 'integrar wa':
			await message.channel.send('Digita tu número de telefono de Whatsapp sin guiones')
			try:
				numero = await self.wait_for('message', check=lambda m: m.author == message.author, timeout=30)
				base = sqlite3.connect('zanma.db')
				cursor = base.cursor()
				cursor.execute(f'UPDATE PLAYERS SET Bot_waintegracion = {numero.content} WHERE id = {message.author.id}')
				base.commit()
				base.close()
				await message.channel.send('Se ha integrado correctamente tu número de Whatsapp')
			except asyncio.TimeoutError:
				await message.channel.send('Te tardaste mucho, intentalo de nuevo')
		
		if message.content.lower() == 'casar':
			await message.channel.send('Con quien quieres casarte?')
			try:
				casado = await self.wait_for('message', check=lambda m: m.author == message.author, timeout=30)
				if self.jugador_existe(casado.author.id) is None:
					self.agregar_jugador(casado.author.id)
					
				base = sqlite3.connect('zanma.db')
				cursor = base.cursor()
				id_usuario = re.sub(r'\D', '', casado.content)
				nombre_display = await self.obtener_display_name(message.guild.id, int(id_usuario))
				cursor.execute(f'UPDATE PLAYERS SET casado = "{nombre_display}" WHERE id = {message.author.id}')
				cursor.execute('UPDATE PLAYERS SET casado = ? WHERE id = ?', (message.author.display_name, id_usuario))
				base.commit()
				base.close()
				await message.channel.send(f'{message.author.mention} se ha casado con {nombre_display}')
			except asyncio.TimeoutError:
				await message.channel.send('Te tardaste mucho, intentalo de nuevo')
		if message.content.startswith('m'):
			searh = message.content.split(' ')[1]
			await self.coneccion_canal_llamada(message.author, searh)
	
	def jugador_existe(self, id):
		base = sqlite3.connect('zanma.db')
		cursor = base.cursor()
		cursor.execute(f'SELECT * FROM PLAYERS WHERE id = {id}')
		jugador = cursor.fetchone()
		base.close()
		return jugador
	
	def agregar_jugador(self, id):
		base = sqlite3.connect('zanma.db')
		cursor = base.cursor()
		cursor.execute(f'INSERT INTO PLAYERS (id) VALUES ({id})')
		base.commit()
		base.close()
	
	def datos_jugador(self, id):
		base = sqlite3.connect('zanma.db')
		cursor = base.cursor()
		cursor.execute(f'SELECT * FROM PLAYERS WHERE id = {id}')
		jugador = cursor.fetchone()
		base.close()
		return jugador
	
	async def obtener_display_name(self, guild_id, user_id):
		guild = self.get_guild(guild_id)
		if guild is not None:
			member = guild.get_member(user_id)
			if member is not None:
				return member.display_name
		return None
	
	def obtener_dato_Wajugador(self, id:str):
		l = os.path.dirname(os.path.realpath(__file__))
		l = l.replace('zanma', 'bot-whatsapp.js')
		r = os.path.join(l, 'data.json')
		
		with open(r , 'r') as file:
			data = json.load(file)
		for player in data['players']: 
			if player['id'] == id:
				return player
	async def coneccion_canal_llamada(self, id, searh):
		canal_voz = id.voice.channel if id.voice else None
		print(self.voice_clients.is_connected())
		if canal_voz:
			voice_client = await canal_voz.connect()
			YouTube(search(searh).search_for).streams.get_audio_only().download(filename='audio.mp3')
			source = FFmpegPCMAudio('audio.mp3')
			voice_client.play(source) 

intentos = discord.Intents.default()
intentos.message_content = True
client = Cliente(intents=intentos)
client.run(Token)