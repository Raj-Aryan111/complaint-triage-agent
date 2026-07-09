from src.llm import get_llm

llm = get_llm()

response = llm.generate(
    prompt="What is the capital of India?"
)

print(response)