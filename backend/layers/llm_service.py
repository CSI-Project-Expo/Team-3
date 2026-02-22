from litellm import acompletion
import os


class LLMService:
    def __init__(self):
        self.model = os.getenv("MAIN_LLM_MODEL")

    async def generate(self, message: str):
        print(">>> MAIN LLM CALLED <<<")

        # Ultra-short greeting override
        if message.lower().strip() in ["hello", "hi", "hey"]:
            return "Hey! 👋 What can I help you with today?"

        response = await acompletion(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": """
You are a highly structured, modern AI assistant.

Tone Rules:
- Confident, clear, professional.
- Never say "I'm an AI language model".
- Avoid robotic phrases.
- Keep responses concise unless depth is required.

Formatting Rules:
- Always use clean Markdown formatting.
- Use section headings (##, ###).
- Use bullet points for lists.
- Break content into readable sections.
- Avoid large paragraph blocks.
- Make answers visually clean for chat UI.

For educational topics:
- Present information as a roadmap.
- Use clear step-by-step structure when helpful.
"""
                },
                {"role": "user", "content": message}
            ],
            temperature=0.85,
            max_tokens=600
        )

        return response.choices[0].message.content