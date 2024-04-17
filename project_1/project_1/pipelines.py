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

import mysql.connector 
class SaveToMySQLPipeLine:
    def __init__(self):
        self.cnx = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'Mysql!147456369',
            database = 'news'
        )
        self.cur = self.cnx.cursor()
        
        # create news table if none exists
        self.cur.execute ("""
            CREATE TABLE IF NOT EXISTS news(
                PRIMARY KEY (id),
                id int NOT NULL auto_increment, 
                url VARCHAR (225),
                title VARCHAR (225),
                author_name VARCHAR (225),
                author_email VARCHAR(225),
                publish_date DATETIME
            )
        """)
    def process_item (self, item, spider):
        self.cur.execute ("""
            insert into news (url, title, author_name, author_email, publish_date)
            values (%s,%s,%s,%s,%s)
        """,
        params = (item ['url'], 
        item ['title'], 
        item ['author_name'], 
        item ['author_email'], 
        item ['publish_date'], )
        )
        self.cnx.commit ()
        return item
    
    def close_spider (self,spider):
        self.cur.close()
        self.cnx.close()