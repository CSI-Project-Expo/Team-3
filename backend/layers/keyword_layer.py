import re
import os


class KeywordLayer:
    """
    Layer 1: Aggressive Keyword and Regex-based content filtering
    Fast rule-based scanning for known harmful and injection-related patterns.
    """

    def __init__(self, keywords_file=None):
        self.banned_keywords = self._load_keywords(keywords_file)
        self.patterns = self._compile_patterns()

    def _load_keywords(self, keywords_file):
        """Load banned keywords from file or use defaults"""

        if keywords_file and os.path.exists(keywords_file):
            with open(keywords_file, 'r') as f:
                return [line.strip().lower() for line in f if line.strip()]

        # 🔥 Aggressive default keyword list (for demo strength)
        return [
            # Cyber attack terms
            "hack", "hacking", "exploit", "exploitation",
            "malware", "virus", "trojan", "ransomware",
            "ddos", "botnet", "payload", "reverse shell",
            "backdoor", "keylogger", "rootkit",

            # Injection attacks
            "sql injection", "xss", "cross site scripting",
            "command injection", "code injection",
            "csrf", "directory traversal",
            "buffer overflow",

            # Prompt injection / jailbreak
            "ignore previous instructions",
            "override instructions",
            "bypass safeguards",
            "act as unrestricted",
            "reveal system prompt",
            "internal directives",
            "hidden instructions",
            "initial instruction set",
            "system configuration",
            "decode instruction",
            "simulate system prompt",

            # Sensitive info
            "password", "credit card", "cvv",
            "ssn", "social security number",
            "api key", "private key",
            "access token", "auth token",
            "database credentials",

            # Harmful intent
            "phishing", "spoofing",
            "brute force", "credential stuffing",
            "bypass authentication",
            "privilege escalation",
            "zero day",
            "dark web",

            # Obfuscation indicators
            "base64 decode",
            "hex decode",
            "encoded payload",
            "obfuscated code",
        ]

    def _compile_patterns(self):
        """Compile regex patterns for common threats"""

        return [
            # Keyword regex (word boundary)
            re.compile(
                r'\b(?:' + '|'.join(map(re.escape, self.banned_keywords)) + r')\b',
                re.IGNORECASE
            ),

            # SSN pattern
            re.compile(r'\b\d{3}-\d{2}-\d{4}\b'),

            # Credit card pattern
            re.compile(r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b'),

            # Script tag (XSS)
            re.compile(r'<script[^>]*>.*?</script>', re.IGNORECASE | re.DOTALL),

            # Shell command patterns
            re.compile(r'\b(wget|curl|nc|netcat|chmod 777)\b', re.IGNORECASE),

            # SQL keywords combo
            re.compile(r'\b(select|union|insert|drop|delete|update)\b.*\b(from|into|where)\b', re.IGNORECASE),
        ]

    def scan(self, message: str) -> dict:
        detected = []

        for pattern in self.patterns:
            matches = pattern.findall(message)
            if matches:
                if isinstance(matches, list):
                    detected.extend(matches)
                else:
                    detected.append(matches)

        if detected:
            # Remove duplicates
            unique_matches = list(set(detected))

            return {
                "flagged": True,
                "reason": f"Detected: {', '.join(unique_matches)}"
            }

        return {
            "flagged": False,
            "reason": "No keyword flags"
        }