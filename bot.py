import asyncio
import random
import time
import datetime
import re
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ==========================================
# 🔑 METS TON NOUVEAU TOKEN ICI (sans guillemets)
# ==========================================
TOKEN = 8127363800:AAHOaSWjmbJG5Yy7AoFTBybONoaiZX-nXYk

# ==========================================
# STATS & DONNÉES
# ==========================================
user_stats = {}

JOKES = [
    "🤣 Pourquoi les développeurs détestent la nature ? Parce qu'il y a trop de bugs !",
    "🤣 Quel est le langage préféré des robots ? Le Python, bien sûr !",
    "🤣 Un pirate entre dans un bar... Il demande un root beer.",
    "🤣 Pourquoi les programmeurs préfèrent le noir ? Parce que le blanc est trop lumineux !",
    "🤣 Un robot est tombé dans l'eau... Il est électrocuté !",
]

QUOTES = [
    "💡 « Le code, c'est comme la poésie. »",
    "💡 « Un robot vaut mieux que 100 développeurs fatigués. »",
    "💡 « Les bugs sont des fonctionnalités non documentées. »",
    "💡 « L'IA ne remplacera pas les humains. »",
]

WEATHER_DATA = {
    "paris": "☀️ 22°C - Ensoleillé",
    "londres": "🌧️ 15°C - Pluie",
    "new york": "⛅ 20°C - Nuageux",
    "tokyo": "🌧️ 18°C - Pluie",
    "dakar": "☀️ 32°C - Très chaud",
    "moscou": "❄️ -5°C - Gel",
    "dubai": "☀️ 38°C - Canicule",
    "sydney": "☀️ 25°C - Agréable"
}

BOT_IMAGE_URL = "https://files.catbox.moe/oziw3x.png"

# ==========================================
# COMMANDES
# ==========================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=BOT_IMAGE_URL,
        caption="✨ **Bienvenue sur EchoMiroirBot !** ✨\n\n🤖 Je suis ton assistant.\n📌 Tape /help pour voir mes 35+ commandes.\n\n👤 Créé par HAENYLTR",
        parse_mode='Markdown'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = """
🌟 **ECHOMIROIRBOT** 🌟

📝 **TEXTE**
/echo <txt> · Répète
/caps <txt> · MAJUSCULES
/low <txt>  · minuscules
/cap <txt>  · Majuscule au début
/rev <txt>  · Texte inversé
/mix <txt>  · Mélange les lettres
/spoil <txt> · Message caché
/len <txt>  · Compte les caractères

🧮 **CALCULS & HASARD**
/calc <expr> · Calcule (ex: 5+3*2)
/roll <n>    · Dé personnalisé (1-n)
/random <a> <b> · Nombre aléatoire

🎲 **JEUX**
/dice   · Dé (1-6)
/coin   · Pile ou face
/roulette · Roulette russe
/joke   · Blague
/quote  · Citation
/choose <a> <b> · Choisit entre 2

🕐 **TEMPS & MÉTÉO**
/time   · Heure actuelle
/date   · Date du jour
/weather <ville> · Météo (simulée)

⚡ **UTILITAIRES**
/ping   · Test de latence
/cdown <n> · Compte à rebours
/stats  · Tes messages comptés
/uid    · Ton ID Telegram
/uptime · Temps de fonctionnement

🛠️ **FUN & DIVERS**
/flip   · Retourne une phrase
/emoji <mot> · Remplace les lettres par des emojis
/pyramide <n> · Fait une pyramide
/morse <txt> · Simule du morse
/encrypt <txt> · Chiffre simple (César)
/decrypt <txt> · Déchiffre

👤 Créé par HAENYLTR
"""
    await update.message.reply_photo(photo=BOT_IMAGE_URL, caption=txt, parse_mode='Markdown')

# --- Texte ---
async def echo(update, context):
    await update.message.reply_text(f"🔊 **{update.message.text}**", parse_mode='Markdown')

async def caps(update, context):
    t = ' '.join(context.args)
    await update.message.reply_text(f"🔠 **{t.upper()}**" if t else "❌ Ex: /caps hello", parse_mode='Markdown')

async def low(update, context):
    t = ' '.join(context.args)
    await update.message.reply_text(f"🔡 **{t.lower()}**" if t else "❌ Ex: /low HELLO", parse_mode='Markdown')

