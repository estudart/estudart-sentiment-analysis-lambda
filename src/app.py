import asyncio
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

from langchain_text_splitters import RecursiveCharacterTextSplitter

from utils.extensions import postgres_instance, logger
from prompts.crypto_prompt import translate_chain, summarize_chain, insight_chain


executor = ThreadPoolExecutor()


def chunk_text(text, chunk_size=3000, overlap=200):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap
    )
    return splitter.split_text(text)


async def translate_and_summarize_chunk(chunk):
    translated = await asyncio.get_event_loop().run_in_executor(
        executor,
        lambda: translate_chain.invoke({"transcript": chunk})
    )

    summary = await asyncio.get_event_loop().run_in_executor(
        executor,
        lambda: summarize_chain.invoke({"transcript": translated})
    )

    return summary


async def crypto_analizys_chain(transcript):
    chunks = chunk_text(transcript)

    # Schedule all tasks at once
    tasks = [translate_and_summarize_chunk(chunk) for chunk in chunks]

    # Run them in parallel (order preserved)
    summaries = await asyncio.gather(*tasks)

    for summary in summaries:
        logger.info(summary)

    merged_summary = "\n".join(summaries)
    insights = insight_chain.invoke({"transcript": merged_summary})

    return insights


query = (
    """
    SELECT yv.body
    FROM youtube_videos as yv
    WHERE yv.topic = 'crypto_international'
    AND yv.channel_title = 'Altcoin Daily'
    ORDER BY yv.created_utc DESC
    LIMIT 1
    """
)
data = postgres_instance.fetch_data(query)
for transcript in data:
    loop_start_time = datetime.now(timezone.utc)

    result = asyncio.run(crypto_analizys_chain(transcript[0]))
    print(result)

    loop_finished_time = datetime.now(timezone.utc)
    time_difference = (
        (loop_finished_time - loop_start_time)
        .total_seconds())
    print(f"Loop took {round(time_difference, 2)} seconds")
