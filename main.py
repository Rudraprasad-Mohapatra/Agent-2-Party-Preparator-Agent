from smolagents import CodeAgent, ToolCallingAgent, WebSearchTool, Tool, tool, InferenceClientModel
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

@tool
def catering_service_tool(query: str) -> str:
    """
    This tool returns the highest rated catering service in Gotham City.

    Args:
        query: A search term for finding catering services.
    """

    # Example list of catering services & their ratings:
    services = {
        "Gotham Catering Co.": 4.9,
        "Wayne Manor Catering": 4.8,
        "Gotham City Events": 4.7,
    }

    # Find the highest rated catering service (simulating search query filtering)
    best_service = max(services, key=services.get)

    return best_service

class SuperheroPartyThemeTool(Tool):
    name = "superhero_party_theme_generator"
    description = """
    This tool suggests creative superhero-themed party ideas based on a category.
    It returns a unique party theme idea."""

    inputs = {
        "category": {
            "type": "string",
            "description": "The type of superhero party (e.g., 'classic heroes', 'villain masquerade', 'futuristic Gotham').",
        }
    }

    output_type = "string"

    def forward(self, category: str):
        themes = {
            "classic heroes": "Justice League Gala: Guests come dressed as their favorite DC heroes with themed cocktails like 'The Kryptonite Punch'.",
            "villain masquerade": "Gotham Rogues' Ball: A mysterious masquerade where guests dress as classic Batman villains.",
            "futuristic Gotham": "Neo-Gotham Night: A cyberpunk-style party inspired by Batman Beyond, with neon decorations and futuristic gadgets."
        }

        return themes.get(category.lower(), "Themed party idea not found. Try 'classic heroes', 'villain masquerade', or 'futuristic Gotham'.")

# Instantiate the tool
party_theme_tool = SuperheroPartyThemeTool()

# ---- AGENT ----
agent = CodeAgent(
    tools = [
        WebSearchTool(), # Music Web Search
        suggest_menu,
    ],
    model = InferenceClientModel(
        token = HF_TOKEN
    ),
    additional_authorized_imports = ["datetime"], #time calc
    max_steps = 6
)

agent2 = ToolCallingAgent(tools=[WebSearchTool(),catering_service_tool,
party_theme_tool], model=InferenceClientModel( model_id="meta-llama/Llama-3.1-70B-Instruct",token = HF_TOKEN),
max_steps = 6
)

# ---- RUN ----
# result = agent.run("""
# Plan a party at Wayne's mansion:

# 1. Suggest a formal menu
# 2. Find a good music playlist for the party
# 3. Calculate total preparation time:
#     - drinks: 30 min
#     - decoration: 60 min
#     - menu: 45 min
#     - music: 45 min
# 4. If we start right now, at what time will the party be ready?

# IMPORTANT:
# - Do NOT print anything
# - Do NOT explain
# - Return ONLY valid JSON

# Format:
# {
#   "menu": "...",
#   "playlist": "...",
#   "total_time": 0,
#   "ready_at": "HH:MM"
# }
# """)

# print(result)

# result2 = agent2.run("Search for the best music recommendations for a party at the Wayne's mansion.")

# print(result2)

# Run the agent to find the best catering service
# result3 = agent.run(
#     "Can you give me the name of the highest-rated catering service in Gotham City?"
# )
# print(result3) # Output: Gotham Catering Co.

result4 = agent.run(
    "What would be a good superhero party idea for a 'villain masquerade' theme?"
)
print(result4)