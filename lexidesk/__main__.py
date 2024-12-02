from db import CardDatabase, Card
import asyncio

async def main():
    database = await CardDatabase.ConnectDatabase()

    values = ['John', 'Jane', 'Tin', 'Alan']
    await asyncio.gather(CardDatabase.InsertIntoDatabase(database, values), CardDatabase.ReadDatabaseAndPrint(database))

    card = await CardDatabase.FetchCardById(database, 1)
    if card:
        print(f"Card fetched: {card.name}, {card.top_content}, {card.bottom_content}")

    await database.close()


if __name__ == "__main__":
    asyncio.run(main())
