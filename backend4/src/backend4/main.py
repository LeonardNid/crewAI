#!/usr/bin/env python
import sys
import warnings

import weave

from backend4.crew import Backend4

weave.init(project_name="backend4")
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    # inputs = {
    #     'topic': 'Football',
    #     'customer': (
    #         "I want to safe my football team and player data. "
    #         "Every team has a name, a city, a country, and a stadium."
    #         "Every player has a name, a position, a team, and a country."
    #     )
    # }

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
    
    inputs = {
        'topic': 'Movies/Series',
        'customer': (
            """
            I want to safe my watched movies and series. I want to rate them from 1 star to 10 stars.
            Each movie and series has a director, a cast with many actors, a description and a length.
            I would like a way to get all the movies sequels/prequels.
            I would also like a way to get all the movies/series from a director or
            all the movies/series where a specific actor plays in.
            For the series I also want to safe how many seasons and episodes each seasion has.
            """
        )
    }

    
    try:
        Backend4().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


# def train():
#     """
#     Train the crew for a given number of iterations.
#     """
#     inputs = {
#         "topic": "AI LLMs"
#     }
#     try:
#         Backend4().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

#     except Exception as e:
#         raise Exception(f"An error occurred while training the crew: {e}")

# def replay():
#     """
#     Replay the crew execution from a specific task.
#     """
#     try:
#         Backend4().crew().replay(task_id=sys.argv[1])

#     except Exception as e:
#         raise Exception(f"An error occurred while replaying the crew: {e}")

# def test():
#     """
#     Test the crew execution and returns the results.
#     """
#     inputs = {
#         "topic": "AI LLMs",
#         "current_year": str(datetime.now().year)
#     }
#     try:
#         Backend4().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

#     except Exception as e:
#         raise Exception(f"An error occurred while testing the crew: {e}")
