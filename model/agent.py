from utils import *

import random
import networkx as nx
from math import inf
from functools import lru_cache

MAXSIZE = None


class Agent:
    def __init__(self, world, name, color):
        self.world = world
        self.softmax_beta = 3      # for estimating other agent's policy
        self.name = name
        self.color = color

    @lru_cache(MAXSIZE)
    def V(self, state):
        return 0

    @lru_cache(MAXSIZE)
    def Q(self, state, action):
        return 0

    def best_action(self, state, belief_help = None,
                    softmax_beta = None, epsilon = 0, f = None):

        assert state.turn == self.agent
        # rounding to help with computing efficiency
        if belief_help: belief_help = round(belief_help, 1)
        Q = {action: self.Q(state, action, belief_help) for action in self.world.valid_actions(state)}
        print_Q = ', '.join([f'{k}: {v:.3f}' for k, v in Q.items()])
        f.write(f'\nQ: {{{print_Q}}}')
        
        if softmax_beta:
            Q = get_softmax(Q, softmax_beta)
            actions, values = zip(*Q.items())
            action = random.choices(actions, values, k = 1)[0]
    
        # select optimal action with probability 1 - epsilon, otherwise random
        elif bernoulli(1 - epsilon):
            best_Q = max(Q.values())
            # control for near-ties (floating point trailing errors)
            best_actions = [action for action, Q in Q.items() if best_Q - Q < 10**-3]
            f.write(f'\nSelecting optimal action from {best_actions}')
            # prefer STAY over equally good move actions
            if STAY in best_actions:
                action = STAY
            else:
                action = random.choice(best_actions)
        else:
            f.write(f'\nSelecting random action')
            action = random.choice(list(Q.keys()))

        return action


# =============================================================================


class NaiveRedAgent(Agent):
    def __init__(self, world, name = 'red player', color = Color.RED):
        super().__init__(world, name, color)
        self.agent = 'red'
        self.blue_intentions = {0: None}
    
    
    @lru_cache(MAXSIZE)
    def V(self, state, belief_help = None):
        if self.world.is_terminal(state):
            return 0
        box_graph = self.world.box_graph(state.boxes)
        reach = nx.single_source_shortest_path_length(box_graph,
                state.red_location, cutoff=state.time_limit)
        # distance to goal without counting boxes
        d_prox = self.world.distance(state.red_location, self.world.goal)
        if self.world.goal in reach.keys():
            d = reach[self.world.goal]
            r_action = -geom_sum(GAMMA, d)
            r_prox = proximity_reward(d, d_prox)
            r_goal = R_GOAL * (GAMMA ** (d - 1))
            g = r_action + r_goal + r_prox
            return g
        best_g = -inf
        for location in reach.keys():
            d = reach[location]
            r_action = -geom_sum(GAMMA, state.time_limit)
            r_prox = proximity_reward(state.time_limit, d_prox)
            r_goal = self.world.terminal_reward(location) * (GAMMA ** (state.time_limit - 1))
            g = r_action + r_goal + r_prox
            if g > best_g:
                best_g = g
        return best_g


    @lru_cache(MAXSIZE)
    def Q(self, state, action, belief_help = None):
        if self.world.is_terminal(state):
            return 0
        if state.turn == 'blue':
            return 0
        new_state = self.world.execute(state, action)
        r = self.world.reward(state, action, new_state)
        q = r + GAMMA * self.V(new_state)
        return q


    def update_belief(self, prior_help, state, blue_action):
        return None


# =============================================================================


class NaiveBlueAgent(Agent):
    def __init__(self, world, name = 'blue player', color = Color.BLUE,
                 red = None, intention = 'help'):
        super().__init__(world, name, color)
        self.agent = 'blue'
        self.intention = intention   # help or hinder
        self.social_param = 1 if self.intention == 'help' else -1
        self.present_param = None
        self.red = red if red else NaiveRedAgent(self.world)


    @lru_cache(MAXSIZE)
    def V(self, state):
        if self.world.is_terminal(state):
            return 0
        if state.turn == 'blue':
            qs = {action: self.Q(state, action) for action in self.world.valid_actions(state)}
            q = max(qs.values()) if qs else 0
            return q
        else:
            red_qs = {action: self.red.Q(state, action) for action in self.world.valid_actions(state)}
            red_p = get_softmax(red_qs, self.softmax_beta)
            v = 0
            for action, p in red_p.items():
                new_state = self.world.execute(state, action)
                r = self.world.reward(state, action, new_state)
                new_v = self.V(new_state)
                delta_v = p * (self.social_param * r + GAMMA * new_v)
                v += delta_v
            return v


    @lru_cache(MAXSIZE)
    def Q(self, state, action, belief_help = None):
        if self.world.is_terminal(state):
            return 0
        if state.turn == 'red':
            return 0
        new_state = self.world.execute(state, action)
        r = self.world.reward(state, action, new_state)
        v = GAMMA * self.V(new_state)
        return r + v


