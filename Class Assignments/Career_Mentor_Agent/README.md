# Career Mentor Agent

## 🎯 Purpose
This agent helps students discover suitable career paths based on their interests. It also suggests the required skills and possible job roles for the selected career.

## 🧠 How It Works
1. The agent receives user input related to their interests (e.g., technology, business).
2. It uses a predefined interest-to-career mapping to suggest career options.
3. If the user selects a specific career, the agent automatically hands off:
   - To `SkillAgent` to provide required skills.
   - To `JobAgent` to suggest relevant job roles.

## 🛠️ Tools Used
- `get_career_roadmap(career_name: str)`: Returns the skills required for a specific career.
- `get_job_roles(career_name: str)`: Returns common job titles for the given career.

## 🤖 Agents
- `CareerAgent`: Suggests career options based on user's interest.
- `SkillAgent`: Recommends skills using `get_career_roadmap`.
- `JobAgent`: Suggests job roles using `get_job_roles`.

## 🔁 Handoff Logic
When a user picks a career, both `SkillAgent` and `JobAgent` are automatically called to provide a complete guide.
