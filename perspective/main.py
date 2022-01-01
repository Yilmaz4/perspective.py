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

class Attributes:
    # Production attributes
    class TOXICITY:
        """
        ## TOXICITY
        A rude, disrespectful, or unreasonable comment that is likely to make people leave a discussion.

        ### Supported language(s)

        Arabic (ar), Chinese (zh), Czech (cs), Dutch (nl), English (en), French (fr), German (de),
        Hindi (hi), Hinglish (hi-Latn), Indonesian (id), Italian (it), Japanese (ja), Korean (ko),
        Polish (pl), Portuguese (pt), Russian (ru), Spanish (es)
        """
        supportedLanguages = ["ar", "zh", "cs", "nl", "en", "fr", "de", "hi", "id", "it", "ja", "ko", "pl", "pt", "ru", "es"]
        description = "A rude, disrespectful, or unreasonable comment that is likely to make people leave a discussion."
        isExperimental = False
        def __repr__(self):
            return "TOXICITY"
    TOXICITY = TOXICITY()
    class SEVERE_TOXICITY:
        """
        ## SEVERE_TOXICITY
        A very hateful, aggressive, disrespectful comment or otherwise very likely to make a user leave
        a discussion or give up on sharing their perspective. This attribute is much less sensitive to
        more mild forms of toxicity, such as comments that include positive uses of curse words.

        ### Supported language(s)

        German (de), English (en), Spanish (es), French (fr), Italian (it), Portuguese (pt), Russian (ru)
        """
        supportedLanguages = ["de", "en", "es", "fr", "it", "pt", "ru"]
        description = "A very hateful, aggressive, disrespectful comment or otherwise very likely to make a user leave a discussion or give up on sharing their perspective. This attribute is much less sensitive to more mild forms of toxicity, such as comments that include positive uses of curse words."
        isExperimental = False
        def __repr__(self):
            return "SEVERE_TOXICITY"
    SEVERE_TOXICITY = SEVERE_TOXICITY()
    class IDENTIFY_ATTACK:
        """
        ## IDENTIFY_ATTACK
        Negative or hateful comments targeting someone because of their identity.

        ### Supported language(s)

        German (de), English (en), Italian (it), Portuguese (pt), Russian (ru)
        """
        supportedLanguages = ["de", "en", "it", "pt", "ru"]
        description = "Negative or hateful comments targeting someone because of their identity."
        isExperimental = False
        def __repr__(self):
            return "IDENTIFY_ATTACK"
    IDENTIFY_ATTACK = IDENTIFY_ATTACK()
    class INSULT:
        """
        ## INSULT
        Insulting, inflammatory, or negative comment towards a person or a group of people.

        ### Supported language(s)

        German (de), English (en), Italian (it), Portuguese (pt), Russian (ru)
        """
        supportedLanguages = ["de", "en", "it", "pt", "ru"]
        description = "Insulting, inflammatory, or negative comment towards a person or a group of people."
        isExperimental = False
        def __repr__(self):
            return "INSULT"
    INSULT = INSULT()
    class PROFANITY:
        """
        ## PROFANITY
        Swear words, curse words, or other obscene or profane language.

        ### Supported language(s)

        German (de), English (en), Italian (it), Portuguese (pt), Russian (ru)
        """
        supportedLanguages = ["de", "en", "it", "pt", "ru"]
        description = "Swear words, curse words, or other obscene or profane language."
        isExperimental = False
        def __repr__(self):
            return "PROFANITY"
    PROFANITY = PROFANITY()
    class THREAT:
        """
        ## THREAT
        Describes an intention to inflict pain, injury, or violence against an individual or group.

        ### Supported language(s)

        German (de), English (en), Italian (it), Portuguese (pt), Russian (ru)
        """
        supportedLanguages = ["de", "en", "it", "pt", "ru"]
        description = "Describes an intention to inflict pain, injury, or violence against an individual or group."
        isExperimental = False
        def __repr__(self):
            return "THREAT"
    THREAT = THREAT()

    # Experimental attributes
    class TOXICITY_EXPERIMENTAL:
        """
        ## TOXICITY_EXPERIMENTAL
        A rude, disrespectful, or unreasonable comment that is likely to make people leave a discussion.

        ### Important notes on using experimental attributes:

         - Once experimental attributes are deprecated and production attributes are created, the experimental attribute will stop working. When that happens, you will need to update the API call's attribute name to the new production attribute name.
        
         - Expect language availability to change over time as we test attribute performance and move attributes to production.

        """
        description = "A rude, disrespectful, or unreasonable comment that is likely to make people leave a discussion."
        isExperimental = True
        def __repr__(self):
            return "TOXICITY_EXPERIMENTAL"
    TOXICITY_EXPERIMENTAL = TOXICITY_EXPERIMENTAL()
    class SEVERE_TOXICITY_EXPERIMENTAL:
        """
        ## SEVERE_TOXICITY_EXPERIMENTAL
        A very hateful, aggressive, disrespectful comment or otherwise very likely to make a user leave
        a discussion or give up on sharing their perspective. This attribute is much less sensitive to
        more mild forms of toxicity, such as comments that include positive uses of curse words.

        ### Important notes on using experimental attributes:

         - Once experimental attributes are deprecated and production attributes are created, the experimental attribute will stop working. When that happens, you will need to update the API call's attribute name to the new production attribute name.
        
         - Expect language availability to change over time as we test attribute performance and move attributes to production.

        """
        description = "A very hateful, aggressive, disrespectful comment or otherwise very likely to make a user leave a discussion or give up on sharing their perspective. This attribute is much less sensitive to more mild forms of toxicity, such as comments that include positive uses of curse words."
        isExperimental = True
        def __repr__(self):
            return "SEVERE_TOXICITY_EXPERIMENTAL"
    SEVERE_TOXICITY_EXPERIMENTAL = SEVERE_TOXICITY_EXPERIMENTAL()
    class IDENTIFY_ATTACK_EXPERIMENTAL:
        """
        ## IDENTIFY_ATTACK_EXPERIMENTAL
        Negative or hateful comments targeting someone because of their identity.

        ### Important notes on using experimental attributes:

         - Once experimental attributes are deprecated and production attributes are created, the experimental attribute will stop working. When that happens, you will need to update the API call's attribute name to the new production attribute name.
        
         - Expect language availability to change over time as we test attribute performance and move attributes to production.

        """
        description = "Negative or hateful comments targeting someone because of their identity."
        isExperimental = True
        def __repr__(self):
            return "IDENTIFY_ATTACK_EXPERIMENTAL"
    IDENTIFY_ATTACK_EXPERIMENTAL = IDENTIFY_ATTACK_EXPERIMENTAL()
    class INSULT_EXPERIMENTAL:
        """
        ## INSULT_EXPERIMENTAL
        Insulting, inflammatory, or negative comment towards a person or a group of people.

        ### Important notes on using experimental attributes:

         - Once experimental attributes are deprecated and production attributes are created, the experimental attribute will stop working. When that happens, you will need to update the API call's attribute name to the new production attribute name.
        
         - Expect language availability to change over time as we test attribute performance and move attributes to production.

        """
        description = "Insulting, inflammatory, or negative comment towards a person or a group of people."
        isExperimental = True
        def __repr__(self):
            return "INSULT_EXPERIMENTAL"
    INSULT_EXPERIMENTAL = INSULT_EXPERIMENTAL()
    class PROFANITY_EXPERIMENTAL:
        """
        ## PROFANITY_EXPERIMENTAL
        Swear words, curse words, or other obscene or profane language.

        ### Important notes on using experimental attributes:

         - Once experimental attributes are deprecated and production attributes are created, the experimental attribute will stop working. When that happens, you will need to update the API call's attribute name to the new production attribute name.
        
         - Expect language availability to change over time as we test attribute performance and move attributes to production.

        """
        description = "Swear words, curse words, or other obscene or profane language."
        isExperimental = True
        def __repr__(self):
            return "PROFANITY_EXPERIMENTAL"
    PROFANITY_EXPERIMENTAL = PROFANITY_EXPERIMENTAL()
    class THREAT_EXPERIMENTAL:
        """
        ## THREAT_EXPERIMENTAL
        Describes an intention to inflict pain, injury, or violence against an individual or group.

        ### Important notes on using experimental attributes:

         - Once experimental attributes are deprecated and production attributes are created, the experimental attribute will stop working. When that happens, you will need to update the API call's attribute name to the new production attribute name.
        
         - Expect language availability to change over time as we test attribute performance and move attributes to production.

        """
        description = "Describes an intention to inflict pain, injury, or violence against an individual or group."
        isExperimental = True
        def __repr__(self):
            return "THREAT_EXPERIMENTAL"
    THREAT_EXPERIMENTAL = THREAT_EXPERIMENTAL()
    class SEXUALLY_EXPLICIT:
        """
        ## SEXUALLY_EXPLICIT
        Contains references to sexual acts, body parts, or other lewd content.

        ### Important notes on using experimental attributes:

         - Once experimental attributes are deprecated and production attributes are created, the experimental attribute will stop working. When that happens, you will need to update the API call's attribute name to the new production attribute name.
        
         - Expect language availability to change over time as we test attribute performance and move attributes to production.

        """
        description = "Contains references to sexual acts, body parts, or other lewd content."
        isExperimental = True
        def __repr__(self):
            return "SEXUALLY_EXPLICIT"
    SEXUALLY_EXPLICIT = SEXUALLY_EXPLICIT()
    class FLIRTATION:
        """
        ## FLIRTATION
        Pickup lines, complimenting appearance, subtle sexual innuendos, etc.

        ### Important notes on using experimental attributes:

         - Once experimental attributes are deprecated and production attributes are created, the experimental attribute will stop working. When that happens, you will need to update the API call's attribute name to the new production attribute name.
        
         - Expect language availability to change over time as we test attribute performance and move attributes to production.

        """
        description = "Pickup lines, complimenting appearance, subtle sexual innuendos, etc."
        isExperimental = True
        def __repr__(self):
            return "FLIRTATION"
    FLIRTATION = FLIRTATION()
    
    # New York Times attributes
    class ATTACK_ON_AUTHOR:
        """
        ## ATTACK_ON_AUTHOR
        Attack on the author of an article or post.

        ### Supported language(s)

        English (en)
        """
        supportedLanguages = ["en"]
        description = "Attack on the author of an article or post."
        isExperimental = True
        def __repr__(self):
            return "ATTACK_ON_AUTHOR"
    ATTACK_ON_AUTHOR = ATTACK_ON_AUTHOR()
    class ATTACK_ON_COMMENTER:
        """
        ## ATTACK_ON_COMMENTER
        Attack on fellow commenter.

        ### Supported language(s)

        English (en)
        """
        supportedLanguages = ["en"]
        description = "Attack on fellow commenter."
        isExperimental = True
        def __repr__(self):
            return "ATTACK_ON_COMMENTER"
    ATTACK_ON_COMMENTER = ATTACK_ON_COMMENTER()
    class INCOHERENT:
        """
        ## INCOHERENT
        Difficult to understand, nonsensical.

        ### Supported language(s)

        English (en)
        """
        supportedLanguages = ["en"]
        description = "Difficult to understand, nonsensical."
        isExperimental = True
        def __repr__(self):
            return "INCOHERENT"
    INCOHERENT = INCOHERENT()
    class INFLAMMATORY:
        """
        ## INFLAMMATORY
        Intending to provoke or inflame.

        ### Supported language(s)

        English (en)
        """
        supportedLanguages = ["en"]
        description = "Intending to provoke or inflame."
        isExperimental = True
        def __repr__(self):
            return "INFLAMMATORY"
    INFLAMMATORY = INFLAMMATORY()
    class LIKELY_TO_REJECT:
        """
        ## LIKELY_TO_REJECT
        Overall measure of the likelihood for the comment to be rejected according to the NYT's moderation.

        ### Supported language(s)

        English (en)
        """
        supportedLanguages = ["en"]
        description = "Overall measure of the likelihood for the comment to be rejected according to the NYT's moderation."
        isExperimental = True
        def __repr__(self):
            return "LIKELY_TO_REJECT"
    LIKELY_TO_REJECT = LIKELY_TO_REJECT()
    class OBSCENE:
        """
        ## OBSCENE
        Obscene or vulgar language such as cursing.

        ### Supported language(s)

        English (en)
        """
        supportedLanguages = ["en"]
        description = "Obscene or vulgar language such as cursing."
        isExperimental = True
        def __repr__(self):
            return "OBSCENE"
    OBSCENE = OBSCENE()
    class SPAM:
        """
        ## SPAM
        Irrelevant and unsolicited commercial content.

        ### Supported language(s)

        English (en)
        """
        supportedLanguages = ["en"]
        description = "Irrelevant and unsolicited commercial content."
        isExperimental = True
        def __repr__(self):
            return "SPAM"
    SPAM = SPAM()
    class UNSUBSTANTIAL:
        """
        ## UNSUBSTANTIAL
        Trivial or short comments.

        ### Supported language(s)

        English (en)
        """
        supportedLanguages = ["en"]
        description = "Trivial or short comments."
        isExperimental = True
        def __repr__(self):
            return "UNSUBSTANTIAL"
    UNSUBSTANTIAL = UNSUBSTANTIAL()

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
        except httplib2.error.ServerNotFoundError as exceptionDetails:
            raise HTTPException("Unable to connect to the API.")
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
            return difflib.get_close_matches(attribute, ["TOXICITY", "SEVERE_TOXICITY", "IDENTIFY_ATTACK", "INSULT", "PROFANITY", "THREAT_EXPERIMENTAL", "TOXICITY_EXPERIMENTAL", "SEVERE_TOXICITY_EXPERIMENTAL", "IDENTIFY_ATTACK_EXPERIMENTAL", "INSULT_EXPERIMENTAL", "PROFANITY_EXPERIMENTAL", "THREAT_EXPERIMENTAL", "SEXUALLY_EXPLICIT", "FLIRTATION", "ATTACK_ON_AUTHOR", "ATTACK_ON_COMMENTER", "INCOHERENT", "INFLAMMATORY", "LIKELY_TO_REJECT", "OBSCENE", "SPAM", "UNSUBSTANTIAL"], n=1)[0]
        except IndexError:
            return None

    def analyze(self, text: str, requestedAttributes: list[str], language: Optional[str] = None) -> dict:
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

        Returns
        --------
        :class:`dict`
            A dictionary containing percents of every attribute requested.
        """
        if text.replace(" ", "") == "":
            raise EmptyTextError("Text cannot be empty.")

        for attribute in requestedAttributes:
            if f'{attribute=}'.split('=')[1].replace('\'','').upper() in ["TOXICITY", "SEVERE_TOXICITY", "IDENTIFY_ATTACK", "INSULT", "PROFANITY", "THREAT_EXPERIMENTAL", "TOXICITY_EXPERIMENTAL", "SEVERE_TOXICITY_EXPERIMENTAL", "IDENTIFY_ATTACK_EXPERIMENTAL", "INSULT_EXPERIMENTAL", "PROFANITY_EXPERIMENTAL", "THREAT_EXPERIMENTAL", "SEXUALLY_EXPLICIT", "FLIRTATION", "ATTACK_ON_AUTHOR", "ATTACK_ON_COMMENTER", "INCOHERENT", "INFLAMMATORY", "LIKELY_TO_REJECT", "OBSCENE", "SPAM", "UNSUBSTANTIAL"]:
                requestedAttributes[requestedAttributes.index(attribute)] = f'{attribute=}'.split('=')[1].replace('\'','').upper()
            else:
                if not self.__get_attribute(f'{attribute=}'.split('=')[1].replace('\'','').upper()):
                    raise UnknownAttributeError("Attribute \"{}\" is unknown. See https://developers.perspectiveapi.com/s/about-the-api-attributes-and-languages for all attributes.".format(f'{attribute=}'.split('=')[1].replace('\'','')))
                else:
                    requestedAttributes[requestedAttributes.index(attribute)] = self.__get_attribute(f'{attribute=}'.split('=')[1].replace('\'','').upper())

        requestedAttributes_dict = {}
        for attribute in requestedAttributes:
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
        try:
            response = self.client.comments().analyze(body=analyze_request).execute()
        except errors.HttpError as exceptionDetails:
            if "does not support request languages" in str(exceptionDetails):
                attribute = str(exceptionDetails).replace(f"<HttpError 400 when requesting https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={self.__token}&alt=json returned \"Attribute ", "").split()[0]
                language = str(exceptionDetails)[str(exceptionDetails).find(attribute):].replace(attribute, "").replace(" does not support request languages: ", "").split("\"")[0]
                raise UnsupportedLanguageError(f"{self.__get_language_name(language=language)} ({self.__get_language_code(language=language)}) is not supported by \"{attribute}\" attribute.")
                return
        result = {}

        for attribute in requestedAttributes:
            result[str(attribute)] = float(response['attributeScores'][str(attribute)]['spanScores'][0]['score']['value'])*100

        return result