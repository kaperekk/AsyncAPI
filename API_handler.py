import aiohttp
import asyncio
from pprint import pprint
import time


def get_time():
    return time.time()

async def fetch_random_wikipedia_page(session):
    url = f"https://en.wikipedia.org/api/rest_v1/page/random/summary"
    cpu_time1 = get_time()
    try:
        async with session.get(url) as response:
            data = await response.json()
            cpu_time2 = get_time()

            return (cpu_time2 - cpu_time1), data['description'], data['title'], data['extract_html']
    except Exception:
        cpu_time2 = get_time()

        return (cpu_time2 - cpu_time1), "Bad_Querry", "NULL", "NULL"
    
async def get_wiki_pages(N: int):
    connector = aiohttp.TCPConnector(ssl=False)  # Disable SSL verification
    cpu_time1 = get_time()
    bad_query_counter = 0
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [fetch_random_wikipedia_page(session) for _ in range(N)]
        results = await asyncio.gather(*tasks)

    cpu_time2 = get_time()
    html_content = f"<h1>{N} Random Wikipedia Pages</h1>"
    avg_time = 0

    for time, desc, title, html in results:
        if "NULL" in html:
            bad_query_counter += 1
        avg_time += time
        html_content += f"<h2>{desc, title}</h2><p>Request querry time: {time:.2f} s {html}</p> "

    full_time = cpu_time2 - cpu_time1
    avg_time = avg_time / N
    html_content += f"<h2>full querry time {full_time:.2f} s </h2>"
    html_content += f"<h2>avg time per request {avg_time:.2f} s </h2>"
    html_content += f"<h2>AsyncIO saved ~ {avg_time * N - full_time  :.2f} s, which is {(avg_time * N - full_time ) / N :.2f} s per request with {N} requests</h2>"
    html_content += f"<h2>With {bad_query_counter} NULL query errors which is {bad_query_counter / N *100 :.2f} %</h2>"


    return html_content

async def main():
    N = 10
    html_content = await get_wiki_pages(N=N)
    print(html_content)

if __name__ == '__main__':
    asyncio.run(main())
