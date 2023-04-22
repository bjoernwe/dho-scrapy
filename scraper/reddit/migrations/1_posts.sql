CREATE TABLE posts (
    id VARCHAR(20) PRIMARY KEY,
    title TEXT,
    author TEXT,
    created_utc TIMESTAMP,
    num_comments INTEGER,
    score INTEGER,
    url TEXT,
    text TEXT,
    subreddit TEXT
);
