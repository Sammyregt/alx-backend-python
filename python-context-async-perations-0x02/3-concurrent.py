#!/usr/bin/python3
import aiosqlite
import asyncio


async def async_fetch_users():
    """
    Fetch all users from the database asynchronously
    with a context manager
    """
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            users = await cursor.fetchall()
            return users


async def async_fetch_older_users():
    """
    Fetch users older than 40 from the database
    asynchronously with a context manager
    """
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            users = await cursor.fetchall()
            return users


async def fetch_concurrently():
    """
    This function runs multiple queries concurrently
    and returns results in a dictionary
    """
    all_users, older_users = await asyncio.gather(
        async_fetch_users(), async_fetch_older_users()
    )
    return {"all_users": all_users, "older_users": older_users}


if __name__ == "__main__":
    result = asyncio.run(fetch_concurrently())
    print(f"Result: {result}")