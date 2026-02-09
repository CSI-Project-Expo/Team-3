import os
from litellm import acompletion


class AILayer:
    """
    Layer 2: AI-based content analysis using LiteLLM
    Deep semantic understanding for complex threats
    """
    
    def __init__(self):
        self.model = os.getenv("LITELLM_MODEL", "gpt-3.5-turbo")
        self.system_prompt = """You are a content safety judge. Analyze the given message for:
- Harmful intent (threats, harassment, hate speech)
- Security risks (phishing attempts, social engineering)
- Privacy violations (personal information sharing)
- Manipulation attempts

Respond with ONLY 'SAFE' or 'UNSAFE: <brief reason>'."""
    
    async def analyze(self, message: str) -> dict:
        """
        Analyze message using AI model
        Returns: dict with 'safe' (bool) and 'reason' (str)
        """
        try:
            response = await acompletion(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": message}
                ],
                temperature=0.3,
                max_tokens=100
            )
            
            result = response.choices[0].message.content.strip()
            
            if result.upper().startswith("SAFE"):
                return {
                    "safe": True,
                    "reason": "Passed AI analysis"
                }
            elif result.upper().startswith("UNSAFE"):
                reason = result.split(":", 1)[1].strip() if ":" in result else "AI flagged as unsafe"
                return {
                    "safe": False,
                    "reason": reason
                }
            else:
                # Fallback: assume safe if unclear
                return {
                    "safe": True,
                    "reason": "AI analysis inconclusive, defaulting to safe"
                }
        
        except Exception as e:
            # In production, you might want to fail closed (assume unsafe)
            # For development, we'll log and pass
            print(f"AI Layer Error: {str(e)}")
            return {
                "safe": True,
                "reason": f"AI layer unavailable: {str(e)}"
            }
