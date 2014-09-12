__author__ = "Christopher Raleigh and Anthony Ferrero"


class FoodAgentAI(object):
    """An intelligence that controls a food agent"""

    def __init__(self, board_state, heuristic):
        self.board_state = board_state
        self._heuristic = heuristic

    def on_food_agent_turn(self):
        """Actions for the AI to perform on its agent's turn."""
        # TO DO: Someone needs to implement this function
