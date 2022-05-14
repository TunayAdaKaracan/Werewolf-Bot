import discord
from discord.ext import commands
import asyncpg
import asyncio
import random

open_instances = []


class Sheriff(discord.ui.View):
    def __init__(self, game):
        super().__init__(timeout=None)
        self.game = game

    async def send_message(self, button, interaction, id):
        if self.game.round != "Day":
            await interaction.response.send_message("Geceyken Kullanıcı Öldüremezsin!")
            return
        if self.game.users[id]["alive"] != "yes":
            await interaction.user.send("Bu Kullanıcı Çoktan Ölmüş!")
            button.disabled = True
            await interaction.response.edit_message(view=self)
        else:
            filtered = list(filter(lambda key: self.game.users[key]["id"] == interaction.user.id, list(
                self.game.users.keys())))[0]
            if self.game.users[filtered]["alive"] != "yes":
                await interaction.response.send_message("Bu Oyunda Çoktan Ölmüşsün!")
                return
            for item in self.children:
                item.disabled = True
                item.style = discord.ButtonStyle.green
            await interaction.response.edit_message(content=f"{id} ID'li Kişiyi Öldürüyorum", view=self)
            #await self.game.sheriff_kill_user(filtered, id)
            self.stop()

    def close_buttons(self):
        for item in self.children:
            item.disabled = True
            item.style = discord.ButtonStyle.green

    @discord.ui.button(label="Öldür: 1", style=discord.ButtonStyle.blurple, row=0)
    async def kill_1(self, button, interaction):
        await self.send_message(button, interaction, 1)

    @discord.ui.button(label="Öldür: 2", style=discord.ButtonStyle.blurple, row=0)
    async def kill_2(self, button, interaction):
        await self.send_message(button, interaction, 2)

    @discord.ui.button(label="Öldür: 3", style=discord.ButtonStyle.blurple, row=0)
    async def kill_3(self, button, interaction):
        await self.send_message(button, interaction, 3)

    @discord.ui.button(label="Öldür: 4", style=discord.ButtonStyle.blurple, row=0)
    async def kill_4(self, button, interaction):
        await self.send_message(button, interaction, 4)

    @discord.ui.button(label="Öldür: 5", style=discord.ButtonStyle.blurple, row=1)
    async def kill_5(self, button, interaction):
        await self.send_message(button, interaction, 5)

    @discord.ui.button(label="Öldür: 6", style=discord.ButtonStyle.blurple, row=1)
    async def kill_6(self, button, interaction):
        await self.send_message(button, interaction, 6)

    @discord.ui.button(label="Öldür: 7", style=discord.ButtonStyle.blurple, row=1)
    async def kill_7(self, button, interaction):
        await self.send_message(button, interaction, 7)

    @discord.ui.button(label="Öldür: 8", style=discord.ButtonStyle.blurple, row=1)
    async def kill_8(self, button, interaction):
        await self.send_message(button, interaction, 8)

    @discord.ui.button(label="Öldür: 9", style=discord.ButtonStyle.blurple, row=2)
    async def kill_9(self, button, interaction):
        await self.send_message(button, interaction, 9)

    @discord.ui.button(label="Öldür: 10", style=discord.ButtonStyle.blurple, row=2)
    async def kill_10(self, button, interaction):
        await self.send_message(button, interaction, 10)

    @discord.ui.button(label="Öldür: 11", style=discord.ButtonStyle.blurple, row=2)
    async def kill_11(self, button, interaction):
        await self.send_message(button, interaction, 11)

    @discord.ui.button(label="Öldür: 12", style=discord.ButtonStyle.blurple, row=2)
    async def kill_12(self, button, interaction):
        await self.send_message(button, interaction, 12)

    @discord.ui.button(label="Öldür: 13", style=discord.ButtonStyle.blurple, row=3)
    async def kill_13(self, button, interaction):
        await self.send_message(button, interaction, 13)

    @discord.ui.button(label="Öldür: 14", style=discord.ButtonStyle.blurple, row=3)
    async def kill_14(self, button, interaction):
        await self.send_message(button, interaction, 14)

    @discord.ui.button(label="Öldür: 15", style=discord.ButtonStyle.blurple, row=3)
    async def kill_15(self, button, interaction):
        await self.send_message(button, interaction, 15)

    @discord.ui.button(label="Öldür: 16", style=discord.ButtonStyle.blurple, row=3)
    async def kill_16(self, button, interaction):
        await self.send_message(button, interaction, 16)


