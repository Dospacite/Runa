from datetime import datetime
from discord.ext import commands
from codecs import open
from json import load, dump
from scripts import EdogaSonDerseKatıl
from discord import Embed


class Edoga(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.filename = './json/auth.json'

        self.login_url = "https://edoga.dogakoleji.com/login?ignorelivelesson=true"
        self.join_class_url = "https://uygulama.sebitvcloud.com/VCloudFrontEndService/livelesson/instudytime/start"
        self.class_list_url = "https://uygulama.sebitvcloud.com/VCloudFrontEndService/studytime/getstudentstudytime"

    def get_auth_files(self):
        with open(self.filename, encoding='utf-8') as file:
            json_file = load(file)
        return json_file

    def set_auth_files(self, keyword, value):
        temp_dict = dict(self.get_auth_files())
        temp_dict[keyword] = value
        with open(self.filename, 'r+', encoding='utf-8') as file:
            dump(temp_dict, file, ensure_ascii=False, indent=2)
            return dict(self.get_auth_files())

    @commands.command(name="lesson", help="Son Dersi Gönderir.", aliases=['ders', 'etüt'])
    async def lesson(self, ctx, a="B", finished=1, index=1):
        auth_dict = dict(self.get_auth_files())
        # Decide on which login-info to use
        login_info = auth_dict['a_login'] if a == "A" or a == "a" else auth_dict['b_login']
        # Decide on cookie path so that it's easier to set later
        cookie_path = 'a_cookie' if a == "A" or a == "a" else 'b_cookie'

        if await EdogaSonDerseKatıl.is_logged_in(auth_dict[cookie_path]):  # If the present cookie can be reused,
            # Then don't login, reuse cookies.
            cookies = {'sid': auth_dict[cookie_path]}
        else:  # If it can't be reused,
            # Then login, use new cookies.
            cookies = await EdogaSonDerseKatıl.get_cookies(login_info['username'], login_info['password'])
            self.set_auth_files(cookie_path, cookies['sid'])

        # Get latest class id
        latest_class = await EdogaSonDerseKatıl.get_latest_class_id({'sid': cookies['sid']}, finished, index)
        if not latest_class:  # If get_latest_class_id returns None, which means no class is present
            await ctx.send("Aktif ders yok!")
            return False
        join_info = await EdogaSonDerseKatıl.get_join_info(latest_class, {'sid': cookies['sid']})
        if not join_info:  # If get_join_info returns None, which means class was expired
            await ctx.send("Aktif ders yok!")
            return False
        class_embed = Embed().from_dict({
            "title": "Şimdiki Canlı Ders",
            "color": 10150599,
            "fields": [
                {
                    "name": f"{cookie_path[0].upper()} Sınıfının {join_info[2]} Dersi",
                    "value": "Start Time: {0}\nMeeting ID: {1}\nPassword: {2}"
                             # Adjust to timezone by adding 3 Hours to the time
                             .format(datetime.utcfromtimestamp(int(str(join_info[3])[:-3]) + 10800),
                                     join_info[0],
                                     join_info[1]),
                    "inline": False
                }
            ]
        })
        await ctx.send(embed=class_embed)


def setup(client):
    client.add_cog(Edoga(client))
