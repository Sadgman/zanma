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

#------------------------------------Respuestas automatica--------------------------------------

@bot.command()

async def candee(ctx, contador):

	contador=0

	if contador == 0:

		await ctx.send("Un día me pregunté si hay alguna riqueza en el mundo por la cual renunciaría a mi amor, pero en realidad, ¿hay alguna riqueza comparable a tu sonrisa? ¿De qué me servirían todas las cosas materiales que podría desear si no puedo disfrutarlas a tu lado?")

		contador+=1

	elif contador == 1:

		await ctx.send("Lo único que sé es que te quiero más que a nada en el mundo, el resto lo ignoro totalmente.")

		contador+=1

	elif contador == 2:

		await ctx.send("Tengo la ligera impresión de que en la larga marea del tiempo nadie podrá ocupar tu lugar.")

	else:

		contador=0

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


#------------------------------prefijo--------------------------------------------

@bot.command(name="prefijo")

async def prefijo(ctx,prefi):

	bot = commands.Bot(command_prefix=prefi)

	responder = ("tu prefijo a sido cambiado exitosamente",prefi)

	await ctx.send(responder)

#--------------------------------creador del bot-----------------------------------
@bot.command(name="creador")

async def creador(ctx):

	response = "creador de todo el universo Angel24"

	await ctx.send(response)

bot.run(Token)