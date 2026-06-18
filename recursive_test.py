import sys
import subprocess


if (__name__ == "__main__"):
    maps: list[str] = ["easy/01_linear_path.txt",
                       "easy/02_simple_fork.txt",
                       "easy/03_basic_capacity.txt",
                       "medium/01_dead_end_trap.txt",
                       "medium/02_circular_loop.txt",
                       "medium/03_priority_puzzle.txt",
                       "hard/01_maze_nightmare.txt",
                       "hard/02_capacity_hell.txt",
                       "hard/03_ultimate_challenge.txt",
                       "challenger/01_the_impossible_dream.txt"]
    for file in maps:
        result: subprocess.CompletedProcess = subprocess.run([sys.executable,
                                                              "fly-in.py",
                                                              f"maps/{file}"],
                                                             check=True)
        if (result.returncode == 1):
            print(file, "deu erro")
            break
