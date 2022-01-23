# perspective.py

The perspective.py library is an easy-to-use API wrapper written in Python for [Perspective API](https://www.perspectiveapi.com/), an API that uses machine learning to identify "toxic" comments.

## Installation

Download & install git for your operating system from https://git-scm.com/ and run below command in command prompt or powershell:

```powershell
python -m pip install --upgrade git+https://github.com/Yilmaz4/perspective.py.git
```

Or alternatively, you can install from the PyPI (Python Package Index) server using pip:
```powershell
pyhton -m pip install --upgrade perspective.py
```

## Getting an API key

You need to have an API key from Google to use Perspective API. Instructions to get an API key are explained in [this article](https://developers.perspectiveapi.com/s/docs-get-started).

## Command arguments

> `text: str` The text to analyze
>
> `attributes: list[str]` A list of attributes to analyze the text for.
>
> `language: str` The language of text.

You can use either `Attributes.TOXICITY` object (for example) or simply `"TOXICITY"` as a string for `attributes` argument. Alternatively, you can use groups, such as `Attributes.Production` which contains all production-ready attributes or `Attributes.Experimental` which contains all experimental attributes.

You can specify the language of the text by using `language` argument. `language` argument accepts both language codes (such as "en" or "es") and language names (such as "English" or "Spanish"). Small spelling mistakes in language names can also be accepted (such as "Eglish" or "Spamish"). If you set `language` argument to `None`, language will be automatically detected by the API itself.

You can find a list of all attributes and languages each attribute supports in [this article](https://developers.perspectiveapi.com/s/about-the-api-attributes-and-languages).

## Example usage

```python
from perspective import Client, Attributes, utils

# Create the Client object which we will use to make requests with the API key
API_KEY = "your_api_key"
client = Client(token = API_KEY)

# Make a request to Perspective API with a text to analyze and the attributes that you want the text to be analyzed for
response = client.analyze(text = "Hey! How are you?", attributes = [Attributes.TOXICITY, Attributes.INSULT])

# Print the response as a dictionary
print(response)

# Print the score value of TOXICITY attribute
print(response["TOXICITY"]

print("  ")

# Iterate over the response
for attribute, result in response.items():
    print(attribute.capitalize() + ": " + "%.2f" % result + "%")

print("  ")

# Or alternatively, use utils.format_response to print a formatted text of the response which would return almost the same result as the above code
print(utils.format_response(response, align_right=True))
```

### Output

```python
{'TOXICITY': 7.019685000000001, 'INSULT': 3.9963423999999996}
7.019685000000001

Toxicity: 7.02%
Insult: 4.00%

Toxicity: 7.02%
  Insult: 4.00%
```

As you can see in the output, `Client.analyze` returns a dictionary with requested attributes and their analysis results as percents. You can get percents of each attribute, or iterate over dictionary.

## Example usage for creating a bar chart
```python
from perspective import Client, Attributes, utils

# Create the Client object which we will use to make requests with the API key
API_KEY = "your_api_key"
client = Client(token = API_KEY)

# Make a request to Perspective API with a text to analyze and the attributes that you want the text to be analyzed for
response = client.analyze(text = "Hey! How are you?", requestedAttributes = Attributes.Production) # Attributes.Production includes all production-ready attributes

# Create a horizontal bar chart and show it by popping up a window
utils.show_graph(response=response, title="Sample graph")

# Or alternatively, you can save the chart to an image file
utils.save_graph(response=response, filename="my_chart.png", title="Sample graph")
```

### Output
![image](https://user-images.githubusercontent.com/77583632/148606000-d21cb4b7-566c-45dd-9215-4248d831a62c.png)

# License

MIT License

Copyright (c) 2021-2022 Yilmaz Alpaslan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
