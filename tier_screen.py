import os
from PIL import Image, ImageDraw
if __name__ == '__main__':
    import argparse


template_file = 'images/template.jpg'


class Pos:
    """A position. This class uses `__slots__`.

    Args:
        x: The x coordinate of this postion.
        y: The y coordinate of this postion.

    Attributes:
        x (int): The x coordinate of this postion.
        y (int): The y coordinate of this postion.
    """
    __slots__ = ('x', 'y')

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'Pos(x={self.x}, y={self.y})'

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __getitem__(self, index):
        if index == 0:
            return self.x
        if index == 1:
            return self.y
        raise IndexError()

    def tup(self):
        """Get the position as a tuple."""
        return (self.x, self.y)


class Bar:
    """A bar to be drawn on a bar graph.

    Args:
        pos: The position of the bar from the bottom left corner.
        width: The width of the bar.
        height: The height of the bar.
        color: The color of the bar. Should contain three numbers (red,
            green, blue), each in the range 0-255.

    Attributes:
        pos (Pos): The position of the bar from the bottom left corner.
        width (int): The width of the bar.
        height (int): The height of the bar.
        color (tuple): The color of the bar. Contains three numbers
            (red, green, blue) each in the range 0-255.
    """

    def __init__(self, pos: Pos, width: int, height: int, color):
        self.pos = pos
        self.width = width
        self.height = height
        self.color = color

    def draw(self, image):
        """Draw this bar on `image`."""
        if self.height == 0 or self.width == 0:
            return
        draw = ImageDraw.Draw(image)
        top_right = Pos(self.pos.x + self.width, self.pos.y - self.height)
        draw.rectangle(self.pos.tup() + top_right.tup(), fill=self.color)


class TierScreen:
    """A tier screen.
    
    Args:
        template_file: The file containing the tier screen template.
        image: The image to use in the tier screen. This should be
            460x396.
        *heights: The heights of the bars in the graph in range 0-100.
            Order: (int, pwr, def, mbl, hp, stl). If the first item is
            an iterable, that will become the heights list.

    Attributes:
        template_file (os.PathLike): The file containing the tier screen
            template.
        image (Image): The image to use in the tier screen.
        bars (dict): A list of `Bar` objects. These are the bars of the
            graph for the int, pwr, def, mbl, hp, and stl.
    """

    def __init__(self, template_file: os.PathLike, image: Image, *heights: int):
        self.template_file = template_file
        self.image = image.convert('RGB')
        self.image.thumbnail((460, 396), Image.ANTIALIAS)
        self._image_pos = Pos(100, 151)
        if len(heights) == 1:
            heights = heights[0]
        bar_width = 60
        self._graph_bottom = 628
        self._graph_top = 156
        bar_height = self._graph_bottom - self._graph_top
        self.bars = {
            'int': Bar(Pos(804,  self._graph_bottom), bar_width, heights[0] / 100 * bar_height, (255, 255, 255)),
            'pwr': Bar(Pos(901,  self._graph_bottom), bar_width, heights[1] / 100 * bar_height, (247, 130, 1)),
            'def': Bar(Pos(999,  self._graph_bottom), bar_width, heights[2] / 100 * bar_height, (65,  148, 254)),
            'mbl': Bar(Pos(1096, self._graph_bottom), bar_width, heights[3] / 100 * bar_height, (102, 190, 54)),
            'hp':  Bar(Pos(1191, self._graph_bottom), bar_width, heights[4] / 100 * bar_height, (174, 37,  21)),
            'stl': Bar(Pos(1287, self._graph_bottom), bar_width, heights[5] / 100 * bar_height, (100, 119, 151)),
        }

    def save(self, filename: str):
        """Save the tier screen to file `filename`."""
        tier_screen_image = Image.open(self.template_file)
        tier_screen_image.paste(self.image, self._image_pos.tup())
        for bar in self.bars.values():
            bar.draw(tier_screen_image)
        tier_screen_image.save(filename, 'jpeg')


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--image', '-i', action='store', type=str,
                        help='the name of file containing the image to use. should be 460x396')
    parser.add_argument('--output', '-o', action='store', type=str, help='the name of output file')
    parser.add_argument('--int', '-I', action='store', type=int, help='the int to be dispalyed on the tier screen image')
    parser.add_argument('--pwr', '-P', action='store', type=int, help='the pwr to be dispalyed on the tier screen image')
    parser.add_argument('--def', '-D', action='store', type=int, help='the def to be dispalyed on the tier screen image',
                        dest='def_')
    parser.add_argument('--mbl', '-M', action='store', type=int, help='the mbl to be dispalyed on the tier screen image')
    parser.add_argument('--hp',  '-H', action='store', type=int, help='the hp to be dispalyed on the tier screen image')
    parser.add_argument('--stl', '-S', action='store', type=int, help='the stl to be dispalyed on the tier screen image')
    return parser.parse_args()


def main():
    args = parse_args()
    image = Image.open(args.image)
    tier_screen = TierScreen(template_file, image,
                             args.int, args.pwr, args.def_, args.mbl, args.hp, args.stl)
    tier_screen.save(args.output)


if __name__ == '__main__':
    main()
