import requests
from bs4 import BeautifulSoup

class MCServer:
    def __init__(self, server_addr, server_name, server_index, shortened_desc, players_online, players_max):
        self.server_addr = server_addr
        self.server_name = server_name
        self.server_index = server_index
        self.shortened_desc = shortened_desc
        self.players_online = players_online
        self.players_max = players_max

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

def remove_b4_ext(s, substr):
    return s[s.find(substr)+len(substr):]

def fetch_servers(url_end):
    mc_servers = []

    url = "https://minecraft-server-list.com/" + url_end
    response = requests.get(url, headers=headers)
    page_raw = response.text

    soup = BeautifulSoup(page_raw, 'html.parser')

    if soup.title.string == "Just a moment...":
        raise Exception("The page is not ready yet. Please try again later.")

    if soup.find('tbody') is not None:
        tbody = soup.find('tbody')
        tr_bodies = tbody.find_all('tr', class_=True)

        for tr in tr_bodies:
            td_elements = tr.find_all('td')

            for i in range(len(td_elements)):
                td = td_elements[i].get_text()
                match i:
                    case 0:
                        no_nl = td.replace('\n', '')
                        hashtag_pos = no_nl.rfind('#')
                        listed_name = no_nl[1:hashtag_pos]
                        list_index = int(no_nl[2+len(listed_name):-1])
                        print(str(list_index) + ": " + listed_name)
                    case 1:
                        shortened_desc = td[1:-2]
                    case 2:
                        tmp = remove_b4_ext(td, 'Players Online:')
                        players_raw = tmp[:tmp.find('Votes')-1]
                        players_split = players_raw.split("/")
                        players_online_raw = players_split[0]
                        players_max_raw = players_split[1]

                        if players_online_raw == ' ':
                            players_online = 0
                        else:
                            players_online = int(players_online_raw[1:-1])

                        players_max_str = players_max_raw[1:-1]
                        if players_max_str == '?':
                            players_max = -1
                        else:
                            players_max = int(players_max_str)

            td_n2 = tr.find('td', class_='n2')

            if td_n2.has_attr('id'):
                ip = td_n2['id']
            else:
                raise Exception("Couldn't find server IP in td_n2")

            mc_servers.append(MCServer(ip, listed_name, list_index, shortened_desc, players_online, players_max))
    else:
        raise Exception("Could not find tbody")

    return mc_servers

def fetch_servers_new():
    return fetch_servers('new')

def fetch_servers_main_page():
    return fetch_servers('')

def fetch_servers_page(page):
    return fetch_servers('page/' + str(page))

def print_server_info(mc_server):
    print(f"""
{mc_server.server_name}:
    Address: {mc_server.server_addr}
    Players: {mc_server.players_online}/{mc_server.players_max}
          """)

def print_server_infos(mc_servers):
    for mc_server in mc_servers:
        print_server_info(mc_server)
