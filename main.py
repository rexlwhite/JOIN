import os
import discord
from keep_alive import keep_alive
from discord import app_commands
from discord.ext import commands

# ตั้งค่า Intents พื้นฐาน
intents = discord.Intents.default()
intents.message_content = True

# สร้างอินสแตนซ์ของบอท
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'ล็อกอินเข้าสู่ระบบในชื่อ {bot.user.name}')
    try:
        # ซิงค์ Slash Commands ไปยัง Discord Global 
        # (หมายเหตุ: คำสั่งอาจใช้เวลาสักครู่ถึงจะอัปเดตใน Discord)
        synced = await bot.tree.sync()
        print(f"ซิงค์สำเร็จ {len(synced)} คำสั่ง")
    except Exception as e:
        print(f"เกิดข้อผิดพลาดในการซิงค์คำสั่ง: {e}")

# 1. Slash Command สำหรับเข้าห้องเสียง
@bot.tree.command(name="join", description="สั่งให้บอทเข้าห้องเสียงที่คุณอยู่")
async def join(interaction: discord.Interaction):
    # ตรวจสอบว่าผู้ใช้ที่พิมพ์คำสั่งอยู่ในห้องเสียงหรือไม่
    if interaction.user.voice:
        channel = interaction.user.voice.channel

        # ตรวจสอบว่าบอทเชื่อมต่ออยู่กับห้องเสียงใดๆ ในเซิร์ฟเวอร์นี้แล้วหรือยัง
        if interaction.guild.voice_client:
            # ถ้าบอทอยู่ห้องอื่น ให้ย้ายมาห้องเดียวกับผู้ใช้
            await interaction.guild.voice_client.move_to(channel)
        else:
            # ถ้าบอทยังไม่ได้เข้าห้องไหนเลย ให้ทำการเชื่อมต่อเข้าไป
            await channel.connect()

        await interaction.response.send_message(f"🔊 เข้าไปที่ห้องเสียง **{channel.name}** เรียบร้อยแล้วค่ะ!")
    else:
        # หากผู้ใช้คำสั่งไม่ได้อยู่ในห้องเสียงใดๆ เลย
        await interaction.response.send_message("❌ คุณจำเป็นต้องเข้าไปอยู่ในห้องเสียงก่อนสั่งฉันค่ะ!", ephemeral=True)

# 2. Slash Command สำหรับออกจากห้องเสียง
@bot.tree.command(name="leave", description="สั่งให้บอทออกจากห้องเสียง")
async def leave(interaction: discord.Interaction):
    # ตรวจสอบว่ามีบอทอยู่ในห้องเสียงของเซิร์ฟเวอร์นี้หรือไม่
    if interaction.guild.voice_client:
        # สั่งให้ตัดการเชื่อมต่อ
        await interaction.guild.voice_client.disconnect()
        await interaction.response.send_message("👋 ออกจากห้องเสียงเรียบร้อยแล้วค่ะ!")
    else:
        # หากบอทไม่ได้อยู่ในห้องเสียงไหนเลย
        await interaction.response.send_message("❌ ตอนนี้ฉันไม่ได้อยู่ในห้องเสียงไหนเลยค่ะ!", ephemeral=True)

keep_alive()

# ใส่ TOKEN บอทของคุณที่นี่
bot.run(os.getenv('TOKEN'))
