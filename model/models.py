import scipy as sp

from utils import action_cost, STAY
from environment import *
from agent import *
from world import make_state


class EffortModel:
    def __init__(self, action_record):
        self.action_record = action_record

    def run(self):
        blue_path = [a for (t, i), a in sorted(self.action_record.items()) if i == 1]
        costs = [action_cost(a) for a in blue_path if a != STAY]
        return sum(costs)


# =========================================================

class CounterfactualModel:
    def __init__(self, world, action_record, initial_state,
                 prob_follow = 0.5, softmax_beta = None):
        self.world = world
        self.action_record = action_record
        self.initial_state = initial_state
        self.prob_follow = prob_follow
        self.softmax_beta = softmax_beta


    def run(self, n_simulations):
        # Run simulations and track success rate
        num_successes = 0
        for i in range(n_simulations):
            num_successes += self.simulate_once()
        success_rate = num_successes / n_simulations
        return success_rate


class NeutralCounterfactualModel(CounterfactualModel):
    def __init__(self, world, action_record, initial_state,
                 prob_follow = 0.5, softmax_beta = 1, red_level = 0):
        super().__init__(world, action_record, initial_state,
                         prob_follow = prob_follow, softmax_beta = softmax_beta)
        self.red = NaiveRedAgent(self.world) if red_level == 0 else SophisticatedRedAgent(self.world)
        self.blue = NaiveBlueAgent(self.world)

    
    def simulate_once(self):
        red_path = [a for (t, i), a in sorted(self.action_record.items()) if i == 0]
        blue_path = [STAY]*self.initial_state.time_limit
        state = make_state(self.initial_state.red_location, 
                           (-1, -1), None, False,
                           self.initial_state.boxes,
                           self.initial_state.time_limit,
                           'red')
        env = Environment(self.world, self.red, self.blue)
        is_success, action_record, state_record, = env.run(state,
                red_path = red_path,
                blue_path = blue_path,
                prob_follow = self.prob_follow,
                softmax_beta = self.softmax_beta)
        return is_success


class UniformPriorCounterfactualModel(CounterfactualModel):
    def __init__(self, world, action_record, initial_state,
                 prob_follow = 0.5, softmax_beta = 1,
                 softmax_beta_belief = 0.5):
        super().__init__(world, action_record, initial_state,
                         prob_follow = prob_follow,
                         softmax_beta = softmax_beta)
        self.red = SophisticatedRedAgent(self.world, softmax_beta_belief = softmax_beta_belief)
        self.blue = NaiveBlueAgent(self.world)
    
    def simulate_once(self):
        # condition on actual paths
        red_path = [a for (t, i), a in sorted(self.action_record.items()) if i == 0]
        blue_path = [a for (t, i), a in sorted(self.action_record.items()) if i == 1]
        env = Environment(self.world, self.red, self.blue)
        is_success, _, _, = env.run(
                self.initial_state,
                red_path = red_path,
                blue_path = blue_path,
                prob_follow = self.prob_follow,
                softmax_beta = self.softmax_beta)
        return is_success


class UpdatedPriorCounterfactualModel(CounterfactualModel):
    def __init__(self, world, action_record, initial_state, prior,
                 prob_follow = 0.5, softmax_beta = 1,
                 softmax_beta_belief = 0.5):
        super().__init__(world, action_record, initial_state,
                         prob_follow = prob_follow,
                         softmax_beta = softmax_beta)
        self.prior = prior
        self.red = SophisticatedRedAgent(self.world, prior = self.prior,
                                         softmax_beta_belief = softmax_beta_belief)
        self.blue = NaiveBlueAgent(self.world)
    
    def simulate_once(self):
        # condition on actual paths
        red_path = [a for (t, i), a in sorted(self.action_record.items()) if i == 0]
        blue_path = [a for (t, i), a in sorted(self.action_record.items()) if i == 1]
        env = Environment(self.world, self.red, self.blue)
        is_success, _, _, = env.run(
                self.initial_state,
                red_path = red_path,
                blue_path = blue_path,
                prob_follow = self.prob_follow,
                softmax_beta = self.softmax_beta)
        return is_success


# =========================================================

class IntentionModel:
    def __init__(self, world, action_record, state_record, initial_state, prior = 0.5, softmax_beta = 0.5):
        self.world = world
        self.action_record = action_record
        self.state_record = state_record
        self.initial_state = initial_state
        self.prior = prior
        self.softmax_beta = softmax_beta

    def run(self):
        # infer intentions from a sophisticated red's perspective
        agent = SophisticatedRedAgent(self.world)
        agent.softmax_beta_belief = self.softmax_beta
        int_beliefs = {0: self.prior}
        last_t = sorted([t for (t, i) in self.action_record.keys() if i == 1])[-1]
        for t in range(1, last_t + 1):
            int_beliefs[t] = agent.update_belief(
                    prior_help = int_beliefs[t-1],
                    state = self.state_record[t, 1],
                    blue_action = self.action_record[t, 1])
        return int_beliefs[last_t]
