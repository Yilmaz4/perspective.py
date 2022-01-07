# perspective.py

An easy-to-use API wrapper written in Python, for [Perspective API](https://www.perspectiveapi.com/), an API that uses machine learning to identify "toxic" comments.

## Installation

Download & install git from https://git-scm.com/ and run below command:

```powershell
python -m pip install --upgrade git+https://github.com/Yilmaz4/perspective.py.git
```

Or alternatively, you can install from PyPI (Python Package Index):
```powershell
pyhton -m pip install --upgrade perspective.py
```

## Getting an API key

You need to get an API key from Google to use Perspective API. Instructions are explained in [this article](https://developers.perspectiveapi.com/s/docs-get-started).

## Command arguments

> `text: str` The text to analyze
>
> `requestedAttributes: list[str]` A list of attributes to analyze the text for.
>
> `language: str` The language of text.

You can use either `Attributes.TOXICITY` object or simply `"TOXICITY"` as a string for `requestedAttributes` argument.

You can specify the language of the text by using `language` argument. `language` argument accepts both language codes (such as "en" or "es") and language names (such as "English" or "Spanish"). Small spelling mistakes in language names can also be accepted (such as "Eglish" or "Spamish"). If you set `language` argument to `None`, language will be automatically detected.

You can find a list of all attributes and languages each attribute supports in [this article](https://developers.perspectiveapi.com/s/about-the-api-attributes-and-languages).

## Example usage

```python
from perspective import Client, Attributes

# Creating the Client object with the API key
API_KEY = "your_api_key"
client = Client(token = API_KEY)

# Make a request to Perspective API with a text to analyze and requested attributes
response = client.analyze(text = "Hey! How are you?", requestedAttributes = [Attributes.TOXICITY, Attributes.INSULT])

# Print the response (dict)
print(response)

# Print the percent of TOXICITY attribute
print(response["TOXICITY"]

# Iterate over the response
for attribute, result in response.items():
    print(attribute.capitalize() + ": " + "%.2f" % result + "%")
```

### Output

```python
{'TOXICITY': 7.019685000000001, 'INSULT': 3.9963423999999996}
7.019685000000001
Toxicity: 7.02%
Insult: 4.00%
```

As you can see in the output, `Client.analyze` returns a dictionary with requested attributes and their analysis results as percents. You can get percents of each attribute, or iterate over dictionary.
