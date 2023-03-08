# import asyncio
# import json
# import requests
# from asgiref.sync import sync_to_async


# async def via_cep(cep):
#     r = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
#     response = json.loads(r.text)
#     print (response)
#     response = response.get('erro')

#     if not response:
#         return r.text
#     else:
#         return False


# import asyncio


# async def example_coroutine():
#     print("Coroutines are cool!")
#     try:
#         result = await asyncio.wait_for(via_cep('51350630'), timeout=0.000001)
#         print(f"Result: {result}")
#     except asyncio.TimeoutError:
#         print("Timeout!")
#     print("Coroutines are done!")


# async def main():
#     await asyncio.gather(
#         example_coroutine(),
#         example_coroutine(),
#         example_coroutine()
#     )

# asyncio.run(main())



if 1 != 1:
    print (1)
else:
    print (2)

print (3)