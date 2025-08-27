import sqlite3

class LudoDB:
    def __init__(self, db_name="ludo.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        """Create players table if it doesn't exist"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                wins INTEGER DEFAULT 0,
                losses INTEGER DEFAULT 0
            )
        ''')
        self.conn.commit()

    # -------------------- CRUD Methods --------------------
    def create_player(self, name):
        try:
            self.cursor.execute("INSERT INTO players (name) VALUES (?)", (name,))
            self.conn.commit()
        except sqlite3.IntegrityError:
            print(f"Player '{name}' already exists.")

    def get_player(self, name):
        self.cursor.execute("SELECT * FROM players WHERE name = ?", (name,))
        return self.cursor.fetchone()

    def get_all_players(self):
        self.cursor.execute("SELECT * FROM players ORDER BY wins DESC")
        return self.cursor.fetchall()
    
    def update_player_stats(self, name, wins, losses):
        """Update a player's wins and losses directly""" 
        self.cursor.execute("UPDATE players SET wins = ?, losses = ? WHERE name = ?", 
                       (wins, losses, name))
        self.conn.commit()

    def get_player_by_id(self, player_id):
        """Get a player by their ID"""
        self.cursor.execute("SELECT * FROM players WHERE id = ?", (player_id,))
        return self.cursor.fetchone()

    def update_score(self, name, won=False):
        if won:
            self.cursor.execute("UPDATE players SET wins = wins + 1 WHERE name = ?", (name,))
        else:
            self.cursor.execute("UPDATE players SET losses = losses + 1 WHERE name = ?", (name,))
        self.conn.commit()

    def delete_player(self, name):
        self.cursor.execute("DELETE FROM players WHERE name = ?", (name,))
        self.conn.commit()

    def close(self):
        self.conn.close()