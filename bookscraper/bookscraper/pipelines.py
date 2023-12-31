# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BookscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Strip all whitespaces from strings
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != 'description':
                value = adapter.get(field_name)
                adapter[field_name] = value.strip()

        # Switch to lowercase the category, product type
        lowercase_fields = ['category', 'product_type']
        for lowercase_field in lowercase_fields:
            value = adapter.get(lowercase_field)
            adapter[lowercase_field] = value.lower()

        # Convert price to float
        price_fields = ['price', 'price_excl_tax', 'price_incl_tax', 'tax']
        for price_field in price_fields:
            value = adapter.get(price_field)
            value = value.replace('£', '')  # Remove char first before converting
            adapter[price_field] = float(value)

        # Extract number of books in stock (availability)
        availability_str = adapter.get('availability')
        split_str_array = availability_str.split('(')  # Sample value of availability: 'In stock (19 available)'
        if len(split_str_array) < 2:
            adapter['availability'] = 0
        else:
            availability_arr = split_str_array[1].split(' ')
            adapter['availability'] = int(availability_arr[0])

        # Convert reviews from string to int
        num_reviews_str = adapter.get('num_reviews')
        adapter['num_reviews'] = int(num_reviews_str)

        # Convert stars from string to int
        stars_str = adapter.get('stars')
        split_stars_array = stars_str.split(' ')  # Sample value of stars: 'star-rating Five'
        stars_str_value = split_stars_array[1].lower()
        if stars_str_value == 'zero':
            adapter['stars'] = 0
        elif stars_str_value == 'one':
            adapter['stars'] = 1
        elif stars_str_value == 'two':
            adapter['stars'] = 2
        elif stars_str_value == 'three':
            adapter['stars'] = 3
        elif stars_str_value == 'four':
            adapter['stars'] = 4
        elif stars_str_value == 'five':
            adapter['stars'] = 5

        return item
