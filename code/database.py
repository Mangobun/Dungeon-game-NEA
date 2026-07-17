import sqlite3

class Database:
    def __init__(self):
        self.connection = sqlite3.connect("high_scores.db")
        self.cursor = self.connection.cursor()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS high_scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                score INTEGER NOT NULL
            )
        """)
        self.connection.commit()

    def add_score(self, name, score):
        # retrieves the existing score for the player
        self.cursor.execute(
            "SELECT score FROM high_scores WHERE name = ?",
            (name,)
        )
        existing_score = self.cursor.fetchone()

        # if the player does not exist, insert a new record
        if existing_score is None:
            self.cursor.execute(
                "INSERT INTO high_scores (name, score) VALUES (?, ?)",
                (name, score)
            )

        # if the new score is higher, update the player's existing score
        elif score > existing_score[0]:
            self.cursor.execute(
                "UPDATE high_scores SET score = ? WHERE name = ?",
                (score, name)
            )

    def get_high_scores(self):
        self.cursor.execute("""
            SELECT name, score
            FROM high_scores
            ORDER BY score DESC
            LIMIT 5
        """)

        return self.cursor.fetchall()

    def close(self):
        self.connection.close()