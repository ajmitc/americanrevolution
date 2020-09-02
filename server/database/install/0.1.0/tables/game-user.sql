-- This table defines the role of a user in a game
CREATE TABLE IF NOT EXISTS game_user(
    gameid TEXT,
    -- Must map to user::id
    userid TEXT,
    -- User's allegiance (England vs Colonist)
    allegiance TEXT NOT NULL,
    -- User's current rank (lieutenant, captain, colonel, general, etc)
    rank TEXT NOT NULL,
    -- Current location of user
    location_id TEXT,
    -- User's travel status (camp, moving, holding, etc)
    travel_status TEXT,
    -- User's commander
    commander_userid TEXT,
    -- User's assigned role
    -- It may be a political office, etc
    role TEXT DEFAULT NULL,

    PRIMARY KEY (gameid, userid),
    FOREIGN KEY (gameid) REFERENCES game(id),
    FOREIGN KEY (userid) REFERENCES user_account(id)
);