class Game:
    def __init__(self, client, lobby_id, ctx):
        self.client = client
        self.votes = {}
        self.users = {}
        self.vote_message = None
        self.round = "Day"
        self.jobs_obj_list = {Sheriff(self): None}
        self.jobs_obj = {"Villager": None, "Seer": None, "Fool": None, "Hunter": None, "Sheriff": list(
            self.jobs_obj_list)[0], "Werewolf": None, "Priest": None, "Apprentice Seer": None}
        #self.jobs = {"Villager": {"max": 7,"given":0,"mission":"Kurtadamları Ve Kötü Rollü Kişileri Asarak Kazanmak."},"Seer":{"max":1,"given":0,"mission":"Geceleri Bir Kullanıcının Rolüne Bakarak Köylülere Bilgi Vermek"},"Fool":{"max":1,"given":0,"mission":"Kensini Astırmak"},"Hunter":{"max":1,"given":0,"mission":"Hedefini Astırmak"},"Sheriff":{"max":1,"given":0,"mission":"Kurt Adamları Birkere Silahla Vurma Hakkın Var. Onun Dışında Normal Köylüsün"},"Werewolf":{"max":3,"given":0,"mission": "Köylüleri Geceleri Öldürerek Kazanmak"}, "Priest":{"max":1,"given":0,"mission":"Zemzem Suyunu Bir Kullanıcıya Atarsın. Kullanıcı Bir Kurtadamsa Ölür. Eğer Değilse Sen Ölürsün"}, "Apprentice Seer":{"max":1,"given":0,"mission":"Geceleri Oyuncuların Auralarına Bakabilirsin"}}
        self.jobs = {"Villager": {"max": 0, "given": 0, "mission": "Kurtadamları Ve Kötü Rollü Kişileri Asarak Kazanmak."}, "Seer": {"max": 0, "given": 0, "mission": "Geceleri Bir Kullanıcının Rolüne Bakarak Köylülere Bilgi Vermek"}, "Fool": {"max": 0, "given": 0, "mission": "Kensini Astırmak"}, "Hunter": {"max": 0, "given": 0, "mission": "Hedefini Astırmak"}, "Sheriff": {"max": 0, "given": 0,
                                                                                                                                                                                                                                                                                                                                                                                       "mission": "Kurt Adamları Birkere Silahla Vurma Hakkın Var. Onun Dışında Normal Köylüsün"}, "Werewolf": {"max": 2, "given": 0, "mission": "Köylüleri Geceleri Öldürerek Kazanmak"}, "Priest": {"max": 0, "given": 0, "mission": "Zemzem Suyunu Bir Kullanıcıya Atarsın. Kullanıcı Bir Kurtadamsa Ölür. Eğer Değilse Sen Ölürsün"}, "Apprentice Seer": {"max": 0, "given": 0, "mission": "Geceleri Oyuncuların Auralarına Bakabilirsin"}}
        self.timer = 12
        self.vote_time = 10
        self.lobby_id = lobby_id
        self.ctx = ctx
        self.task = None
        self.task2 = None
        self.game_ended = False

    async def day_manager(self, day):
        if self.game_ended == True:
            return
        if day == "night":
            self.round = "Night"
            await self.make_night()
        else:
            self.round = "Day"
            await self.make_day()

    async def start_game(self, players):
        if self.game_ended == True:
            return
        open_instances.append(self)
        for member in players:
            remains = list(filter(
                lambda key: self.jobs[key]["max"] != self.jobs[key]["given"], list(self.jobs.keys())))
            job = random.choice(remains)
            self.jobs[job]["given"] += 1
            self.users[players.index(
                member)+1] = {"Job": job, "alive": "yes", "id": member.id}
        for i in range(1, len(list(self.users.keys()))+1):
            self.votes[i] = []
        await self.send_start_message()
        await self.day_manager("day")

    async def send_start_message(self):
        if self.game_ended == True:
            return
        embed = discord.Embed(title="Rolün...", color=discord.Colour.blurple())
        hunter = list(
            filter(lambda key: self.users[key]["Job"] == "Hunter", list(self.users.keys())))
        if len(hunter) != 0:
            hunter = hunter[0]
            potential_hunts = list(filter(
                lambda key: self.users[key]["Job"] != "Fool" and self.users[key]["Job"] != "Hunter", list(self.users.keys())))
            hunt = random.choice(potential_hunts)
            self.users[hunter]["hunt"] = hunt
        for user in list(self.users.keys()):
            id = 'id'
            job = 'Job'
            işler = self.users[user]["Job"].replace('Villager', 'Köylü').replace('Seer', 'Gözcü').replace('Fool', 'Soytarı').replace('Hunter', 'Kelle Avcısı').replace(
                'Sheriff', 'Silahşör').replace('Werewolf', 'Kurtadam').replace('Priest', 'İmam').replace('Apprentice Gözcü', 'Aura Gözcüsü')
            xd = ' '.join(map(lambda item: str(self.ctx.guild.get_member(self.users[item]['id'])), list(
                filter(lambda key: self.users[key]['Job'] == 'Werewolf', list(self.users.keys())))))
            embed.description = f"ID (Numaran): {user}\n**Rolün**: {işler}\n\n**Görevin**: {self.jobs[self.users[user]['Job']]['mission']}\n{f'**Hedefin**: {str(self.ctx.guild.get_member(self.users[hunt][id]))}' if self.users[user][job] == 'Hunter' else ''}{f'**Arkadaşların**: {xd}' if self.users[user]['Job'] == 'Werewolf' else ''}"
            member = self.ctx.guild.get_member(self.users[user]["id"])
            await member.send(embed=embed)
            if self.jobs_obj[self.users[user]["Job"]] != None:
                if isinstance(self.jobs_obj[self.users[user]["Job"]], Sheriff):
                    msg = await member.send("Vurmak İstediğin Kullanıcıyı Seç!", view=self.jobs_obj[self.users[user]["Job"]])
                self.jobs_obj_list[self.jobs_obj[self.users[user]["Job"]]] = msg

    async def make_day(self):
        if self.game_ended == True:
            return
        embed = discord.Embed(
            title="Oyuncular", color=discord.Colour.blurple())
        for member in self.users:
            işler = self.users[member]["Job"].replace('Villager', 'Köylü').replace('Seer', 'Gözcü').replace('Fool', 'Soytarı').replace('Hunter', 'Kelle Avcısı').replace(
                'Sheriff', 'Silahşör').replace('Werewolf', 'Kurtadam').replace('Priest', 'İmam').replace('Apprentice Gözcü', 'Aura Gözcüsü')
            embed.add_field(
                name=f"ID: {member}", value=f"Ad: {str(self.ctx.guild.get_member(self.users[member]['id']))}\nYaşıyor: {'<a:yasir:864474264681971722>' if self.users[member]['alive'] == 'yes' else '<a:yasamir:864474264857346048>'}\n{f'Mesleği: {işler}' if self.users[member]['alive'] != 'yes' else ''}")
        embed.set_footer(
            text=f"Lobi: {self.lobby_id}", icon_url="https://cdn.discordapp.com/avatars/845659385980256276/cad9f3ca6cc9fd4492e5aa7a637e3262.webp?size=1024")
        if self.game_ended == True:
            return
        await self.ctx.send(f"Gün Başladı!\n`{self.timer}` Saniyelik Konuşma Süreniz Başladı", embed=embed)
        while self.timer != 0:
            await asyncio.sleep(1)
            self.timer -= 1
        self.timer = 12
        embed = discord.Embed(title="Oylama", color=discord.Colour.blurple())
        for key in list(self.users.keys()):
            member = self.ctx.guild.get_member(self.users[key]["id"])
            embed.add_field(name=f"{key} : {str(member)}", value="Oylayan Yok")
        if self.game_ended == True:
            return
        self.vote_message = await self.ctx.send(f"Konuşma Süreniz Bitti!\n`{self.vote_time}` Saniyelik Oylama Süreniz Başladı\n`ww.oyla {{ID}}` Yazarak Oylayabilirsiniz", embed=embed)
        await self.vote_message.pin()

        async def timer_counter():
            while self.vote_time != 0:
                if self.game_ended == True:
                    return
                await asyncio.sleep(1)
                self.vote_time -= 1

        async def wait_msg():
            while self.vote_time != 0:
                if self.game_ended == True:
                    return
                try:
                    command_msg = await self.client.wait_for("message", check=lambda m: m.guild == self.ctx.guild, timeout=1)
                except:
                    continue
                if command_msg.content.startswith("ww.oyla"):
                    args = command_msg.content.split(" ")
                    sender = list(filter(
                        lambda key: self.users[key]["id"] == command_msg.author.id, list(self.users.keys())))
                    if len(sender) == 0:
                        await command_msg.reply("Sen Bu Oyunda Değilsin!")
                        continue
                    if len(args) == 1:
                        await command_msg.reply("Lütfen Bir Kullanıcı ID Belirtin")
                        continue
                    if args[1].isdigit() == False:
                        await command_msg.reply("Lütfen Bir Kullanıcı ID Giriniz")
                        continue
                    filtered = list(filter(lambda key: int(
                        args[1]) == key, list(self.users.keys())))
                    if len(filtered) == 0:
                        await command_msg.reply("Böyle Bir Kullanıcı Bulunmamakta")
                        continue
                    filtered = filtered[0]
                    if self.users[filtered]["alive"] != "yes":
                        await command_msg.reply("Bu Kullanıcı Yaşamamakta")
                        continue
                    if self.users[sender[0]]["alive"] != "yes":
                        await command_msg.reply("Bu Oyunda Yaşamıyorsun")
                        continue
                    if filtered == sender[0]:
                        await command_msg.reply("Kendine Oy Veremezsin.")
                        continue
                    member = self.ctx.guild.get_member(
                        self.users[filtered]["id"])
                    await self.vote_user(sender[0], filtered, command_msg)
        self.task = self.client.loop.create_task(timer_counter())
        self.task2 = self.client.loop.create_task(wait_msg())
        await self.task2
        if self.game_ended == True:
            return
        self.vote_time = 10
        self.task = None
        self.task2 = None
        await self.vote_message.unpin()
        self.vote_message = None
        max = -1
        asilcak = -1
        for item in list(self.votes.keys()):
            if len(self.votes[item]) > max and len(self.votes[item]) != 0:
                max = len(self.votes[item])
                asilcak = item
            elif len(self.votes[item]) == max:
                max = "ASILMICAK"
                asilcak = max
                break
            else:
                continue
        if asilcak == "ASILMICAK" or asilcak == -1:
            await self.ctx.send("Oylama Süresi Bitti!!\n\nOylar Eşit Çıktı Kimse Asılmıcak!")
            await self.day_manager("night")
        else:
            await self.vote_kill(asilcak)
            await self.day_manager("night")

    async def make_night(self):
        werewolfs = list(filter(
            lambda key: self.users[key]["Job"] == "Werewolf", list(self.users.keys())))
        werewolf_players = list(
            map(lambda item: self.ctx.guild.get_member(self.users[item]['id']), werewolfs))
        for user_id in werewolfs:
            member = self.ctx.guild.get_member(self.users[user_id]["id"])
            await member.send(f"{self.timer} Saniyelik Konuşma Süreniz Başladı,Burdan Birbirinizle Konuşabilirsiniz")

        async def timer_counter(tur):
            if tur == "konuşma":
                while self.timer != 0:
                    if self.game_ended == True:
                        return
                    await asyncio.sleep(1)
                    self.timer -= 1
            else:
                while self.vote_time != 0:
                    if self.game_ended == True:
                        return
                    await asyncio.sleep(1)
                    self.vote_time -= 1

        async def wait_msg():
            while self.timer != 0:
                if self.game_ended == True:
                    return
                try:
                    msg = await self.client.wait_for("message", check=lambda m: isinstance(m.channel, discord.DMChannel) and len(list(filter(lambda key: self.users[key]["id"] == m.author.id, list(self.users.keys())))) != 0 and list(filter(lambda key: self.users[key]["id"] == m.author.id, list(self.users.keys())))[0] in werewolfs)
                except:
                    continue
                for player in werewolf_players:
                    if player == msg.author:
                        continue
                    await player.send(f"[{str(msg.author)}]: {msg.content}")

        self.task1 = self.client.loop.create_task(timer_counter("konuşma"))
        self.task2 = self.client.loop.create_task(wait_msg())
        await self.task2
        if self.game_ended == True:
            return
        self.task = None
        self.task2 = None
        self.timer = 12
        for player in werewolf_players:
            await player.send(f"Konuşma Süreniz Bitti!\n{self.vote_time} Saniyelik Oylama Süreniz Başladı!")
        embed = discord.Embed(title="Oylama", color=discord.Colour.blurple())
        for key in list(self.users.keys()):
            member = self.ctx.guild.get_member(self.users[key]["id"])
            embed.add_field(name=f"{key} : {str(member)}", value="Oylayan Yok")
        for player in werewolf_players:
            await player.send(embed=embed)
        self.task1 = self.client.loop.create_task(timer_counter(""))
        self.task2 = self.client.loop.create_task(wait_msg())

    async def vote_kill(self, user_key):
        if self.game_ended == True:
            return
        werewolfs = list(filter(
            lambda key: self.users[key]["Job"] == "Werewolf" and self.users[key]["alive"] == "yes", list(self.users.keys())))
        self.users[user_key]["alive"] = "no"
        köylüler = list(filter(
            lambda key: key not in werewolfs and self.users[key]["alive"] == "yes", list(self.users.keys())))
        hunter_filter = list(
            filter(lambda key: self.users[key]["Job"] == "Hunter", list(self.users.keys())))
        if len(hunter_filter) != 0:
            hunter = self.users[hunter_filter[0]]
        else:
            hunter = None
        await self.ctx.send(f"Oylama Süresi Bitti!!\n\n{str(self.ctx.guild.get_member(self.users[user_key]['id']))} Kullanıcısı Asılıyor...\nMesleği: {self.users[user_key]['Job'].replace('Villager','Köylü').replace('Seer', 'Gözcü').replace('Fool', 'Soytarı').replace('Hunter','Kelle Avcısı').replace('Sheriff','Silahşör').replace('Werewolf','Kurtadam').replace('Priest','İmam').replace('Apprentice Gözcü','Aura Gözcüsü')}")
        if hunter != None and hunter["hunt"] == user_key:
            await self.close("Kelle Avcısı")
        elif self.users[user_key]['Job'] == "Fool":
            await self.close("Soytarı")
        elif len(werewolfs) >= len(köylüler):
            await self.close("Kurt Adamlar")

    async def kill_user(self, killer, kill):
        await self.ctx.send("Öldüüüü")

    async def vote_user(self, voter, voted, command_msg):
        filtered = list(
            filter(lambda key: voter in self.votes[key], list(self.votes.keys())))
        kaldırma = False
        oylanan = self.ctx.guild.get_member(self.users[list(
            filter(lambda key: key == voted, list(self.users.keys())))[0]]['id'])
        if len(filtered) != 0:
            if filtered[0] == voted:
                kaldırma = True
                self.votes[filtered[0]].remove(voter)
                await command_msg.reply(f"`{str(oylanan)}` Kullanıcısına Olan Oyunu Geri Aldın")
            else:
                self.votes[filtered[0]].remove(voter)
        if kaldırma != True:
            self.votes[voted].append(voter)
        # {1: [3,5,7,8], 2:[4,6]}
        embed = discord.Embed(title="Oylama", color=discord.Colour.blurple())
        for key in list(self.users.keys()):
            member = self.ctx.guild.get_member(self.users[key]["id"])
            others = []
            for item in self.votes[key]:
                others.append(self.ctx.guild.get_member(
                    self.users[item]["id"]))
            embed.add_field(name=f"{key} : {str(member)}", value=' '.join(
                list(map(lambda m: m.mention, others))) if len(others) != 0 else "Oylayan Yok")
        if kaldırma != True:
            await command_msg.reply(f"`{str(oylanan)}` Kullanıcısına Başarıyla Oy Verdin!")
        await self.vote_message.edit(embed=embed)

    async def close(self, kazananlar):
        self.game_ended = True
        open_instances.remove(self)
        if self.task != None and self.task2 != None:
            self.task.cancel()
            self.task2.cancel()
        for instance in list(self.jobs_obj_list):
            instance.close_buttons()
            if self.jobs_obj_list[instance] != None:
                await self.jobs_obj_list[instance].edit(view=instance)
            instance.stop()
        await self.ctx.send(f"Oyun Bitti!!!\n\n**Kazanan**: {kazananlar}")
        async with self.client.pool.acquire() as con:
            await con.execute(f"update lobby set players=$1,players_count='0',status='empty' where server_id='{self.ctx.guild.id}' and lobby_id='{self.lobby_id}'", [])
        return

    async def force_shutdown(self):
        await self.ctx.send("|---------------------\n|\n|\n|\n|           Botun Bakıma Girmesi Nedeniyle Tüm Oyunlar Kapatıldı\n|\n|\n|\n|---------------------")
        self.game_ended = True
        if self.task != None and self.task2 != None:
            self.task.cancel()
            self.task2.cancel()
        for instance in list(self.jobs_obj_list):
            instance.close_buttons()
            if self.jobs_obj_list[instance] != None:
                await self.jobs_obj_list[instance].edit(view=instance)
            instance.stop()
        return


