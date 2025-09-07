import random

from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict, Literal


# ANSI escape codes for colors
class Color:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class State(TypedDict):
    my_message: str

def construct_msg(state: State, text: str) -> State:
    msg = state['my_message']
    state['my_message'] = msg + text
    return state

def node1(state: State) -> State:
    # Colored print statement
    print(f"{Color.HEADER}Running Node1{Color.RESET}")
    return construct_msg(state, ", I'm ")

def node2(state: State) -> State:
    print(f"{Color.GREEN}Running Node2{Color.RESET}")
    return construct_msg(state, " Happy :)")

def node3(state: State) -> State:
    print(f"{Color.YELLOW}Running Node3{Color.RESET}")
    return construct_msg(state, " Sad :(")

def decide_node(state: State) -> Literal["n2", "n3"]:
    n = random.randint(0,10)
    print(f"{Color.CYAN}Running DecisionNode, Chosen Number: {n} {Color.RESET}")
    if n > 5:
        return "n3"
    return "n2"

graph = StateGraph(State)
graph.add_node("n1", node1)
graph.add_node("n2", node2)
graph.add_node("n3", node3)

graph.add_edge(START, "n1")
graph.add_conditional_edges("n1", decide_node)
graph.add_edge( "n2", END)
graph.add_edge( "n3", END)
builder = graph.compile()

if __name__ == "__main__":
    human = str(input("Press Enter your message to continue..."))
    msg = builder.invoke({"my_message": human})
    print(msg)