import asyncio
import edge_tts

async def list_voices():
    voices = await edge_tts.list_voices()
    print(f"{'Name':<50} {'ShortName':<25} Gender")
    print("-"*90)
    for v in voices:
        name = v.get("FriendlyName", v["ShortName"])
        print(f"{name:<50} {v['ShortName']:<25} {v.get('Gender', 'N/A')}")

asyncio.run(list_voices())
