import os
import functools
from math import pi
from typing import Tuple, List
if __name__ == '__main__':
    import argparse

from PIL import Image, ImageDraw


icons = {
    'int': Image.open('images/icons/int.jpg'),
    'pwr': Image.open('images/icons/pwr.jpg'),
    'def': Image.open('images/icons/def.jpg'),
    'mbl': Image.open('images/icons/mbl.jpg'),
    'hp':  Image.open('images/icons/hp.jpg'),
    'stl': Image.open('images/icons/stl.jpg'),
}


def memoize(obj, depends: List[str]=None, *depends_iter: str):
    if depends_iter:
        depends = [depends, *depends_iter]

    def wrapper(func):

        @functools.wraps(func)
        def wrapped(obj, *args, **kwargs):
            depends_values = tuple(getattr(obj, i) for i in depends)
            try:
                return obj.__memoized[depends_values]
            except KeyError:
                pass
            except AttributeError:
                obj.__memoize = {}
            result = func(obj, *args, **kwargs)
            obj.__memoize[depends_values] = result
            return result

        return wrapped()

    return wrapper


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

    def __init__(self, x: int, y: int=None):
        if not isinstance(x, int):
            x, y = iter(x)
        self.x = x
        self.y = y

    def __repr__(self):
        return f'Pos(x={self.x}, y={self.y})'

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        return Pos(self.x + other[0], self.y + other[1])

    def __radd__(self, other):
        return Pos(other[0] + self.x, other[1] + self.y)

    def __iadd__(self, other):
        self.x += other[0]
        self.y += other[1]
        return self

    def __sub__(self, other):
        return Pos(self.x - other[0], self.y - other[1])

    def __rsub__(self, other):
        return Pos(other[0] - self.x, other[1] - self.y)

    def __isub__(self, other):
        self.x -= other[0]
        self.y -= other[1]
        return self

    def __iter__(self):
        return (self.x, self.y)

    def __getitem__(self, index):
        if index == 0:
            return self.x
        if index == 1:
            return self.y
        raise IndexError()