async def cap(update, context):
    t = ' '.join(context.args)
    await update.message.reply_text(f"📌 **{t.capitalize()}**" if t else "❌ Ex: /cap bonjour", parse_mode='Markdown')

async def rev(update, context):
    t = ' '.join(context.args)
    await update.message.reply_text(f"🔄 **{t[::-1]}**" if t else "❌ Ex: /rev bonjour", parse_mode='Markdown')

async def mix(update, context):
    t = list(' '.join(context.args))
    random.shuffle(t)
    await update.message.reply_text(f"🔀 **{''.join(t)}**" if t else "❌ Ex: /mix hello", parse_mode='Markdown')

async def spoil(update, context):
    t = ' '.join(context.args)
    await update.message.reply_text(f"||{t}||" if t else "❌ Ex: /spoil secret", parse_mode='MarkdownV2')

async def length(update, context):
    t = ' '.join(context.args)
    await update.message.reply_text(f"📏 **{len(t)}** caractères" if t else "❌ Donne un texte", parse_mode='Markdown')

# --- Calculs ---
async def calc(update, context):
    expr = ' '.join(context.args)
    if not expr: return await update.message.reply_text("❌ Ex: /calc 5+3*2")
    try:
        if not re.match(r'^[\d+\-*/().\s]+$', expr): raise Exception
        await update.message.reply_text(f"🧮 **{expr} = {eval(expr)}**", parse_mode='Markdown')
    except: await update.message.reply_text("❌ Erreur de calcul")

async def roll(update, context):
    try:
        n = int(context.args[0])
        if n > 0: await update.message.reply_text(f"🎲 **{random.randint(1,n)}** (1-{n})", parse_mode='Markdown')
    except: await update.message.reply_text("❌ Ex: /roll 10")

async def rand(update, context):
    try:
        a, b = int(context.args[0]), int(context.args[1])
        await update.message.reply_text(f"🎲 **{random.randint(a,b)}** (entre {a} et {b})", parse_mode='Markdown')
    except: await update.message.reply_text("❌ Ex: /random 1 10")

# --- Jeux ---
async def dice(update, context): await update.message.reply_text(f"🎲 **{random.randint(1,6)}**", parse_mode='Markdown')
async def coin(update, context): await update.message.reply_text(random.choice(["👑 Pile", "🪙 Face"]))
async def roulette(update, context): await update.message.reply_text("💀 **CLIC !**" if random.randint(1,6)==1 else "🔫 *CLIC...* Rien !")
async def joke(update, context): await update.message.reply_text(random.choice(JOKES))
async def quote(update, context): await update.message.reply_text(random.choice(QUOTES))
async def choose(update, context):
    opts = context.args
    if len(opts) < 2: return await update.message.reply_text("❌ Ex: /choose pizza sushi")
    await update.message.reply_text(f"🤔 Je choisis... **{random.choice(opts)}** !", parse_mode='Markdown')

# --- Temps ---
async def time_cmd(update, context): await update.message.reply_text(f"🕐 **{datetime.datetime.now().strftime('%H:%M:%S')}**", parse_mode='Markdown')
async def date_cmd(update, context): await update.message.reply_text(f"📅 **{datetime.datetime.now().strftime('%d/%m/%Y')}**", parse_mode='Markdown')
async def weather(update, context):
    city = ' '.join(context.args).lower()
    if not city: return await update.message.reply_text("❌ Ex: /weather Paris")
    for k, v in WEATHER_DATA.items():
        if k in city: return await update.message.reply_text(f"🌍 **{city.capitalize()} :**\n{v}", parse_mode='Markdown')
    await update.message.reply_text("🌍 Villes dispo: Paris, Londres, NY, Tokyo, Dakar, Moscou, Dubai, Sydney")

# --- Utilitaires ---
async def ping(update, context):
    s = time.time()
    msg = await update.message.reply_text("🏓 Ping...")
    await msg.edit_text(f"🏓 Pong ! `{round((time.time()-s)*1000, 2)} ms`", parse_mode='Markdown')

async def cdown(update, context):
    try:
        n = int(context.args[0])
        if n <= 0: raise Exception
        for i in range(n, 0, -1):
            await update.message.reply_text(f"⏱️ **{i}**", parse_mode='Markdown')
            await asyncio.sleep(1)
        await update.message.reply_text("🚀 **BOUM !**")
    except: await update.message.reply_text("❌ Ex: /cdown 5")

