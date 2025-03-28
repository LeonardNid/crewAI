#!/usr/bin/env python
import sys
import warnings

import agentops
import os

from datetime import datetime

from crew import Backend1

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

agentops.init(api_key=os.getenv("AGENTOPS_API_KEY"), auto_start_session=False)

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
    }
    
    try:
        agentops.start_session()

        Backend1().crew().kickoff(inputs=inputs)

        agentops.end_session("success")
    except Exception as e:
        agentops.end_session("failure")
        raise Exception(f"An error occurred while running the crew: {e}")


run()