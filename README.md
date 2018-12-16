# AutoZoo
AutoZoo is a tool to create TierZoo-like statscreens.

![Harambe :(](https://i.imgur.com/OmoCdmx.jpg)

## How to use
You must have [Python 3](https://www.python.org) installed, as well as pip (pip is installed from the python installer).

1. Download the repository with either `git clone https://github.com/HLiam/autozoo/master` or the Download button in the top left. Then `cd` into it from the command-line
2. Run `pip install -r requirements.txt` to install the requirements
3. Use `py stat_screen.py [-h] -i IMAGE -o OUTPUT -I INT -P PWR -D DEF -M MBL -H HP -S STL` (equivalent to `py stat_screen.py [-h] --image IMAGE --output OUTPUT --int INT --pwr PWR --def DEF --mbl MBL --hp HP --stl STL`) to create the stat screen.

## Example
`py stat_screen.py -i input.jpg -o output.jpg -I 100 -P 50 -D 20 -M 10 -H 5 -S 2` would create a stat screen in file `output.jpg` using image `input.png` with stats:

int: 100

pwr: 50

def: 20

mbl: 10

hp:  5

stl: 2
