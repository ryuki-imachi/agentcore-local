"""
AgentCore Local - Strands Agent with FastAPI
"""
import os
import json
import asyncio
from datetime import datetime
from typing import Optional
from contextlib import asynccontextmanager

import aiosqlite
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from strands import Agent
from strands.models.ollama import OllamaModel
from strands_tools import current_time

# 環境変数
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3:8b")
DB_PATH = "/app/data/conversations.db"

# グローバル変数
db: Optional[aiosqlite.Connection] = None
agent: Optional[Agent] = None


# Pydanticモデル
class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    timestamp: str


class Conversation(BaseModel):
    id: str
    title: str
    created_at: str
    updated_at: str


class ConversationDetail(BaseModel):
    id: str
    title: str
    messages: list[dict]
    created_at: str
    updated_at: str


# データベース初期化
async def init_db():
    global db
    db = await aiosqlite.connect(DB_PATH)
    await db.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)
    await db.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (conversation_id) REFERENCES conversations(id)
        )
    """)
    await db.commit()


# Agent初期化
def init_agent():
    global agent
    
    ollama_model = OllamaModel(
        host=OLLAMA_HOST,
        model_id=OLLAMA_MODEL,
    )
    
    system_prompt = """あなたは親切で知識豊富なAIアシスタントです。
ユーザーの質問に日本語で丁寧に答えてください。
現在の日時を聞かれた場合は、current_timeツールを使用して正確な時刻を取得してください。
回答は簡潔かつ分かりやすくしてください。"""
    
    agent = Agent(
        model=ollama_model,
        tools=[current_time],
        system_prompt=system_prompt,
    )


# ライフスパン管理
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 起動時
    await init_db()
    init_agent()
    yield
    # 終了時
    if db:
        await db.close()


# FastAPIアプリ
app = FastAPI(
    title="AgentCore Local",
    description="Local AgentCore Runtime with Strands Agent",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ヘルパー関数
def generate_conversation_id() -> str:
    return datetime.now().strftime("%Y%m%d%H%M%S%f")


async def get_conversation_messages(conversation_id: str) -> list[dict]:
    async with db.execute(
        "SELECT role, content FROM messages WHERE conversation_id = ? ORDER BY id",
        (conversation_id,)
    ) as cursor:
        rows = await cursor.fetchall()
        return [{"role": row[0], "content": row[1]} for row in rows]


async def save_message(conversation_id: str, role: str, content: str):
    timestamp = datetime.now().isoformat()
    await db.execute(
        "INSERT INTO messages (conversation_id, role, content, timestamp) VALUES (?, ?, ?, ?)",
        (conversation_id, role, content, timestamp)
    )
    await db.execute(
        "UPDATE conversations SET updated_at = ? WHERE id = ?",
        (timestamp, conversation_id)
    )
    await db.commit()


async def create_conversation(conversation_id: str, title: str):
    timestamp = datetime.now().isoformat()
    await db.execute(
        "INSERT INTO conversations (id, title, created_at, updated_at) VALUES (?, ?, ?, ?)",
        (conversation_id, title, timestamp, timestamp)
    )
    await db.commit()


# APIエンドポイント
@app.get("/health")
async def health_check():
    return {"status": "healthy", "model": OLLAMA_MODEL}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """チャットエンドポイント"""
    if not agent:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    
    # 会話IDの処理
    conversation_id = request.conversation_id
    is_new_conversation = False
    
    if not conversation_id:
        conversation_id = generate_conversation_id()
        is_new_conversation = True
    
    # 新規会話の作成
    if is_new_conversation:
        title = request.message[:50] + "..." if len(request.message) > 50 else request.message
        await create_conversation(conversation_id, title)
    
    # ユーザーメッセージを保存
    await save_message(conversation_id, "user", request.message)
    
    # 会話履歴を取得
    history = await get_conversation_messages(conversation_id)
    
    # コンテキストを構築
    context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history[:-1]])
    
    # Agentを実行（同期処理をスレッドプールで実行）
    try:
        prompt = request.message
        if context:
            prompt = f"これまでの会話:\n{context}\n\nユーザー: {request.message}"
        
        # Strands Agentは同期的なので、別スレッドで実行
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, lambda: agent(prompt))
        
        # レスポンスを文字列に変換
        response_text = str(result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")
    
    # アシスタントの応答を保存
    await save_message(conversation_id, "assistant", response_text)
    
    return ChatResponse(
        response=response_text,
        conversation_id=conversation_id,
        timestamp=datetime.now().isoformat(),
    )


@app.get("/conversations", response_model=list[Conversation])
async def list_conversations():
    """会話一覧を取得"""
    async with db.execute(
        "SELECT id, title, created_at, updated_at FROM conversations ORDER BY updated_at DESC"
    ) as cursor:
        rows = await cursor.fetchall()
        return [
            Conversation(
                id=row[0],
                title=row[1],
                created_at=row[2],
                updated_at=row[3],
            )
            for row in rows
        ]


@app.get("/conversations/{conversation_id}", response_model=ConversationDetail)
async def get_conversation(conversation_id: str):
    """特定の会話を取得"""
    async with db.execute(
        "SELECT id, title, created_at, updated_at FROM conversations WHERE id = ?",
        (conversation_id,)
    ) as cursor:
        row = await cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        messages = await get_conversation_messages(conversation_id)
        
        return ConversationDetail(
            id=row[0],
            title=row[1],
            messages=messages,
            created_at=row[2],
            updated_at=row[3],
        )


@app.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """会話を削除"""
    await db.execute("DELETE FROM messages WHERE conversation_id = ?", (conversation_id,))
    await db.execute("DELETE FROM conversations WHERE id = ?", (conversation_id,))
    await db.commit()
    return {"status": "deleted"}
