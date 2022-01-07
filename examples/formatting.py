from perspective import Client, Attributes, utils

API_KEY = "token"
client = Client(token = API_KEY)

response = client.analyze(text = "you're currently looking at examples", attributes = [Attributes.TOXICITY])

print(utils.format_response(response=response, align_right=True))