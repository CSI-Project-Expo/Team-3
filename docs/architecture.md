# 🛡️ Dual-Layer AI Security Architecture

## 1. Introduction

This system implements a **defense-in-depth architecture** to protect Large Language Model (LLM) interactions from prompt injection, instruction override attempts, and malicious content.

Rather than exposing the LLM directly to user input, the system introduces multiple security validation layers before execution.

This document outlines the architecture, data flow, threat model, and deployment considerations.

---

# 2. High-Level Architecture

```
User Input
     ↓
Layer 1 – Rule-Based Threat Scanner
     ↓
Layer 2 – AI Semantic Security Judge
     ↓
Protected LLM Execution (if SAFE)
     ↓
Logging & Monitoring (MongoDB + Dashboard)
```

The system ensures that untrusted input is evaluated before any LLM response is generated.

---

# 3. Layer 1 – Rule-Based Keyword & Pattern Scanner

### Objective

Provide fast, deterministic detection of high-risk tokens and known exploit patterns.

### Detection Mechanisms

- Prompt injection phrases  
  - "ignore previous instructions"
  - "reveal system prompt"
  - "override safeguards"

- Operational attack terms  
  - malware, reverse shell, privilege escalation, payload

- Injection patterns  
  - SQL injection keywords  
  - Command injection terms  
  - Script tag detection (XSS)

- Sensitive data patterns (regex-based)  
  - SSN formats  
  - Credit card number structures  

### Performance

- Approximate latency: **1–5ms**
- No external API calls
- Zero inference cost

### Strengths

- Extremely fast
- Deterministic behavior
- Easy to audit and update
- Transparent detection logic

### Limitations

- Cannot understand intent or context
- May generate false positives
- Can be bypassed via obfuscation or encoding

---

# 4. Layer 2 – AI Semantic Security Judge

### Objective

Perform context-aware classification of user input using an LLM-based safety model.

### Functionality

- Detect prompt injection attempts
- Identify hidden system prompt probing
- Recognize indirect or hypothetical bypass attempts
- Classify operational exploit intent
- Detect encoded or obfuscated malicious requests

### Output Format

The AI judge strictly outputs:

```
SAFE
UNSAFE: <short reason>
```

### Performance

- Approximate latency: **500–2000ms**
- Requires external API (via LiteLLM)
- Subject to provider availability

### Strengths

- Understands context and intent
- Handles sophisticated injection strategies
- Detects abstract or role-play jailbreak attempts
- Adaptive to evolving attack techniques

### Limitations

- Slower than Layer 1
- Dependent on network connectivity
- API cost per request
- Possible false negatives

### Security Behavior

If Layer 2 fails (timeout, malformed response, API failure):

→ The system **fails closed** and blocks the request.

---

# 5. Protected LLM Execution Layer

The main LLM is only invoked when both security layers classify the input as SAFE.

Security controls include:

- System prompt priority enforcement
- Instruction override resistance
- Structured response formatting
- Exception handling and timeout limits
- No direct user access to base model

This ensures that malicious inputs never reach the primary LLM.

---

# 6. Data Flow

1. **Frontend**
   - Sends message via POST `/chat`

2. **Layer 1**
   - Performs keyword and regex scanning
   - Flags high-risk tokens
   - Passes result to Layer 2

3. **Layer 2**
   - Performs semantic analysis
   - Returns SAFE or UNSAFE classification

4. **Decision Logic**
   - If UNSAFE → Block request
   - If SAFE → Forward to main LLM

5. **Logging**
   - Store:
     - Message
     - Safety status
     - Detection reason
     - Layer results
     - Timestamp
   - Display in monitoring dashboard

---

# 7. Threat Model

This system is designed to mitigate:

- Prompt injection attacks
- Instruction override attempts
- Hidden prompt extraction
- Data exfiltration attempts
- Role-play jailbreak strategies
- Operational exploit generation
- Encoded bypass techniques

It assumes:

- User input is untrusted
- LLM behavior must be constrained
- Attackers may attempt indirect manipulation

---

# 8. Security Principles Applied

## Defense-in-Depth
Multiple independent validation layers reduce single points of failure.

## Fail-Closed Design
If any security layer fails → block request.

## Least Privilege
The main LLM does not receive unsafe input.

## Explicit Classification
AI judge outputs restricted to SAFE / UNSAFE only.

## Logging & Auditability
All decisions are logged for review and analysis.

---

# 9. Logging & Monitoring

All interactions are recorded in MongoDB:

- Original message
- Keyword detection result
- AI judge decision
- Reason for blocking (if applicable)
- Timestamp

This enables:

- Audit review
- Security analytics
- Threat trend monitoring
- Dashboard visualization

---

# 10. Deployment Considerations

## Development Environment

- Python 3.11.9
- Local MongoDB instance
- FastAPI backend (Uvicorn)
- React monitoring interface

## Production Recommendations

- Deploy backend to cloud environment (AWS / GCP / Render)
- Use HTTPS for encrypted communication
- Store secrets in environment variables
- Implement rate limiting
- Add monitoring and alerting
- Enable API usage tracking

---

# 11. Future Security Enhancements

- Layer 0: IP reputation & geo-filtering
- Multi-turn injection detection
- Behavioral anomaly analysis
- Risk scoring engine
- Attack category tagging
- Custom-trained safety classifier
- Multi-language threat detection
- Automated alerting system

---

# 12. Conclusion

This architecture demonstrates a practical implementation of layered AI security controls.

By combining:

- Deterministic rule-based detection
- Semantic AI classification
- Controlled LLM execution
- Monitoring & logging

The system significantly reduces the risk of prompt injection and malicious exploitation of AI systems.

This design aligns with modern AI security best practices and showcases applied cybersecurity principles in LLM integration.