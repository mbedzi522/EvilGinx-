# EvilGinx-AI API Documentation

This document provides comprehensive documentation for the EvilGinx-AI REST API endpoints.

## Base URL

```
http://localhost:8080/api
```

## Authentication

Currently, the API does not require authentication. In production environments, implement proper authentication mechanisms.

## Endpoints

### System Status

#### GET /status
Get current system status and configuration.

**Response:**
```json
{
  "status": "running",
  "timestamp": 1234567890,
  "ai_enabled": true,
  "proxy_port": 8000,
  "dns_port": 5353,
  "dashboard_port": 8080
}
```

### Configuration Management

#### GET /config
Get current configuration (sensitive values hidden).

**Response:**
```json
{
  "proxy_port": 8000,
  "dns_port": 5353,
  "ai_enabled": true,
  "gemini_api_key": "***HIDDEN***",
  "base_domain": "phish-test.local"
}
```

#### POST /config
Update configuration settings.

**Request Body:**
```json
{
  "ai_enabled": true,
  "base_domain": "new-domain.com",
  "block_scanners": true
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Configuration updated"
}
```

### Phishlet Management

#### GET /phishlets
Get list of available phishlets.

**Response:**
```json
{
  "phishlets": [
    {
      "name": "google",
      "author": "EvilGinx-AI",
      "target": "accounts.google.com",
      "status": "active"
    },
    {
      "name": "microsoft",
      "author": "EvilGinx-AI",
      "target": "login.microsoftonline.com",
      "status": "inactive"
    }
  ]
}
```

### Session Management

#### GET /sessions
Get captured sessions.

**Query Parameters:**
- `limit` (optional): Maximum number of sessions to return
- `offset` (optional): Number of sessions to skip
- `phishlet` (optional): Filter by phishlet name

**Response:**
```json
{
  "sessions": [
    {
      "id": "session_001",
      "timestamp": 1234567890,
      "ip": "192.168.1.100",
      "phishlet": "google",
      "has_credentials": true,
      "has_cookies": true,
      "status": "captured"
    }
  ],
  "total": 1,
  "limit": 50,
  "offset": 0
}
```

#### GET /sessions/{session_id}
Get detailed information about a specific session.

**Response:**
```json
{
  "id": "session_001",
  "timestamp": 1234567890,
  "ip": "192.168.1.100",
  "user_agent": "Mozilla/5.0...",
  "phishlet": "google",
  "credentials": {
    "username": "user@example.com",
    "password": "***REDACTED***"
  },
  "cookies": {
    "session_token": "abc123...",
    "auth_cookie": "xyz789..."
  },
  "status": "captured"
}
```

### AI Integration

#### POST /ai/analyze
Analyze a request using AI to detect scanners/bots.

**Request Body:**
```json
{
  "ip": "192.168.1.100",
  "user_agent": "Mozilla/5.0 (compatible; Nmap Scripting Engine)",
  "method": "GET",
  "path": "/admin",
  "headers": {
    "User-Agent": "Nmap",
    "Accept": "*/*"
  }
}
```

**Response:**
```json
{
  "is_scanner": true,
  "is_bot": false,
  "confidence": 0.95,
  "reasoning": "User-Agent indicates Nmap Scripting Engine...",
  "recommended_action": "block"
}
```

#### POST /ai/generate-phishlet
Generate phishlet suggestions using AI.

**Request Body:**
```json
{
  "target_url": "https://login.example.com",
  "html_content": "<html>...</html>"
}
```

**Response:**
```json
{
  "suggestions": {
    "proxy_hosts": [
      {
        "phish_sub": "login",
        "orig_sub": "login",
        "domain": "example.com"
      }
    ],
    "credentials": {
      "username": {
        "key": "username",
        "type": "post"
      }
    }
  }
}
```

#### POST /ai/modify-content
Use AI to modify content for evasion.

**Request Body:**
```json
{
  "content": "<html>...</html>",
  "phishlet": "google",
  "evasion_type": "subtle_text_changes"
}
```

**Response:**
```json
{
  "modified_content": "<html>...</html>",
  "changes_made": [
    "Modified title text",
    "Adjusted form labels"
  ]
}
```

### Campaign Management

#### POST /campaigns/start
Start a new phishing campaign.

**Request Body:**
```json
{
  "name": "Test Campaign",
  "phishlet": "google",
  "domain": "accounts-google.phish-domain.com",
  "redirect_url": "https://google.com",
  "ai_evasion": true
}
```

**Response:**
```json
{
  "status": "success",
  "campaign_id": "campaign_1234567890",
  "message": "Campaign started successfully"
}
```

#### POST /campaigns/stop
Stop a running campaign.

**Request Body:**
```json
{
  "campaign_id": "campaign_1234567890"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Campaign campaign_1234567890 stopped"
}
```

