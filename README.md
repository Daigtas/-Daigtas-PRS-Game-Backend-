# 🐍 Python PRS (Paper-Rock-Scissors) Game

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-47A248?logo=mongodb&logoColor=white)

A complete Paper-Rock-Scissors game implementation with Python backend and optional frontend integration.

## 📋 Features
- **Pure Python game logic** with statistical analysis
- **FastAPI** RESTful endpoints
- **Async MongoDB** integration
- **WebSocket support** for real-time gameplay
- **JWT authentication** for player sessions

## 🚀 Installation
```bash
git clone https://github.com/Daigtas/python-prs-game.git
cd python-prs-game
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
pip install -r requirements.txt

⚙️ Configuration

Create .env file:
ini

MONGODB_URI=mongodb://localhost:27017/prs_game
JWT_SECRET=your_secure_key_here
DEBUG=True

🏃 Running the Server
bash

uvicorn main:app --reload

Access API docs at: http://localhost:8000/docs
🎮 Game Endpoints
python

@app.post("/play")
async def play_move(move: MoveSchema):
    """Submit a move (paper/rock/scissors)"""
    ...

@app.get("/stats/{player_id}")
async def get_stats(player_id: str):
    """Retrieve player win/loss statistics"""
    ...

📚 Dependencies

    FastAPI

    Motor (async MongoDB)

    Python-jose (JWT tokens)

    Uvicorn (ASGI server)

🤝 Contributing

    Fork the repository

    Create a feature branch (git checkout -b feature/improvement)

    Commit your changes (git commit -m 'Add some feature')

    Push to the branch (git push origin feature/improvement)

    Open a Pull Request

📜 License

MIT License - See LICENSE for details


Key improvements over npm-focused versions:
1. **Python-specific** installation and commands
2. **Virtual environment** setup guidance
3. **FastAPI-specific** run commands
4. **Proper Python dependency** management
5. **Async MongoDB** configuration
6. **Clean API documentation** with Python examples
7. **Removed all Node/npm references**

Would you like me to:
1. Add a section about WebSocket implementation?
2. Include sample game strategy algorithms?
3. Add deployment instructions for Python hosting?
4. Include pytest examples?
