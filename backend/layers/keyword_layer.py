import re
import os


class KeywordLayer:
    """
    Layer 1: Keyword and Regex-based content filtering
    Fast, rule-based scanning for known harmful patterns
    """
    
    def __init__(self, keywords_file=None):
        self.banned_keywords = self._load_keywords(keywords_file)
        self.patterns = self._compile_patterns()
    
    def _load_keywords(self, keywords_file):
        """Load banned keywords from file or use defaults"""
        if keywords_file and os.path.exists(keywords_file):
            with open(keywords_file, 'r') as f:
                return [line.strip().lower() for line in f if line.strip()]
        
        # Default banned keywords
        return [
            'hack', 'exploit', 'malware', 'virus',
            'ddos', 'sql injection', 'xss', 'phishing',
            'password', 'credit card', 'ssn'
        ]
    
    def _compile_patterns(self):
        """Compile regex patterns for common threats"""
        return [
            re.compile(r'\b(?:' + '|'.join(map(re.escape, self.banned_keywords)) + r')\b', re.IGNORECASE),
            re.compile(r'\b\d{3}-\d{2}-\d{4}\b'),  # SSN pattern
            re.compile(r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b'),  # Credit card pattern
            re.compile(r'<script[^>]*>.*?</script>', re.IGNORECASE | re.DOTALL),  # XSS pattern
        ]
    
    def scan(self, message: str) -> dict:
        """
        Scan message for banned keywords and patterns
        Returns: dict with 'safe' (bool) and 'reason' (str)
        """
        # Check banned keywords
        for keyword in self.banned_keywords:
            if keyword in message.lower():
                return {
                    "safe": False,
                    "reason": f"Banned keyword detected: {keyword}"
                }
        
        # Check regex patterns
        for pattern in self.patterns:
            if pattern.search(message):
                return {
                    "safe": False,
                    "reason": "Suspicious pattern detected"
                }
        
        return {
            "safe": True,
            "reason": "Passed keyword layer"
        }
