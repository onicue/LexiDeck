import aiosqlite
from sqlite3 import Error
from datetime import datetime

CARD_BD_NAME = "cards.db"

class Card:
    def __init__(self, card_id, name, groups=None, top_content="", bottom_content="", repetition_times=None):
        self.id = card_id
        self.name = name
        self.top_content = top_content
        self.bottom_content = bottom_content
        self.groups = groups if groups else []
        self.repetition_times = repetition_times
        # (
        #     [datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
        #     if repetition_times is None else repetition_times
        # )

def PrintCard(card):
    print(f"""
        Card ID: {card.id}
        Name: {card.name}
        Top Content: {card.top_content if card.top_content else 'None'}
        Bottom Content: {card.bottom_content if card.bottom_content else 'None'}
        Groups: {', '.join(card.groups) if card.groups else 'None'}
        Repetition Times: {', '.join(card.repetition_times) if card.repetition_times else 'None'}
    """)

class CardDatabase:
    @staticmethod
    async def ConnectDatabase():
        try:
            db = await aiosqlite.connect(CARD_BD_NAME)
            async with db.cursor() as c:
                await c.execute("""
                    CREATE TABLE IF NOT EXISTS cards (
                        id INTEGER PRIMARY KEY,
                        Name TEXT NOT NULL,
                        TopContent TEXT DEFAULT '',
                        BottomContent TEXT DEFAULT '',
                        Groups TEXT DEFAULT '',
                        RepetitionTimes TEXT DEFAULT ''
                    )
                    """)
                await db.commit()
            return db
        except Error as e:
            print(f"Database connection error: {e}")

    @staticmethod
    async def InsertIntoDatabase(db, values):
        try:
            async with db.cursor() as c:
                await c.executemany("INSERT INTO cards (Name) VALUES (?)", [(v,) for v in values])
            await db.commit()
        except Error as e:
            print(f"Insert error: {e}")

    @staticmethod
    async def ReadDatabase(db):
        try:
            async with db.cursor() as c:
                await c.execute("SELECT * FROM cards")
                records = await c.fetchall()

                cards = []
                for record in records:
                    if not record:
                        continue
                    card = CardDatabase.__map_record_to_card(record)
                    cards.append(card)

                return cards
        except Error as e:
            print(f"Read error: {e}")

    @staticmethod
    async def ReadDatabaseAndPrint(db):
        cards = await CardDatabase.ReadDatabase(db)
        if cards:
            for card in cards:
                PrintCard(card)
        else:
            print("No cards found.")

    @staticmethod
    async def FetchCardById(db, card_id):
        try:
            async with db.cursor() as c:
                await c.execute("SELECT * FROM cards WHERE id = ?", (card_id,))
                record = await c.fetchone()
                if record:
                    card = CardDatabase.__map_record_to_card(record)
                    return card
                else:
                    print(f"No card found with ID: {card_id}")
                    return None
        except Error as e:
            print(f"Fetch error: {e}")

    @staticmethod
    def __map_record_to_card(record):
        return Card(
            card_id=record[0],
            name=record[1],
            top_content=record[2],
            bottom_content=record[3],
            groups=record[4].split(',') if record[4] else [],
            repetition_times=record[5].split(',') if record[5] else None
        )
