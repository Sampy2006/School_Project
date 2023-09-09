import sqlite3


class Database:
    def __init__(self, dp_file):
        self.connection = sqlite3.connect(dp_file)
        self.cursor = self.connection.cursor()

    def user_exists(self, user_id):  # Проверка на наличие в бд
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `users` WHERE `user_id` = ?", (user_id,)).fetchmany(1)
            return bool(len(result))

    def add_user(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO `users` (`user_id`) VALUES (?)", (user_id,))

    def add_username(self, user_name):
        with self.connection:
            return self.cursor.execute("INSERT INTO `users` (`user_name`) VALUES (?)", (user_name,))

    def add_link(self, link, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `link` = ? WHERE `user_id` = ?", (link, user_id,))

    def add_admin(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO `admins` (`admin_id`) VALUES (?)", (user_id,))

    def delete_admin(self, user_id):
        with self.connection:
            return self.cursor.execute("DELETE FROM `admins` WHERE `admin_id` = ?", (user_id,))

    def get_admins(self):
        with self.connection:
            return self.cursor.execute("SELECT `admin_id` FROM `admins`").fetchall()

    def get_link(self):
        with self.connection:
            return self.cursor.execute("SELECT `link` FROM `users`").fetchall()

    def set_link(self, link):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `link` = ?", (link,))

    def set_active(self, user_id, active):  # Проверка на то, активен ли пользователь или нет
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `active` = ? WHERE `user_id` = ?", (active, user_id,))

    def get_users(self):  # Для рассылки сообщений (В идее проекта это не будет использоваться и сделано на будущее)
        with self.connection:
            return self.cursor.execute("SELECT `user_id`, `active` FROM `users`").fetchall()
