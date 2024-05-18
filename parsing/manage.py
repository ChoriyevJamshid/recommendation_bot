import asyncio
import logging

from parsing import alifshop
from parsing import bemarket
from parsing import mediapark
from parsing import olcha
from parsing import sello
from parsing import texnomart
from parsing import uzummarket


logger = logging.getLogger(__name__)


async def run_tasks():
    tasks = [
        alifshop.parser.Parser(
            category=alifshop.parser.categories['smartphone']['category'],
            subcategory=alifshop.parser.categories['smartphone']['subcategory'],
            dirname="alifshop"
        ).run(),
        bemarket.parser.Parser(
            category=bemarket.parser.categories['smartphone']['category'],
            subcategory=bemarket.parser.categories['smartphone']['subcategory'],
            dirname="bemarket"
        ).run(),
        mediapark.parser.Parser(
            category=mediapark.parser.categories['smartphone']['category'],
            subcategory=mediapark.parser.categories['smartphone']['subcategory'],
            dirname="mediapark"
        ).run(),
        olcha.parser.Parser(
            category=olcha.parser.categories['smartphone']['category'],
            subcategory=olcha.parser.categories['smartphone']['subcategory'],
            dirname="olcha"
        ).run(),
        sello.parser.Parser(
            category=sello.parser.categories['smartphone']['category'],
            subcategory=sello.parser.categories['smartphone']['subcategory'],
            dirname="sello"
        ).run(),
        texnomart.parser.Parser(
            category=texnomart.parser.categories['smartphone']['category'],
            subcategory=texnomart.parser.categories['smartphone']['subcategory'],
            dirname="texnomart"
        ).run(),
    ]

    await asyncio.gather(*tasks)


def main():
    logger.info("main() function is called")
    uzum_parser = uzummarket.parser.AsyncParser(
        category=uzummarket.parser.categories['smartphone']['category'],
        subcategory=uzummarket.parser.categories['smartphone']['subcategory'],
        dirname="uzummarket"
    )
    while True:
        try:
            asyncio.run(run_tasks())
            asyncio.run(uzum_parser.run())
            break
        except Exception as exc:
            print(exc)


if __name__ == "__main__":
    main()

