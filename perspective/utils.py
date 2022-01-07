from typing import Optional
import matplotlib.pyplot as plt

class Utils:
    @staticmethod
    def format_response(response: dict, align_right: bool = False) -> str:
        """
        Format the dictionary that the `analyze` function returned to a text which is easily readable by a human. The score values of attributes' digit count after the decimal will be decreased to 2 and the attribute names will be in lowercase. As an example, formatted text looks like the below text:
        
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
            Whether the attribute names should be aligned to right or not. `False` by default.

        Returns
        --------
        :class:`str`: The formatted text.
        """
        return_var = str()
        max_char = len(max(response, key=len))
        for attribute, result in response.items():
            if list(response.items()).index((attribute, result)) == 0:
                if align_right:
                    return_var += " " * (max_char - len(attribute)) + attribute.replace("_"," ").title().replace("On","on").replace("To","to") + ": " + "%.2f" % result + "%"
                else:
                    return_var += attribute.replace("_"," ").title().replace("On ","on ").replace("To ","to ") + ": " + " " * (max_char - len(attribute)) + "%.2f" % result + "%"
                continue
            if align_right:
                return_var += "\n" + " " * (max_char - len(attribute)) + attribute.replace("_"," ").title().replace("On","on").replace("To","to") + ": " + "%.2f" % result + "%"
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
            Other keyword arguments that belong to `matplotlib.pyplot.barh` function; such as `height`, `width` etc.
        """
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
    
        if grid_lines:
            plt.grid(b = True, color ='grey', linestyle ='-', linewidth = 0.5, alpha = 0.2)

        plt.show()

    @staticmethod
    def save_graph(response: dict, filename: str, title: Optional[str] = None, grid_lines: bool = False, **kwargs):
        r"""
        Draws a bar chart/plot with the data that the `analyze` function returned and saves it as a *.png file with the specified filename to the specified directory, using the matplotlib library..

        Parameters
        -----------
        response: :class:`dict`
            The dictionary that the `analyze` function returned.
        filename: :class:`str`
            The path that you want the file to be saved, including the filename (such as `C:\path\to\my\file.png`)
        title: :class:`Optional[str]`
            The title for the chart. Default is "Perspective API result".
        grid_lines: :class:`bool`
            Whether the chart should have grid lines or not. Default is `True`
        **kwargs
            Other keyword arguments that belong to `matplotlib.pyplot.barh` function; such as `height`, `width` etc.
        """
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
    
        if grid_lines:
            plt.grid(b = True, color ='grey', linestyle ='-', linewidth = 0.5, alpha = 0.2)

        plt.savefig(filename, bbox_inches='tight')