import aiosqlite
from sqlite3 import Error

def printError(name, what):
    print(f"Error {name}: {what}")

def databaseIsNotConnected(name):
    print(f"Error {name}: database is not connected")

class DatabaseManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.db = None

    async def connect(self):
        try:
            self.db = await aiosqlite.connect(self.db_name)
        except Error as e:
            printError("database connection", e)

    async def close(self):
        if self.db:
            await self.db.close()
            self.db = None

    async def execute_query(self, query, params=()):
        if self.db:
            try:
                async with self.db.cursor() as c:
                    await c.execute(query, params)
                    await self.db.commit()
            except Error as e:
                printError("executing query", e)
        else:
            databaseIsNotConnected("executing query")

    async def execute_many(self, query, params_list):
        if self.db:
            try:
                async with self.db.cursor() as c:
                    await c.executemany(query, params_list)
                    await self.db.commit()
            except Error as e:
                printError("executing many queries", e)
        else:
            databaseIsNotConnected("executing many queries")

    async def fetch_all(self, query, params=()):
        if self.db:
            try:
                async with self.db.cursor() as c:
                    await c.execute(query, params)
                    return await c.fetchall()
            except Error as e:
                printError("fetching all", e)
        else:
            databaseIsNotConnected("fetching all")
        return []

    async def fetch_one(self, query, params=()):
        if self.db:
            try:
                async with self.db.cursor() as c:
                    await c.execute(query, params)
                    return await c.fetchone()
            except Error as e:
                printError("fetching one", e)
        else:
            databaseIsNotConnected("fetching one")
        return None

    async def table_exists(self, table_name):
        query = f"PRAGMA table_info({table_name})"
        if self.db:
            try:
                async with self.db.cursor() as c:
                    await c.execute(query)
                    columns = await c.fetchall()
                    return len(columns) > 0
            except Error as e:
                printError("table existence check", e)
        else:
            databaseIsNotConnected("table existence check")
        return False
