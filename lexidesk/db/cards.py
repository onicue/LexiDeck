import aiosqlite
from sqlite3 import Error
from db.manager import DatabaseManager
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

def map_record_to_card(record):
    return Card(
        card_id=record[0],
        name=record[1],
        top_content=record[2],
        bottom_content=record[3],
        groups=record[4].split(',') if record[4] else [],
        repetition_times=record[5].split(',') if record[5] else None
    )

def PrintCard(card):
    print(f"""
        Card ID: {card.id}
        Name: {card.name}
        Top Content: {card.top_content if card.top_content else 'None'}
        Bottom Content: {card.bottom_content if card.bottom_content else 'None'}
        Groups: {', '.join(card.groups) if card.groups else 'None'}
        Repetition Times: {', '.join(card.repetition_times) if card.repetition_times else 'None'}
    """)

class CardDB(DatabaseManager):
    def __init__(self, db_name):
        super().__init__(db_name)

    async def init(self):
        await self.connect()
        await self.execute_query("""
            CREATE TABLE IF NOT EXISTS cards (
                id INTEGER PRIMARY KEY,
                Name TEXT NOT NULL,
                TopContent TEXT DEFAULT '',
                BottomContent TEXT DEFAULT '',
                Groups TEXT DEFAULT '',
                RepetitionTimes TEXT DEFAULT ''
            )
            """)

    async def InsertIntoDatabase(self, values):
        await self.execute_many("INSERT INTO cards (Name) VALUES (?)", [(v,) for v in values])

    async def ReadDatabase(self):
        records = await self.fetch_all("SELECT * FROM cards")

        cards = []
        for record in records:
            if not record:
                continue
            card = map_record_to_card(record)
            cards.append(card)

        return cards

    async def ReadDatabaseAndPrint(self):
        cards = await self.ReadDatabase()
        if cards:
            for card in cards:
                PrintCard(card)
        else:
            print("No cards found.")

    async def FetchCardById(self, card_id):
        record = await self.fetch_one("SELECT * FROM cards WHERE id = ?", (card_id,))
        if record:
            card = map_record_to_card(record)
            return card
        else:
            print(f"No card found with ID: {card_id}")
            return None

