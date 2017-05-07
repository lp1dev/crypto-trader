colors = {'dark_gray': 30, 'radish_red': 31, 'grass_green': 32, 'yolk_yellow': 33, 'blood_blue': 34, 'magenta': 35,
          'cyan': 36, 'white': 37, 'crimson': 38, 'highlighted_red': 41, 'highlighted_green': 42,
          'highlighted_brown': 43, 'highlighted_blue': 44, 'highlighted_magenta': 45, 'highlighted_cyan': 46,
          'highlighted_gray': 47, 'highlighted_crimson': 48}


def colorize(string, color):
    return "\033[1;%sm%s\033[1;m" % (colors[color], string)
