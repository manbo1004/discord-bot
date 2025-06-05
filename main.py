import discord
from discord.ext import commands
from flask import Flask
from keep_alive import keep_alive
import random
import os

TOKEN = os.environ["TOKEN"]

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
user_data = {}

shop_items = {
    "치킨": 30000,
    "500만 메소": 30000,
    "피자": 45000,
    "족발": 60000,
    "길드 명찰": 10000
}

@bot.event
async def on_ready():
    print(f"✅ {bot.user} 봇 실행됨")

@bot.command()
async def 출석(ctx):
    uid = str(ctx.author.id)
    user_data[uid] = user_data.get(uid, 0) + 100
    await ctx.send(f"{ctx.author.mention} 출석 완료! (+100P)")

@bot.command()
async def 포인트(ctx):
    uid = str(ctx.author.id)
    await ctx.send(f"{ctx.author.mention}님의 포인트: {user_data.get(uid, 0)}P")

@bot.command()
async def 슬롯(ctx):
    uid = str(ctx.author.id)
    if user_data.get(uid, 0) < 500:
        await ctx.send("포인트가 부족합니다. (500P 필요)")
        return
    user_data[uid] -= 500
    emojis = ["🍒", "🍋", "🍇"]
    result = [random.choice(emojis) for _ in range(3)]
    if result.count(result[0]) == 3:
        user_data[uid] += 3000
        await ctx.send(f"{' | '.join(result)}\n3개 일치! +3000P")
    else:
        await ctx.send(f"{' | '.join(result)}\n꽝! 다음 기회에!")

@bot.command()
async def 송금(ctx, 대상: discord.User, 금액: int):
    sender = str(ctx.author.id)
    receiver = str(대상.id)
    if user_data.get(sender, 0) < 금액:
        await ctx.send("포인트가 부족합니다.")
        return
    user_data[sender] -= 금액
    user_data[receiver] = user_data.get(receiver, 0) + 금액
    await ctx.send(f"{대상.mention}님에게 {금액}P 송금 완료!")

@bot.command()
async def 랭킹(ctx):
    sorted_data = sorted(user_data.items(), key=lambda x: x[1], reverse=True)
    msg = ""
    for i, (uid, point) in enumerate(sorted_data[:5], start=1):
        user = await bot.fetch_user(int(uid))
        msg += f"{i}위: {user.name} - {point}P\n"
    await ctx.send(f"📊 포인트 랭킹 TOP 5 📊\n{msg}")

@bot.command()
async def 상점(ctx, 아이템: str):
    uid = str(ctx.author.id)
    if 아이템 not in shop_items:
        await ctx.send("존재하지 않는 아이템입니다.")
        return
    price = shop_items[아이템]
    if user_data.get(uid, 0) < price:
        await ctx.send(f"포인트가 부족합니다. ({price}P 필요)")
        return
    user_data[uid] -= price
    await ctx.send(f"{아이템} 구매 완료! (-{price}P)")

@bot.command()
async def 홀짝(ctx, 선택: str):
    uid = str(ctx.author.id)
    if user_data.get(uid, 0) < 1000:
        await ctx.send("포인트가 부족합니다. (1000P 필요)")
        return
    user_data[uid] -= 1000
    num = random.randint(1, 100)
    결과 = "홀" if num % 2 else "짝"
    if 선택 == 결과:
        user_data[uid] += 2000
        await ctx.send(f"{num} → {결과}! 정답! +2000P")
    else:
        await ctx.send(f"{num} → {결과}! 틀렸습니다!")

@bot.command()
async def 주사위(ctx, 숫자: int):
    uid = str(ctx.author.id)
    if user_data.get(uid, 0) < 1000:
        await ctx.send("포인트가 부족합니다. (1000P 필요)")
        return
    if 숫자 < 1 or 숫자 > 6:
        await ctx.send("숫자는 1~6 사이로 입력하세요.")
        return
    user_data[uid] -= 1000
    주사위 = random.randint(1, 6)
    if 숫자 == 주사위:
        user_data[uid] += 6000
        await ctx.send(f"🎲 {주사위}! 정답입니다! +6000P")
    else:
        await ctx.send(f"🎲 {주사위}! 틀렸습니다!")

@bot.command()
async def 경마(ctx, 번호: int):
    uid = str(ctx.author.id)
    if user_data.get(uid, 0) < 2000:
        await ctx.send("포인트가 부족합니다. (2000P 필요)")
        return
    if 번호 not in [1, 2, 3, 4]:
        await ctx.send("1~4 중에서 선택해주세요.")
        return
    user_data[uid] -= 2000
    승자 = random.randint(1, 4)
    if 번호 == 승자:
        user_data[uid] += 8000
        await ctx.send(f"🏇 승자: {승자}번 말! 정답입니다! +8000P")
    else:
        await ctx.send(f"🏇 승자: {승자}번 말! 틀렸습니다!")

keep_alive()
bot.run(TOKEN)
