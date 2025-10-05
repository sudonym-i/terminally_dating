CREATE TABLE IF NOT EXISTS Users (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    username      TEXT NOT NULL UNIQUE,
    email         TEXT NOT NULL UNIQUE,
    age           INTEGER,
    usr_location  TEXT,
    bio           TEXT,
    profile_link  TEXT, -- Link to user's profile page on LinkedIn??
    password_hash TEXT NOT NULL,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Test insertion
INSERT INTO Users (username, email, age, usr_location, bio, profile_link, password_hash)
VALUES ('testuser', 'testemail', 111, 'testlocation', 'testbio', 'testlink', 'testhash')

CREATE TABLE IF NOT EXISTS Connections (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id         INTEGER NOT NULL,
    connection_id   INTEGER NOT NULL,
    status          TEXT CHECK(status IN ('pending', 'accepted', 'rejected')) DEFAULT 'pending',
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE,
    FOREIGN KEY (connection_id) REFERENCES Users(id) ON DELETE CASCADE,
    UNIQUE(user_id, connection_id)
);

CREATE TABLE IF NOT EXISTS Messages (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id    INTEGER NOT NULL,
    receiver_id  INTEGER NOT NULL,
    content      TEXT NOT NULL,
    sent_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES Users(id) ON DELETE CASCADE,
    FOREIGN KEY (receiver_id) REFERENCES Users(id) ON DELETE CASCADE
);

CREATE TABLE IF EXISTS Profile_links (
  id          TEXT PRIMARY KEY,
  profile_id  TEXT NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  kind        TEXT CHECK (kind IN ('linkedin','github','website','instagram','other')),
  url         TEXT NOT NULL
);

CREATE TABLE IF EXISTS Answers (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  -- question    TEXT NOT NULL,
  answer      TEXT NOT NULL,
  usr_flag    INTEGER CHECK (usr_flag IN (1,2)) DEFAULT 1,
  user_id     INTEGER NOT NULL REFERENCES Users(id) ON DELETE CASCADE,
);