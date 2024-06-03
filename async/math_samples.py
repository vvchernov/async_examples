def math_sample_sync(number = 10 ** 7):
    return sum(i * i for i in range(number))


async def math_sample_async(number = 10 ** 7):
    return sum(i * i for i in range(number))
