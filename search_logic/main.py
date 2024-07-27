import search_logic.graph as graph
import search_logic.SampleSolution as sample
import search_logic.level1 as lv1
import search_logic.level2 as lv2
import search_logic.level3 as lv3
import search_logic.format_output as fo
from search_logic.solution import SolutionBase
import os

from search_logic.map_config import *


def load_data(path):
    with open(path, "r") as f:
        # Read the first line for n, m, time, and gas
        n, m, time, gas = map(int, f.readline().split())

        # Read the grid
        grid = []
        for _ in range(n):
            grid.append(f.readline().strip().split())

        # Initialize an array to store start ('S') and goal ('G') positions
        start_goal_positions = [[] for _ in range(10)]

        for i in range(n):
            for j in range(m):
                if grid[i][j] == "S":
                    start_goal_positions[0].append((i, j))
                    if len(start_goal_positions[0]) > 1:
                        # reverse the order of the start and goal positions
                        start_goal_positions[0][0], start_goal_positions[0][1] = (
                            start_goal_positions[0][1],
                            start_goal_positions[0][0],
                        )
                elif grid[i][j] == "G":
                    start_goal_positions[0].append((i, j))
                elif grid[i][j].startswith("S"):
                    identifier = int(grid[i][j][1:])
                    start_goal_positions[identifier].append((i, j))
                    if len(start_goal_positions[identifier]) > 1:
                        # reverse the order of the start and goal positions
                        (
                            start_goal_positions[identifier][0],
                            start_goal_positions[identifier][1],
                        ) = (
                            start_goal_positions[identifier][1],
                            start_goal_positions[identifier][0],
                        )
                elif grid[i][j].startswith("G"):
                    identifier = int(grid[i][j][1:])
                    start_goal_positions[identifier].append((i, j))
                elif grid[i][j].startswith("F"):
                    grid[i][j] = ("F", int(grid[i][j][1:]))
                else:
                    grid[i][j] = int(grid[i][j])

        # Validate and store agent positions
        if not start_goal_positions[0] or len(start_goal_positions[0]) < 2:
            raise ValueError(
                "Error: Expected at least one 'S' and one 'G' in the grid."
            )

        # Remove empty positions from agent list
        start_goal_positions = [
            positions for positions in start_goal_positions if positions
        ]

    return grid, start_goal_positions, time, gas


def run_solutions_on_maps():
    solutions = [
        ("Level1", lv1.GBFS, ["g", "agent_list", "grid"], "gbfs"),
        ("Level1", lv1.Astar, ["g", "agent_list", "grid"], "astar"),
        ("Level1", lv1.DFS, ["g", "agent_list", "grid"], "dfs"),
        ("Level1", lv1.BFS, ["g", "agent_list", "grid"], "bfs"),
        ("Level1", lv1.UCS, ["g", "agent_list", "grid"], "ucs"),
        ("Level2", lv2.Level2, ["g", "agent_list", "grid", "time"], "Level2"),
        ("Level3", lv3.Level3, ["g", "agent_list", "grid", "time", "gas"], "Level3"),
    ]
    levels = ["lv1", "lv2", "lv3"]

    for map_name in MAP_NAME:
        for solution_name, SolutionClass, init_args, algo_name in solutions:
            input_path = f"{MAP_FOLDER}lv{str(solution_name[-1])}/{map_name}.txt"
            grid, agent_list, time, gas = load_data(input_path)
            g = graph.GridGraph(grid)

            print(f"Running {solution_name} {algo_name} on {input_path}...")

            # Dynamically prepare the arguments
            init_args_values = {
                "g": g,
                "agent_list": agent_list,
                "grid": grid,
                "time": time,
                "gas": gas,
            }
            args = [init_args_values[arg] for arg in init_args]
            solution = SolutionClass(*args)

            solution.solve()
            move_log_path = "search_logic/move.txt"
            solution.save_move_logs(move_log_path)
            if solution_name != "Level1":
                output_file = f"{JSON_FOLDER}lv{str(solution_name[-1])}/{map_name}.json"
            else:
                output_file = f"{JSON_FOLDER}lv{str(solution_name[-1])}/{algo_name}/{map_name}.json"
            os.makedirs(os.path.dirname(output_file), exist_ok=True)

            # Determine goal files or None if not applicable
            if solution_name == "Level3":
                goal_files = [f"{MAP_FOLDER}lv{str(solution_name[-1])}/{map_name}_goal_{i+1}.txt" for i in range(len(agent_list))]
                goal_files = [goal if os.path.exists(goal) else None for goal in goal_files]
                data = fo.create_json_output(grid, [move_log_path], goal_files, agent_list, gas, time)
            elif solution_name == "Level2":
                goal_files = [f"{MAP_FOLDER}lv{str(solution_name[-1])}/{map_name}_goal_{i+1}.txt" for i in range(len(agent_list))]
                goal_files = [goal if os.path.exists(goal) else None for goal in goal_files]
                data = fo.create_json_output(grid, [move_log_path], goal_files, agent_list, None, time)
            else:
                data = fo.create_json_output(grid, [move_log_path], [None] * len(agent_list), agent_list)

            # Save JSON to file
            fo.save_to_json(data, output_file)
