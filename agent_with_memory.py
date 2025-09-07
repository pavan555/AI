
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import START
from langgraph.graph import StateGraph, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition


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

def subtract(x, y):
    """
    This function subtracts two numbers.
    :param x: first number
    :param y: second number
    :return: result of subtraction of @param x and @param y
    """
    print(f'{Color.CYAN}Subtraction Node Called {x} - {y} {Color.RESET}')
    return x - y

def divide(x, y):
    """
    This function Divides first number with second number.
    :param x: first number
    :param y: second number
    :return: result of division of @param x and @param y
    """
    print(f'{Color.CYAN}Division Node Called {x} / {y} {Color.RESET}')
    return x / y


tools = [add, multiply, divide, subtract]
llm = ChatOpenAI(model="gpt-4o")
llm_with_tools = llm.bind_tools(tools)
SYS_PROMPT = SystemMessage("You are a helpful assistant tasked with performing arithmetic on a set of inputs.")

def tool_llm_call(state: MessagesState):
    result = llm_with_tools.invoke([SYS_PROMPT] + state.get("messages"))
    return {"messages": [result]}


builder = StateGraph(MessagesState)
builder.add_node("assistant", tool_llm_call)
builder.add_node("tools", ToolNode(tools))

builder.add_conditional_edges("assistant", tools_condition)
builder.add_edge(START, "assistant")
builder.add_edge("tools", "assistant") #observe
### Memory - Previous Each Node History By Thread ID
in_memory_saver = MemorySaver()
graph = builder.compile(checkpointer=in_memory_saver)
config = {"configurable": {"thread_id": "thread-1"}}

def invoke_chat():
    msg = HumanMessage(str(input("Enter a message: ")))
    result = graph.invoke({"messages": [msg]}, config)
    for m in result.get("messages"):
        m.pretty_print()

if __name__ == "__main__":
    invoke_chat()
    invoke_chat()
    invoke_chat()
    invoke_chat()

