import sqlite3
from pathlib import Path


DATABASE = Path("memory.db")


def get_connection():

    connection = sqlite3.connect(
        DATABASE
    )

    connection.row_factory = sqlite3.Row

    return connection


def initialize_memory():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS memories (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            memory_type TEXT NOT NULL,

            content TEXT NOT NULL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
        """
    )

    connection.commit()

    connection.close()


def save_memory(
    memory_type,
    content
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO memories (
            memory_type,
            content
        )

        VALUES (?, ?)
        """,
        (
            memory_type,
            content
        )
    )

    connection.commit()

    connection.close()


def get_recent_memories(
    limit=10
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            memory_type,
            content,
            created_at

        FROM memories

        ORDER BY created_at DESC

        LIMIT ?
        """,
        (limit,)
    )

    memories = cursor.fetchall()

    connection.close()

    return memories