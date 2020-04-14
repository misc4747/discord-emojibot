import discord
from asyncio import sleep

TOKEN = "TOKEN" #Replace TOKEN with your discort bot token
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
        embed.add_field(name=":hogehoge: react",value="一つ前のメッセージにリアクションをつける。'react'部分は'r'でも、無くても可。",inline=False)
        await message.channel.send(embed=embed)

    if message.content.startswith(':'):
        guild = message.guild.id
        emoji_ary = message.content.split()
        emoji = discord.utils.get(message.guild.emojis, name=emoji_ary[0].strip(':'))
        print(emoji)
        if emoji and emoji.animated:
            if len(emoji_ary) == 1 or emoji_ary[1] == "r" or emoji_ary[1] == "react":
                msgs = []
                async for x in message.channel.history(limit=(2)):
                    msgs.append(x)
                await msgs[1].add_reaction(emoji)
                await message.delete()
            elif emoji_ary[1] == "m" or emoji_ary[1] == "msg":
                await message.channel.send(emoji)
                await message.delete()
            else:
                await message.delete()
                attention = await message.channel.send('コマンドが誤っています。詳しくは"/help emojibot"を参照してください。このメッセージは5秒後に削除されます。')
                await sleep(5)
                await attention.delete()

client.run(TOKEN)
