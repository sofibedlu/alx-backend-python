import asyncio
import aiosqlite

async def async_fetch_users(db_path):
    async with aiosqlite.connect(db_path) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            users = await cursor.fetchall()
            return users

async def async_fetch_older_users(db_path):
    async with aiosqlite.connect(db_path) as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            older_users = await cursor.fetchall()
            return older_users

async def fetch_concurrently(db_path):
    users, older_users = await asyncio.gather(
        async_fetch_users(db_path),
        async_fetch_older_users(db_path)
    )
    print("All users:", users)
    print("Users older than 40:", older_users)

if __name__ == "__main__":
    db_path = "users.db"
    asyncio.run(fetch_concurrently(db_path))