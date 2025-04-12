#!/usr/bin/env python
import warnings
import shutil
from pathlib import Path
from backend4.crew import Backend4

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def clean_directories():
    """
    Cleans the Output and instance directories before running the crew.
    """
    for folder in ["Output", "instance"]:
        dir_path = Path(folder)
        if dir_path.exists() and dir_path.is_dir():
            for item in dir_path.iterdir():
                try:
                    if item.is_file() or item.is_symlink():
                        item.unlink()
                    elif item.is_dir():
                        shutil.rmtree(item)
                except Exception as e:
                    print(f"⚠️ Could not delete {item}: {e}")
        else:
            dir_path.mkdir(parents=True, exist_ok=True)
        print(f"✅ Cleared folder: {folder}")


def run():
    """
    Run the Backend4 crew and retry bugfixes if test failures occur.
    """

    inputs = {
        'topic': 'Football',
        'customer': (
            "I want to safe my football team and player data. "
            "Every team has a name, a city, a country, and a stadium."
            "Every player has a name, a position, a team, and a country."
        )
    }

    # inputs = {
    #     'topic': 'Football Extended',
    #     'customer': (
    #         "I want to save my football team and player data. Teams have a name, city, country, stadium.\n"
    #         "Players have a name, position, team, country.\n\n"
    #         "Now I've realized each stadium must also have an address, but I'm not sure what fields that includes. "
    #         "I also think some sponsors might have addresses too. \n\n"
    #         "Also, I'd like to store any contact details for the referee."
    #         "Please decide which fields we have for addresses and contact info."
    #     )
    # }

    # inputs = {
    #     'topic': 'Movies/Series',
    #     'customer': (
    #         """
    #         I want to safe my watched movies and series. I want to rate them from 1 star to 10 stars.
    #         Each movie and series has a director, a cast with many actors, a description and a length.
    #         I would like a way to get all the movies sequels/prequels.
    #         I would also like a way to get all the movies/series from a director or
    #         all the movies/series where a specific actor plays in.
    #         For the series I also want to safe how many seasons and episodes each seasion has.
    #         """
    #     )
    # }

    clean_directories()

    crew_instance = Backend4()

    try:
        crew_instance.crew().kickoff(inputs=inputs)
        crew_instance.retry_fixing_errors(inputs=inputs, max_attempts=3)

    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

if __name__ == "__main__":
    run()
