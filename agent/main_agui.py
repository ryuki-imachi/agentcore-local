"""
AgentCore Local - AG-UI Protocol Compatible Backend
Strands Agent with AG-UI Integration
"""
import os
from ag_ui_strands import StrandsAgent, create_strands_app
from strands import Agent
from strands.models.ollama import OllamaModel
from strands_tools import current_time

# 環境変数
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3:8b")

# Initialize Ollama model
ollama_model = OllamaModel(
    host=OLLAMA_HOST,
    model_id=OLLAMA_MODEL,
)

system_prompt = """あなたは親切で知識豊富なAIアシスタントです。
ユーザーの質問に日本語で丁寧に答えてください。
現在の日時を聞かれた場合は、current_timeツールを使用して正確な時刻を取得してください。
回答は簡潔かつ分かりやすくしてください。"""

# Create Strands agent with tools
strands_agent = Agent(
    model=ollama_model,
    tools=[current_time],
    system_prompt=system_prompt,
)

# Wrap with AG-UI integration
agui_agent = StrandsAgent(
    agent=strands_agent,
    name="strands_agent",
    description="A helpful assistant powered by Strands and Ollama",
)

# Create the FastAPI app with AG-UI protocol support
agent_path = os.getenv("AGENT_PATH", "/invocations")
app = create_strands_app(agui_agent, agent_path)

# Add health check endpoints
@app.get("/ping")
async def ping():
    """AG-UI Protocol - Health Check"""
    return {"status": "ok", "model": OLLAMA_MODEL}

@app.get("/health")
async def health():
    """Legacy health check endpoint"""
    return {"status": "healthy", "model": OLLAMA_MODEL}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("AGENT_PORT", 8000))
    uvicorn.run("main_agui:app", host="0.0.0.0", port=port, reload=True)