# =============================================================================


class SophisticatedRedAgent(Agent):
    def __init__(self, world, name = 'red player', color = Color.RED,
                 prior = 0.5, softmax_beta_belief = 0.5):
        super().__init__(world, name, color)
        self.agent = 'red'
        self.softmax_beta_belief = softmax_beta_belief
        self.blue_intentions = {0: prior}
        self.blue_help = NaiveBlueAgent(self.world, intention = 'help')
        self.blue_hinder = NaiveBlueAgent(self.world, intention = 'hinder')


    @lru_cache(MAXSIZE)
    def V(self, state, belief_help = 0.5):
        if self.world.is_terminal(state):
            if state.red_location == self.world.goal:
                return 0
            else:
                return self.world.terminal_reward(state.red_location)
        if state.turn == 'red':
            qs = {action: self.Q(state, action, belief_help) for action in self.world.valid_actions(state)}
            q = max(qs.values()) if qs else 0
            return q
        else:
            # predict blue policy as mixture of intentions
            blue_actions = self.world.valid_actions(state)
            q_help = {a: self.blue_help.Q(state, a) for a in blue_actions}
            q_help = get_softmax(q_help, self.softmax_beta)
            q_hinder = {a: self.blue_hinder.Q(state, a) for a in blue_actions}
            q_hinder = get_softmax(q_hinder, self.softmax_beta)
            v = 0
            for a in blue_actions:
                p = belief_help * q_help[a] + (1 - belief_help) * q_hinder[a]
                new_state = self.world.execute(state, a)
                new_belief_help = round(self._update_belief(belief_help, q_help[a], q_hinder[a]), 1)
                delta_v = p * GAMMA * self.V(new_state, new_belief_help)
                v += delta_v
            return v


    @lru_cache(MAXSIZE)
    def Q(self, state, action, belief_help = 0.5):
        if self.world.is_terminal(state):
            return 0
        if state.turn == 'blue':
            return 0
        new_state = self.world.execute(state, action)
        r = self.world.reward(state, action, new_state)
        v = GAMMA * self.V(new_state, belief_help)
        return r + v


    def update_belief(self, prior_help, state, blue_action):
        assert state.turn == 'blue'
        blue_actions = self.world.valid_actions(state)
        q_help = {a: self.blue_help.Q(state, a) for a in blue_actions}
        q_hinder = {a: self.blue_hinder.Q(state, a) for a in blue_actions}
        q_help = get_softmax(q_help, self.softmax_beta_belief)
        q_hinder = get_softmax(q_hinder, self.softmax_beta_belief)
        prob_help = q_help[blue_action]
        prob_hinder = q_hinder[blue_action]
        return self._update_belief(prior_help, prob_help, prob_hinder)


    def _update_belief(self, prior_help, prob_help, prob_hinder):
        # internal function to save computation when prob_help/hinder are provided
        post_help = (prior_help + 1e-4) * prob_help
        post_hinder = (1 - prior_help + 1e-4) * prob_hinder
        return post_help / (post_help + post_hinder)


# =============================================================================


class SophisticatedBlueAgent(Agent):
    def __init__(self, world, name = 'blue player', color = Color.BLUE,
                 red = None, intention = 'help'):
        super().__init__(world, name, color)
        self.agent = 'blue'
        self.intention = intention   # help, hinder, fake help, or fake hinder
        self.social_param = 1 if self.intention in ['help', 'fake-hinder'] else -1
        self.present_param = 13 if 'help' in self.intention else -13
        self.red = red if red else SophisticatedRedAgent(self.world)
        self.my_belief = 0 if self.social_param == -1 else 1


    @lru_cache(MAXSIZE)
    def V(self, state, red_belief = 0.5):
        if self.world.is_terminal(state):
            return 0
        if state.turn == 'blue':
            qs = {action: self.Q(state, action, red_belief) for action in self.world.valid_actions(state)}
            q = max(qs.values()) if qs else 0
            return q
        else:
            red_qs = {action: self.red.Q(state, action, red_belief) for action in self.world.valid_actions(state)}
            red_p = get_softmax(red_qs, self.softmax_beta)
            v = 0
            for action, p in red_p.items():
                new_state = self.world.execute(state, action)
                r = self.world.reward(state, action, new_state)
                new_v = self.V(new_state, red_belief)
                delta_v = p * (self.social_param * r + GAMMA * new_v)
                v += delta_v
            return v


    @lru_cache(MAXSIZE)
    def Q(self, state, action, red_belief = 0.5):
        if self.world.is_terminal(state):
            return 0
        if state.turn == 'red':
            return 0
        new_state = self.world.execute(state, action)
        r = self.world.reward(state, action, new_state)
        r_social = self.social_param * self.red.V(new_state, red_belief)
        new_belief = round(self.red.update_belief(red_belief, state, action), 1)
        r_present = self.present_param * new_belief
        v = GAMMA * self.V(new_state, red_belief)
        q = r + r_social + r_present + v
        return q
