"""Mimo2API Python版本 - 主程序入口"""

import os
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from app.routes import router
from app.config import config_manager

# 创建FastAPI应用
app = FastAPI(
    title="Mimo2API",
    description="将小米 Mimo AI 转换为 OpenAI 兼容 API",
    version="1.0.0"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由（API 路由，无认证）
app.include_router(router)

# 静态文件目录
web_dir = Path(__file__).parent / "web"

# ---------- 添加 Basic Auth 保护管理界面 ----------
# 从环境变量读取认证信息，若未设置则使用默认值（建议生产环境必须设置）
AUTH_USER = os.environ.get("MIMO_AUTH_USER", "admin")
AUTH_PASS = os.environ.get("MIMO_AUTH_PASS", "your-strong-password")

# 创建 HTTP Basic 安全方案实例
security = HTTPBasic()

def verify_auth(credentials: HTTPBasicCredentials = Depends(security)):
    """验证 HTTP Basic 认证凭据"""
    correct_username = AUTH_USER
    correct_password = AUTH_PASS
    if credentials.username != correct_username or credentials.password != correct_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials

# 修改根路由，添加认证依赖
@app.get("/")
async def serve_admin(credentials: HTTPBasicCredentials = Depends(verify_auth)):
    """提供管理界面（需要 Basic Auth 认证）"""
    index_file = web_dir / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {"message": "Admin interface not found"}

# ---------- 其余路由无需改动 ----------

def main():
    """主函数"""
    # 获取端口配置
    port = int(os.getenv("PORT", "8080"))

    print(f"""
╔══════════════════════════════════════════════════════════╗
║                    Mimo2API Python                       ║
║          将小米 Mimo AI 转换为 OpenAI 兼容 API           ║
╚══════════════════════════════════════════════════════════╝

🚀 服务器启动中...
📍 地址: http://localhost:{port}
📊 管理界面: http://localhost:{port} (需要 Basic Auth)
📡 API端点: http://localhost:{port}/v1/chat/completions (无需认证)
📖 API文档: http://localhost:{port}/docs (无需认证)

配置信息:
  - API Keys: {len(config_manager.config.api_keys.split(','))} 个
  - Mimo账号: {len(config_manager.config.mimo_accounts)} 个

按 Ctrl+C 停止服务器
""")

    # 启动服务器
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )

if __name__ == "__main__":
    main()
