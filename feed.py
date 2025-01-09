import yaml
import xml.etree.ElementTree as xml_tree

with open('feed.yaml', 'r') as file:
    yaml_data = yaml.safe_load(file)

    rss_element = xml_tree.Element('rss', {
        'version': '2.0',
        'xmlns:itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd',
        'xmlns:content': 'http://purl.org/rss/1.0/modules/content/'
    })

channel_element = xml_tree.SubElement(rss_element, 'channel')

link_prefix = yaml_data['link']

# Basic channel elements
title_element = xml_tree.SubElement(channel_element, 'title')
title_element.text = yaml_data['title']

format_element = xml_tree.SubElement(channel_element, 'format')
format_element.text = yaml_data['format']

subtitle_element = xml_tree.SubElement(channel_element, 'subtitle')
subtitle_element.text = yaml_data['subtitle']

author_element = xml_tree.SubElement(channel_element, 'itunes:author')
author_element.text = yaml_data['author']

desc_element = xml_tree.SubElement(channel_element, 'description')
desc_element.text = yaml_data['description']

image_element = xml_tree.SubElement(channel_element, 'itunes:image', {'href': link_prefix + yaml_data['image']})

lang_element = xml_tree.SubElement(channel_element, 'language')
lang_element.text = yaml_data['language']

link_element = xml_tree.SubElement(channel_element, 'link')
link_element.text = link_prefix

category_element = xml_tree.SubElement(channel_element, 'itunes:category')
category_element.text = yaml_data['category']

# Items loop - changed 'items' to 'item'
for item in yaml_data['item']:
    item_element = xml_tree.SubElement(channel_element, 'item')
    xml_tree.SubElement(item_element, 'title').text = item['title']
    xml_tree.SubElement(item_element, 'itunes:author').text = yaml_data['author']  # Using channel author
    xml_tree.SubElement(item_element, 'description').text = item['description']
    xml_tree.SubElement(item_element, 'itunes:duration').text = item['duration']
    xml_tree.SubElement(item_element, 'pubDate').text = item['published']
    
    # Fixed the length value to handle the comma in the string
    length = str(item['length']).replace(',', '')
    
    enclosure = xml_tree.SubElement(item_element, 'enclosure', {
        'url': link_prefix + item['file'],
        'type': yaml_data['format'],
        'length': length
    })

output_tree = xml_tree.ElementTree(rss_element)
output_tree.write('podcast.xml', encoding='UTF-8', xml_declaration=True)