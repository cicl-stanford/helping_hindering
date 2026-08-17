import argparse
import json
import random
import numpy as np
import pandas as pd

from environment import *
from world import *
from agent import *
from models import *
from utils import make_dir, set_params


def parse_arguments():
    parser = argparse.ArgumentParser("Responsibility")
    
    # Experiment arguments
    parser.add_argument('--exp', type=int, default=1,
                        help='experiment to run (1, 2, or 3)')
    parser.add_argument('--trial', type=int, default=0,
                        help='trial to run (exp1: 1-30, exp2: 1-24, exp3: 1-12)')
    parser.add_argument('--t1', action='store_true', default=False,
                        help='[exp3 only] run interaction 1 of the trial')
    parser.add_argument('--t2', action='store_true', default=False,
                        help='[exp3 only] run interaction 2 of the trial')
    parser.add_argument('--visualize', action='store_true', default=False,
        help='create and store images and gif')
    parser.add_argument('--colors', action='store_true', default=False,
        help='[exp3 only] run trials with modified colors')

    # Model types
    parser.add_argument('--int', action='store_true', default=False,
        help='run intention model')
    parser.add_argument('--int-prior', action='store_true', default=False,
        help='[exp3 only] run intention model for t2 with t1 as prior')
    parser.add_argument('--effort', action='store_true', default=False,
        help='run effort model')
    parser.add_argument('--cf', action='store_true', default=False,
        help='run counterfactual model')
    parser.add_argument('--cf-uniform-prior', action='store_true', default=False,
        help='[exp3 only] run counterfactual model for red with uniform priors')
    parser.add_argument('--cf-updated-prior', action='store_true', default=False,
        help='[exp3 only] run counterfactual model for red with updated priors')

    # Model parameters
    parser.add_argument('--n-simulations', type=int, default=1000,
        help='number of counterfactual simulations')
    parser.add_argument('--prob-follow', type=float, default=0.1,
        help='probability of counterfactual following observed history')
    parser.add_argument('--seed', type=int, default=0,
        help='set pseudorandom seed')
    parser.add_argument('--epsilon', type=float, default=0.2,
        help='for epsilon-greedy action selection')
    parser.add_argument('--cf-softmax-beta', type=float, default=1,
        help='softmax beta for action selection in counterfactual simulations')
    parser.add_argument('--int-softmax-beta', type=float, default=1,
        help='softmax beta for intention inference')
    parser.add_argument('--softmax-beta-belief', type=float, default=0.5,
        help='softmax beta for sophisticated agent belief updating')

    return parser.parse_args()


def fix_seed(seed):
    np.random.seed(seed)
    random.seed(seed)


def run_trial(arglist, trial_info, trial_dir):
    w = World()
    boxes = w.read_world(filename = f'grids/exp{arglist.exp}/{trial_info["trial"]}.txt')
    s0 = make_state(red_location = tuple(trial_info['red_start']),
                    blue_location = tuple(trial_info['blue_start']),
                    blue_box = None,
                    box_moved = False,
                    boxes = boxes,
                    time_limit = 10,
                    turn = 'red')

    if 'red_color' not in trial_info or not arglist.colors:
        trial_info['red_color'] = 'Color.RED'
    if 'red_name' not in trial_info or not arglist.colors:
        trial_info['red_name'] = 'red player'
    if trial_info['red_level'] == 2:
        red_agent = SophisticatedRedAgent(
                w, name = trial_info['red_name'],
                color = eval(trial_info['red_color']))
    else:
        red_agent = NaiveRedAgent(
                w, name = trial_info['red_name'],
                color = eval(trial_info['red_color']))

    if 'blue_color' not in trial_info or not arglist.colors:
        trial_info['blue_color'] = 'Color.BLUE'
    if 'blue_name' not in trial_info or not arglist.colors:
        trial_info['blue_name'] = 'blue player'
    if trial['blue_level'] == 3:
        blue_agent = SophisticatedBlueAgent(
                w, intention = trial['blue_intention'],
                name = trial_info['blue_name'],
                color = eval(trial_info['blue_color']))
    else:
        blue_agent = NaiveBlueAgent(
                w, intention = trial['blue_intention'],
                name = trial_info['blue_name'],
                color = eval(trial_info['blue_color']))
                
    env = Environment(w, red_agent, blue_agent, trial_dir)
    blue_path = trial_info['blue_path'] if 'blue_path' in trial_info else []
    result = env.run(
            initial_state = s0,
            blue_path = blue_path,
            visualize = arglist.visualize,
            epsilon = arglist.epsilon)
    return w, s0, result



EXP_TRIALS = {1: range(1, 31), 2: range(1, 25), 3: range(1, 13)}