class Box:
    def __init__(self, p1: Pos=None, p2: Pos=None, anchor: str='NW'):
        self._p1 = Pos(min(p1.x, p2.x), min(p1.y, p2.y))
        self._p2 = Pos(max(p1.x, p2.x), max(p1.y, p2.y))
        self.set_from_anchor(anchor)

    def __repr__(self):
        return f'Box(top_left={self.top_left}, bottom_right={self.bottom_right})'

    def __eq__(self, other):
        return self._p1 == other.p1 and self._p2 == other._p2

    @property
    def top_left(self) -> Pos:
        return self._p1

    @top_left.setter
    def top_left(self, value: Pos):
        self._p1 = value

    @property
    def top_right(self) -> Pos:
        return Pos(self._p2.x, self._p1.y)

    @top_right.setter
    def top_right(self, value: Pos):
        self._p1.y = value.y
        self._p2.x = value.x

    @property
    def bottom_left(self) -> Pos:
        return Pos(self._p1.x, self._p2.y)

    @bottom_left.setter
    def bottom_left(self, value: Pos):
        self._p1.x = value.x
        self._p2.y = value.y

    @property
    def bottom_right(self) -> Pos:
        return self._p2

    @bottom_right.setter
    def bottom_right(self, value: Pos):
        self._p2 = value

    @property
    def top(self) -> int:
        return self._p1.y

    @top.setter
    def top(self, value: int):
        self._p1.y = value

    @property
    def bottom(self) -> int:
        return self._p2.y

    @bottom.setter
    def bottom(self, value: int):
        self._p2.y = value

    @property
    def left(self) -> int:
        return self._p1.x

    @left.setter
    def left(self, value: int):
        self._p1.x = value

    @property
    def right(self) -> int:
        return self._p2.x

    @right.setter
    def right(self, value: int):
        self._p2.x = value

    @property
    def width(self) -> int:
        return (self._p1.x + self._p2.x) // 2

    @width.setter
    def width(self, value: int):
        vertical_center = (self._p1.x + self._p2.x) // 2
        self._p1.x = vertical_center - value // 2
        self._p2.x = vertical_center + value // 2

    @property
    def height(self) -> int:
        return (self._p1.y + self._p2.y) // 2

    @height.setter
    def height(self, value: int):
        horizontal_center = (self._p1.y + self._p2.y) // 2
        self._p1.y = horizontal_center - value // 2
        self._p2.y = horizontal_center + value // 2

    @property
    def size(self) -> Tuple[int]:
        return self.width, self.height

    @property
    def top_middle(self) -> Pos:
        return Pos(self._p1.x + self.width // 2, self._p1.y)

    @top_middle.setter
    def top_middle(self, value: Pos):
        width, height = self.size
        self._p1 = Pos(value.x - width // 2, value.y)
        self._p2 = Pos(value.x + width // 2, value.y + height)

    @property
    def right_middle(self) -> Pos:
        return Pos(self._p2.x, self._p2.y - self.height // 2)

    @right_middle.setter
    def right_middle(self, value: Pos):
        width, height = self.size
        self._p1 = Pos(value.x - width, value.y - height // 2)
        self._p2 = Pos(value.x, value.y + height // 2)

    @property
    def bottom_middle(self) -> Pos:
        return Pos(self._p2.x - self.width // 2, self._p2.y)

    @bottom_middle.setter
    def bottom_middle(self, value: Pos):
        width, height = self.size
        self._p1 = Pos(value.x - width // 2, value.y - height)
        self._p2 = Pos(value.x + width // 2, value.y)

    @property
    def left_middle(self) -> Pos:
        return Pos(self._p1.x, self._p1.y + self.height // 2)

    @left_middle.setter
    def left_middle(self, value: Pos):
        width, height = self.size
        self._p1 = Pos(value.x, value.y - height // 2)
        self._p2 = Pos(value.x + width, value.y + height // 2)

    @property
    def center(self) -> Pos:
        return Pos((self._p1.x + self._p2.x) // 2, (self._p1.y + self._p2.y) // 2)

    @center.setter
    def center(self, value: Pos):
        width = self.width
        height = self.height
        self._p1 = Pos(self._p1 + width // 2, self._p1 + height // 2)
        self._p2 = Pos(self._p2 - width // 2, self._p2 - height // 2)

    def anchor(self, anchor: str) -> Pos:
        anchor = anchor.upper()
        valid_anchors = {
            'N': lambda: self.top_middle,
            'E': lambda: self.right_middle,
            'S': lambda: self.bottom_middle,
            'W': lambda: self.left_middle,
            'NE': lambda: self.top_right,
            'NW': lambda: self.top_left,
            'SE': lambda: self.bottom_right,
            'SW': lambda: self.bottom_left,
            'NESW': lambda: self.center,
        }
        try:
            return valid_anchors[anchor]()
        except KeyError:
            raise AttributeError(f'anchor {anchor!r} not valid')

    def set_from_anchor(self, pos: Pos, anchor: str):
        anchor = anchor.upper()
        valid_anchors = {
            'N': lambda: setattr(self, 'top_middle', pos),
            'E': lambda: setattr(self, 'right_middle', pos),
            'S': lambda: setattr(self, 'bottom_middle', pos),
            'W': lambda: setattr(self, 'left_middle', pos),
            'NE': lambda: setattr(self, 'top_right', pos),
            'NW': lambda: setattr(self, 'top_left', pos),
            'SE': lambda: setattr(self, 'bottom_right', pos),
            'SW': lambda: setattr(self, 'bottom_left', pos),
            'NESW': lambda: setattr(self, 'center', pos),
        }
        try:
            valid_anchors[anchor]()
        except KeyError:
            raise AttributeError(f'anchor {anchor!r} not valid')


class Rectangle(Box):
    def __init__(self, p1: Pos=None, p2: Pos=None, color: Tuple[int]=None):
        super().__init__(p1, p2)
        self.color = color

    def draw(self, image: Image):
        if self._p1.x - self._p2.x == 0 or self._p1.y - self._p2.y == 0:
            return
        draw = ImageDraw.Draw(image)
        draw.rectangle(tuple(self._p1), tuple(self._p2), fill=self.color)


class Text:
    def __init__(self, text, font=None, color=None):
        self.text = text
        self.font = font  # TODO: this needs to be a font object instead of None
        self.color = color

    def __repr__(self):
        return f'Text(, text={self.text!r}, font={self.font!r}, color={self.color!r})'

    def __str__(self):
        return self.text

    @property
    @memoize('text', 'font')
    def size(self) -> Tuple[int]:
        return self.font.getsize(self.text)

    @property
    def width(self) -> int:
        return self.size[0]

    @property
    def height(self) -> int:
        return self.size[1]

    def draw(self, image: Image, pos: Pos, anchor: str='NW', rotation: float=0):
        # TODO: add anchor (N, E, S, W, NE, NW, SE, SW) to draw from
        # this needs to be drawn on an image, then the image rotated in order for the text to be rotatable
        pos = Box(pos, pos + self.size, anchor).top_left
        draw = ImageDraw.Draw(image)
        draw.text(pos, self.text, self.color, self.font)


class PlotLabel:
    def __init__(self, text: Text, icon: Image, space: int):
        self.text = text
        self.icon = icon
        self.space = space

    @property
    def width(self) -> int:
        return max(self.text.width, self.icon.width)

    @property
    def height(self) -> int:
        return self.text.height + self.icon.height + self.space

    def draw(self, image: Image, pos: Pos):
        pos = Pos(pos)
        self.text.draw(image, Pos(pos.x - self.text.width // 2, pos.y - self.text.height))
        image.paste(self.icon, (pos.x - self.icon.width // 2, pos.y - self.icon.height - self.space))


class Plotable:
    def __init__(self, label: PlotLabel, value: int, width: int, space: int, color: Tuple[int], upper_bound: int=None,
                 lower_bound: int=None):
        self.label = label
        self.value = value
        self.width = width
        self.space = space
        self.color = color
        self.upper_bound = upper_bound
        self.lower_bound = lower_bound

    def draw(self, image: Image, pos: Pos):
        self.label.draw(image, pos)
        bar_bottom_middle = Pos(self.pos.x, self.pos.y - self.label.height() - self.space)
        bar = Rectangle(bar_bottom_middle, bar_bottom_middle, self.color)
        bar.width = self.width
        bar.top = self.lower_bound + self.value * abs(self.upper_bound - self.lower_bound)
        bar.draw(image)


class Graph:
    def __init__(self, items: List[Plotable], lower_bound: int, upper_bound: int, graduation_labels: List[Text],
                 space: int, sep_width: int, sep_color: Tuple[int], x_overhang: int=0, y_overhang: int=0,
                 x_label: Text=None, y_label: Text=None, label_offset: int=None, x_label_offset: int=None,
                 y_label_offset: int=None, bar_vertical_offset: int=1, bar_height=None,
                 graduation_label_offset: int=10):
        # x and y label offset: px from sep or inline with furthest left/lowest graduation label if None
        self.items = items
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.graduation_levels = self.graduation_levels
        self.sep_width = sep_width
        self.sep_color = sep_color
        self.x_overhang = x_overhang
        self.y_overhang = y_overhang
        self.x_label = x_label
        self.y_label = y_label
        self.x_label_offset = label_offset if x_label_offset is None else x_label_offset
        self.y_label_offset = label_offset if y_label_offset is None else y_label_offset
        self.bar_vertical_offset = bar_vertical_offset
        self.bar_height = bar_height
        for item in self.items:
            item.upper_bound = self.upper_bound
            item.lower_bound = self.lower_bound
            item.space += self.sep_width

    def _x_sep_length(self) -> int:
        return (self.plotables[0].width + self.space) * 2 + self.x_overhang

    def _bars_start(self) -> int:
        return

    def _draw_seperators(self, image: Image, pos: Pos):
        Rectangle(pos, Pos(pos.x + self.sep_width - 1, 
                           pos.y - self.bar_height - self.y_overhang - self.bar_vertical_offset),
                  self.sep_color).draw(image)
        Rectangle(pos, Pos(pos.x + self._x_sep_length(),
                           pos.y - self.sep_width - 1),
                  self.color).draw(image)

    def _draw_labels(self, image: Image, pos: Pos):
        if self.x_label is not None:
            self.x_label.draw(image, Pos(pos.x + self._x_sep_length() // 2,
                                         max(plotable.label.height for plotable in self.plotables)
                                         + self.x_label_offset),
                              'N')
        if self.y_label is not None:
            self.y_label.draw(image,
                              Pos(pos.x - max(i.text.width for i in self.graduation_levels) - self.y_label_offset,
                                  pos.y - self.bar_height // 2),
                              'S', 0.5 * pi)

    def _draw_graduations(self, image: Image, pos: Pos):
        offset = Pos(pos.x - self.graduation_offset, self._bars_start())
        for n, text in enumerate(self.graduation_labels):
            text.draw(image, Pos(offset.x, offset.y - (n / len(self.graduation_levels) * self.bar_height) * n), 'E')

    def draw(self, image: Image, pos: Pos):
        """Draw this graph.

        Args:
            image: the image to draw on.
            pos: The bottom-left-most pixel of the seperator of this
                graph.
        """
        self._draw_seperators(image, pos)
        self._draw_labels(image, pos)
        self._draw_graduations(image, pos)
        plotable_offset = Pos(pos.x + self.sep_width - 1 + self.space // 2 + self.plotables[0].width // 2,
                              pos.y + self.sep_width - 1 + self.bar_vertical_offset)
        for n, plotable in enumerate(self.plotables):
            plotable.draw(image, Pos(plotable_offset.x + (n * (plotable.width + self.space)), plotable_offset.y))


class StatScreen:
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
        """Save the stat screen to file `filename`."""
        stat_screen_image = Image.open(self.template_file)
        stat_screen_image.paste(self.image, tuple(self._image_pos))
        for bar in self.bars.values():
            bar.draw(stat_screen_image)
        stat_screen_image.save(filename, 'jpeg')


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--image', '-i', action='store', type=str, required=True,
                        help='the name of file containing the image to use. should be 460x396')
    parser.add_argument('--output', '-o', action='store', type=str, required=True, help='the name of output file')
    parser.add_argument('--int', '-I', action='store', type=int, required=True,
                        help='the int to be displayed on the stat screen image')
    parser.add_argument('--pwr', '-P', action='store', type=int, required=True,
                        help='the pwr to be displayed on the stat screen image')
    parser.add_argument('--def', '-D', action='store', type=int, required=True,
                        help='the def to be displayed on the stat screen image', dest='def_')
    parser.add_argument('--mbl', '-M', action='store', type=int, required=True,
                        help='the mbl to be displayed on the stat screen image')
    parser.add_argument('--hp',  '-H', action='store', type=int, required=True,
                        help='the hp to be displayed on the stat screen image')
    parser.add_argument('--stl', '-S', action='store', type=int, required=True,
                        help='the stl to be displayed on the stat screen image')
    return parser.parse_args()


def main():
    args = parse_args()
    image = Image.open(args.image)
    stat_screen = StatScreen(template_file, image,
                             args.int, args.pwr, args.def_, args.mbl, args.hp, args.stl)
    stat_screen.save(args.output)


if __name__ == '__main__':
    main()
