from py_spoo_url import Shortener

shortener = Shortener()
long_url = "https://www.example.com"
result = shortener.shorten(long_url, password="SuperSecretPassword@444", max_clicks=100) # for custom alias, put `alias=<your_choice>`
print(result)

# for emoji urls

result = shortener.emojify(long_url)  # other parameters are also supported in this
print(result)