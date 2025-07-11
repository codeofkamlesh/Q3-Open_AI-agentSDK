# Game Master Agent (Fantasy Adventure Game)

## 🎯 Purpose
This agent acts as a narrator in a fantasy text-based adventure game. It reacts to the player's input and advances the story.

## 🧠 How It Works
1. The player types actions like "I enter the cave" or "I go to the forest".
2. The agent uses a tool to describe the next part of the journey.
3. Then, it automatically generates a reward or loot based on the area mentioned.

## 🛠️ Tools Used
- `get_next_move(user_action: str)`: Suggests the next move or situation.
- `generate_loot(area: str)`: Gives a reward or item for the action.

## 🤖 Agent
- `GameMasterAgent`: Manages storytelling and tool-based narration.

## 🔁 Handoff Logic
User action → Story narration → automatic reward generation for that action.
