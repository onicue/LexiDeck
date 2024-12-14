from db import CardDB, Card
import asyncio

async def main():
    database = CardDB("cards")

    await database.init()
    cards = [Card("Card 1", ["Group 1"], "Top 1", "Bottom 1", ["2024-12-14"]),
             Card("Card 2", ["Group 2"], "Top 2", "Bottom 2")]
    await asyncio.gather(database.insertCards(cards), database._CardDB__ReadDatabaseAndPrint())

    card = await database.getCardById(1)
    if card:
        print(f"Card fetched: {card.name}, {card.top_content}, {card.bottom_content}")

    await database.close()

if __name__ == "__main__":
    asyncio.run(main())