if __name__ == '__main__':
    arglist = parse_arguments()
    trial_info = json.load(open(f'trial_info/exp{arglist.exp}/trial_info.json', 'r'))
    set_params(arglist.exp)

    trials_to_run = [arglist.trial] if arglist.trial != 0 else EXP_TRIALS[arglist.exp]

    for trial_num in trials_to_run:
        trial = trial_info[trial_num - 1]

        if arglist.exp in [1, 2]:
            seed = trial['seed'] if arglist.seed == 0 else arglist.seed
            fix_seed(seed)
            print('='*20, f'\nGenerating experiment {arglist.exp} trial {trial_num}...')
            trial_dir = f'trials/exp{arglist.exp}/{trial_num}'
            make_dir(trial_dir)
            w, s0, result = run_trial(arglist, trial, trial_dir)
            _, action_record, state_record = result

        elif arglist.exp == 3:
            seed = trial['t1']['seed']
            fix_seed(seed)
            print('='*20, f'\nGenerating trial {trial_num} round 1...')
            colors_dir = '_colors' if arglist.colors else ''
            trial_dir = f'trials/exp{arglist.exp}{colors_dir}/{trial_num}/t1'
            make_dir(trial_dir)
            trial['red_level'] = trial['t1']['red_level']
            trial['blue_level'] = trial['t1']['blue_level']
            trial['blue_intention'] = trial['t1']['blue_intention']
            w, s0, result = run_trial(arglist, trial, trial_dir)
            _, action_record_t1, state_record_t1 = result

            seed = trial['t2']['seed']
            fix_seed(seed)
            print('='*20, f'\nGenerating trial {trial_num} round 2...')
            trial_dir = f'trials/exp{arglist.exp}{colors_dir}/{trial_num}/t2'
            make_dir(trial_dir)
            trial['red_level'] = trial['t2']['red_level']
            trial['blue_level'] = 1
            trial['blue_intention'] = 'help'
            trial['blue_path'] = [a for (t, i), a in sorted(action_record_t1.items()) if i == 1]
            w, s0, result = run_trial(arglist, trial, trial_dir)
            _, action_record_t2, state_record_t2 = result

        fix_seed(1)

        # Models
        if arglist.effort:
            print('Running effort model...')
            if arglist.exp == 3:
                action_record = action_record_t1 if arglist.t1 else action_record_t2
            model = EffortModel(action_record)
            effort = model.run()
            print(f'\tBlue effort: {effort}')

        if arglist.int or arglist.int_prior:
            print('Running intention model...')
            prior = 0.5
            if arglist.exp == 3:
                if arglist.t1:
                    action_record = action_record_t1
                    state_record = state_record_t1
                if arglist.t2:
                    action_record = action_record_t2
                    state_record = state_record_t2
                    if arglist.int_prior:
                        df = pd.read_csv(f'trial_info/exp3/model_predictions.csv')
                        prior = df.loc[df['trial'] == trial_num, 't1_int'].iloc[0]
            model = IntentionModel(w, action_record, state_record, s0,
                                   prior = prior,
                                   softmax_beta = arglist.int_softmax_beta)
            intention = model.run()
            print(f'\tIntention: {intention:.4f}')

        if arglist.cf:
            print('Running counterfactual model without blue...')
            if arglist.exp == 3:
                action_record = action_record_t1 if arglist.t1 else action_record_t2
            model = NeutralCounterfactualModel(
                    w, action_record, s0,
                    prob_follow = arglist.prob_follow,
                    softmax_beta = arglist.cf_softmax_beta,
                    red_level = 0 if arglist.exp == 1 else 2)
            success_rate = model.run(arglist.n_simulations)
            print(f'\tCounterfactual: {success_rate} over {arglist.n_simulations} simulations')

        if arglist.cf_uniform_prior:
            assert arglist.exp == 3
            print('Running counterfactual model with uniform priors...')
            action_record = action_record_t2
            model = UniformPriorCounterfactualModel(
                    w, action_record, s0,
                    prob_follow = arglist.prob_follow,
                    softmax_beta = arglist.cf_softmax_beta,
                    softmax_beta_belief = arglist.softmax_beta_belief)
            success_rate = model.run(arglist.n_simulations)
            print(f'\tCounterfactual: {success_rate} over {arglist.n_simulations} simulations')

        if arglist.cf_updated_prior:
            assert arglist.exp == 3
            df = pd.read_csv(f'trial_info/exp3/model_predictions.csv')
            prior = df.loc[df['trial'] == trial_num, 't1_int'].iloc[0]
            action_record = action_record_t2
            print('Running counterfactual model with prior {prior}...')
            model = UpdatedPriorCounterfactualModel(
                    w, action_record, s0, prior = prior,
                    prob_follow = arglist.prob_follow,
                    softmax_beta = arglist.cf_softmax_beta,
                    softmax_beta_belief = arglist.softmax_beta_belief)
            success_rate = model.run(arglist.n_simulations)
            print(f'\tCounterfactual: {success_rate} over {arglist.n_simulations} simulations')

        print("="*20)
