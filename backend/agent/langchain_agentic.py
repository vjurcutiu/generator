from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI

# Define a simple tool: Echo tool returns the input string prefixed with 'Echo:'
def echo_tool(input_text: str) -> str:
    return f"Echo: {input_text}"

# Register the tool with a name and description
tools = [
    Tool(
        name="Echo",
        func=echo_tool,
        description="Echoes the input provided to it."
    )
]

# Initialize the LLM (ensure your API key is set in the environment)
llm = OpenAI(temperature=0)

# Create an agent using the provided tools.
# The 'zero-shot-react-description' agent will choose and call tools as needed.
agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

if __name__ == '__main__':
    prompt = "Tell me to echo 'Hello, world!'"
    result = agent.run(prompt)
    print("Agent Result:", result)
