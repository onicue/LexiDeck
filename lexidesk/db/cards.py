import aiosqlite
from sqlite3 import Error
from db.manager import DatabaseManager
from datetime import datetime

CARD_BD_NAME = "cards.db"

class Card:
    def __init__(self, name, groups=[], top_content="", bottom_content="", repetition_times=[], card_id=None):
        if not isinstance(groups, list):
            raise ValueError(f"Expected 'groups' to be a list, got {type(groups)}.")
        if not isinstance(repetition_times, list):
            raise ValueError(f"Expected 'repetition_times' to be a list, got {type(repetition_times)}.")

        self.id = card_id
        self.name = name
        self.top_content = top_content
        self.bottom_content = bottom_content
        self.groups = groups or []
        self.repetition_times = repetition_times or [datetime.now().strftime('%Y-%m-%d %H:%M:%S')]

    def deserialize_group(self):
        return ",".join(self.groups)

    def serialize_group(self, groups):
        self.groups = groups.split(",")

    def deserialize_repetition_times(self):
        return ",".join(self.repetition_times)

    def serialize_repetition_times(self, groups):
        self.repetition_times = repetition_times.split(",")

    def getValues(self):
        return (
            self.name,
            self.top_content,
            self.bottom_content,
            self.deserialize_group(),
            self.deserialize_repetition_times(),
        )

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
        await self.execute_query(f"""
            CREATE TABLE IF NOT EXISTS {self.db_name} (
                id INTEGER PRIMARY KEY,
                Name TEXT NOT NULL,
                TopContent TEXT DEFAULT '',
                BottomContent TEXT DEFAULT '',
                Groups TEXT DEFAULT '',
                RepetitionTimes TEXT DEFAULT ''
            )
            """)

    async def insertCard(self, card):
        await self.execute_query(f"""
            INSERT INTO {self.db_name} (Name, TopContent, BottomContent, Groups, RepetitionTimes)
            VALUES (?, ?, ?, ?, ?);
        """, card.getValues)

    async def insertCards(self, cards):
        values = [ card.getValues() for card in cards ]
        await self.execute_many(f"""
            INSERT INTO {self.db_name} (Name, TopContent, BottomContent, Groups, RepetitionTimes)
            VALUES (?, ?, ?, ?, ?);
        """, values)

    async def getCards(self) -> list:
        records = await self.fetch_all(f"SELECT * FROM {self.db_name}")

        cards = []
        for record in records:
            if not record:
                continue
            card = map_record_to_card(record)
            cards.append(card)

        return cards

    # for debug
    async def __ReadDatabaseAndPrint(self):
        cards = await self.getCards()
        if cards:
            for card in cards:
                PrintCard(card)
        else:
            print("No cards found.")

    async def getCardById(self, card_id) -> Card:
        record = await self.fetch_one(f"SELECT * FROM {self.db_name} WHERE id = ?", (card_id,))
        if record:
            card = map_record_to_card(record)
            return card
        else:
            print(f"No card found with ID: {card_id}")
            return None

    async def deleteCardById(self, card_id: int):
        await self.execute_query(f"DELETE FROM {self.db_name} WHERE id = ?", card_id)


    async def deleteCard(self, card: Card):
        await self.execute_query(f"DELETE FROM {self.db_name} WHERE id = ?", card.id)
