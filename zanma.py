from modulos import *
#------------------------TOKENS-------------------------

load_dotenv()

yotube= os.getenv("clave")

Token = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix="!")


#------------------------------reproduccion-----------------------

@bot.command(pass_context=True)

async def play(ctx):

	if (ctx.author.voice):

	    channel=ctx.message.author.voice.channel

	    voice = await channel.connect()

	    source = FFmpegPCMAudio("stay.mp3")
	    musiclist1= FFmpegPCMAudio("Stressed Out.mp3")
	    contador=1
	    if contador==1:
	        player = voice.play(source)
	        contador-1
	    else:
	        player = voice.play(musiclist1)
	        contador+1

	else:

		await ctx.send("no estas en un chat de voz")

#--------------------------------------------preguntas------------------------------------------------------------------

@bot.command()

async def dios(ctx, existe):

	await ctx.send("claro que dios existe, no te puedo decir el porque pero confia en mi soy un bot y se todo")

@bot.command(pass_context=False)

#----------------------------------------------	Salir del chat de voz---------------------------------------------------

async def salir(ctx):

	if (ctx.voice_client):

		await ctx.guild.voice_client.disconnect()

		await ctx.send("me voy")

	else:

		await ctx.send("no estoy en el chat de voz")

#----------------------------------informacion del servidor-------------------------------------------------

@bot.command()

async def informacion(ctx):

	embed=discord.Embed(title=f"{ctx.guild.name}",description = "nigga",timestamp = datetime.datetime.utcnow(), color = discord.Color.blue())

	embed.add_field(name="servidor creado a", value=f"{ctx.guild.created_at}")

	embed.add_field(name='propietario del servidor', value=f"{ctx.guild.owner}")

	embed.add_field(name='region del servidor', value=f"{ctx.guild.region}")

	embed.add_field(name="id del servidor", value=f"{ctx.guild.id}")

	embed.set_thumbnail(url="https://logos-marcas.com/wp-content/uploads/2020/04/Movistar-Logo.png")

	await ctx.send(embed=embed)

#--------------------------------creador del bot-----------------------------------
@bot.command(name="creador")

async def creador(ctx):

	response = "creador de todo el universo Angel24"

	await ctx.send(response)

bot.run(Token)
