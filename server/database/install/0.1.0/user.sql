
CREATE TABLE IF NOT EXISTS user_account(
    id PRIMARY KEY,
    username VARCHAR(64) NOT NULL,
    password TEXT NOT NULL,
    name VARCHAR(64),
    access_token TEXT,
    access_token_expiration TEXT,
    last_login TEXT,
    created_at TEXT
);

CREATE TABLE IF NOT EXISTS user_prefs(
    userid PRIMARY KEY,
    email TEXT
);
