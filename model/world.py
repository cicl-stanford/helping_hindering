from utils import *

from collections import namedtuple
import networkx as nx
import numpy as np
import random
from math import inf



State = namedtuple('State', ['red_location', 'blue_location', 'blue_box', 'box_moved', 'boxes', 'time_limit', 'turn'])

def make_state(red_location, blue_location, blue_box, box_moved, boxes, time_limit, turn):
    return State(red_location,
                 blue_location,
                 blue_box,
                 box_moved,
                 tuple(sorted(boxes)),
                 time_limit,
                 turn)


# =============================================================================


class World():
    def __init__(self):
        self.width = 0
        self.height = 0
        self.goal = (0, 0)
        self.graph = nx.Graph()


    def read_world(self, filename):
        lines = open(filename, 'r').readlines()
        boxes = set()
        self.height = len(lines)
        for y, line in enumerate(lines):
            line = line.strip('\n')
            for x, rep in enumerate(line):
                if rep == '.':
                    self.graph.add_edge((x//2, y), (x//2 + 1, y))
                elif rep != '|':
                    self.graph.add_node((x//2, y))
                    if rep.lower() == 'g':
                        self.goal = (x//2, y)
                    if rep.lower() == 'x':
                        boxes.add((x//2, y))
                    if y < self.height-1 and rep not in '_GX':
                        self.graph.add_edge((x//2, y), (x//2, y + 1))
        self.width = x//2 + 1
        return boxes


    def box_graph(self, boxes = set()):
        box_graph = self.graph.copy()
        for box in boxes:
            box_graph.remove_edges_from(list(box_graph.edges(box)))
        return box_graph


    def inbounds(self, location):
        x, y = location
        return min(max(x, 0), self.width-1), min(max(y, 0), self.height-1)


    def get_action(self, location_one, location_two):
        return tuple(map(lambda i, j: int(j-i), location_one, location_two))


    def get_new_location(self, location, action):
        return self.inbounds([sum(x) for x in zip(location, action)])

    
    def get_path_from_locations(self, locations):
        if len(locations) < 2:
            return [STAY]
        path = []
        for i in range(len(locations) - 1):
            path.append(self.get_action(locations[i], locations[i+1]))
        return path


    def is_terminal(self, state):
        return state.time_limit == 0 or state.red_location == self.goal


    def terminal_reward(self, location):
        d = self.distance(location, self.goal)
        return R_GOAL * PROX_DECAY ** d


    def reward(self, state, action, new_state):
        # blue's turn
        if state.turn == 'blue':
            return -action_cost(action)
        # red's turn
        r_action = -1
        r_goal = self.terminal_reward(new_state.red_location) if self.is_terminal(new_state) else 0
        d = self.distance(new_state.red_location, self.goal)
        r_prox = proximity_reward(1, d+1)
        return r_action + r_goal + r_prox


    def distance(self, start, end, count_boxes = False, boxes = set()):
        g = self.graph if not count_boxes else self.box_graph(boxes)
        if nx.has_path(g, start, end):
            return nx.shortest_path_length(g, start, end)
        return inf
        


    def valid_actions(self, state):
        """ Returns all valid actions in given state """
        if self.is_terminal(state): return []

        if state.turn == 'blue' and state.blue_location == (-1, -1):
            return [STAY]

        valid_actions = set([STAY])
        box_graph = self.box_graph(state.boxes)
        if state.turn == 'red':
            # Check move actions
            for new_location in box_graph.neighbors(state.red_location):
                valid_actions.add(self.get_action(state.red_location, new_location))
        elif state.turn == 'blue' and state.blue_box is None:
            # Check move actions
            for new_location in box_graph.neighbors(state.blue_location):
                valid_actions.add(self.get_action(state.blue_location, new_location))
            # Check hold actions
            if not state.box_moved:
                for box in state.boxes:
                    if (state.blue_location, box) in self.graph.edges:
                        action = self.get_action(state.blue_location, box)
                        valid_actions.add(HOLD_ACTIONS[ACTIONS.index(action)])
        elif state.turn == 'blue' and state.blue_box is not None:
            box = state.blue_box
            if not state.box_moved:
                box_graph = self.box_graph(set(state.boxes) - {box})
                # Check push action
                push_action = self.get_action(state.blue_location, box)
                new_box = self.get_new_location(box, push_action)
                if (((box, new_box) in box_graph.edges) and
                    (new_box != state.red_location) and
                    (new_box != self.goal)):
                    valid_actions.add(push_action)
                # Check pull action
                pull_action = self.get_action(box, state.blue_location)
                new_agent = self.get_new_location(state.blue_location, pull_action)
                if (((state.blue_location, new_agent) in box_graph.edges) and
                    (state.blue_location != state.red_location) and
                    (state.blue_location != self.goal)):
                    valid_actions.add(pull_action)
            # Check release action
            action = self.get_action(state.blue_location, box)
            valid_actions.add(RELEASE_ACTIONS[ACTIONS.index(action)])

        return valid_actions

    
    def execute(self, state, action):
        new_red_location, new_blue_location, new_blue_box, new_box_moved, _, new_time_limit, _ = state
        new_boxes = set(state.boxes)
        new_turn = 'red' if state.turn == 'blue' else 'blue'
        assert action in self.valid_actions(state), f'Invalid action {action} for state {state}'

        if state.turn == 'red':
            new_red_location = self.get_new_location(state.red_location, action)

        elif state.blue_location == (-1, -1):
            new_time_limit -= 1
            new_blue_location = (-1, -1)
        else:
            new_time_limit -= 1
            new_location = self.get_new_location(state.blue_location, unit_action(action))
            if action in HOLD_ACTIONS:
                new_blue_box = new_location
            elif action in RELEASE_ACTIONS:
                new_blue_box = None
                new_box_moved = True
            elif action in ACTIONS:
                new_blue_location = new_location
                if state.blue_box is not None:
                    new_box = self.get_new_location(state.blue_box, action)
                    new_boxes.remove(state.blue_box)
                    new_boxes.add(new_box)
                    new_blue_box = new_box
                    if action != STAY:
                        new_box_moved = True

        new_state = make_state(new_red_location, new_blue_location, new_blue_box, new_box_moved, new_boxes, new_time_limit, new_turn)

        return new_state

