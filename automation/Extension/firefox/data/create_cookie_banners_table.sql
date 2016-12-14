/* TODO: link with requests */
CREATE TABLE IF NOT EXISTS cookie_banners(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    crawl_id INTEGER,
    visit_id INTEGER,
    url TEXT NOT NULL,
    banner_text TEXT,
    banner_width INTEGER NOT NULL,
    banner_height INTEGER NOT NULL,
    banner_x_pos INTEGER NOT NULL,
    banner_y_pos INTEGER NOT NULL
);
