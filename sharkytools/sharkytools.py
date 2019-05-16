import discord
from redbot.core import commands, checks


class SharkyTools(commands.Cog):
    """Sharky Tools"""

    @commands.command(name="sharkinfo", aliases=['fishinfo'])
    @commands.guild_only()
    @commands.bot_has_permissions(embed_links=True, send_messages=True)
    async def sharkinfo(self, ctx, *, member: discord.Member):
        """
        You wot?
        """
        member_mention = member.mention # Mentions
        member_disc = member.discriminator # The four digits
        member_name = member.name # Default Discord name
        member_id = member.id # USERID
        member_avatar = member.avatar_url_as(static_format="png") # Avatar, static is formated as png
        member_voice = member.voice # Tells us the voice chat they're in
        
        member_role = sorted(member.roles)[1:] # this and line 35 are required for role formats
        if member_role: #this lets us format the roles properly so theyr'e named correctly
            member_role = ", ".join([x.name for x in member_role]) 
        joined = member.joined_at.strftime("%d %b %Y %H:%M")
        created = member.created_at.strftime("%d %b %Y %H:%M")     
        notice = "Notice: This is a test from Sharky The King#0001"

    #   Embeds
        embed = discord.Embed(color=0xEE2222, title=f'{member_name}\'s information')
        embed.add_field(name='Name:', value=f'{member_mention}\n{member_name}#{member_disc}')
        embed.add_field(name='ID:', value=f'{member_id}')
        embed.add_field(name="Joined Date:", value=f'{joined}')
        embed.add_field(name="Account Creation:", value=f'{created}')
        embed.add_field(name='Roles:', value=f'{member_role}')
        if member_voice and member_voice.channel: #this formats the voice call chunk into a proper message
            embed.add_field(
                name=("Current voice channel"),
                value="<#{0.id}> (ID: {0.id})".format(member_voice.channel),
                inline=False)

    # Non-fielded embedsets    
    #    embed.set_image(url=member_avatar) - Ignore this entirely, just something extra-
        embed.set_footer(text=f'{notice}')
        embed.set_thumbnail(url=member_avatar)
        embed.set_author(name=f'{member_name}#{member_disc}', icon_url=f'{member_avatar}')  
        await ctx.send(embed=embed)

#   Embed base = Trying to find if user is banned in Discord.
    @commands.command()
    @commands.bot_has_permissions(ban_members=True, embed_links=True, send_messages=True)  # Makes sure the bot has the proper permissions to do this command.
    @commands.guild_only()
    async def findban(self, ctx, *, banneduser):
        """Check if a user is banned"""
        guild = ctx.guild  # Self explained
        bot = ctx.bot  # Self explained
        try:  # This tries to see if member works, if it doesn't it'll error out without this
            member = await bot.fetch_user(banneduser)  # Contains the bot.fetch_user
        except discord.NotFound:
            embed = discord.Embed(color=0xEE2222, title='Unknown User')
            embed.add_field(name=f'Not Valid', value=f'{banneduser} is not a Valid User\n Please make sure you\'re using a correct UserID.\nHow you ask? [Go here](https://support.discordapp.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-)')
            return await ctx.send(embed=embed)
        except discord.HTTPException:
            embed = discord.Embed(color=0xEE2222, title='Invalid Input')
            embed.add_field(name=f'ID10T Error:', value=f'**{banneduser}** is not a valid input...but you knew that, didn\'t you?')
            return await ctx.send(embed=embed)
        mid = banneduser
        hammer = 'https://cdn.discordapp.com/emojis/404084568354979845.png'
        try:
            tban = await guild.fetch_ban(await bot.fetch_user(banneduser))
            #   embeds
            embed = discord.Embed(color=0xEE2222, title='Ban Found')
            embed.add_field(name=f'User Found:', value=f'{member}\n({mid})', inline=True)
            embed.add_field(name=f'Ban reason:', value=f'{tban[0]}', inline=False)
            embed.set_thumbnail(url=hammer)
            return await ctx.send(embed=embed)
        except discord.NotFound:
            embed = discord.Embed(color=0xEE2222, title='Ban **NOT** Found')
            embed.add_field(name=f'They are not banned from the server.', value=f'{member} ({mid})')
            return await ctx.send(embed=embed)