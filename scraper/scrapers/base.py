from abc import ABC, abstractmethod
from typing import List, Optional

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from scraper.models.item import Item, ItemLink, GroupLink


class BaseScraper(ABC):
    __items_per_page__: int = 0
    __domain__: str = ""

    @abstractmethod
    def _retrieve_items_list(self, pages_count: int, keyword: str) -> List[ItemLink]:
        pass

    def _get_page_content(self, query: str) -> Optional[BeautifulSoup]:
        resp = requests.get(f"{self.__domain__}/{query}")
        if resp.status_code == 200:
            return BeautifulSoup(resp.content, features="html.parser")
        raise Exception("Cannot reach content!")


    def scrape(self, keyword: str) -> List[Item]:
        categories_links: List[Optional[GroupLink]] = self._retrieve_categories_list()
        
        scraped_items_links: List[Optional[ItemLink]] = []
        for categorie in categories_links[5:8]:
            items_links: List[Optional[ItemLink]] = self._retrieve_items_list(categorie.url)
            scraped_items_links.append(items_links)

        scrapped_items_data: List[Item] = []
        for item_link_group in scraped_items_links: #TODO one for less
            for item_link in tqdm(item_link_group):
                data = self._retrieve_item_data(item_link.url)
                scrapped_items_data.append(data)
                
        return scrapped_items_data
