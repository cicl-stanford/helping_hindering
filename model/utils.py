import csv
import numpy as np
import imageio.v3 as iio
from pygifsicle import optimize
from scipy.special import softmax
from pathlib import Path
from collections import defaultdict


DOWN, UP, LEFT, RIGHT, STAY = (0, 1), (0, -1), (-1, 0), (1, 0), (0, 0)
ACTIONS = [DOWN, UP, LEFT, RIGHT, STAY]
MOVE_ACTIONS = [DOWN, UP, LEFT, RIGHT]

HOLD_DOWN, HOLD_UP, HOLD_LEFT, HOLD_RIGHT = (0, 2), (0, -2), (-2, 0), (2, 0)
HOLD_ACTIONS = [HOLD_DOWN, HOLD_UP, HOLD_LEFT, HOLD_RIGHT]

RELEASE_DOWN, RELEASE_UP, RELEASE_LEFT, RELEASE_RIGHT = (0, 3), (0, -3), (-3, 0), (3, 0)
RELEASE_ACTIONS = [RELEASE_DOWN, RELEASE_UP, RELEASE_LEFT, RELEASE_RIGHT]

def unit_action(action):
    return ((action[0] > 0) - (action[0] < 0),
            (action[1] > 0) - (action[1] < 0))

HOLD_COST = 2
RELEASE_COST = 0
ACTION_COST = 1

# REWARD PARAMETERS
R_GOAL = 20         # Reward for reaching goal
PROX_DECAY = 0.8    # Decay factor for distance to goal
GAMMA = 0.9         # Discount factor for future rewards
BETA = 0.5            # Weight of dense proximity bonus


def bernoulli(p):
    if np.random.rand() < p:
        return True
    return False


def geom_sum(a, n):
    """
    Return sum_{k=0}^{n-1} a^k. Handles a=1.
    """
    if n <= 0:
        return 0.0
    if abs(a - 1.0) < 1e-12:
        return float(n)
    return (1.0 - a**n) / (1.0 - a)


def prox_series(a, b, n, d):
    """
    Returns sum_{k=0}^{n-1} a^k * b^(d - (k+1))
    = b^(d-1) * sum_{k=0}^{n-1} (a/b)^k
    """
    base = b ** (d-1)
    r = a / b
    if abs(r - 1) < 1e-12:
        return base * float(n)
    return base * geom_sum(r, n)


def set_params(exp):
    global HOLD_COST
    global BETA
    if exp == 2 or exp == 3:
        HOLD_COST = 1.5
        BETA = 1
    # set any other experiment-specific parameters here


def action_cost(action):
    if action in HOLD_ACTIONS:
        return HOLD_COST
    elif action in RELEASE_ACTIONS:
        return RELEASE_COST
    return ACTION_COST


def proximity_reward(d, d_prox):
    # d: distance to goal counting boxes
    # d_prox: distance to goal ignoring boxes
    return BETA * prox_series(GAMMA, PROX_DECAY, d, d_prox)


# put a list of dict values through a softmax using the given beta
def get_softmax(items, beta = 1):
    try:
        if isinstance(items, list):
            return softmax([beta * i for i in items])
        if isinstance(items, dict):
            new_values = softmax([beta * v for v in items.values()])
            return dict(zip(items.keys(), new_values))
    except:
        import pdb; pdb.set_trace()


# create gif from all images in a directory
def make_gif(image_dir, file_path = None):
    p = Path(image_dir)
    if file_path:
        out = Path(file_path).with_suffix('.gif')
    else:
        out = Path(image_dir + '/full.gif')
    images = []
    for f in sorted(p.iterdir()):
        if 'blank' in f.name.lower():
           images.append(iio.imread(f))
    # hold first and last frame a little longer
    images = [images[0]]*3 + images
    images += [images[-1]]*3
    frames = np.stack(images, axis=0)
    iio.imwrite(out, images, duration=1000/1.75, loop=0)
    optimize(out)


# read in list of names to use in experiment
def read_names(experiment_name):
    names = defaultdict(list)
    with open('../../experiments/files-{}/names.csv'.format(experiment_name),
              'r', encoding = 'utf-8-sig') as f:
        for row in csv.DictReader(f):
            names[int(row['trial'])] = dict(row)
    return names


# clear directory or create if doesn't exist
def make_dir(path):
    p = Path(path)
    if p.exists():
        for child in p.iterdir():
            child.unlink()
    else:
        p.mkdir(parents=True, exist_ok=True)


# =============================================================================


class Color:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    FLOOR = (255, 255, 255)  # white
    LINE = (200, 200, 200)   # light grey
    WALL = (0, 0, 0)         # black
    BOX = (0, 0, 0)
    RED = (255, 60, 60)
    LIGHT_RED = (255, 150, 150)
    BLUE = (0, 170, 255)
    LIGHT_BLUE = (120, 220, 255)
    LIME = (0, 200, 0)
    GREEN = (0, 128, 0)
    TEAL = (0, 128, 128)
    YELLOW = (255, 200, 0)
    MAGENTA = (255, 0, 255)
    PURPLE = (128, 0, 128)
    MAROON = (128, 0, 0)
    NAVY = (0, 0, 128)
    CORAL = (255, 127, 80)
    ORANGE = (255, 140, 0)
    DARK_GREEN = (0, 100, 0)
    AQUA = (150, 200, 230)
    MEDIUM_PURPLE = (147, 112, 219)
    PINK = (255, 105, 180)
    DARK_PINK = (199, 21, 133)
    SALMON = (250, 128, 114)
    CRIMSON = (220, 20, 60)
    GOLD = (218, 165, 32)
    LIGHT_PURPLE = (230, 191, 250)
    BROWN = (188, 143, 143)
    LIGHT_ORANGE = (230, 140, 0)
    MEDIUM_PINK = (229, 121, 206)
    DULL_PURPLE = (104, 79, 132)
    ALIEN_GREEN = (9, 240, 24)


color_to_str = {Color.BLACK: 'black',
                Color.WHITE: 'white',
                Color.RED: 'red',
                Color.BLUE: 'blue',
                Color.LIGHT_BLUE: 'light blue',
                Color.LIME: 'lime',
                Color.GREEN: 'green',
                Color.TEAL: 'teal',
                Color.YELLOW: 'yellow',
                Color.MAGENTA: 'magenta',
                Color.PURPLE: 'purple',
                Color.MAROON: 'maroon',
                Color.NAVY: 'navy',
                Color.CORAL: 'coral',
                Color.ORANGE: 'orange',
                Color.DARK_GREEN: 'dark green',
                Color.AQUA: 'aqua',
                Color.MEDIUM_PURPLE: 'purple',
                Color.PINK: 'pink',
                Color.DARK_PINK: 'dark pink',
                Color.SALMON: 'salmon',
                Color.CRIMSON: 'crimson',
                Color.GOLD: 'gold',
                Color.LIGHT_PURPLE: 'light purple',
                Color.BROWN: 'brown',
                Color.LIGHT_ORANGE: 'light orange'
                }
str_to_color = {v: k for k, v in color_to_str.items()}
