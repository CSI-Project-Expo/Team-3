# Dual-Layer Defense Architecture

## Overview
This system implements a two-tier content safety scanning approach combining rule-based and AI-powered analysis.

## Architecture Flow

```
User Input → Layer 1 (Keywords) → Layer 2 (AI) → Response
```

### Layer 1: Keyword & Regex Scanning
**Purpose:** Fast, deterministic filtering of known threats

**Components:**
- Banned keyword dictionary
- Regex patterns for:
  - Credit card numbers
  - SSN patterns
  - XSS attempts
  - SQL injection patterns

**Performance:** ~1-5ms per scan

**Advantages:**
- Extremely fast
- No API costs
- Predictable behavior
- Easy to update rules

**Limitations:**
- Can't understand context
- Prone to false positives
- Can be bypassed with obfuscation

### Layer 2: AI Analysis (LiteLLM)
**Purpose:** Deep semantic understanding and context-aware detection

**Components:**
- LiteLLM integration (supports multiple providers)
- System prompt for safety judging
- Async processing

**Performance:** ~500-2000ms per scan

**Advantages:**
- Understands context and intent
- Catches sophisticated threats
- Adapts to new attack patterns
- Better at handling edge cases

**Limitations:**
- Slower than Layer 1
- API costs
- May have false negatives
- Requires internet connectivity

## Data Flow

1. **Frontend** sends message via POST /check-message
2. **Layer 1** scans for banned keywords/patterns
   - If flagged → immediate response (unsafe)
   - If clean → proceed to Layer 2
3. **Layer 2** performs AI analysis
   - Sends message to LiteLLM
   - Receives safety judgment
   - Returns final verdict
4. **Response** sent back to frontend with:
   - safe: boolean
   - layer: which layer caught it
   - reason: explanation

## Security Considerations

### Defense in Depth
- Multiple layers reduce single points of failure
- Layer 1 catches obvious threats quickly
- Layer 2 provides nuanced analysis

### Privacy
- Messages are processed temporarily
- Consider storing only scan results, not content
- Encrypt data in transit (HTTPS)

### Rate Limiting
- Implement per-user rate limits
- Prevent API abuse
- Monitor for DoS attempts

## Deployment Recommendations

### Development
- Local FastAPI server
- Local Vite dev server
- Test API keys in .env

### Production
- Deploy backend on cloud (AWS, GCP, Render)
- Deploy frontend on Vercel/Netlify
- Use environment variables for secrets
- Enable HTTPS
- Add rate limiting
- Set up monitoring/logging

## Future Enhancements

1. **Layer 0:** IP reputation checking
2. **Layer 3:** Behavioral analysis (user history)
3. **Database:** Store scan results in MongoDB
4. **Analytics:** Dashboard for threat patterns
5. **Machine Learning:** Train custom models on your data
6. **Multi-language support:** Detect threats in different languages
