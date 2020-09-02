
CREATE TABLE location (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    x REAL NOT NULL,
    y REAL NOT NULL
);

CREATE TABLE location_tag(
    id TEXT PRIMARY KEY,
    location_id TEXT NOT NULL,
    tag TEXT NOT NULL,
    FOREIGN KEY (location_id) REFERENCES location(id)
)