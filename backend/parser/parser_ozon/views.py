# pylint: disable=E1101

import os

import requests
import telegram

from bs4 import BeautifulSoup
from rest_framework.views import APIView
from rest_framework.response import Response


from .serializers import ProductSerializer
from .models import Product

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')


class ProductListView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductDetailView(APIView):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)


class ScrapeProductView(APIView):
    def post(self, request):
        products_count = int(request.data.get('products_count', 10))
        if products_count > 50:
            products_count = 50

        url = 'https://www.ozon.ru/seller/2/products/'

        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            product_items = soup.find_all('div', class_='a0c6')

            scraped_products = []
            for product in product_items[:products_count]:
                name = product.find('a', class_='b3u9').text.strip()
                price = float(product.find(
                    'span', class_='c2h5'
                    ).text.strip().replace(' ', ''))
                description = product.find(
                    'span', class_='b5v6'
                    ).text.strip()
                image_url = product.find(
                    'img', class_='d2t7'
                    )['src']
                discount = product.find(
                    'div', class_='e1q3'
                    ).text.strip() if product.find(
                        'div', class_='e1q3') else None

                product_instance = Product(
                    name=name, price=price,
                    description=description,
                    image_url=image_url,
                    discount=discount)
                scraped_products.append(product_instance)

            Product.objects.all().delete()
            Product.objects.bulk_create(scraped_products)

            serializer = ProductSerializer(scraped_products, many=True)

            bot_token = TELEGRAM_BOT_TOKEN
            chat_id = TELEGRAM_CHAT_ID

            message = ""
            for product in serializer.data:
                message += f"Name: {product['name']}\n"
                message += f"Price: {product['price']}\n"
                message += f"Description: {product['description']}\n"
                message += f"Image URL: {product['image_url']}\n"
                message += f"Discount: {product['discount']}\n\n"

            bot = telegram.Bot(token=bot_token)
            bot.send_message(chat_id=chat_id, text=message)

            return Response(serializer.data)
        else:
            return Response({'error': 'Failed to scrape the page.',
                             'status_code': response.status_code})
