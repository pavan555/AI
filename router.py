# ANSI escape codes for colors
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.constants import START, END
from langgraph.graph import StateGraph, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition


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

def multiply(x, y):
    """
    This function multiplies two numbers.
    :param x: first number to multiply
    :param y: second number to multiply
    :return: result of multiplication of @param x and @param y
    """
    print(f"{Color.BLUE}Multiplying {x} and {y}...{Color.RESET}")
    return x * y

def add(x, y):
    """
    This function adds two numbers.
    :param x: first number to add
    :param y: second number to add
    :return: result of addition of @param x and @param y
    """
    print(f'{Color.CYAN}Addition Node Called {x} + {y} {Color.RESET}')
    return x + y

llm = ChatOpenAI(model="gpt-4o")
llm_with_tools = llm.bind_tools([add, multiply])


def tool_llm_call(state: MessagesState) -> MessagesState:
    result = llm_with_tools.invoke(state.get("messages"))
    print(f"{Color.CYAN}Tool LLM Call Called with result {result} {Color.RESET}")
    return {"messages": [result]}


graph = StateGraph(MessagesState)
graph.add_node("tools_llm", tool_llm_call)
graph.add_node("tools", ToolNode([add, multiply]))

graph.add_edge(START, "tools_llm")
graph.add_conditional_edges("tools_llm", tools_condition, )
graph.add_edge("tools", END)
# graph.add_edge("tools_llm", END)
builder = graph.compile()

if __name__ == "__main__":
    msg = str(input("Hi, How can I help you?"))
    result = builder.invoke({"messages": HumanMessage(msg)})
    print(result)