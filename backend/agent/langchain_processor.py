from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Define a prompt template to process incoming messages.
template = "You are a helpful assistant. Process the following message and provide a concise response:\n\n{message}"
prompt = PromptTemplate(template=template, input_variables=["message"])

# Initialize the language model.
# Ensure you have set your OpenAI API key in the environment variable OPENAI_API_KEY.
llm = OpenAI(temperature=0.7)

# Create a chain that combines the prompt and the language model.
chain = LLMChain(llm=llm, prompt=prompt)

def process_message(message: str) -> str:
    """
    Processes an incoming message using the LangChain pipeline.
    
    Args:
        message (str): The input message to be processed.
    
    Returns:
        str: The processed response from the LLM.
    """
    response = chain.run(message=message)
    return response

# For quick testing.
if __name__ == '__main__':
    test_message = "Tell me a joke about programming."
    result = process_message(test_message)
    print("Processed Message:", result)
