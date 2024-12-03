from db import CardDB, Card
import asyncio

async def main():
    database = CardDB("cards.db")

    await database.init()
    values = ['John', 'Jane', 'Tin', 'Alan']
    await asyncio.gather(database.InsertIntoDatabase(values), database.ReadDatabaseAndPrint())

    card = await database.FetchCardById(1)
    if card:
        print(f"Card fetched: {card.name}, {card.top_content}, {card.bottom_content}")

    await database.close()


if __name__ == "__main__":
    asyncio.run(main())
