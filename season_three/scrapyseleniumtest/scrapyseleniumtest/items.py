# -*- coding: utf-8 -*-
from scrapy import Item, Field


class ProductItem(Item):
    collection = 'products'

    image = Field()
    price = Field()
    deal = Field()
    title = Field()
    shop = Field()
    location = Field()
