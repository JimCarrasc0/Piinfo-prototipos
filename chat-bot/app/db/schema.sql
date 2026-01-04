-- HISTORIAL DE CONVERSACIONES
CREATE TABLE IF NOT EXISTS messages (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id TEXT NOT NULL,
  role TEXT NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
  content TEXT NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_messages_session
ON messages(session_id);

-- PUBLICACIONES SIMULADAS
CREATE TABLE IF NOT EXISTS posts (
  id TEXT PRIMARY KEY,
  platform TEXT NOT NULL,
  caption TEXT,
  created_at DATETIME NOT NULL
);

-- MÉTRICAS SIMULADAS (META)
CREATE TABLE IF NOT EXISTS meta_metrics (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  post_id TEXT NOT NULL,
  metric_name TEXT NOT NULL,
  period TEXT NOT NULL,
  value INTEGER NOT NULL,
  end_time DATETIME NOT NULL,
  FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
  UNIQUE (post_id, metric_name, period)
);

CREATE INDEX IF NOT EXISTS idx_metrics_post
ON meta_metrics(post_id);

-- COMENTARIOS SIMULADOS
CREATE TABLE IF NOT EXISTS meta_comments (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  post_id TEXT NOT NULL,
  comment_id TEXT NOT NULL,
  text TEXT NOT NULL,
  sentiment TEXT CHECK (
    sentiment IN ('positive', 'neutral', 'negative')
  ),
  timestamp DATETIME NOT NULL,
  FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
  UNIQUE (comment_id)
);

CREATE INDEX IF NOT EXISTS idx_comments_post
ON meta_comments(post_id);

-- EMBEDDINGS SEMÁNTICOS (RAG)
CREATE TABLE IF NOT EXISTS embeddings (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  source_type TEXT NOT NULL,     
  source_id TEXT NOT NULL,       
  content TEXT NOT NULL,         
  embedding TEXT NOT NULL,       
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  UNIQUE (source_type, source_id, content)
);

CREATE INDEX IF NOT EXISTS idx_embeddings_source
ON embeddings(source_type, source_id);