async def stats(update, context):
    uid = update.effective_user.id
    await update.message.reply_text(f"📊 Tu as envoyé **{user_stats.get(uid, 0)}** messages !", parse_mode='Markdown')

async def uid(update, context): await update.message.reply_text(f"🆔 Ton ID : `{update.effective_user.id}`", parse_mode='Markdown')

start_time = time.time()
async def uptime(update, context):
    delta = int(time.time() - start_time)
    m, s = divmod(delta, 60)
    h, m = divmod(m, 60)
    await update.message.reply_text(f"⏳ Bot en ligne depuis **{h}h {m}m {s}s**", parse_mode='Markdown')

# --- Fun ---
async def flip(update, context):
    t = ' '.join(context.args)
    if not t: return await update.message.reply_text("❌ Ex: /flip Hello")
    await update.message.reply_text(t[::-1].swapcase())

async def emoji(update, context):
    t = ' '.join(context.args).lower()
    if not t: return await update.message.reply_text("❌ Ex: /emoji bonjour")
    d = {'a':'🅰️','b':'🅱️','c':'©️','d':'🅳️','e':'🅴️','f':'🅵️','g':'🅶️','h':'🅷️','i':'🅸️','j':'🅹️','k':'🅺️','l':'🅻️','m':'🅼️','n':'🅽️','o':'🅾️','p':'🅿️','q':'🆀','r':'🆁','s':'🆂','t':'🆃','u':'🆄','v':'🆅','w':'🆆','x':'🆇','y':'🆈','z':'🆉'}
    await update.message.reply_text(' '.join(d.get(c, c) for c in t))

async def pyramide(update, context):
    try:
        n = int(context.args[0])
        if n > 10: n = 10
        res = '\n'.join('*' * i for i in range(1, n+1))
        await update.message.reply_text(f"```\n{res}\n```", parse_mode='Markdown')
    except: await update.message.reply_text("❌ Ex: /pyramide 5")

async def morse(update, context):
    t = ' '.join(context.args).upper()
    if not t: return await update.message.reply_text("❌ Ex: /morse SOS")
    d = {'A':'.-','B':'-...','C':'-.-.','D':'-..','E':'.','F':'..-.','G':'--.','H':'....','I':'..','J':'.---','K':'-.-','L':'.-..','M':'--','N':'-.','O':'---','P':'.--.','Q':'--.-','R':'.-.','S':'...','T':'-','U':'..-','V':'...-','W':'.--','X':'-..-','Y':'-.--','Z':'--..',' ':'/'}
    await update.message.reply_text(' '.join(d.get(c, '?') for c in t))

async def encrypt(update, context):
    t = ' '.join(context.args)
    if not t: return await update.message.reply_text("❌ Ex: /encrypt hello")
    await update.message.reply_text(f"🔒 **{''.join(chr(ord(c)+1) for c in t)}**", parse_mode='Markdown')

async def decrypt(update, context):
    t = ' '.join(context.args)
    if not t: return await update.message.reply_text("❌ Ex: /decrypt ifmmp")
    await update.message.reply_text(f"🔓 **{''.join(chr(ord(c)-1) for c in t)}**", parse_mode='Markdown')

# --- Compteur ---
async def count_messages(update, context):
    uid = update.effective_user.id
    user_stats[uid] = user_stats.get(uid, 0) + 1

# ==========================================
# MAIN
# ==========================================
async def main():
    app = Application.builder().token(TOKEN).build()
    
    # Ajout des commandes
    cmds = [
        ("start", start), ("help", help_command),
        ("echo", echo), ("caps", caps), ("low", low), ("cap", cap), ("rev", rev), ("mix", mix), ("spoil", spoil), ("len", length),
        ("calc", calc), ("roll", roll), ("random", rand),
        ("dice", dice), ("coin", coin), ("roulette", roulette), ("joke", joke), ("quote", quote), ("choose", choose),
        ("time", time_cmd), ("date", date_cmd), ("weather", weather),
        ("ping", ping), ("cdown", cdown), ("stats", stats), ("uid", uid), ("uptime", uptime),
        ("flip", flip), ("emoji", emoji), ("pyramide", pyramide), ("morse", morse), ("encrypt", encrypt), ("decrypt", decrypt)
    ]
    for name, func in cmds:
        app.add_handler(CommandHandler(name, func))
    
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, count_messages))
    
    print("🤖 EchoMiroirBot est en ligne (35+ commandes) !")
    print("👤 Créé par HAENYLTR")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
