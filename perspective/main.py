"""
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
"""

from googleapiclient import discovery, errors
from typing import Optional, Literal, Union
from pycountry import languages

from .attributes import Attributes, all_attrs, all_attr_grps
from .errors import *
from .utils import Utils as utils

import httplib2
import difflib
import logging
import sys
import os
import time
import traceback

class Client:
    @staticmethod
    def __supports_ansi_esc() -> bool:
        plat = sys.platform
        supported_platform = plat != 'Pocket PC' and (plat != 'win32' or 'ANSICON' in os.environ)
        is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
        return supported_platform and is_a_tty

    def __init__(self, token: str, logging_level: Optional[Union[Literal["NOTSET", "DEBUG", "INFO", "WARN", "ERROR", "CRITICAL"], Literal[0, 10, 20, 30, 40, 50]]] = None):
        global logger
        logger = logging.getLogger(__name__)
        if not not logging:
            levels = {"NOTSET":logging.NOTSET, "DEBUG":logging.DEBUG, "INFO":logging.INFO, "WARN":logging.WARN, "ERROR":logging.ERROR, "CRITICAL":logging.CRITICAL}
            levels_inverted = {v: k for k, v in levels.items()}
            try:
                final_level = levels[logging_level]
            except KeyError:
                try:
                    final_level = levels_inverted[logging_level]
                except KeyError:
                    logging.basicConfig(
                        format='%(asctime)s [%(levelname)-0s] %(message)s',
                        level=logging_level,
                        datefmt='%Y-%m-%d %H:%M:%S'
                    )
                else:
                    logging.basicConfig(
                        format='%(asctime)s [%(levelname)-0s] %(message)s',
                        level=final_level,
                        datefmt='%Y-%m-%d %H:%M:%S'
                    )
            else:
                logging.basicConfig(
                    format='%(asctime)s [%(levelname)-0s] %(message)s',
                    level=final_level,
                    datefmt='%Y-%m-%d %H:%M:%S'
                )
            self.__logging_level = final_level
            logger.disabled = False
        else:
            logging.basicConfig(
                format='%(asctime)s %(levelname)-8s %(message)s',
                level=logging.CRITICAL + 1,
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            logger.disabled = True
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
                if self.__supports_ansi_esc():
                    raise InvalidToken(r"The token you've entered is not a valid API key. Refer to \033[4mhttps://developers.perspectiveapi.com/s/docs-get-started\033[0m to get a new API key.").with_traceback(exceptionDetails.__traceback__) from None
                else:
                    raise InvalidToken("The token you've entered is not a valid API key. Refer to https://developers.perspectiveapi.com/s/docs-get-started to get a new API key.").with_traceback(exceptionDetails.__traceback__) from None
            else:
                raise HTTPException(str(exceptionDetails)).with_traceback(exceptionDetails.__traceback__) from None
        except httplib2.error.ServerNotFoundError as exceptionDetails:
            raise HTTPException("Unable to connect to the API. Please check your internet connection.").with_traceback(exceptionDetails.__traceback__) from None
        else:
            self.__token = token

    @property
    def logging_level(self):
        return self.__logging_level

    @logging_level.setter
    def logging_level(self, level: Optional[Union[Literal["NOTSET", "DEBUG", "INFO", "WARN", "ERROR", "CRITICAL"], Literal[0, 10, 20, 30, 40, 50]]] = None):
        if not not level:
            levels = {"NOTSET":logging.NOTSET, "DEBUG":logging.DEBUG, "INFO":logging.INFO, "WARN":logging.WARN, "ERROR":logging.ERROR, "CRITICAL":logging.CRITICAL}
            levels_inverted = {v: k for k, v in levels.items()}
            try:
                final_level = levels[level]
            except KeyError:
                try:
                    final_level = levels_inverted[level]
                except KeyError:
                    logging.basicConfig(
                        format='%(asctime)s [%(levelname)-0s] %(message)s',
                        level=level,
                        datefmt='%Y-%m-%d %H:%M:%S'
                    )
                else:
                    logging.basicConfig(
                        format='%(asctime)s [%(levelname)-0s] %(message)s',
                        level=final_level,
                        datefmt='%Y-%m-%d %H:%M:%S'
                    )
            else:
                logging.basicConfig(
                    format='%(asctime)s [%(levelname)-0s] %(message)s',
                    level=final_level,
                    datefmt='%Y-%m-%d %H:%M:%S'
                )
            self.__logging_level = final_level
            logger.disabled = False

    def change_token(self, token: str):
        if not token == self.__token:
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
                    if self.__supports_ansi_esc():
                        raise InvalidToken(r"The token you've entered is not a valid API key. Refer to \033[4mhttps://developers.perspectiveapi.com/s/docs-get-started\033[0m to get a new API key.").with_traceback(exceptionDetails.__traceback__) from None
                    else:
                        raise InvalidToken("The token you've entered is not a valid API key. Refer to https://developers.perspectiveapi.com/s/docs-get-started to get a new API key.").with_traceback(exceptionDetails.__traceback__) from None
                else:
                    raise HTTPException(str(exceptionDetails)).with_traceback(exceptionDetails.__traceback__) from None
            except httplib2.error.ServerNotFoundError as exceptionDetails:
                raise HTTPException("Unable to connect to the API. Please check your internet connection.").with_traceback(exceptionDetails.__traceback__) from None
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
            return difflib.get_close_matches(attribute, all_attrs, n=1)[0]
        except IndexError:
            return None

    def analyze(self, text: str, attributes: list[str] = Attributes.Production, language: Optional[str] = None, **options) -> dict:
        """
        Make a request to the Perspective API with the text and requested attributes that you've specified.

        Parameters
        -----------
        text: :class:`str`
            The text to analyze.
        attributes: :class:`list[str]`
            A list of attributes to analyze the text for. Default is `perspective.Attributes.Production` (all production-ready attributes).
        language: :class:`Optional[str]`
            The language of text. If `None`, language will be automatically detected. Default is `None`.
        \*\*options
            skip_on_lang: :class:`bool`
                Whether to skip the attribute if the attribute does not support the text's language, or raise an `UnsupportedLanguageError` exception. Default is `False`.
            skip_on_unknown: :class:`bool`
                Whether to skip the attribute if it's invalid/unknown. Default is `False`.
            return_raw: :class:`bool`
                Whether to return the raw response or a simplified response with only attributes and their score values. Default is `False`.

        Returns
        --------
        :class:`dict`: A dictionary containing percents of every attribute requested.
        """
        start_timestamp = time.time()
        try:
            if list(attributes) == []:
                raise MissingAttributes("No valid attributes were provided in attributes argument. Please specify at least one attribute.") from None
        except TypeError:
            pass
        if type(attributes) is str and any(attr in attributes for attr in all_attrs):
            if str(attributes) in all_attrs:
                attributes = [str(attributes)]
            else:
                raise InvalidFormat("The format of attributes provided is invalid. Please specify attributes by putting them into a list, such as [\"TOXICITY\", \"INSULT\"].") from None
        elif type(attributes) is str and not any(attr in attributes for attr in all_attrs):
            raise MissingAttributes("No valid attributes were provided in attributes argument. Please specify at least one attribute.") from None
        try:
            for _ in attributes:
                pass
        except TypeError as exceptionDetails:
            if type(attributes) is not list:
                if type(attributes) is not str:
                    attributes = repr(attributes)
                attr_pass = 0
                for i in range(len(attributes.split("\",\""))):
                    if attributes.split("\",\"")[i] in all_attrs:
                        attr_pass += 1
                if attr_pass == len(attributes.split("\",\"")):
                    attributes = attributes.split("\",\"")
                else:
                    raise UnknownAttribute("Attribute \"{}\" is unknown.".format(f'{attributes=}'.split('=')[1].replace('\'',''))).with_traceback(exceptionDetails.__traceback__) from None
        attributes = list(attributes)
        if text.replace(" ", "") == "":
            raise EmptyText("The text cannot be empty.") from None

        for _ in range(2):
            for attribute in attributes:
                if f'{attribute=}'.split('=')[1].replace('\'','').upper() in all_attrs:
                    attributes[attributes.index(attribute)] = f'{attribute=}'.split('=')[1].replace('\'','').upper()
                else:
                    if not self.__get_attribute(f'{attribute=}'.split('=')[1].replace('\'','').upper()):
                        if type(attributes) is list:
                            operation = 0
                            for attr in attributes:
                                if attr in all_attr_grps:
                                    attributes += repr(all_attr_grps[all_attr_grps.index(attr)]).split("\",\"")
                                    del attributes[attributes.index(attr)]
                                    operation += 1
                                else:
                                    continue
                            if operation != 0:
                                break
                        if "skip_on_unknown" in options and options["skip_on_unknown"]:
                            logger.debug("Skipping \"{}\" attribute since it's unknown.".format(f'{attribute=}'.split('=')[1].replace('\'','').upper()))
                            del attributes[attributes.index(attribute)]
                            continue
                        else:
                            raise UnknownAttribute("Attribute \"{}\" is unknown.".format(f'{attribute=}'.split('=')[1].replace('\'','').upper())) from None
                    else:
                        attributes[attributes.index(attribute)] = self.__get_attribute(f'{attribute=}'.split('=')[1].replace('\'','').upper())
                        if not attributes[attributes.index(attribute)]:
                            if "skip_on_unknown" in options and options["skip_on_unknown"]:
                                del attributes[attributes.index(attribute)]
                                continue
                            else:
                                raise UnknownAttribute("Attribute \"{}\" is unknown.".format(f'{attribute=}'.split('=')[1].replace('\'',''))) from None

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
                        language = str(exceptionDetails)[str(exceptionDetails).find(attribute):].replace(attribute, "").replace(" does not support request languages: ", "").split("\"")[0]
                        del analyze_request["requestedAttributes"][str(attribute)]
                        logger.debug(f"Skipping \"{attribute}\" attribute since {self.__get_language_name(language=language)} ({self.__get_language_code(language=language)}) is not supported by the attribute.")
                        continue
                    else:
                        raise HTTPException(str(exceptionDetails)).with_traceback(exceptionDetails.__traceback__) from None
                else:
                    break
        else:
            try:
                response = self.client.comments().analyze(body=analyze_request).execute()
            except errors.HttpError as exceptionDetails:
                if "does not support request languages" in str(exceptionDetails):
                    attribute = str(exceptionDetails).replace(f"<HttpError 400 when requesting https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={self.__token}&alt=json returned \"Attribute ", "").split()[0]
                    language = str(exceptionDetails)[str(exceptionDetails).find(attribute):].replace(attribute, "").replace(" does not support request languages: ", "").split("\"")[0]
                    raise UnsupportedLanguage(f"{self.__get_language_name(language=language)} ({self.__get_language_code(language=language)}) is not supported by \"{attribute}\" attribute.").with_traceback(exceptionDetails.__traceback__) from None
                else:
                    raise HTTPException("An unknown error occured. Please try again. Exception details: " + str(exceptionDetails)) from None
        result = {}

        for attribute in analyze_request["requestedAttributes"].keys():
            result[str(attribute)] = float(response['attributeScores'][str(attribute)]['spanScores'][0]['score']['value'])*100

        try:
            if "return_raw" in options and options["return_raw"]:
                return response
            return result
        except Exception:
            pass
        finally:
            logger.info("Perspective API text analysis has been completed. Request took {:.2f} seconds to process. The attribute with highest score value is {} with a score value of {:.2f}.".format(time.time() - start_timestamp, utils.get_highest(result), result[utils.get_highest(result)]))