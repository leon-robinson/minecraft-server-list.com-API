# minecraft-server-list.com-API
WIP

Can read info from servers posted on the list, but still have to be able to parse info at specific server pages, 'minecraft-server-list.com/server/.../'

Example usage, getting servers from list:
```python
# The fetch functions return a list of MCServer classes.
a = fetch_servers_main_page() # Get servers on the main home page.
b = fetch_servers_page(3) # Get servers on page 3.
c = fetch_servers_new() # Fetch new servers.
```

MCServer class:
```python
class MCServer:
    def __init__(self, server_addr, server_name, server_index, shortened_desc, players_online, players_max):
        self.server_addr = server_addr
        self.server_name = server_name
        self.server_index = server_index
        self.shortened_desc = shortened_desc
        self.players_online = players_online
        self.players_max = players_max
```

Example usage, printing info from MCServer class:
```python
# The fetch functions return a list of MCServer classes.
a = fetch_servers_main_page() # Get servers on the main home page.

first_server = a[0] # Get the first server on the home page.
print(first_server.server_addr) # Print first server's IP addr.
```
