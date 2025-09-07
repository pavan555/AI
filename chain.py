from typing import TypedDict, List


from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, add_messages, MessagesState
from langgraph.constants import START, END
from typing_extensions import Annotated

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
    messages: Annotated[List[str], add_messages]

class MessageState(MessagesState):
    count: int
    pass

def tool_call(a: int, b: int) -> int:
    """
    This function will add two number and returns the result.
    :param a: first number
    :param b: second number
    :return: sum of a+b
    """
    print(f"{Color.YELLOW}Tool call triggered {Color.RESET}")
    print(f"{Color.CYAN} a: {a} b: {b} result:{a+b}{Color.RESET}")
    return a + b

llm = ChatOpenAI(model="gpt-4o")
llm = llm.bind_tools([tool_call])

def llm_node(state: MessageState) -> MessageState:
    count = (state["count"] or 0) + 1
    messages = state["messages"]
    print(f"{Color.BLUE}LLM node triggered {Color.RESET}")
    result = llm.invoke(messages)
    return {"messages": [result], "count": count}


graph = StateGraph(MessageState)
graph.add_node("llm", llm_node)

graph.add_edge(START, "llm")
graph.add_edge("llm", END)
builder = graph.compile()

if __name__ == "__main__":

    message = str(input("How can i help you?\n"))
    messages = [HumanMessage("Hey Hi"), AIMessage("Hey, How can i help you?"), message]
    print(builder.invoke(messages))