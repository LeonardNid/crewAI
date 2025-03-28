#!/usr/bin/env python
from dotenv import load_dotenv
load_dotenv()
import os
import sys
import warnings
import agentops

from datetime import datetime

from backend3.crew import Backend3

agentops.init(api_key=os.getenv("AGENTOPS_API_KEY"), auto_start_session=False)

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")



# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': 'Football',
        'goal': 'A fully fletched python backend application with a Flask API and a SQLite database.',
        'customer': 'I want to safe my football team and plyer data. Every team has a name, a city, a country, and a stadium. Every player has a name, a position, a team, and a country.',
    }
    
    try:
        agentops.start_session()
        Backend3().crew().kickoff(inputs=inputs)
        agentops.end_session("Success")
    except Exception as e:
        agentops.end_session("Fail", str(e))
        raise Exception(f"An error occurred while running the crew: {e}")


# def train():
#     """
#     Train the crew for a given number of iterations.
#     """
#     inputs = {
#         "topic": "AI LLMs"
#     }
#     try:
#         Backend3().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

#     except Exception as e:
#         raise Exception(f"An error occurred while training the crew: {e}")

# def replay():
#     """
#     Replay the crew execution from a specific task.
#     """
#     try:
#         Backend3().crew().replay(task_id=sys.argv[1])

#     except Exception as e:
#         raise Exception(f"An error occurred while replaying the crew: {e}")

# def test():
#     """
#     Test the crew execution and returns the results.
#     """
#     inputs = {
#         "topic": "AI LLMs"
#     }
#     try:
#         Backend3().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

#     except Exception as e:
#         raise Exception(f"An error occurred while testing the crew: {e}")
