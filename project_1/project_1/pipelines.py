# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from datetime import datetime
import re

class Project1Pipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        field_names = adapter.field_names()
        for field_name in field_names:
            value = adapter.get(field_name)
            if value is not None:
                value = value.strip (" \n")
                value = re.sub (r'^-?\s*','', value)
                adapter [field_name] = value
            if field_name == 'publish_date': 
                publish_date_str = adapter.get('publish_date')
                input_format = '%d/%m/%Y %H:%M GMT+7'
                try:
                    # Parse the publish date string into a datetime object
                    publish_date = datetime.strptime(publish_date_str, input_format)
                    # Convert the datetime object to the standard datetime format for database storage
                    standard_format = publish_date.strftime('%Y-%m-%d %H:%M:%S')
                    # Update the value of the publish date field in the item
                    adapter['publish_date'] = standard_format
                except ValueError:
                    # Handle parsing errors
                    pass
        return item
