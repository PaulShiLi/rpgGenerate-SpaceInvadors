from aitextgen import aitextgen
from discord.ext import commands
import discord
import re

bot = commands.Bot(command_prefix='~')
token = 'NDk1OTkzMjE2MTI3MDc0MzA5.GAjKlB.xeTBA3yKJ7VcozonaM_e-f6yHvlQ6s01qdDX1U'

aiPersonality = aitextgen(model_folder="personality_model/", tokenizer_file="personality_model/aitextgen.tokenizer.json", to_gpu=True)

aiBackstory = aitextgen(model_folder="backstory_model/", tokenizer_file="backstory_model/aitextgen.tokenizer.json", to_gpu=True)

@bot.command()
async def personality(ctx):
    '''
    Function: generates text randomly or based on a prompt. 
    '''

    message = await ctx.send('Thinking...')
    output = aiPersonality.generate(n=2,
                         max_length=120,
                         prompt="They are",
                         temperature=0.8,
                         return_as_list=True)
    await message.edit(content='\n\n'.join(output))

@bot.command()
async def backstory(ctx):
    '''
    Function: generates text randomly or based on a prompt. 
    '''

    message = await ctx.send('Thinking...')
    output = aiBackstory.generate(n=2,
                         max_length=120,
                         temperature=0.8,
                         return_as_list=True)
    
    await message.edit(content='\n\n'.join(output))

@bot.command()
async def generate(ctx):

    message = await ctx.send('Thinking...')

    # Personality
    outputPersonality = aiPersonality.generate(n=2,
                         max_length=120,
                         prompt="They are",
                         temperature=0.8,
                         return_as_list=True)
    finalPersonality = []
    for x in outputPersonality:
        finalPersonality.append(x.split("\n")[0])

    # Backstory
    outputBackstory = aiBackstory.generate(n=2,
                         max_length=120,
                         temperature=0.8,
                         return_as_list=True)

    finalBackstory = []
    for x in outputBackstory:
        finalBackstory.append(x.split("\n")[0])

    texts = []
    for x in finalBackstory:
        startIndex, endIndex = [periodObj for periodObj in re.finditer('\.', x)][-1].span()
        texts.append(x[:endIndex])

    # Embed
    embed=discord.Embed(title="Generated RPG Character")
    embed.add_field(name="Backstory", value='\n\n'.join(texts), inline=False)
    embed.add_field(name="Personality Traits", value=finalPersonality[0], inline=False)
    embed.add_field(name="Physical Traits", value="____", inline=False)
    embed.set_thumbnail(url="https://static.wixstatic.com/media/12b467_a4ceef0f338c41c7885cb083ea36a00f~mv2_d_1742_1743_s_2.png/v1/fill/w_85,h_85,al_c,q_85,usm_0.66_1.00_0.01,enc_auto/ai%20camp%20logo.png")
    await message.edit(embed=embed, content="")

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

bot.run(token)
