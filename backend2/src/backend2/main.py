#!/usr/bin/env python
import sys
import warnings

import agentops
import os

from datetime import datetime

from backend2.crew import Backend2

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
        'goal': 'A fully fletched python backend application with a Flask API and a SQLite database.',
        'customer': 'I want to safe my football team and plyer data. Every team has a name, a city, a country, and a stadium. Every player has a name, a position, a team, and a country.',
    }
    
    try:
        agentops.init(api_key=os.getenv("AGENTOPS_API_KEY"))

        Backend2().crew().kickoff(inputs=inputs)

        agentops.end_session("success")
    except Exception as e:
        agentops.end_session("failure")
        raise Exception(f"An error occurred while running the crew: {e}")


run()