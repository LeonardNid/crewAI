#!/usr/bin/env python
import json

from pydantic import BaseModel

from crewai.flow import Flow, listen, start, router, or_

from backend5.crews.backend_crew.backend_crew import DesignCrew
from backend5.crews.test_crew.test_crew import TestCrew
from backend5.crews.bug_fix_crew.bug_fix_crew import BugFixCrew

import weave
import shutil
from pathlib import Path

class BackendState(BaseModel):
    test_count: int = 0
    test_result: str = ""


class BackendFlow(Flow[BackendState]):

    weave.init(project_name="backend5")

    @start()
    def clean_directories(self):
        """
        Cleans the Output and instance directories before running the crews.
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

    @listen(clean_directories)
    def generate_Design(self):
        print("Design crew started")
        inputs = {
            'topic': 'Football',
            'customer': (
                "I want to safe my football team and player data. "
                "Every team has a name, a city, a country, and a stadium."
                "Every player has a name, a position, a team, and a country."
            )
        }
        # inputs = {
        #     'topic': 'bicycle workshop',
        #     'customer': ('''
        #         I want to store the inventory of my bicycle workshop with the various parts and their compatibility.
        #         There are many different parts: 
        #         Frames: Measurements, brand, material, maximum tire width, compatible brakes, compatible bicycle gears, type of compatible drivetrain (hub, chain), type of frame (gravel, road bike, touring bike, city bike, etc.), each frame type also has specific properties (for example, gravel frames might have mounting points for attaching bags, road bike frames might have aerodynamic optimization, etc.), price, name (to uniquely identify the frame), weight, geometry, compatible handlebars, how much weight the frame can carry, compatible seatposts, type of cable routing (external, internal).
        #         Rims: Tire width, compatible tire types (tubeless, with tube, etc.), rim height, weight, price, required valve length, material, compatible frames, brand.
        #         Brakes (sometimes brakes and bicycle gears come as one inseparable unit, e.g. on road and gravel bikes): Type (hydraulic, mechanical), compatible frames, weight, price, brand, compatible bicycle gears.
        #         Bicycle gears (sometimes brakes and bicycle gears come as one inseparable unit, e.g. on road and gravel bikes): Type (electronic, mechanical), compatible frames, weight, price, brand, compatible brakes.
        #         Handlebars: Type (flat, road, gravel, mountain bike), material, weight, brand, compatible frames, compatible brakes, compatible bicycle gears, price.
        #         Saddles: Type (padding, etc.), shape, compatible seatposts, brand, price, weight.
        #         Seatposts: Material, compatible frames, compatible seatposts, brand, price, weight.
        #         Brake pads: Brake type, compatible Brakes, brand, Price.
        #         And overall, I want, for example, to be able to select a frame and then see the possible choices of compatible components. You should also be able to specify exactly which components should be listed if, for instance, only one part is broken. But in theory, it would also be nice if you could configure a whole bike, so you can see what fits together.
        #         '''
        #     )
        # }
        result = (
            DesignCrew()
            .crew()
            .kickoff(inputs=inputs)
        )
        from backend5.tools.Utils import cleanup_quotes_in_file
        for target_file in ["Output/app.py", "Output/models.py"]:
            cleanup_quotes_in_file(target_file) 
        print("Design crew finished")

    @listen("failed")
    def fix_bug(self):
        print("Bug fix crew started")
        inputs = {
            "test_result": self.state.test_result,
        }
        result = (
            BugFixCrew()
            .crew()
            .kickoff(inputs=inputs)
        )
        print("Bug fix crew finished")

    @listen(or_(generate_Design, fix_bug))
    def test_Backend(self):
        print("Test crew started")
        # input("Pause") # Temporary pause for debugging
        inputs = {
            
        }
        result = (
            TestCrew()
            .crew()
            .kickoff(inputs=inputs)
        )
        self.state.test_count += 1
        print("Test crew finished")
        return result.raw

    @router(test_Backend)
    def check_results(self, test_result):
        """
        Parses the JSON test_result to check for any failed requests.
        Returns 'failed' if any request has a status code >= 400.
        """

        try:
            results = json.loads(test_result)

            for entry in results:
                code = entry.get("status_code", "")
                if code >= 400:
                    self.state.test_result = test_result
                    print("Test failed ❌")
                    return "failed"

            print("Test passed ✅")
            return "success"

        except Exception as e:
            print("⚠️ Error parsing test_result:", e)
            return "failed"
        
    @listen("success")
    def final(self):
        print("All tests passed successfully!")
        print("Test attempts:", self.state.test_count)
    

def kickoff():
    backendFlow = BackendFlow()
    backendFlow.kickoff()


def plot():
    backendFlow = BackendFlow()
    backendFlow.plot()


if __name__ == "__main__":
    kickoff()
