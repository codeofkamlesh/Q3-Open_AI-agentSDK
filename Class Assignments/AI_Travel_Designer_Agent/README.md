# AI Travel Designer

## 🎯 Purpose
This agent helps users plan travel based on their interests, such as adventure, relaxation, or low budget. It also gives a packing list based on the destination.

## 🧠 How It Works
1. The user types their travel interest (e.g., "I want a budget trip").
2. The agent suggests a destination using a tool.
3. When the user confirms a location, it automatically hands off to the packing tool.

## 🛠️ Tools Used
- `get_travel_plan(user_interest: str)`: Suggests a suitable destination.
- `get_packing_list(destination: str)`: Suggests what to pack based on the selected destination.

## 🤖 Agent
- `TravelAgent`: Handles both travel suggestion and packing list logic using tools.

## 🔁 Handoff Logic
User’s interest → travel suggestion → user confirms destination → packing list is generated automatically.
