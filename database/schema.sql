CREATE TABLE IF NOT EXISTS records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL CHECK(type IN ('income', 'expense')),
    category TEXT NOT NULL,
    amount REAL NOT NULL CHECK(amount >= 0),
    date TEXT NOT NULL,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS mrt_fares (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    start_station TEXT NOT NULL,
    end_station TEXT NOT NULL,
    fare INTEGER NOT NULL,
    UNIQUE(start_station, end_station)
);
