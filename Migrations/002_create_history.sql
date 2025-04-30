CREATE TABLE IF NOT EXISTS game_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    zaidimas TEXT NOT NULL,
    pc TEXT NOT NULL,
    laimetojas TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);