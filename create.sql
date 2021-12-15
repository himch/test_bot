-- SQL script to bootstrap the DB:
--
-- Картинки и Аудио
CREATE TABLE IF NOT EXISTS media
                (
                tgid INTEGER,
                file_name TEXT,
                media_type TEXT
                );

--
--
-- Пользователи бота
CREATE TABLE IF NOT EXISTS users
                (
                tgid INTEGER,
                chatid INTEGER,
                subscribed INTEGER
                );
--
--
-- Менеджеры бота
CREATE TABLE IF NOT EXISTS managers
                (
                tgid INTEGER
                );
--
--
-- Сообщения подписчикам бота
CREATE TABLE IF NOT EXISTS broadcastmessages
                (
                id INTEGER PRIMARY KEY,
                message TEXT
                );
--
--
-- Отправленные сообщения подписчикам бота
CREATE TABLE IF NOT EXISTS sendedbroadcastmessages
                (
                tgid INTEGER,
                broadcastmessagesid INTEGER,
                timestamp DATETIME,
                success INTEGER,
                comment TEXT
                );
