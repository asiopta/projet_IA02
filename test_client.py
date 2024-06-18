#!/usr/bin/python3

import ast
import argparse
from typing import Dict, Any
from gndclient import start, Action, Score, Player, State, Time, DODO_STR, GOPHER_STR
from gopher import strategy_alphabeta_gopher
from dodo import strategy_alphabeta_dodo

Environment = Dict[str, Any]


def initialize(
    game: str, state: State, player: Player, hex_size: int, total_time: Time
) -> Environment:
    env: Environment = {}
    print("Init")
    print(f"{game} playing {player} on a grid of size {hex_size}. Time remaining: {total_time}")
    if game == "gopher":
        env["game"] = "gopher"
        strategy = strategy_alphabeta_gopher
    elif game == "dodo":
        env["game"] = "dodo"
        strategy = strategy_alphabeta_dodo


    return env


def strategy(env: Environment, state: State, player: Player, time_left: Time) -> tuple[Environment, Action]:
    '''Cette fonction est la strategie qu'on utilise pour jouer.
    Cette fonction est lancée à chaque fois que c'est à notre joueur de jouer.'''
    if(env["game"] == "gopher"):
        return (env, strategy_alphabeta_gopher(state, player, time_left))
    elif env["game"] == "dodo":
        return (env, strategy_alphabeta_dodo(state, player, time_left))


def final_result(state: State, score: Score, player: Player):
    print(f"Ending: {player} wins with a score of {score}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="ClientTesting", description="Test the IA02 python client"
    )

    parser.add_argument("group_id")
    parser.add_argument("members")
    parser.add_argument("password")
    parser.add_argument("-s", "--server-url", default="http://localhost:8080/")
    parser.add_argument("-d", "--disable-dodo", action="store_true")
    parser.add_argument("-g", "--disable-gopher", action="store_true")
    args = parser.parse_args()

    available_games = [DODO_STR, GOPHER_STR]
    if args.disable_dodo:
        available_games.remove(DODO_STR)
    if args.disable_gopher:
        available_games.remove(GOPHER_STR)

    start(
        args.server_url,
        args.group_id,
        args.members,
        args.password,
        available_games,
        initialize,
        strategy,
        final_result,
        gui=True,
    )