class Lobbys(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="force-shutdown", aliases=["fc-sh"])
    async def force_shutdown(self, ctx):
        if ctx.author.id != 711460493352632351:
            await ctx.send("Bu Komutu Sadece Yapımcım Kullanabilir")
            return
        msg = await ctx.send(f"Oyunlar Kapatılıyor ({len(open_instances)}) Adet.... <a:yasamir:864474264857346048>\nLobiler Temizleniyor.... <a:yasamir:864474264857346048>\nBot Kapatılıyor.... <a:yasamir:864474264857346048>")
        for instance in open_instances:
            await instance.force_shutdown()
        await asyncio.sleep(1)
        await msg.edit(content=f"Oyunlar Kapatılıyor ({len(open_instances)}) Adet.... <a:yasir:864474264681971722>\nLobiler Temizleniyor.... <a:yasamir:864474264857346048>\nBot Kapatılıyor.... <a:yasamir:864474264857346048>")
        async with self.client.pool.acquire() as con:
            await con.execute(f"update lobby set players=$1,players_count='0',status='empty'", [])
        await asyncio.sleep(1)
        await msg.edit(content=f"Oyunlar Kapatılıyor ({len(open_instances)}) Adet.... <a:yasir:864474264681971722>\nLobiler Temizleniyor.... <a:yasir:864474264681971722>\nBot Kapatılıyor.... <a:yasamir:864474264857346048>")
        await asyncio.sleep(1)
        await msg.edit(content=f"Oyunlar Kapatılıyor ({len(open_instances)}) Adet.... <a:yasir:864474264681971722>\nLobiler Temizleniyor.... <a:yasir:864474264681971722>\nBot Kapatılıyor.... <a:yasir:864474264681971722>")
        await self.client.close()

    @commands.command(name="lobiler", aliases=["lobbys", "lb"])
    @commands.guild_only()
    async def lobbys(self, ctx):
        async with self.client.pool.acquire() as con:
            lobbys = await con.fetch(f"select * from lobby where server_id='{ctx.guild.id}' order by lobby_id asc")
            embed = discord.Embed(
                title="Lobiler", color=discord.Color.from_rgb(75, 196, 182))
            for lob in lobbys:
                embed.add_field(
                    name=f"Lobi: {lob['lobby_id']}", value=f"Durum: {'<:dolu:863838040636129320>' if lob['status'] == 'playing' else '<:bekliyor:863838040228364320>' if lob['status'] == 'waiting' else '<:bos:863838040526422036>'}\nOyuncu Sayısı: {lob['players_count']}/16", inline=True)
            await ctx.reply(embed=embed)

    @commands.command(name="lobby-çık", aliases=["lb-e", "lb-ç", "lb-çık"])
    @commands.guild_only()
    async def exit_lobby(self, ctx):
        async with self.client.pool.acquire() as con:
            all_lobbys = await con.fetch(f"select * from lobby where server_id='{ctx.guild.id}'")
            old_lobby = list(filter(lambda lob: str(
                ctx.author.id) in lob["players"], all_lobbys))
            if len(old_lobby) != 0:
                old_lobby = old_lobby[0]
                new_member_list = old_lobby["players"]
                new_member_list.pop(new_member_list.index(str(ctx.author.id)))
                if int(old_lobby["players_count"]) - 1 == 0:
                    await con.execute(f"update lobby set players=$1,players_count='{int(old_lobby['players_count'])-1}',status='empty' where server_id='{ctx.guild.id}' and lobby_id='{old_lobby['lobby_id']}'", new_member_list)
                elif int(old_lobby["players_count"]) == 16:
                    await ctx.reply("Şuanda Olduğun Lobide Oyun Başlamış! Çıkamazsın!")
                    return
                else:
                    await con.execute(f"update lobby set players=$1,players_count='{int(old_lobby['players_count'])-1}',status='waiting' where server_id='{ctx.guild.id}' and lobby_id='{old_lobby['lobby_id']}'", new_member_list)
                await ctx.send(f"Şuanda Olduğun `{old_lobby['lobby_id']}` Numaralı Lobiden Çıkartıyorum Seni.")
            else:
                await ctx.reply("Bir Lobide Değilsin")

    @commands.command(name="force-start", aliases=["fc-st"])
    @commands.guild_only()
    async def force_start(self, ctx):
        async with self.client.pool.acquire() as con:
            all_lobbys = await con.fetch(f"select * from lobby where server_id='{ctx.guild.id}'")
            old_lobby = list(filter(lambda lob: str(
                ctx.author.id) in lob["players"], all_lobbys))
            if len(old_lobby) == 0:
                await ctx.reply("Bir Lobiye girin!")
                return
            else:
                def mapper(item):
                    member = ctx.guild.get_member(int(item))
                    return member
                members = list(map(mapper, old_lobby[0]["players"]))
                await con.execute(f"update lobby set status='playing' where server_id='{ctx.guild.id}' and lobby_id='{old_lobby[0]['lobby_id']}'")
                await ctx.send(f"Oyun Başlıyor!!\nLobi Numarası: `{old_lobby[0]['lobby_id']}`\nKatılımcılar: {' '.join(list(map(lambda m: m.mention,members)))}")
                new_game = Game(self.client, old_lobby[0]["lobby_id"], ctx)
                await new_game.start_game(members)

    @commands.command(name="lobby-gir", aliases=["lb-j", "lb-join", "lobby-join"])
    @commands.guild_only()
    async def join_lobby(self, ctx, lobby_id=None):
        async with self.client.pool.acquire() as con:
            if lobby_id == None:
                await ctx.send("Lütfen Bir Lobi Numarası Giriniz")
                return
            lobby = await con.fetchrow(f"select * from lobby where server_id='{ctx.guild.id}' and lobby_id='{lobby_id}'")
            if lobby == None:
                await ctx.send("Geçerli Bir Lobi Numarası Giriniz")
                return
            if lobby["players_count"] == "16":
                await ctx.send("Bu Lobi Zaten Oyuna Başlamış Ve Ya Yakında Başlayacak!")
                return
            all_lobbys = await con.fetch(f"select * from lobby where server_id='{ctx.guild.id}'")
            old_lobby = list(filter(lambda lob: str(
                ctx.author.id) in lob["players"], all_lobbys))
            if len(old_lobby) != 0:
                old_lobby = old_lobby[0]
                new_member_list = old_lobby["players"]
                new_member_list.pop(new_member_list.index(str(ctx.author.id)))
                if int(old_lobby["players_count"]) - 1 == 0:
                    await con.execute(f"update lobby set players=$1,players_count='{int(old_lobby['players_count'])-1}',status='empty' where server_id='{ctx.guild.id}' and lobby_id='{old_lobby['lobby_id']}'", new_member_list)
                elif int(old_lobby["players_count"]) == 16:
                    await ctx.reply("Şuanda Olduğun Lobide Oyun Başlamış! Çıkamazsın!")
                    return
                else:
                    await con.execute(f"update lobby set players=$1,players_count='{int(old_lobby['players_count'])-1}',status='waiting' where server_id='{ctx.guild.id}' and lobby_id='{old_lobby['lobby_id']}'", new_member_list)
                await ctx.send(f"Şuanda Olduğun `{old_lobby['lobby_id']}` Numaralı Lobiden Çıkartıyorum Seni.")
            try:
                await ctx.author.send(f"Başarıyla {lobby_id} Numaralı Lobiye Katıldın.")
            except:
                await ctx.reply("DM'lerin Kapalı! Lütfen DMlerinizi Açınız")
                return
            if int(lobby["players_count"]) + 1 == 16:
                new_member_list = lobby["players"]
                new_member_list.append(str(ctx.author.id))
                await con.execute(f"update lobby set players=$1,players_count='{int(lobby['players_count'])+1}',status='playing' where server_id='{ctx.guild.id}' and lobby_id='{lobby_id}'", new_member_list)

                def mapper(item):
                    member = ctx.guild.get_member(int(item))
                    return member
                members = list(map(mapper, lobby["players"]))
                await ctx.reply(f"`{lobby_id}` Numaralı Lobiye Başarıyla Katıldın")
                await ctx.send(f"Oyun Başlıyor!!\nLobi Numarası: `{lobby_id}`\nKatılımcılar: {' '.join(list(map(lambda m: m.mention,members)))}")
                new_game = Game(self.client, lobby_id, ctx)
                await new_game.start_game(members)
            else:
                new_member_list = lobby["players"]
                new_member_list.append(str(ctx.author.id))
                await con.execute(f"update lobby set players=$1,players_count='{int(lobby['players_count'])+1}',status='waiting' where server_id='{ctx.guild.id}' and lobby_id='{lobby_id}'", new_member_list)
                await ctx.reply(f"`{lobby_id}` Numaralı Lobiye Başarıyla Katıldın")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        async with self.client.pool.acquire() as con:
            for i in range(1, 6):
                await con.execute(f"insert into lobby(server_id,players,players_count,status,lobby_id) values('{guild.id}',$1,'0','empty','{i}')", [])


def setup(client):
    client.add_cog(Lobbys(client))
