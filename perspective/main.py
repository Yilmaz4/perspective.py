"""
Copyright (c) 2021 Yilmaz Alpaslan

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
"""

from googleapiclient import discovery, errors
from typing import Optional
from pycountry import languages

from .attributes import Attributes

import httplib2
import difflib

class EmptyTextError(Exception):
    pass

class UnknownAttributeError(Exception):
    pass

class InvalidTokenError(Exception):
    pass

class HTTPException(Exception):
    pass

class UnsupportedLanguageError(Exception):
    pass

class Client:
    def __init__(self, token: str):
        try:
            self.client = discovery.build(
                "commentanalyzer",
                "v1alpha1",
                developerKey = token,
                discoveryServiceUrl = "https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
                static_discovery = False,
            )
        except errors.HttpError as exceptionDetails:
            if str(exceptionDetails).startswith(f"<HttpError 400 when requesting https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1&key={token} returned \"API key not valid. Please pass a valid API key.\"."):
                raise InvalidTokenError("The token you've entered is not a valid API key. Refer to https://developers.perspectiveapi.com/s/docs-get-started to get a new API key.")
            else:
                raise HTTPException("An unknown error occured. Please try again. Exception details: " + str(exceptionDetails))
        except httplib2.error.ServerNotFoundError as exceptionDetails:
            raise HTTPException("Unable to connect to the API. Please check your internet connection.")
        else:
            self.__token = token

    @staticmethod
    def __get_language_code(language: str) -> Optional[str]:
        try:
            lang_code = languages.get(alpha_2=language).alpha_2
        except AttributeError:
            try:
                lang_code = languages.get(name=language).alpha_2
            except AttributeError:
                languages_name = []
                for lang in languages:
                    languages_name.append(str(lang.name))
                try:
                    return languages.get(name=difflib.get_close_matches(language, languages_name, n=1)[0]).alpha_2
                except IndexError:
                    return None
            else:
                return lang_code
        else:
            return lang_code
    @staticmethod
    def __get_language_name(language: str) -> Optional[str]:
        try:
            lang_name = languages.get(alpha_2=language).name
        except AttributeError:
            try:
                lang_name = languages.get(name=language).name
            except AttributeError:
                languages_name = []
                for lang in languages:
                    languages_name.append(str(lang.name))
                try:
                    return languages.get(name=difflib.get_close_matches(language, languages_name, n=1)[0]).name
                except IndexError:
                    return None
            else:
                return lang_name
        else:
            return lang_name
    
    @staticmethod
    def __get_attribute(attribute: str) -> Optional[str]:
        try:
            return difflib.get_close_matches(attribute, ["TOXICITY", "SEVERE_TOXICITY", "IDENTITY_ATTACK", "INSULT", "PROFANITY", "THREAT_EXPERIMENTAL", "TOXICITY_EXPERIMENTAL", "SEVERE_TOXICITY_EXPERIMENTAL", "IDENTITY_ATTACK_EXPERIMENTAL", "INSULT_EXPERIMENTAL", "PROFANITY_EXPERIMENTAL", "THREAT_EXPERIMENTAL", "SEXUALLY_EXPLICIT", "FLIRTATION", "ATTACK_ON_AUTHOR", "ATTACK_ON_COMMENTER", "INCOHERENT", "INFLAMMATORY", "LIKELY_TO_REJECT", "OBSCENE", "SPAM", "UNSUBSTANTIAL"], n=1)[0]
        except IndexError:
            return None

    def analyze(self, text: str, attributes: list[str] = Attributes.Production, language: Optional[str] = None, **options) -> dict:
        """
        Make a request to the Perspective API with the text and requested attributes that you've entered.

        Parameters
        -----------
        text: :class:`str`
            The text to analyze.
        requestedAttributes: :class:`list[str]`
            A list of attributes to analyze the text for.
        language: :class:`Optional[str]`
            The language of text. If `None`, language will be automatically detected.
        \*\*options
            skip_on_lang: :class:`bool`
                Whether to skip the attribute if the attribute does not support the text's language, or raise an `UnsupportedLanguageError` exception. Default is `False`.
            skip_on_unknown: :class:`bool`
                Whether to skip the attribute if it's invalid/unknown. Default is `False`.

        Returns
        --------
        :class:`dict`: A dictionary containing percents of every attribute requested.
        """
        try:
            for _ in attributes:
                pass
        except TypeError:
            if type(attributes) is not list:
                if type(attributes) is not str:
                    attributes = repr(attributes)
                attr_pass = 0
                for i in range(len(attributes.split("\",\""))):
                    if attributes.split("\",\"")[i] in ["TOXICITY", "SEVERE_TOXICITY", "IDENTITY_ATTACK", "INSULT", "PROFANITY", "THREAT", "TOXICITY_EXPERIMENTAL", "SEVERE_TOXICITY_EXPERIMENTAL", "IDENTITY_ATTACK_EXPERIMENTAL", "INSULT_EXPERIMENTAL", "PROFANITY_EXPERIMENTAL", "THREAT_EXPERIMENTAL", "SEXUALLY_EXPLICIT", "FLIRTATION", "ATTACK_ON_AUTHOR", "ATTACK_ON_COMMENTER", "INCOHERENT", "INFLAMMATORY", "LIKELY_TO_REJECT", "OBSCENE", "SPAM", "UNSUBSTANTIAL"]:
                        attr_pass += 1
                if attr_pass == len(attributes.split("\",\"")):
                    attributes = attributes.split("\",\"")
                else:
                    raise UnknownAttributeError("Attribute \"{}\" is unknown.".format(f'{attributes=}'.split('=')[1].replace('\'','')))
        attributes = list(attributes)
        if text.replace(" ", "") == "":
            raise EmptyTextError("The text cannot be empty.")

        for attribute in attributes:
            if f'{attribute=}'.split('=')[1].replace('\'','').upper() in ["TOXICITY", "SEVERE_TOXICITY", "IDENTITY_ATTACK", "INSULT", "PROFANITY", "THREAT", "TOXICITY_EXPERIMENTAL", "SEVERE_TOXICITY_EXPERIMENTAL", "IDENTITY_ATTACK_EXPERIMENTAL", "INSULT_EXPERIMENTAL", "PROFANITY_EXPERIMENTAL", "THREAT_EXPERIMENTAL", "SEXUALLY_EXPLICIT", "FLIRTATION", "ATTACK_ON_AUTHOR", "ATTACK_ON_COMMENTER", "INCOHERENT", "INFLAMMATORY", "LIKELY_TO_REJECT", "OBSCENE", "SPAM", "UNSUBSTANTIAL"]:
                attributes[attributes.index(attribute)] = f'{attribute=}'.split('=')[1].replace('\'','').upper()
            else:
                if not self.__get_attribute(f'{attribute=}'.split('=')[1].replace('\'','').upper()):
                    if attributes in [[Attributes.All], [Attributes.Production], [Attributes.Experimental], [Attributes.NewYorkTimes]]:
                        return self.analyze(text=text, attributes=attributes[0], language=language, **options)
                    if "skip_on_lang" in options and options["skip_on_lang"]:
                        del attributes[attributes.index(attribute)]
                        continue
                    else:
                        raise UnknownAttributeError("Attribute \"{}\" is unknown.".format(f'{attribute=}'.split('=')[1].replace('\'','')))
                else:
                    attributes[attributes.index(attribute)] = self.__get_attribute(f'{attribute=}'.split('=')[1].replace('\'','').upper())
                    if not attributes[attributes.index(attribute)]:
                        if "skip_on_unknown" in options and options["skip_on_unknown"]:
                            del attributes[attributes.index(attribute)]
                            continue
                        else:
                            raise UnknownAttributeError("Attribute \"{}\" is unknown.".format(f'{attribute=}'.split('=')[1].replace('\'','')))

        requestedAttributes_dict = {}
        for attribute in attributes:
            requestedAttributes_dict[str(attribute)] = {}
        
        if not language:
            analyze_request = {
                'comment': { 'text': text},
                'requestedAttributes': requestedAttributes_dict,
            }
        else:
            language = self.__get_language_code(language=language)
            analyze_request = {
                'comment': { 'text': text},
                'requestedAttributes': requestedAttributes_dict,
                'languages': [language]
            }
        if "skip_on_lang" in options and options["skip_on_lang"]:
            for _ in range(len(requestedAttributes_dict)):
                try:
                    response = self.client.comments().analyze(body=analyze_request).execute()
                except errors.HttpError as exceptionDetails:
                    if "does not support request languages" in str(exceptionDetails):
                        attribute = str(exceptionDetails).replace(f"<HttpError 400 when requesting https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={self.__token}&alt=json returned \"Attribute ", "").split()[0]
                        del analyze_request["requestedAttributes"][str(attribute)]
                        continue
                    else:
                        raise HTTPException("An unknown error occured. Please try again. Exception details: " + str(exceptionDetails))
                else:
                    break
        else:
            try:
                response = self.client.comments().analyze(body=analyze_request).execute()
            except errors.HttpError as exceptionDetails:
                if "does not support request languages" in str(exceptionDetails):
                    attribute = str(exceptionDetails).replace(f"<HttpError 400 when requesting https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={self.__token}&alt=json returned \"Attribute ", "").split()[0]
                    language = str(exceptionDetails)[str(exceptionDetails).find(attribute):].replace(attribute, "").replace(" does not support request languages: ", "").split("\"")[0]
                    raise UnsupportedLanguageError(f"{self.__get_language_name(language=language)} ({self.__get_language_code(language=language)}) is not supported by \"{attribute}\" attribute.")
                else:
                    raise HTTPException("An unknown error occured. Please try again. Exception details: " + str(exceptionDetails))
        result = {}

        for attribute in analyze_request["requestedAttributes"].keys():
            result[str(attribute)] = float(response['attributeScores'][str(attribute)]['spanScores'][0]['score']['value'])*100

        return result