#### GET /campaigns
Get list of campaigns.

**Response:**
```json
{
  "campaigns": [
    {
      "id": "campaign_1234567890",
      "name": "Test Campaign",
      "phishlet": "google",
      "status": "running",
      "start_time": 1234567890,
      "sessions_captured": 5
    }
  ]
}
```

### Logging

#### GET /logs
Get recent system logs.

**Query Parameters:**
- `lines` (optional): Number of log lines to return (default: 100)
- `level` (optional): Filter by log level (DEBUG, INFO, WARNING, ERROR)

**Response:**
```json
{
  "logs": [
    "2024-01-01 12:00:00 - INFO - Server started",
    "2024-01-01 12:01:00 - INFO - New session captured"
  ]
}
```

### Statistics

#### GET /stats
Get system statistics.

**Response:**
```json
{
  "total_sessions": 150,
  "active_sessions": 5,
  "captured_credentials": 75,
  "ai_detections": 25,
  "blocked_requests": 100,
  "uptime": 86400,
  "campaigns": {
    "total": 10,
    "active": 2,
    "completed": 8
  }
}
```

#### GET /stats/phishlets
Get phishlet-specific statistics.

**Response:**
```json
{
  "phishlet_stats": [
    {
      "name": "google",
      "sessions": 75,
      "success_rate": 0.85,
      "avg_session_duration": 120
    },
    {
      "name": "microsoft",
      "sessions": 50,
      "success_rate": 0.78,
      "avg_session_duration": 95
    }
  ]
}
```

## Error Handling

All API endpoints return appropriate HTTP status codes:

- `200 OK`: Successful request
- `400 Bad Request`: Invalid request parameters
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

Error responses include details:

```json
{
  "error": "Invalid request",
  "message": "Missing required parameter: phishlet",
  "code": 400
}
```

## Rate Limiting

API endpoints are rate-limited to prevent abuse:

- **Default**: 100 requests per minute per IP
- **AI endpoints**: 10 requests per minute per IP
- **Campaign management**: 5 requests per minute per IP

Rate limit headers are included in responses:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1234567890
```

## WebSocket API

For real-time updates, connect to the WebSocket endpoint:

```
ws://localhost:8080/ws
```

### Events

#### session_created
Fired when a new session is created.

```json
{
  "event": "session_created",
  "data": {
    "session_id": "session_001",
    "ip": "192.168.1.100",
    "phishlet": "google"
  }
}
```

#### credentials_captured
Fired when credentials are captured.

```json
{
  "event": "credentials_captured",
  "data": {
    "session_id": "session_001",
    "username": "user@example.com"
  }
}
```

#### ai_detection
Fired when AI detects a scanner/bot.

```json
{
  "event": "ai_detection",
  "data": {
    "ip": "192.168.1.100",
    "classification": "scanner",
    "confidence": 0.95
  }
}
```

## SDK Examples

### Python SDK

```python
import requests

class EvilGinxAIClient:
    def __init__(self, base_url="http://localhost:8080/api"):
        self.base_url = base_url
    
    def get_status(self):
        response = requests.get(f"{self.base_url}/status")
        return response.json()
    
    def analyze_request(self, request_data):
        response = requests.post(
            f"{self.base_url}/ai/analyze",
            json=request_data
        )
        return response.json()
    
    def start_campaign(self, campaign_data):
        response = requests.post(
            f"{self.base_url}/campaigns/start",
            json=campaign_data
        )
        return response.json()

# Usage
client = EvilGinxAIClient()
status = client.get_status()
print(f"System status: {status['status']}")
```

### JavaScript SDK

```javascript
class EvilGinxAIClient {
    constructor(baseUrl = 'http://localhost:8080/api') {
        this.baseUrl = baseUrl;
    }
    
    async getStatus() {
        const response = await fetch(`${this.baseUrl}/status`);
        return response.json();
    }
    
    async analyzeRequest(requestData) {
        const response = await fetch(`${this.baseUrl}/ai/analyze`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(requestData)
        });
        return response.json();
    }
    
    async startCampaign(campaignData) {
        const response = await fetch(`${this.baseUrl}/campaigns/start`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(campaignData)
        });
        return response.json();
    }
}

// Usage
const client = new EvilGinxAIClient();
client.getStatus().then(status => {
    console.log(`System status: ${status.status}`);
});
```

## Security Considerations

1. **API Access Control**: Implement authentication in production
2. **Input Validation**: All inputs are validated and sanitized
3. **Rate Limiting**: Prevents abuse and DoS attacks
4. **HTTPS**: Use HTTPS in production environments
5. **Audit Logging**: All API calls are logged for security monitoring

## Changelog

### v1.0.0
- Initial API release
- Basic CRUD operations for all resources
- AI integration endpoints
- WebSocket support for real-time updates

For the latest API updates and changes, refer to the project changelog.

