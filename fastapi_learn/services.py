import os
import asyncio
import random
import httpx


# Async function to perform the periodic ping
async def ping_service():
    url = os.getenv("PING_URL", "https://render.com")
    delay = int(os.getenv("PING_DELAY", 300))  # Default delay is 5 mins
    while True:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)  # Async HTTP request
                if response.status_code == 200:
                    print(f"ping_service state OK")
                else:
                    print(
                        f"{__name__} ping_service to {url}. Service returned status: {response.status_code}"
                    )
        except Exception as e:
            print(f"Error while pinging service: {e}")

        try:
            # Wait before the next ping (e.g., 300 seconds + random shift)
            await asyncio.sleep(delay + random.uniform(0, delay // 2))
        except asyncio.exceptions.CancelledError:
            print("Ping service was cancelled.")
            break  # Exit loop and terminate task gracefully


if __name__ == "__main__":
    asyncio.run(ping_service())
