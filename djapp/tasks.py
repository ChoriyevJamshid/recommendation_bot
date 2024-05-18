import json
import logging
import time
import os
from celery import shared_task
from djapp.models import Product, Shop, ProductType
from parsing.manage import main as parse_data

logger = logging.getLogger(__name__)


@shared_task
def task_1():
    logger.info('Task1 start')
    time.sleep(10)
    logger.info('Task1 end')


@shared_task
def get_parsing_data():
    logger.info("Parser is working!")
    # parse_data()
    list_dirs = os.listdir('parsing/json_data')
    for file_name in list_dirs:
        dir_name = file_name.split('.')[0]
        try:
            with open(f'parsing/json_data/{file_name}', mode='r') as file:
                data = json.load(file)
        except Exception as e:
            logger.info(e)
            return

        shop, created = Shop.objects.get_or_create(
            title=dir_name
        )
        logger.info(f'shop: {shop}')

        product_type, created = ProductType.objects.get_or_create(
            title='smartphone'
        )

        products = Product.objects.all()
        products.delete()

        for page_data in data.values():
            for product in page_data.values():

                obj = Product(
                    title=product['title'],
                    link=product['link'],
                    price=product['price'],
                    shop=shop,
                    product_type=product_type
                )
                price_credit = product.get('price_credit')
                if price_credit:
                    obj.price_credit = price_credit

                obj.save()
                logger.info(f'Created product: {obj}')



