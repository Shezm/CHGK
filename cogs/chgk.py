from .utils import checks
from .utils.dataIO import fileIO
from discord.ext import commands
from PIL import Image, ImageFont, ImageDraw
from random import choice
from random import randint
import __main__
import aiohttp
import asyncio
import discord
import os
import os.path
import random
import time

try:
    if not discord.opus.is_loaded():
        discord.opus.load_opus('libopus-0.dll')
except OSError: # Incorrect bitness
    opus = False
except: # Missing opus
    opus = None
else:
    opus = True

main_path = os.path.dirname(os.path.realpath(__main__.__file__))

operators = ('testing', 'Jürgen', 'adinadinadin')

class Audio:
    """Music streaming."""

    def __init__(self, bot):
        self.bot = bot
        self.music_player = EmptyPlayer()
        self.settings = fileIO("data/audio/settings.json", "load")

class EmptyPlayer(): #dummy player
    def __init__(self):
        self.paused = False

    def stop(self):
        pass

    def is_playing(self):
        return False

class Chgk:
    """Chgk commands."""

    def __init__(self, bot):
        self.audio = Audio(bot)
        self.bot = bot
        self.channel = None
        self.voice_channel = None

    @commands.command()
    async def volume(self, level : float):
        """Sets the volume (0-1)"""
        if level >= 0 and level <= 1:
            self.audio.settings["VOLUME"] = level
            await self.bot.say("Volume is now set at " + str(level) + ". It will take effect after the current track.")
            fileIO("data/audio/settings.json", "save", self.audio.settings)
        else:
            await self.bot.say("Volume must be between 0 and 1. Example: 0.40")

    @commands.command(pass_context=True, no_pm=False)
    async def score(self, ctx, left:str, right:str):
        '''Число число (пример: score 4 3) - выдаёт табло со счётом'''
        if not str(ctx.message.author).split('#')[0] in operators:
            await self.bot.send_message(ctx.message.author,"You are not allowed")
            return
        if not self.bot.is_voice_connected():
            await self.bot.say("You you need to summon bot first")
            return

        left=left[0]; right=right[0]
        if left.isdigit() and right.isdigit():
            fnt = ImageFont.truetype(main_path + '/resources/OpenSans-Bold.ttf', 225)
            img = Image.new('RGB', (300, 300))
            line = ImageDraw.Draw(img)
            line.line((0, 0) + (0, 300), fill=(15, 100, 250), width=300)
            line.line((300, 0) + (300, 300), fill=(255, 255, 255), width=300)
            imgDrawer = ImageDraw.Draw(img)
            imgDrawer.text((10, 0), left, font=fnt)
            imgDrawer.text((162, 0), right, font=fnt, fill=(15, 100, 250))
            img.save(main_path + "/resources/score.png")
            await self.bot.send_file(self.channel, main_path + '/resources/score.png')
            mus = random.choice(os.listdir(main_path + "/resources/chgk/music"))
            self.audio.music_player.stop()
            self.audio.music_player = self.audio.bot.voice.create_ffmpeg_player(main_path + "/resources/chgk/music/" + mus, options='''-filter:a "volume={}"'''.format(self.audio.settings["VOLUME"]))
            self.audio.music_player.paused = False
            self.audio.music_player.start()

    @commands.command(pass_context=True, no_pm=False)
    async def start(self, ctx):
        '''Запускает игру, начальную заставку'''
        if not str(ctx.message.author).split('#')[0] in operators:
            await self.bot.send_message(ctx.message.author,"You are not allowed")
            return
        if not self.bot.is_voice_connected():
            await self.bot.say("You you need to summon bot first")
            return

        await self.bot.send_file(self.channel, main_path + '/resources/chgk/WhatWhereWhen.png')
        self.audio.music_player.stop()
        self.audio.music_player = self.audio.bot.voice.create_ffmpeg_player(main_path + "/resources/chgk/nachalo.mp3", options='''-filter:a "volume={}"'''.format(self.audio.settings["VOLUME"]))
        self.audio.music_player.start()
        while True:
            if not self.audio.music_player.is_playing():
                self.audio.music_player.stop()
                self.audio.music_player = self.audio.bot.voice.create_ffmpeg_player(main_path + "/resources/chgk/Thus_Sprach_Zarathustra.mp3", options='''-filter:a "volume={}"'''.format(self.audio.settings["VOLUME"]))
                self.audio.music_player.paused = False
                self.audio.music_player.start()
                break
            await asyncio.sleep(1)

    @commands.command(aliases="1", pass_context=True, no_pm=False)
    async def volchok(self, ctx):
        '''(1) - Запускает волчок'''
        if not str(ctx.message.author).split('#')[0] in operators:
            await self.bot.send_message(ctx.message.author,"You are not allowed")
            return
        if not self.bot.is_voice_connected():
            await self.bot.say("You you need to summon bot first")
            return

        await self.bot.send_file(self.channel, main_path + '/resources/chgk/ruletka.jpg')
        self.audio.music_player.stop()
        self.audio.music_player = self.audio.bot.voice.create_ffmpeg_player(main_path + "/resources/chgk/Volchok.mp3", options='''-filter:a "volume={}"'''.format(self.audio.settings["VOLUME"]))
        self.audio.music_player.paused = False
        self.audio.music_player.start()

    @commands.command(pass_context=True, no_pm=False)
    async def blackbox(self, ctx):
        '''Выносит чёрный ящик'''
        if not str(ctx.message.author).split('#')[0] in operators:
            await self.bot.send_message(ctx.message.author,"You are not allowed")
            return
        if not self.bot.is_voice_connected():
            await self.bot.say("You you need to summon bot first")
            return

        await self.bot.send_file(self.channel, main_path + '/resources/chgk/BlackBox.jpg')
        self.audio.music_player.stop()
        self.audio.music_player = self.audio.bot.voice.create_ffmpeg_player(main_path + "/resources/chgk/Ra-ta-ta.mp3", options='''-filter:a "volume={}"'''.format(self.audio.settings["VOLUME"]))
        self.audio.music_player.paused = False
        self.audio.music_player.start()

    @commands.command(aliases="2", pass_context=True, no_pm=False)
    async def gong(self, ctx):
        '''(2) - бьёт гонг'''
        if not str(ctx.message.author).split('#')[0] in operators:
            await self.bot.send_message(ctx.message.author,"You are not allowed")
            return
        if not self.bot.is_voice_connected():
            await self.bot.say("You you need to summon bot first")
            return

        self.audio.music_player.stop()
        self.audio.music_player = self.audio.bot.voice.create_ffmpeg_player(main_path + "/resources/chgk/gong.mp3", options='''-filter:a "volume={}"'''.format(self.audio.settings["VOLUME"]))
        self.audio.music_player.paused = False
        self.audio.music_player.start()

    @commands.command(aliases="3", pass_context=True, no_pm=False)
    async def timer(self, ctx):
        '''(3) - запускает таймер'''
        if not str(ctx.message.author).split('#')[0] in operators:
            await self.bot.send_message(ctx.message.author,"You are not allowed")
            return
        if not self.bot.is_voice_connected():
            await self.bot.say("You you need to summon bot first")
            return

        self.audio.music_player.stop()
        self.audio.music_player = self.audio.bot.voice.create_ffmpeg_player(main_path + "/resources/chgk/Signal_2.mp3", options='''-filter:a "volume={}"'''.format(self.audio.settings["VOLUME"]))
        self.audio.music_player.paused = False
        self.audio.music_player.start()
        await asyncio.sleep(70)
        self.audio.music_player.stop()
        self.audio.music_player = self.audio.bot.voice.create_ffmpeg_player(main_path + "/resources/chgk/Signal_1.mp3", options='''-filter:a "volume={}"'''.format(self.audio.settings["VOLUME"]))
        self.audio.music_player.paused = False
        self.audio.music_player.start()
        await asyncio.sleep(10)
        self.audio.music_player.stop()
        self.audio.music_player = self.audio.bot.voice.create_ffmpeg_player(main_path + "/resources/chgk/Signal_2.mp3", options='''-filter:a "volume={}"'''.format(self.audio.settings["VOLUME"]))
        self.audio.music_player.paused = False
        self.audio.music_player.start()

    @commands.command(aliases="s", pass_context=True, no_pm=False)
    async def stop(self, ctx):
        '''(s) - оставливает любые звуки'''
        if not str(ctx.message.author).split('#')[0] in operators:
            await self.bot.send_message(ctx.message.author,"You are not allowed")
            return

        self.audio.music_player.stop()

    @commands.command(pass_context=True, no_pm=False)
    async def sich(self, ctx):
        '''Под эту команду выносят хрустального сыча'''
        if not str(ctx.message.author).split('#')[0] in operators:
            await self.bot.send_message(ctx.message.author,"You are not allowed")
            return
        if not self.bot.is_voice_connected():
            await self.bot.say("You you need to summon bot first")
            return

        self.audio.music_player.stop()
        self.audio.music_player = self.audio.bot.voice.create_ffmpeg_player(main_path + "/resources/chgk/Homage_To_The_Mountain.mp3", options='''-filter:a "volume={}"'''.format(self.audio.settings["VOLUME"]))
        self.audio.music_player.paused = False
        self.audio.music_player.start()

    @commands.command(aliases="w",pass_context=True, no_pm=False)
    async def win(self, ctx, left:str, right:str):
        '''Число число (пример: win 6 0) - выдаёт табло с победной картинкой'''
        if not str(ctx.message.author).split('#')[0] in operators:
            await self.bot.send_message(ctx.message.author,"You are not allowed")
            return
        if not self.bot.is_voice_connected():
            await self.bot.say("You you need to summon bot first")
            return

        left=left[0]; right=right[0]
        await self.bot.send_message(self.channel, "**Победила команда знатоков со счетом {}:{}!**".format(left, right))
        fnt = ImageFont.truetype(main_path + '/resources/OpenSans-Bold.ttf', 225)
        img = Image.new('RGB', (300, 300))
        line = ImageDraw.Draw(img)
        line.line((0, 0) + (0, 300), fill=(15, 100, 250), width=300)
        line.line((300, 0) + (300, 300), fill=(255, 255, 255), width=300)
        imgDrawer = ImageDraw.Draw(img)
        imgDrawer.text((10, 0), left, font=fnt)
        imgDrawer.text((162, 0), right, font=fnt, fill=(15, 100, 250))
        img.save(main_path + "/resources/score.png")
        await self.bot.send_file(self.channel, main_path + '/resources/score.png')
        img = random.choice(os.listdir(main_path + "/resources/chgk/win"))
        await self.bot.send_file(self.channel, main_path + '/resources/chgk/win/' + img)
        self.audio.music_player.stop()
        self.audio.music_player = self.audio.bot.voice.create_ffmpeg_player(main_path + "/resources/chgk/Dance_Macabre.mp3", options='''-filter:a "volume={}"'''.format(self.audio.settings["VOLUME"]))
        self.audio.music_player.paused = False
        self.audio.music_player.start()

    @commands.command(aliases="l", pass_context=True, no_pm=False)
    async def lose(self, ctx, left:str, right:str):
        '''Число число (пример: lose 0 6) - выдаёт табло с проигрышной картинкой'''
        if not str(ctx.message.author).split('#')[0] in operators:
            await self.bot.send_message(ctx.message.author,"You are not allowed")
            return
        if not self.bot.is_voice_connected():
            await self.bot.say("You you need to summon bot first")
            return

        left=left[0]; right=right[0]
        await self.bot.send_message(self.channel, "**Победила команда телезрителей со счетом {}:{}!**".format(left, right))
        fnt = ImageFont.truetype(main_path + '/resources/OpenSans-Bold.ttf', 225)
        img = Image.new('RGB', (300, 300))
        line = ImageDraw.Draw(img)
        line.line((0, 0) + (0, 300), fill=(15, 100, 250), width=300)
        line.line((300, 0) + (300, 300), fill=(255, 255, 255), width=300)
        imgDrawer = ImageDraw.Draw(img)
        imgDrawer.text((10, 0), left, font=fnt)
        imgDrawer.text((162, 0), right, font=fnt, fill=(15, 100, 250))
        img.save(main_path + "/resources/score.png")
        await self.bot.send_file(self.channel, main_path + '/resources/score.png')
        img = random.choice(os.listdir(main_path + "/resources/chgk/lose"))
        await self.bot.send_file(self.channel, main_path + '/resources/chgk/lose/' + img)
        self.audio.music_player.stop()
        self.audio.music_player = self.audio.bot.voice.create_ffmpeg_player(main_path + "/resources/chgk/Dance_Macabre.mp3", options='''-filter:a "volume={}"'''.format(self.audio.settings["VOLUME"]))
        self.audio.music_player.paused = False
        self.audio.music_player.start()

    @commands.command(pass_context=True, no_pm=False)
    async def muzika(self, ctx):
        '''Музыкальная пауза, джаз'''
        if not str(ctx.message.author).split('#')[0] in operators:
            await self.bot.send_message(ctx.message.author,"You are not allowed")
            return
        if not self.bot.is_voice_connected():
            await self.bot.say("You you need to summon bot first")
            return

        await self.bot.send_file(self.channel, main_path + '/resources/chgk/music.png')
        self.audio.music_player.stop()
        self.audio.music_player = self.audio.bot.voice.create_ffmpeg_player("http://181fm-edge1.cdnstream.com/181-classicaljazz_128k.mp3", use_avconv=True, options='''-filter:a "volume={}"'''.format(self.audio.settings["VOLUME"]))
        self.audio.music_player.paused = False
        self.audio.music_player.start()

    @commands.command(pass_context=True, no_pm=False)
    async def endgame(self, ctx):
        '''Заканчивает игру, финальная музыка'''
        if not str(ctx.message.author).split('#')[0] in operators:
            await self.bot.send_message(ctx.message.author,"You are not allowed")
            return
        if not self.bot.is_voice_connected():
            await self.bot.say("You you need to summon bot first")
            return

        await self.bot.send_file(self.channel, main_path + '/resources/chgk/WhatWhereWhen.png')
        self.audio.music_player.stop()
        self.audio.music_player = self.audio.bot.voice.create_ffmpeg_player(main_path + "/resources/chgk/Max_Greger__Orchestra_-_Serenade_In_Blue.mp3", options='''-filter:a "volume={}"'''.format(self.audio.settings["VOLUME"]))
        self.audio.music_player.paused = False
        self.audio.music_player.start()

    @commands.command(pass_context=True, no_pm=False)
    async def joinserver(self, ctx, server_link=None):
        '''Приглашает бота на сервер'''
        if not str(ctx.message.author).split('#')[0] in operators:
            await self.bot.send_message(ctx.message.author,"You are not allowed")
            return

        try:
            await self.bot.accept_invite(server_link)
            await self.bot.say('Подключился по ссылке %s' % (server_link))
        except Exception:
            await self.bot.say('Подключиться не удалось')

    @commands.command(pass_context=True, no_pm=True)
    async def listids(self, ctx):
        '''Даёт список ID каналов (для программистов)'''
        if not str(ctx.message.author).split('#')[0] in operators:
            await self.bot.send_message(ctx.message.author,"You are not allowed")
            return

        data = ['**Your ID**: %s' % ctx.message.author.id]
        rawudata = None

        data.append("\n**Text Channel IDs**: ")
        tchans = [c for c in ctx.message.author.server.channels if c.type == discord.ChannelType.text]
        rawudata = ['%s: %s ' % (c.name, c.id) for c in tchans]

        rawudata.append("\n**Voice Channel IDs**: ")
        vchans = [c for c in ctx.message.author.server.channels if c.type == discord.ChannelType.voice]
        rawudata.extend('%s: %s ' % (c.name, c.id) for c in vchans)

        if rawudata: data.extend(rawudata)
        await self.bot.say(''.join(data))

    @commands.command(pass_context=True, no_pm=True)
    async def summon(self, ctx):
        '''Приглашает бота в голосовой канал'''
        if not str(ctx.message.author).split('#')[0] in operators:
            await self.bot.send_message(ctx.message.author,"You are not allowed")
            return

        self.voice_channel = discord.Object(id=ctx.message.author.voice_channel.id)
        self.channel = discord.Object(ctx.message.channel.id)

        if self.bot.is_voice_connected():
            await self.bot.voice.disconnect()
        await self.bot.join_voice_channel(self.voice_channel)
        await self.bot.say('Бот подключился к voice каналу')

def setup(bot):
    bot.add_cog(Chgk(bot))
