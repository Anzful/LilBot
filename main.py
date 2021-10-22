
import asyncio
import youtube_dl
import pafy
import discord
from discord.ext import commands
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

Token = 'My Token'

@bot.event
async def on_ready():
    print(f"{bot.user.name} is ready.")

class Player(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
        self.song_queue = {}

        self.setup()

    def setup(self):
        for guild in self.bot.guilds:
            self.song_queue[guild.id] = []

    async def check_queue(self, ctx):
        if len(self.song_queue[ctx.guild.id]) > 0:
            ctx.voice_client.stop()
            await self.play_song(ctx, self.song_queue[ctx.guild.id][0])
            self.song_queue[ctx.guild.id].pop(0)

    async def search_song(self, amount, song, get_url=False):
        info = await self.bot.loop.run_in_executor(None, lambda: youtube_dl.YoutubeDL({"format" : "bestaudio", "quiet" : True}).extract_info(f"ytsearch{amount}:{song}", download=False, ie_key="YoutubeSearch"))
        if len(info["entries"]) == 0: return None

        return [entry["webpage_url"] for entry in info["entries"]] if get_url else info

    async def play_song(self, ctx, song):
        url = pafy.new(song).getbestaudio().url
        ctx.voice_client.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(url)), after=lambda error: self.bot.loop.create_task(self.check_queue(ctx)))
        ctx.voice_client.source.volume = 0.5
    

    async def play_lofi(self, ctx, song2):
      url2 = pafy.new(song2).getbestaudio().url
      ctx.voice_client.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(url2)), after=lambda error: self.bot.loop.create_task
      (self.check_queue(ctx)))     
      ctx.voice_client.source.volume=0.5

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
          embed = discord.Embed(title="Join a voice channel\n", colour=discord.Colour.dark_purple())

          await ctx.send(embed=embed)
        
        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()

        await ctx.author.voice.channel.connect()
        embed = discord.Embed(title="Joined the voice channel\n", colour=discord.Colour.dark_purple())

        await ctx.send(embed=embed)

        channel = ctx.author.voice.channel
        await ctx.guild.change_voice_state(channel=channel, self_mute=False, self_deaf=True)
    
    @commands.command()
    async def j(self, ctx):
        if ctx.author.voice is None:
          embed = discord.Embed(title="Join a voice channel\n", colour=discord.Colour.dark_purple())

          await ctx.send(embed=embed)
        
        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()

        await ctx.author.voice.channel.connect()
        embed = discord.Embed(title="Joined the voice channel\n", colour=discord.Colour.dark_purple())

        await ctx.send(embed=embed)

        channel = ctx.author.voice.channel
        await ctx.guild.change_voice_state(channel=channel, self_mute=False, self_deaf=True)

    @commands.command()
    async def leave(self, ctx):
        if ctx.voice_client is not None:
            embed = discord.Embed(title="Left the voice channel\n", colour=discord.Colour.dark_purple())
            await ctx.send(embed=embed)

            return await ctx.voice_client.disconnect()

        embed = discord.Embed(title="I'm not connected to a voice channel\n", colour=discord.Colour.dark_purple())

        await ctx.send(embed=embed)
    
    @commands.command()
    async def l(self, ctx):
        if ctx.voice_client is not None:
            embed = discord.Embed(title="Left the voice channel\n", colour=discord.Colour.dark_purple())
            await ctx.send(embed=embed)

            return await ctx.voice_client.disconnect()

        embed = discord.Embed(title="I'm not connected to a voice channel\n", colour=discord.Colour.dark_purple())

        await ctx.send(embed=embed)

    @commands.command()
    async def lofi(self, ctx, *, song2=None):
      await self.play_lofi(ctx, song2)
      embed = discord.Embed(title ="Now playing:\n",    description ={song2},
      colour=discord.Colour.dark_purple())

      return await ctx.send(embed=embed)

  

    @commands.command()
    async def play(self, ctx, *, song=None):
        if song is None:
          embed = discord.Embed(title="Include a song\n", colour=discord.Colour.dark_purple())

          return await ctx.send(embed=embed)

        if ctx.voice_client is None:
          embed = discord.Embed(title="I need to be in a voice channel\n", colour=discord.Colour.dark_purple())
          return await ctx.send(embed=embed)

        # handle song where song isn't url
        if not ("youtube.com/watch?" in song or "https://youtu.be/" in song):
            #await ctx.send("Searching for song, this may take a few seconds.")

            result = await self.search_song(1, song, get_url=True)

            if result is None:
              embed = discord.Embed(title="I couldn't find the song. use !search\n", colour=discord.Colour.dark_purple())

              return await ctx.send(embed=embed)

            song = result[0]

        if ctx.voice_client.source is not None:
            queue_len = len(self.song_queue[ctx.guild.id])

            if queue_len < 20:
                self.song_queue[ctx.guild.id].append(song)
                embed = discord.Embed(title="Added to the queue\n", colour=discord.Colour.dark_purple())

                return await ctx.send(embed=embed)

            #else:
                #return await ctx.send("I can only queue up to 10 songs, please wait for the current song to finish.")

        await self.play_song(ctx, song)
        embed = discord.Embed(title="Now playing:\n",
        description={song}, colour=discord.Colour.dark_purple())

        await ctx.send(embed=embed)
    
    @commands.command()
    async def p(self, ctx, *, song=None):
        if song is None:
          embed = discord.Embed(title="Include a song\n", colour=discord.Colour.dark_purple())

          return await ctx.send(embed=embed)

        if ctx.voice_client is None:
          embed = discord.Embed(title="I need to be in a voice channel\n", colour=discord.Colour.dark_purple())
          return await ctx.send(embed=embed)

        # handle song where song isn't url
        if not ("youtube.com/watch?" in song or "https://youtu.be/" in song):
            #await ctx.send("Searching for song, this may take a few seconds.")

            result = await self.search_song(1, song, get_url=True)

            if result is None:
              embed = discord.Embed(title="I couldn't find the song. use !search\n", colour=discord.Colour.dark_purple())

              return await ctx.send(embed=embed)

            song = result[0]

        if ctx.voice_client.source is not None:
            queue_len = len(self.song_queue[ctx.guild.id])

            if queue_len < 20:
                self.song_queue[ctx.guild.id].append(song)
                embed = discord.Embed(title="Added to the queue\n", colour=discord.Colour.dark_purple())

                return await ctx.send(embed=embed)

            #else:
                #return await ctx.send("I can only queue up to 10 songs, please wait for the current song to finish.")

        await self.play_song(ctx, song)
        embed = discord.Embed(title="Now playing:\n",
        description={song}, colour=discord.Colour.dark_purple())

        await ctx.send(embed=embed)

    @commands.command()
    async def search(self, ctx, *, song=None):
        if song is None:
          embed = discord.Embed(title="Include a song\n", colour=discord.Colour.dark_purple())

          return await ctx.send(embed=embed)

        #await ctx.send("Searching for song, this may take a few seconds.")

        info = await self.search_song(5, song)

        embed = discord.Embed(title=f"Results for '{song}':", description="*You can use these URL's to play an exact song if the one you want isn't the first result.*\n", colour=discord.Colour.red())
        
        amount = 0
        for entry in info["entries"]:
            embed.description += f"[{entry['title']}]({entry['webpage_url']})\n"
            amount += 1

        embed.set_footer(text=f"Displaying the first {amount} results.")
        await ctx.send(embed=embed)

    @commands.command()
    async def queue(self, ctx): # display the current guilds queue
        if len(self.song_queue[ctx.guild.id]) == 0:
          embed = discord.Embed(title="No songs in the queue\n", colour=discord.Colour.dark_purple())

          return await ctx.send(embed=embed)

        embed = discord.Embed(title="Song Queue", description="", colour=discord.Colour.dark_purple())
        i = 1
        for url in self.song_queue[ctx.guild.id]:
            embed.description += f"{i}) {url}\n"

            i += 1

        #embed.set_footer(text="Thanks for using me!")
        await ctx.send(embed=embed)

    @commands.command()
    async def q(self, ctx): # display the current guilds queue
        if len(self.song_queue[ctx.guild.id]) == 0:
          embed = discord.Embed(title="No songs in the queue\n", colour=discord.Colour.dark_purple())

          return await ctx.send(embed=embed)

        embed = discord.Embed(title="Song Queue", description="", colour=discord.Colour.dark_purple())
        i = 1
        for url in self.song_queue[ctx.guild.id]:
            embed.description += f"{i}) {url}\n"

            i += 1

        #embed.set_footer(text="Thanks for using me!")
        await ctx.send(embed=embed)
    


    @commands.command()
    async def skip(self, ctx):
        if ctx.voice_client is None:
          embed = discord.Embed(title="Not playing any song\n", colour=discord.Colour.dark_purple())

          return await ctx.send(embed=embed)

        if ctx.author.voice is None:
          embed = discord.Embed(title="You need to connect a voice channel\n", colour=discord.Colour.dark_purple())

          return await ctx.send(embed=embed)

        if ctx.author.voice.channel.id != ctx.voice_client.channel.id:
          embed = discord.Embed(title="Currently not playing\n", colour=discord.Colour.dark_purple())

          return await ctx.send(embed=embed)

        poll = discord.Embed(title=f"Vote to Skip Song by - {ctx.author.name}#{ctx.author.discriminator}", description="**80% of the voice channel must vote to skip for it to pass.**", colour=discord.Colour.dark_purple())
        poll.add_field(name="Skip", value=":white_check_mark:")
        poll.add_field(name="Stay", value=":no_entry_sign:")
        poll.set_footer(text="Voting ends in 10 seconds.")

        poll_msg = await ctx.send(embed=poll) # only returns temporary message, we need to get the cached message to get the reactions
        poll_id = poll_msg.id

        await poll_msg.add_reaction(u"\u2705") # yes
        await poll_msg.add_reaction(u"\U0001F6AB") # no
        
        await asyncio.sleep(10) # 10 seconds to vote

        poll_msg = await ctx.channel.fetch_message(poll_id)
        
        votes = {u"\u2705": 0, u"\U0001F6AB": 0}
        reacted = []

        for reaction in poll_msg.reactions:
            if reaction.emoji in [u"\u2705", u"\U0001F6AB"]:
                async for user in reaction.users():
                    if user.voice.channel.id == ctx.voice_client.channel.id and user.id not in reacted and not user.bot:
                        votes[reaction.emoji] += 1

                        reacted.append(user.id)

        skip = False

        if votes[u"\u2705"] > 0:
            if votes[u"\U0001F6AB"] == 0 or votes[u"\u2705"] / (votes[u"\u2705"] + votes[u"\U0001F6AB"]) > 0.79: # 80% or higher
                skip = True
                embed = discord.Embed(title="Skip Successful", description="***Voting to skip the current song was succesful, skipping now.***", colour=discord.Colour.dark_purple())

        if not skip:
            embed = discord.Embed(title="Skip Failed", description="*Voting to skip the current song has failed.*\n\n**Voting failed, the vote requires at least 80% of the members to skip.**", colour=discord.Colour.dark_purple())

        embed.set_footer(text="Voting has ended.")

        await poll_msg.clear_reactions()
        await poll_msg.edit(embed=embed)

        if skip:
            ctx.voice_client.stop()
            await self.check_queue(ctx)

    @commands.command()
    async def s(self, ctx):
        if ctx.voice_client is None:
          embed = discord.Embed(title="Not playing any song\n", colour=discord.Colour.dark_purple())

          return await ctx.send(embed=embed)

        if ctx.author.voice is None:
          embed = discord.Embed(title="You need to connect a voice channel\n", colour=discord.Colour.dark_purple())

          return await ctx.send(embed=embed)

        if ctx.author.voice.channel.id != ctx.voice_client.channel.id:
          embed = discord.Embed(title="Currently not playing\n", colour=discord.Colour.dark_purple())

          return await ctx.send(embed=embed)

        else: 
         poll = discord.Embed(title=f"Vote to Skip Song by - {ctx.author.name}#{ctx.author.discriminator}", description="**80% of the voice channel must vote to skip for it to pass.**", colour=discord.Colour.dark_purple())
         poll.add_field(name="Skip", value=":white_check_mark:")
         poll.add_field(name="Stay", value=":no_entry_sign:")
         poll.set_footer(text="Voting ends in 10 seconds.")

         poll_msg = await ctx.send(embed=poll) # only returns temporary message, we need to get the cached message to get the reactions
         poll_id = poll_msg.id

         await poll_msg.add_reaction(u"\u2705") # yes
         await poll_msg.add_reaction(u"\U0001F6AB") # no
        
         await asyncio.sleep(10) # 10 seconds to vote

         poll_msg = await ctx.channel.fetch_message(poll_id)
        
         votes = {u"\u2705": 0, u"\U0001F6AB": 0}
         reacted = []

         for reaction in poll_msg.reactions:
             if reaction.emoji in [u"\u2705", u"\U0001F6AB"]:
                 async for user in reaction.users():
                     if user.voice.channel.id == ctx.voice_client.channel.id and user.id not in reacted and not user.bot:
                         votes[reaction.emoji] += 1

                         reacted.append(user.id)

         skip = False

         if votes[u"\u2705"] > 0:
             if votes[u"\U0001F6AB"] == 0 or votes[u"\u2705"] / (votes[u"\u2705"] + votes[u"\U0001F6AB"]) > 0.79: # 80% or higher
                 skip = True
                 embed = discord.Embed(title="Skip Successful", description="***Voting to skip the current song was succesful, skipping now.***", colour=discord.Colour.dark_purple())

         if not skip:
             embed = discord.Embed(title="Skip Failed", description="*Voting to skip the current song has failed.*\n\n**Voting failed, the vote requires at least 80% of the members to skip.**", colour=discord.Colour.dark_purple())

         embed.set_footer(text="Voting has ended.")

         await poll_msg.clear_reactions()
         await poll_msg.edit(embed=embed)

         if skip:
             ctx.voice_client.stop()
             await self.check_queue(ctx)


    @commands.command()
    async def pause(self, ctx):
        if ctx.voice_client.is_paused():
          embed = discord.Embed(title="Already Paused\n", colour=discord.Colour.dark_purple())

          return await ctx.send(embed=embed)

        ctx.voice_client.pause()
        embed = discord.Embed(title="Paused :pause_button:\n", colour=discord.Colour.dark_purple())

        await ctx.send(embed=embed)

    

    @commands.command()
    async def resume(self, ctx):
        if ctx.voice_client is None:
          embed = discord.Embed(title="Not connected to a voice channel\n", colour=discord.Colour.dark_purple())

          return await ctx.send(embed=embed)

        if not ctx.voice_client.is_paused():
          embed = discord.Embed(title="Already playing a song\n", colour=discord.Colour.dark_purple())

          return await ctx.send(embed=embed)
        
        ctx.voice_client.resume()
        embed = discord.Embed(title="Resumed :play_pause:\n", colour=discord.Colour.dark_purple())

        await ctx.send(embed=embed)

async def setup():
    await bot.wait_until_ready()
    bot.add_cog(Player(bot))

bot.loop.create_task(setup())

@bot.event
async def on_ready():
    print('Hi!')

    await bot.change_presence(status =discord.Status.dnd)

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="WRLD999 ⚰️"))

keep_alive()
bot.run(Token)
