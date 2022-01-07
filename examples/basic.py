from perspective import Client, Attributes

API_KEY = "token"
client = Client(token = API_KEY)

response = client.analyze(text = "hi everyone", attributes = [Attributes.TOXICITY])

print(response)