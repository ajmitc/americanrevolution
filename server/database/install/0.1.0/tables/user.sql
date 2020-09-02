-- Generic User Account
-- Does not hold any game data
CREATE TABLE IF NOT EXISTS user_account(
    id TEXT PRIMARY KEY,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    name TEXT,
    access_token TEXT,
    access_token_expiration TEXT,
    last_login TEXT,
    created_at TEXT
);

-- User Preferences
CREATE TABLE IF NOT EXISTS user_prefs(
    userid TEXT PRIMARY KEY,
    email TEXT,
    FOREIGN KEY (userid) REFERENCES user_account(id)
);
