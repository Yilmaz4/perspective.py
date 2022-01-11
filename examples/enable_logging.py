from perspective import Client, Attributes

API_KEY = "AIzaSyA-yzvgANWE1STU9MTbTLrS3rj1956tVAs"

"""
+--------+-----------+
| Number |   Level   |
+--------+-----------+
|   50   |  CRITICAL |
+--------+-----------+
|   40   |   ERROR   |
+--------+-----------+
|   30   |  WARNING  |
+--------+-----------+
|   20   |   INFO    |
+--------+-----------+
|   10   |   DEBUG   |
+--------+-----------+
|    0   |  NOTSET   |
+--------+-----------+
"""

# Set logging level to 20 (INFO) while creating the Client object
perspective = Client(token = API_KEY, logging_level=20)

# Modify logging level to 10 (DEBUG) which would show literally every logging message
perspective.logging_level = 10

# Modify logging level again to 0 (NOTSET) which would disable logging
perspective.logging_level = 0

response = perspective.analyze(text = "Never gonna give you up", attributes = Attributes.All, skip_on_lang=True, skip_on_unknown=False, return_raw=False)

print(response)
