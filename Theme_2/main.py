import asyncio
import time

# async def my_coroutine():
#     """Простая сопрограмма."""
#     print("Задача начата")
#     await asyncio.sleep(1)
#     print("Задача завершена")
#     return "Результат"
#
#
# async def main():
#     """Создание и запуск задачи."""
#     task = asyncio.create_task(my_coroutine())
#     print("Задача создана")
#     result = await task  # Ожидание завершения задачи
#     print(f"Результат задачи: {result}")

async def my_coroutine():
    """Простая сопрограмма."""
    print("Задача начата")
    await asyncio.sleep(1)
    print("Задача завершена")
    return "Результат"


async def main():
    """Создание и запуск задачи."""
    # task = asyncio.create_task(my_coroutine())
    print("Задача создана")
    result = await my_coroutine()  # Ожидание завершения задачи
    print(f"Результат задачи: {result}")

if __name__ == "__main__":
    asyncio.run(main())
