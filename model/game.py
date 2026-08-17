import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
os.environ["SDL_VIDEODRIVER"] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dsp'
import pygame
import numpy as np
from itertools import product

from utils import Color


save_dir = 'screenshots'

_image_library = {}
def get_image(filename):
    global _image_library
    path = 'graphics/{}.png'.format(filename)
    image = _image_library.get(path)
    if image == None:
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        image = pygame.image.load(canonicalized_path)
        _image_library[path] = image
    return image


class Game:
    def __init__(self, world):
        self.world = world
        
        self.small_fsize = 18
        self.large_fsize = 28
        self.text_vspacing = 10

        self.scale = 80   # number of pixels per tile
        self.tile_size = (self.scale, self.scale)
        self.agent_r = 25
        self.eye_size = (16, 22)
        self.eye_offsets = [(-16, -18), (1, -18)]
        self.star_width = 60
        self.star_offset = ((self.scale - self.star_width)//2,
                            (self.scale - self.star_width)//2)
        self.sidebar_width = self.scale * 2
        self.wall_width = 7  # odd so it can be centered
        self.handle_width = 10
        self.box_width = self.scale*3//4
        self.width = self.scale * self.world.width + self.wall_width
        self.screen_width = self.width + self.sidebar_width
        self.height = self.scale * self.world.height + self.wall_width


    def on_init(self, no_sidebar = False):
        pygame.init()
        self.no_sidebar = no_sidebar
        if self.no_sidebar:
            self.screen = pygame.display.set_mode((self.width, self.height))
        else:
            self.screen = pygame.display.set_mode((self.screen_width, self.height))
            self.small_font = pygame.font.SysFont('Arial', self.small_fsize)
            self.large_font = pygame.font.SysFont('Arial', self.large_fsize)


    def on_render(self, state, attributes, blank = False, is_success = None):
        self.draw_world(state)
        self.draw_agents(state, attributes)
        if not self.no_sidebar:
            self.draw_timer(state.time_limit)
            if not blank:
                self.draw_turn(state.turn, attributes)
            self.draw_outcome(is_success)
        pygame.display.flip()
        pygame.display.update()


    def draw_world(self, state):
        self.screen.fill(Color.WHITE)

        # draw base grid
        for x, y in product(range(self.world.width),
                            range(self.world.height)):
            tl = self.top_left((x, y))
            fill = pygame.Rect(tl[0], tl[1], self.scale, self.scale)
            self.screen.fill(Color.FLOOR, fill)
            pygame.draw.rect(self.screen, Color.LINE, fill, 1)

        # draw walls            
        for x, y in product(range(self.world.width),
                            range(self.world.height)):
            # check vertical walls
            if x < self.world.width - 1:
                if ((x, y), (x+1, y)) not in self.world.graph.edges:
                    tl = self.top_left((x+1, y))
                    self.draw_wall(tl, (0, self.scale))
            # check horizontal walls
            if y < self.world.height - 1:
                if ((x, y), (x, y+1)) not in self.world.graph.edges:
                    tl = self.top_left((x, y+1))
                    self.draw_wall(tl, (self.scale, 0))

        # draw goal
        goal = self.top_left(self.world.goal)
        star = pygame.transform.scale(get_image('goal'),
                (self.star_width, self.star_width))
        self.screen.blit(star, np.add(goal, self.star_offset))

        # draw boxes from state
        for box in state.boxes:
            tl = self.top_left(box)
            box_tl = self.offset_top_left(tl, self.box_width)
            fill_box = pygame.Rect(box_tl[0], box_tl[1],
                                   self.box_width, self.box_width)
            self.screen.fill(Color.BOX, fill_box)

        self.draw_perimeter()
    

    def draw_wall(self, start, diff):
        pygame.draw.line(self.screen, Color.WALL, start_pos = start,
            end_pos = np.add(start, diff), width = self.wall_width)


    def draw_perimeter(self):
        self.draw_wall(self.top_left((0, 0)),
                       (self.scale * self.world.width, 0))
        self.draw_wall(self.top_left((self.world.width, 0)),
                       (0, self.scale * self.world.height))
        self.draw_wall(self.top_left((0, self.world.height)),
                       (self.scale * self.world.width, 0))


    def draw_agents(self, state, attributes):
        red_color, blue_color, red_name, blue_name = attributes.values()
        # draw blue's box
        if state.blue_box is not None:
            pygame.draw.line(self.screen, blue_color,
                start_pos = self.center(state.blue_location),
                end_pos = self.center(state.blue_box),
                width = self.handle_width)
            w = self.box_width + self.handle_width
            border_tl = self.offset_top_left(self.top_left(state.blue_box), w)
            border = pygame.Rect(border_tl[0], border_tl[1], w, w)
            pygame.draw.rect(self.screen, blue_color, border,
                             width = self.handle_width,
                             border_radius = self.handle_width//3)
            # redraw box on top
            tl = self.top_left(state.blue_box)
            box_tl = self.offset_top_left(tl, self.box_width)
            fill_box = pygame.Rect(box_tl[0], box_tl[1],
                                   self.box_width, self.box_width)
            self.screen.fill(Color.BOX, fill_box)
        if (state.red_location == state.blue_location):
            self.draw_agent_overlap(0, red_color, state.red_location)
            self.draw_agent_overlap(1, blue_color, state.blue_location)
        else:
            self.draw_agent(red_color, state.red_location)
            self.draw_agent(blue_color, state.blue_location)


    def draw_agent(self, color, location):
        center = self.center(location)
        pygame.draw.circle(self.screen, color, center, self.agent_r)
        pygame.draw.circle(self.screen, Color.WHITE, center, self.agent_r, 2)
        eye = pygame.transform.scale(get_image('eye'), self.eye_size)
        self.screen.blit(eye, np.add(center, self.eye_offsets[0]))   # left eye
        self.screen.blit(eye, np.add(center, self.eye_offsets[1]))   # right eye


    def draw_agent_overlap(self, pos, color, location):
        center = self.offset_left(location) if pos == 0 else self.offset_right(location)
        pygame.draw.circle(self.screen, color, center, self.agent_r)
        pygame.draw.circle(self.screen, Color.WHITE, center, self.agent_r, 2)
        eye = pygame.transform.scale(get_image('eye'), self.eye_size)
        self.screen.blit(eye, np.add(center, self.eye_offsets[0]))   # left eye
        self.screen.blit(eye, np.add(center, self.eye_offsets[1]))   # right eye


    def draw_timer(self, time):
        text_surface = self.small_font.render('time left:', True, Color.BLACK)
        text_w, text_h = text_surface.get_size()
        text_w_margin = (self.sidebar_width - text_w)//2
        self.screen.blit(text_surface, (self.width + text_w_margin,
                                        self.text_vspacing * 4))
        
        surface = self.large_font.render(str(time), True, Color.BLACK)
        w, h = surface.get_size()
        w_margin = (self.sidebar_width - w)//2
        self.screen.blit(surface, (self.width + w_margin,
                                   self.text_vspacing * 5 + text_h))


    def draw_turn(self, whose_turn, attributes):
        if whose_turn == '': return
        red_color, blue_color, red_name, blue_name = attributes.values()
        if whose_turn == 'red':
            text_surface = self.small_font.render(f"{red_name}'s turn", True, red_color)
        elif whose_turn == 'blue':
            text_surface = self.small_font.render(f"{blue_name}'s turn", True, blue_color)
        text_w, text_h = text_surface.get_size()
        text_w_margin = (self.sidebar_width - text_w)//2
        h = self.height//2
        if self.world.height > 4:
            h -= self.text_vspacing * 4
        self.screen.blit(text_surface, (self.width + text_w_margin, h))
        
    
    def draw_outcome(self, is_success):
        text_surface = self.small_font.render('result:', True, Color.BLACK)
        text_w, text_h = text_surface.get_size()
        text_w_margin = (self.sidebar_width - text_w)//2
        self.screen.blit(text_surface, (self.width + text_w_margin,
                                        self.height*2//3))
        if is_success is not None:
            outcome = 'SUCCESS' if is_success else 'FAIL'
            surface = self.large_font.render(outcome, True, Color.BLACK)
            w, h = surface.get_size()
            w_margin = (self.sidebar_width - w)//2
            self.screen.blit(surface, (self.width + w_margin,
                                       self.height*2//3 + self.text_vspacing + text_h))
        

    def save_image(self, file_name):
        pygame.image.save(self.screen, file_name + '.png')


    def screenshot(self, state, attributes, file_name, is_success = None):
        self.on_render(state, attributes, is_success = is_success)
        self.save_image(file_name)
        self.on_render(state, attributes, blank = True, is_success = is_success)
        self.save_image(file_name + '_blank')


    def top_left(self, loc):
        tl = (self.scale * loc[0] + self.wall_width//2,
              self.scale * loc[1] + self.wall_width//2)
        return tl

    
    def center(self, loc):
        c = (self.scale * loc[0] + self.wall_width//2 + self.scale//2,
             self.scale * loc[1] + self.wall_width//2 + self.scale//2)
        return c


    def offset_left(self, loc):
        hl = (self.scale * loc[0] + self.wall_width//2 + (2 * self.scale//5),
                      self.scale * loc[1] + self.wall_width//2 + (2 * self.scale//5))
        return hl


    def offset_right(self, loc):
        hr = (self.scale * loc[0] + self.wall_width//2 + (3 * self.scale//5),
              self.scale * loc[1] + self.wall_width//2 + (3 * self.scale//5))
        return hr


    def offset_top_left(self, tl, width):
        return (tl[0] + (self.scale - width)//2,
                tl[1] + (self.scale - width)//2)


    def on_cleanup(self):
        pygame.display.quit()
        pygame.quit()
