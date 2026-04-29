from smolagents import CodeAgent, WebSearchTool, tool, InferenceClientModel
from dotenv import load_dotenv
import os

# Load env
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

# ---- TOOL 1: MENU ----
@tool
def suggest_menu(occasion: str) -> str:
    """
    Suggests a menu based on this occasion.
    Args:
        occasion (str): casual, formal, superhero, custom
    """
    if occasion == "casual":
        return "Pizza, snacks, drinks"
    elif occasion == "formal":
        return "3-course dinner with wine"
    elif occasion == "superhero":
        return "High-energy buffet"
    else:
        return "Custom menu"

# ---- AGENT ----
agent = CodeAgent(
    tools = [
        WebSearchTool(), # Music Web Search
        suggest_menu
    ],
    model = InferenceClientModel(
        token = HF_TOKEN
    ),
    additional_authorized_imports = ["datetime"], #time calc
    max_steps = 6
)

# ---- RUN ----
result = agent.run("""
plan a aparty at Wayne's mansion:
1. Suggest a formal menu
2. Find a good music playlist for the party
3. Calculate total preparation time:
    - drinks: 30 min
    - decoration: 60 min
    - menu: 45 min
    - music: 45 min
""")

print(result)