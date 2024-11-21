CREATE TABLE dd_dictionary (
    txt_id INTEGER PRIMARY KEY AUTOINCREMENT,
    text_name TEXT NOT NULL UNIQUE,
    text_type TEXT,
    text_alias TEXT,
    icon TEXT,
)