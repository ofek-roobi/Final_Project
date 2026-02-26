import sqlite3
from entities import Person, Member, Trainer, WorkoutSession

class StudioModel:
    def __init__(self, db_name="studio.db"):
        self.db_name = db_name
        self._create_tables() 

    def _get_connection(self):
        return sqlite3.connect(self.db_name)

    def _create_tables(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS members (
                                id_num TEXT PRIMARY KEY, name TEXT, phone TEXT, 
                                member_type TEXT, balance REAL, status TEXT)''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS trainers (
                                id_num TEXT PRIMARY KEY, name TEXT, phone TEXT, 
                                specialty TEXT, rank TEXT)''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS sessions (
                                session_id TEXT PRIMARY KEY, name TEXT, 
                                trainer_id TEXT, max_capacity INTEGER)''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS session_members (
                                session_id TEXT, member_id TEXT,
                                PRIMARY KEY (session_id, member_id))''')
            conn.commit()
            
    def save_person(self, person: Person):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if isinstance(person, Member):
                cursor.execute("INSERT OR REPLACE INTO members VALUES (?, ?, ?, ?, ?, ?)",
                               (person.id_num, person._name, person.phone, 
                                person.member_type, person.balance, person.status))
            elif isinstance(person, Trainer):
                cursor.execute("INSERT OR REPLACE INTO trainers VALUES (?, ?, ?, ?, ?)",
                               (person.id_num, person._name, person.phone, person.specialty, person.rank))
            conn.commit()

    def read_member(self, id_num: str):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM members WHERE id_num=?", (id_num,))
            return cursor.fetchone() 

    def read_trainer(self, id_num: str):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM trainers WHERE id_num=?", (id_num,))
            return cursor.fetchone()

    def get_all_members(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM members")
            return cursor.fetchall()
            
    def get_all_trainers(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM trainers")
            return cursor.fetchall()

    def delete_member(self, id_num: str):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM members WHERE id_num=?", (id_num,))
            conn.commit()
            return cursor.rowcount > 0 

    def save_session(self, session: WorkoutSession):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            trainer_id = session.trainer.id_num if session.trainer else None
            cursor.execute("INSERT OR REPLACE INTO sessions VALUES (?, ?, ?, ?)",
                           (session.session_id, session.name, trainer_id, session.max_capacity))
            conn.commit()

    def enroll_member_to_session(self, session_id: str, member_id: str):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT OR IGNORE INTO session_members VALUES (?, ?)", 
                           (session_id, member_id))
            conn.commit()

    def get_all_sessions(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM sessions")
            return cursor.fetchall()

    def get_members_in_session(self, session_id: str):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT m.* FROM members m
                              JOIN session_members sm ON m.id_num = sm.member_id
                              WHERE sm.session_id = ?''', (session_id,))
            return cursor.fetchall()
        
    def get_studio_summary_for_ai(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT name, balance, status FROM members")
            members = cursor.fetchall()
            
            cursor.execute("SELECT name, specialty FROM trainers")
            trainers = cursor.fetchall()
            
            cursor.execute("SELECT name, max_capacity FROM sessions")
            sessions = cursor.fetchall()
            
            summary = f"Members: {members}, Trainers: {trainers}, Sessions: {sessions}"
            return summary