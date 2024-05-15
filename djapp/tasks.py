import logging
import time
from celery import shared_task

from parsing.manage import main


logger = logging.getLogger(__name__)


@shared_task
def task_1():
    logger.info('Task1 start')
    time.sleep(10)
    logger.info('Task1 end')


@shared_task
def get_parsing_data():
    logger.info("Parser is working!")
    main()



