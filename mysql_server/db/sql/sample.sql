CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE posts (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  title VARCHAR(255) NOT NULL,
  body TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
);


-- ユーザーデータの挿入
INSERT INTO users (name, email) VALUES
  ('John Doe', 'john@example.com'),
  ('Jane Smith', 'jane@example.net'),
  ('Bob Johnson', 'bob@example.org');

-- 投稿データの挿入
INSERT INTO posts (user_id, title, body) VALUES
  (1, '最初の投稿', '本文が入ります。'),
  (2, 'こんにちは', 'よろしくお願いします。'),
  (3, 'テスト投稿', 'これはテストです。');
