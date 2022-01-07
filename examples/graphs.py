from perspective import Client, Attributes, utils

API_KEY = "token"
client = Client(token = API_KEY)

response = client.analyze(text = "don't care didn't ask", attributes = [Attributes.TOXICITY])

utils.show_graph(response=response, title="Analysis result", grid_lines=True)