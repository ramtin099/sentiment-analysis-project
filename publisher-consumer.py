import asyncio
import aio_pika
import scraper

async def send_to_queue(urls):
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")
    queue_name = "scrape_queue"

    async with connection:
        channel = await connection.channel()

        exchange = await channel.declare_exchange('scrape_exchange', aio_pika.ExchangeType.DIRECT)
        queue = await channel.declare_queue(queue_name, durable=True)

        await queue.bind(exchange)

        for url in urls:
            await exchange.publish(
                aio_pika.Message(body=url.encode()),
                routing_key=queue_name
            )
            print(f"Sent URL: {url}")

        print("All URLs sent to the queue!")


async def consume_from_queue(queue_name="scrape_queue"):
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(queue_name, durable=True)

        async for message in queue:
            async with message.process():
                url = message.body.decode()
                print(f"Received URL: {url}")
                await scraper.scrape_page(url)
                print(f"Processed URL: {url}")
urls = [
    "en.isna.ir/archive",
    "en.irna.ir/archive",
    "en.mehrnews.com/archive",
    "tasnimnews.com/en/archive",
]
asyncio.run(send_to_queue(urls))

asyncio.run(consume_from_queue())
