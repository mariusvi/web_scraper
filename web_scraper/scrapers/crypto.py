from typing import List
from web_scraper.models.item import Item, ItemLink, GroupLink
from web_scraper.scrapers.base import BaseScraper



class Crypto(BaseScraper):
    __items_per_page__: int = 44
    __domain__: str = "https://cryptolinks.com"

    def _retrieve_categories_list(self, keyword: str = "") -> List[GroupLink]:
        results: List[GroupLink] = []
        content = self._get_page_content(keyword)
        if content:
            list_segment = content.find("div", class_="thumb__row")
            items_list = list_segment.find_all("a", class_="thumb__head")
            for item_div in items_list:
                link = item_div['href'][24:]
                title = item_div.text
                results.append(GroupLink(url=link, title=title))

        return results

    def _retrieve_items_list(self, keyword: str) -> List[ItemLink]:
        results: List[ItemLink] = []
        content = self._get_page_content(keyword)
        if content:
            list_segment = content.find("div", class_="content__row")
            items_list = list_segment.find_all("div", class_="content__col")
            for item_div in items_list:
                link = item_div.find("a")["href"][24:]
                results.append(ItemLink(url=link))

        return results
        
    def _retrieve_item_data(self, keyword: str) -> List[ItemLink]:
        results: List[ItemLink] = []
        content = self._get_page_content(keyword)
        if content:
            head_segment = content.find("div", class_="review__head")
            title = head_segment.find("h1", class_="review__head-name").text
            url = head_segment.find("a")["href"]
            category_ul = content.find("ul", class_="breadcrumbs__list")
            category = category_ul.find_all("li")[1].find("a").text
            description = str(content.find("div", class_="review__box").find_all("p"))

        return Item(title=title, url=url, description=description, category=category)
            