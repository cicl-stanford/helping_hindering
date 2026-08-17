from game import *
from agent import *

import os
from pathlib import Path
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
os.environ['SDL_AUDIODRIVER'] = 'dsp'
import time
from copy import deepcopy
import re



class Environment:
    def __init__(self, world, red_agent, blue_agent, trial_dir = '.'):
        """ Initiates environment """

        self.world = world
        self.red = red_agent
        self.blue = blue_agent
        self.state = None
        self.trial_dir = trial_dir
        self.game = None
        self.agent_attributes = {
                'red_color': self.red.color,
                'blue_color': self.blue.color,
                'red_name': self.red.name,
                'blue_name': self.blue.name}

        # key = (timestep, agent), value = action taken on that timestep
        self.action_record = {}

        # key = (timestep, agent), value = initial state on that timestep
        self.state_record = {}


    
    def run(self, initial_state, red_path = [], blue_path = [],
            prob_follow = 1, softmax_beta = None, epsilon = 0,
            visualize = False):
        """ Simulates red and blue agents interacting with environment """

        self.state = initial_state

        # initialize game visualization
        if visualize:
            self.game = Game(self.world)
            self.game.on_init()
            self.game.screenshot(
                    self.state, self.agent_attributes,
                    file_name = '{}/00'.format(self.trial_dir))
        f = open(f"{self.trial_dir}/record.txt", "w")
        self.print_status(self.state, f)
        is_success = False
        red_deviated = (len(red_path) == 0)

        for t in range(1, self.state.time_limit + 1):
            f.write(f'\n\n-----TIMESTEP {t}-----')

            # RED'S TURN ------------------------------------------------------
            start_time = time.time()
            f.write('\nRed\'s turn')
            self.state_record[t, 0] = self.state
            if self.red.blue_intentions[t-1]:
                f.write(f'\nRed\'s belief about Blue: {self.red.blue_intentions[t-1]} help')
            if not red_deviated:
                if bernoulli(prob_follow) and len(red_path) > 0:
                    f.write(f'\nFollowing path {red_path}')
                    red_action = tuple(red_path.pop(0))
                    if red_action not in self.world.valid_actions(self.state):
                        red_path.insert(0, red_action)
                        red_action = STAY
                        f.write(f'\nAction not valid, staying instead')
                else:
                    red_deviated = True
                    f.write('\nFinished / deviated from path')
                    red_action = self.red.best_action(
                            self.state,
                            belief_help = self.red.blue_intentions[t-1],
                            softmax_beta = softmax_beta,
                            epsilon = epsilon,
                            f = f)
            else:
                red_action = self.red.best_action(
                        self.state,
                        belief_help = self.red.blue_intentions[t-1],
                        softmax_beta = softmax_beta,
                        epsilon = epsilon,
                        f = f)
            new_state = self.world.execute(self.state, red_action)
            self.state = new_state
            self.action_record[t, 0] = red_action
            f.write(f'\nTook action: {red_action}')
            if visualize:
                self.game.screenshot(
                        self.state, self.agent_attributes,
                        file_name = f'{self.trial_dir}/{2*t-1:02d}')
            if self.world.is_terminal(self.state):
                f.write('\n\nRed reached goal!')
                is_success = True
                break
            end_time = time.time()
            f.write(f'\nTime: {end_time - start_time:.4f} seconds')
            self.print_status(self.state, f)

            # BLUE'S TURN -----------------------------------------------------
            start_time = time.time()
            f.write('\n\nBlue\'s turn')
            self.state_record[t, 1] = self.state
            path_so_far = [a for (tt, i), a in sorted(self.action_record.items()) if i == 1]
            if len(blue_path) > 0:
                blue_action = tuple(blue_path.pop(0))
                if blue_action not in self.world.valid_actions(self.state):
                    blue_path.insert(0, blue_action)
                    blue_action = STAY
                    f.write(f'\nAction not valid, staying instead')
            elif any([a in RELEASE_ACTIONS for a in path_so_far]):
                blue_action = STAY
            else:
                blue_action = self.blue.best_action(
                        self.state,
                        belief_help = 0.5,
                        softmax_beta = softmax_beta,
                        epsilon = epsilon,
                        f = f)
            new_state = self.world.execute(self.state, blue_action)
            self.state = new_state
            self.action_record[t, 1] = blue_action
            f.write(f'\nTook action: {blue_action}')
            if visualize:
                self.game.screenshot(
                        self.state, self.agent_attributes,
                        file_name = f'{self.trial_dir}/{2*t:02d}')
            end_time = time.time()
            f.write(f'\nTime: {end_time - start_time:.4f} seconds')
            self.print_status(self.state, f)

            # update sophisticated red's beliefs
            new_belief = self.red.update_belief(
                prior_help = self.red.blue_intentions[t-1],
                state = self.state_record[t, 1],
                blue_action = blue_action)
            self.red.blue_intentions[t] = new_belief
        
        # termination 
        final_red_path = [a for (t, i), a in sorted(self.action_record.items()) if i == 0]
        final_blue_path = [a for (t, i), a in sorted(self.action_record.items()) if i == 1]
        f.write('\n\n---------------------')
        f.write(f'\n{final_red_path}')
        f.write(f'\n{final_blue_path}')
        f.close()
        
        if visualize:
            final_t = 2*t if is_success else (2*t+1)
            self.game.screenshot(
                    self.state, self.agent_attributes,
                    is_success = is_success,
                    file_name = f'{self.trial_dir}/{final_t}')
            make_gif(self.trial_dir, self.trial_dir + '/full')
            for f in Path(self.trial_dir).iterdir():
                if '_blank' in f.name:
                    f.unlink()
            self.game.on_cleanup()

        return is_success, self.action_record, self.state_record


    def print_status(self, state, f):
        box_status = f'box at {self.state.blue_box}' if self.state.blue_box else 'no box'
        f.write(f'\n\nRed is at {state.red_location}, blue is at {self.state.blue_location} holding {box_status}')
