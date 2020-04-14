import discord
from asyncio import sleep

TOKEN = "TOKEN" #Replace TOKEN with your discord bot token
client = discord.Client()

@client.event
async def on_ready():
    print('{0.user}'.format(client)+'としてログインしました。')

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if message.content == "/help emojibot":
        embed = discord.Embed(title="このbotの使い方",color=discord.Colour.from_rgb(33,173,232))
        embed.add_field(name="機能",value="botの機能を利用してAnimated Emojiを使えるようにする。ただし、普通の絵文字を選択した場合反応しない。",inline=False)
        embed.add_field(name=":hogehoge: msg",value="絵文字をメッセージとして書き込む。'msg'部分は'm'でも可。",inline=False)
        embed.add_field(name=":hogehoge: react",value="一つ前のメッセージにリアクションをつける。'react'部分は'r'でも可。",inline=False)
        embed.add_field(name=":hogehoge: '検索する語句'",value="『検索する語句』と(部分)一致した最も直近のメッセージ一つにリアクションをつける。(50個以上遡れません。また、仕様上'msg'など他のコマンドに使用されている文字列は検索できません。)",inline=False)
        await message.channel.send(embed=embed)

    if message.content.startswith(':'):
        command_ary = message.content.split()
        if len(command_ary) > 1:
            guild = message.guild.id
            emoji = discord.utils.get(message.guild.emojis, name=command_ary[0].strip(':'))
            print(emoji)
            if len(command_ary) == 2:
                if emoji and emoji.animated:
                    if command_ary[1] == "r" or command_ary[1] == "react":
                        msgs = []
                        msg_ids = []
                        async for x in message.channel.history(limit=(5)):
                            msgs.append(x)
                            id = x.id
                            msg_ids.append(id)
                        num = msg_ids.index(message.id) + 1
                        await msgs[num].add_reaction(emoji)
                        await message.delete()
                    elif command_ary[1] == "m" or command_ary[1] == "msg":
                        await message.channel.send(emoji)
                        await message.delete()
                    else:
                        await message.delete()
                        msgs = []
                        msg_contents = []
                        async for x in message.channel.history(limit=(50)):
                            msgs.append(x)
                            content = x.content
                            msg_contents.append(content)
                        for y in msg_contents:
                            if command_ary[1] in y:
                                num = msg_contents.index(y)
                                break
                        try:
                            await msgs[num].add_reaction(emoji)
                        except UnboundLocalError:
                            delmsg = await message.channel.send('検索対象が見当たりませんでした。このメッセージは3秒後に削除されます')
                            await sleep(3)
                            await delmsg.delete()

client.run(TOKEN)
