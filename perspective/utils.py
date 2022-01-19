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

from typing import Optional, Literal

import matplotlib.pyplot as plt
import matplotlib
import sqlite3 as sql
import os

from .errors import *

matplotlib.set_loglevel("CRITICAL")

class Utils:
    @staticmethod
    def format_response(response: dict, align_right: bool = False, sort_by: Optional[Literal["ascending", "descending"]] = None) -> str:
        """
        Format the dictionary that the `analyze` function returned to a text which is easily readable by a human. The score values of attributes' digit count after the decimal will be decreased to 2 and the
        attribute names will be in lowercase. As an example, formatted text looks like the below text:
        
        ```d
        Toxicity:        97.64%
        Severe Toxicity: 84.36%
        Identity Attack: 26.57%
        Insult:          84.34%
        Profanity:       98.34%
        Threat:          32.14%
        ```

        Parameters
        -----------
        response: :class:`dict`
            The dictionary that the `analyze` function returned.
        align_right: :class:`bool`
            Whether the attribute names should be aligned to right or not. Default is `False`.
        sort_by: :class:`Optional[Literal["ascending", "descending"]]`
            Whether to sort the attributes ascending or descending according to their score values. If `None`, attributes will not be sorted. Default is `None`.

        Returns
        --------
        :class:`str`: The formatted text.
        """
        if response == {}:
            raise EmptyResponse("The response provided is an empty dictionary. Please make sure you're specifying the correct dictionary.") from None

        if "attributeScores" in response.keys():
            response_new = {}

            for attribute in response["attributeScores"].keys():
                response_new[str(attribute)] = float(response['attributeScores'][str(attribute)]['summaryScore']['value']) * 100
            response = response_new
            del response_new

        if not not sort_by:
            response = {k: v for k, v in sorted(response.items(), reverse=True if sort_by == "descending" else False if sort_by == "ascending" else None, key=lambda item: item[1])}

        return_var = str()
        max_char = len(max(response, key=len))
        for attribute, result in response.items():
            if list(response.items()).index((attribute, result)) == 0:
                if align_right:
                    return_var += " " * (max_char - len(attribute)) + attribute.replace("_"," ").title().replace("On ","on ").replace("To ","to ") + ": " + "%.2f" % result + "%"
                else:
                    return_var += attribute.replace("_"," ").title().replace("On ","on ").replace("To ","to ") + ": " + " " * (max_char - len(attribute)) + "%.2f" % result + "%"
                continue
            if align_right:
                return_var += "\n" + " " * (max_char - len(attribute)) + attribute.replace("_"," ").title().replace("On ","on ").replace("To ","to ") + ": " + "%.2f" % result + "%"
            else:
                return_var += "\n" + attribute.replace("_"," ").title().replace("On ","on ").replace("To ","to ") + ": " + " " * (max_char - len(attribute)) + "%.2f" % result + "%"
        return return_var

    @staticmethod
    def get_highest(response: dict) -> Optional[str]:
        """
        Returns the attribute with the highest score value.

        Parameters
        -----------
        response: :class:`dict`
            The dictionary that the `analyze` function returned.

        Returns
        --------
        :class:`Optional[str]`: The attribute with highest score value.
        """
        if response == {}:
            raise EmptyResponse("The response provided is an empty dictionary. Please make sure you're specifying the correct dictionary.") from None

        if "attributeScores" in response.keys():
            response_new = {}

            for attribute in response["attributeScores"].keys():
                response_new[str(attribute)] = float(response['attributeScores'][str(attribute)]['summaryScore']['value']) * 100
            response = response_new
            del response_new

        return max(response, key=response.get)
    @staticmethod
    def get_lowest(response: dict) -> Optional[str]:
        """
        Returns the attribute with the lowest score value.

        Parameters
        -----------
        response: :class:`dict`
            The dictionary that the `analyze` function returned.

        Returns
        --------
        :class:`Optional[str]`: The attribute with lowest score value.
        """
        if response == {}:
            raise EmptyResponse("The response provided is an empty dictionary. Please make sure you're specifying the correct dictionary.") from None

        if "attributeScores" in response.keys():
            response_new = {}

            for attribute in response["attributeScores"].keys():
                response_new[str(attribute)] = float(response['attributeScores'][str(attribute)]['summaryScore']['value']) * 100
            response = response_new
            del response_new

        return min(response, key=response.get)

    @staticmethod
    def show_graph(response: dict, title: Optional[str] = None, grid_lines: bool = True, **kwargs) -> None:
        """
        Draws a bar chart/plot with the data that the `analyze` function returned and shows it by creating an interactive window using the matplotlib library.

        Parameters
        -----------
        response: :class:`dict`
            The dictionary that the `analyze` function returned.
        title: :class:`Optional[str]`
            The title for the chart. Default is "Perspective API result".
        grid_lines: :class:`bool`
            Whether the chart should have grid lines or not. Default is `True`
        **kwargs
            Other keyword arguments that belong to `matplotlib.pyplot.barh` function; such as `height`, `color` etc.
        """
        if response == {}:
            raise EmptyResponse("The response provided is an empty dictionary. Please make sure you're specifying the correct dictionary.") from None

        if "attributeScores" in response.keys():
            response_new = {}

            for attribute in response["attributeScores"].keys():
                response_new[str(attribute)] = float(response['attributeScores'][str(attribute)]['summaryScore']['value']) * 100
            response = response_new
            del response_new

        response = {k: v for k, v in sorted(response.items(), key=lambda item: item[1])}
        keys, values = zip(*response.items())
        keys = list(keys)
        for key in keys:
            keys[keys.index(key)] = key.replace("_"," ").title().replace("On ","on ").replace("To ","to ")
        keys = tuple(keys)

        fig = plt.figure("Perspective API result" if not title else title, figsize=(15, 6), dpi=80)
        ax1 = fig.add_subplot(111)

        ax1.barh(keys, values, **kwargs)

        plt.title("Perspective API result" if not title else title)
        plt.xlabel(xlabel="Score values %")
        plt.ylabel(ylabel="Attributes")

        rects = ax1.patches

        for rect in rects:
            x_value = rect.get_width()
            y_value = rect.get_y() + rect.get_height() / 2

            space = 5
            ha = 'left'
            if x_value < 0:
                space *= -1
                ha = 'right'
            label = "{:.1f}%".format(x_value)

            plt.annotate(label, (x_value, y_value), xytext=(space, 0), textcoords="offset points", va='center', ha=ha)

        plt.xticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
    
        if grid_lines == True:
            plt.grid(b = True, color ='grey', linestyle ='-', linewidth = 0.5, alpha = 0.2)

        plt.show()

    @staticmethod
    def save_graph(response: dict, filename: str = "chart.png", title: Optional[str] = None, grid_lines: bool = False, **kwargs):
        r"""
        Draws a bar chart/plot with the data that the `analyze` function returned and saves it as a *.png file with the specified filename to the specified directory, using the matplotlib library.

        Parameters
        -----------
        response: :class:`dict`
            The dictionary that the `analyze` function returned.
        filename: :class:`str`
            The path that you want the file to be saved, including the filename (such as `C:\path\to\my\file.png`). Default is "chart.png" in the same directory script is running.
        title: :class:`Optional[str]`
            The title for the chart. Default is "Perspective API result".
        grid_lines: :class:`bool`
            Whether the chart should have grid lines or not. Default is `True`
        **kwargs
            Other keyword arguments that belong to `matplotlib.pyplot.barh` function; such as `height`, `color` etc.
        """
        if filename.replace(" ","") == "":
            raise EmptyFileName("The filename cannot be an empty string.") from None
        if response == {}:
            raise EmptyResponse("The response provided is an empty dictionary. Please make sure you're specifying the correct dictionary.") from None

        if "attributeScores" in response.keys():
            response_new = {}

            for attribute in response["attributeScores"].keys():
                response_new[str(attribute)] = float(response['attributeScores'][str(attribute)]['summaryScore']['value']) * 100
            response = response_new
            del response_new

        response = {k: v for k, v in sorted(response.items(), key=lambda item: item[1])}
        keys, values = zip(*response.items())
        keys = list(keys)
        keys.reverse()
        for key in keys:
            keys[keys.index(key)] = key.replace("_"," ").title().replace("On ","on ").replace("To ","to ")
        keys = tuple(keys)

        fig = plt.figure("Perspective API result" if not title else title, figsize=(15, 6), dpi=80)
        ax1 = fig.add_subplot(111)

        ax1.barh(keys, values, **kwargs)

        plt.title("Perspective API result" if not title else title)
        plt.xlabel(xlabel="Score values %")
        plt.ylabel(ylabel="Attributes")

        rects = ax1.patches

        for rect in rects:
            x_value = rect.get_width()
            y_value = rect.get_y() + rect.get_height() / 2

            space = 5
            ha = 'left'
            if x_value < 0:
                space *= -1
                ha = 'right'
            label = "{:.1f}%".format(x_value)

            plt.annotate(label, (x_value, y_value), xytext=(space, 0), textcoords="offset points", va='center', ha=ha)

        plt.xticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
    
        if grid_lines == True:
            plt.grid(b = True, color ='grey', linestyle ='-', linewidth = 0.5, alpha = 0.2)

        plt.savefig(filename, bbox_inches='tight')

    @staticmethod
    def save_data(response: dict, filename: str = "data.sqlite3", sort_by: Optional[Literal["ascending", "descending"]] = None) -> None:
        r"""
        Saves the data that the `analyze` function returned to a SQLite3 database. The database will have a table named `data` which shall contain attribute names in `attribute` column and the attribute's
        score value in `value` column. The database will be recreated whenever you call this function with the same `filename` argument.

        Parameters
        -----------
        response: :class:`dict`
            The dictionary that the `analyze` function returned.
        filename: :class:`str`
            The path that you want the database to be saved, including the filename (such as `C:\path\to\my\database.sqlite3`). Default is "data.sqlite3" in the same directory script is running.
        sort_by: :class:`bool`
            Whether to sort the attributes ascending or descending according to their score values. If `None`, attributes will not be sorted. Default is `None`.
        """
        if response == {}:
            raise EmptyResponse("The response provided is an empty dictionary. Please make sure you're specifying the correct dictionary.") from None
        if filename.replace(" ","") == "":
            raise EmptyFileName("The filename cannot be an empty string.") from None

        if "attributeScores" in response.keys():
            response_new = {}

            for attribute in response["attributeScores"].keys():
                response_new[str(attribute)] = float(response['attributeScores'][str(attribute)]['summaryScore']['value']) * 100
            response = response_new
            del response_new
        
        if not not sort_by:
            response = {k: v for k, v in sorted(response.items(), reverse=True if sort_by == "descending" else False, key=lambda item: item[1])}

        if os.path.exists(filename):
            os.remove(filename)
        con = sql.connect(filename)
        cursor = con.cursor()
        cursor.execute(f"CREATE TABLE IF NOT EXISTS data (attribute, value)")

        for attribute, value in response.items():
            cursor.execute(f"INSERT INTO data VALUES ('{attribute.upper()}', {value})")

        con.commit()
        con.close()