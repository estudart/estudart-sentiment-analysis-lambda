import asyncio
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.utils.extensions import postgres_instance, logger
from src.chains.translate.translate_to_english import translate_chain
from src.chains.text_convertions.bullet_to_text import bullet_to_text_chain
from src.chains.crypto import insight_chain, summarize_chain



class VideoAnalyzer:
    def __init__(self, channel_title):
        self.executor = ThreadPoolExecutor()
        self.database_instance = postgres_instance
        self.logger = logger

        self.channel_title = channel_title


    def chunk_text(self, text, chunk_size=3000, overlap=200):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap
        )
        return splitter.split_text(text)


    async def translate_and_summarize_chunk(self, chunk):
        translated = await asyncio.get_event_loop().run_in_executor(
            self.executor,
            lambda: translate_chain.invoke({"transcript": chunk})
        )

        summary = await asyncio.get_event_loop().run_in_executor(
            self.executor,
            lambda: summarize_chain.invoke({"transcript": translated})
        )

        return summary


    async def crypto_analizys_chain(self, transcript):
        chunks = self.chunk_text(transcript)

        # Schedule all tasks at once
        tasks = [self.translate_and_summarize_chunk(chunk) for chunk in chunks]

        # Run them in parallel (order preserved)
        summaries = await asyncio.gather(*tasks)

        merged_summary = "\n".join(summaries)
        paragraph_summary = bullet_to_text_chain.invoke(
            {"bullets": merged_summary})
        insights = insight_chain.invoke(
            {"transcript": paragraph_summary})

        return insights

    def run(self):
        query = (
            f"""
            SELECT yv.body, yv.created_utc
            FROM youtube_videos as yv
            WHERE yv.channel_title = '{self.channel_title}'
            AND yv.created_utc BETWEEN NOW() - INTERVAL '72 HOURS' AND NOW()
            ORDER BY yv.created_utc DESC
            """
        )
        data = self.database_instance.fetch_data(query)
        for transcript in data:
            loop_start_time = datetime.now(timezone.utc)

            result = asyncio.run(self.crypto_analizys_chain(transcript[0]))
            self.logger.info(result)

            loop_finished_time = datetime.now(timezone.utc)
            time_difference = (
                (loop_finished_time - loop_start_time)
                .total_seconds())
            self.logger.info(
                f"Loop took {round(time_difference, 2)} seconds \n"
                "######################################################"    
            )