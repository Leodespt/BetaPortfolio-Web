#CREATE DATABASE BetaPortfolio;

USE BetaPortfolio;

#drop table transactions;
CREATE TABLE transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE,
    qty_bought DECIMAL(10, 2),
    qty_spent DECIMAL(10, 2),
    fee DECIMAL(10, 2),
    price DECIMAL(10, 2),
    fiat VARCHAR(50),
    crypto VARCHAR(50),
    action VARCHAR(50),
    platform VARCHAR(50),
    commentaire TEXT,
    user_id INT,
    creation_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

#drop table users;
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50),
    password VARCHAR(50),
    email VARCHAR(100),
    name VARCHAR(100),
    vorname VARCHAR(100),
    creation_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE transactions
ADD FOREIGN KEY (user_id)
REFERENCES users (user_id);

select * FROM transactions;
select * from users;

INSERT INTO transactions (date, qty_bought, qty_spent, fee, price, fiat, crypto, action, platform, commentaire, user_id)
VALUES
    ('2023-05-01', 2.5, 1000, 10, 400, 'USD', 'BTC', 'buy', 'Coinbase', 'Bought Bitcoin', 1),
    ('2023-05-02', 1.8, 1500, 12, 800, 'USD', 'ETH', 'buy', 'Binance', 'Bought Ethereum', 1),
    ('2023-05-03', 5.2, 3000, 15, 600, 'USD', 'LTC', 'sell', 'Kraken', 'Sold Litecoin', 2);

INSERT INTO users (username, password, email, name, vorname)
VALUES
    ('user1', 'password1', 'user1@example.com', 'John Doe', 'User1'),
    ('user2', 'password2', 'user2@example.com', 'Jane Smith', 'User2');


