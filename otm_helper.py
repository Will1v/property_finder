from logger import get_logger
from bs4 import BeautifulSoup
import requests
import re
import json
from statistics import mean


OTM_URL = "https://www.onthemarket.com/for-sale/property/"
OTM_DETAIL_BASE_URL = "https://www.onthemarket.com/"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
}

logger = get_logger("OnTheMarket Helper")


class OnTheMarketSearch():

    property_types = ("House", "Flat", "Garage", "Other")
    detailed_to_general_property_type_map = {
        "House": "House",
        "Flat": "Flat",
        "Garage": "Garage",
        "Terraced house": "House",
        "Semi-detached house": "House",
        "Detached house": "House",
        "Apartment": "Flat",
        "Penthouse": "Flat",
        "Studio": "Flat",
        "Detached bungalow": "House",
        "Maisonette": "House",
        "Townhouse": "House",
        "Duplex": "Flat",
        "End of terrace house": "House",
    }


    def __init__(self, postcode: str, radius: int = 0.25, min_price: int = None, max_price: int = None,
                 min_bed: int = None, max_bed: int = None, property_type: str = None, potential: bool = False,
                 keywords: list = []):
        logger = get_logger(OnTheMarketSearch.__name__, debug=True)
        assert (property_type == None or set([property_type]) <= set("house", "flat")), f"Incorrect property_type argument found {property_type}, should be house or flat (or nothing)"
        self.postcode = postcode
        self.radius = radius
        self.min_price = min_price
        self.max_price = max_price
        self.min_bed = min_bed
        self.max_bed = max_bed
        self.property_type = property_type
        self.keywords = keywords
        self.potential = potential
        self.page_id = 0
        self.results = []
        self._get_otm_results()

    def _get_otm_results(self) -> list():
        self.results = []  # Empty the list of results on new query
        no_more_results_to_fetch = False
        while not no_more_results_to_fetch:
            response = requests.get(self.search_url, headers=HEADERS)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                results_list = soup.find(id="results").find_all(
                    "div", class_="otm-PropertyCardInfo")
                if len(results_list) == 0:
                    no_more_results_to_fetch = True
                else:
                    logger.debug(f"Retrieving {len(results_list)} results...")
                    for result_raw in results_list:
                        detail_url = self._parse_property_page_url(result_raw)
                        otmr = OnTheMarketResult(detail_url)
                        self.results.append(otmr)
            else:
                logger.error(f'Request failed with status code: {response.status_code}')
                break
            self.page_id += 1
        filtered_out_results = []
        if self.potential:
            for result in self.results:
                if not result.has_potential:
                    filtered_out_results.append(result)
            self.results = [x for x in self.results if x not in filtered_out_results]

        if len(self.keywords) > 0:
            logger.debug(f"Keywords are: {', '.join(self.keywords)}")
            for result in self.results:
                for keyword in self.keywords:
                    if keyword in result.description:
                        logger.debug(f"Keyword '{keyword}' found in {result.url}")
                        result.keywords_found.append(keyword)
            self.results = [x for x in self.results if len(x.keywords_found) > 0]

        logger.debug(f"Returning {len(self.results)} properties")
        return self.results

    @property
    def search_url(self):
        search_criteria = []
        search_criteria.append(f"radius={self.radius}")
        if self.min_price:
            search_criteria.append(f"min-price={self.min_price}")
        if self.max_price:
            search_criteria.append(f"max-price={self.max_price}")
        if self.min_bed:
            search_criteria.append(f"min-bedrooms={self.min_bed}")
        if self.max_bed:
            search_criteria.append(f"max-bedrooms={self.max_bed}")
        if self.property_type:
            if self.property_type == "house":
                search_criteria.append("prop-types=detached&prop-types=semi-detached&prop-types=terraced")
            else:
                search_criteria.append("prop-types=flats-apartments")
        search_criteria.append(f"page={self.page_id}")
        search_url = OTM_URL + f"{self.postcode}/?" + \
            "&".join(search_criteria)
        return search_url

    def _parse_property_page_url(self, result):
        return OTM_DETAIL_BASE_URL + result.find("span", class_="title").find("a").get("href")

    @property
    def average_price_per_sqm(self):
        return self.get_average_price_per_sqm_for_type()

    @property
    def average_price_per_sqm_per_type(self):
        average_price_per_type = {}
        for property_type in sorted(OnTheMarketSearch.property_types):
            average_price_per_type[property_type] = self.get_average_price_per_sqm_for_type(property_type)
        average_price_per_type["All"] = self.average_price_per_sqm
        return average_price_per_type

    def get_average_price_per_sqm_for_type(self, property_types: list = list(property_types)):
        non_zero_list = [x.price_per_sqm for x in self.results if x.price_per_sqm > 0 and OnTheMarketSearch.detailed_to_general_property_type_map.get(x.property_type, "Other") in property_types]
        erronous_per_sqm_prices = [x for x in self.results if len(non_zero_list) > 0 and abs(x.price_per_sqm / mean(non_zero_list) - 1) > 1]
        reasonable_list = [x.price_per_sqm for x in self.results if x.price_per_sqm > 0 and x not in erronous_per_sqm_prices and OnTheMarketSearch.detailed_to_general_property_type_map.get(x.property_type, "Other") in property_types]
        return {"price": int(mean(reasonable_list)) if len(reasonable_list) > 0 else 0, "sample_size": len(reasonable_list)}

    @property
    def results_count(self):
        return len(self.results)


class OnTheMarketResult():

    def __init__(self, url):
        self.url = url
        self.postcode = None
        self.price = None
        self.description = None
        self.bedrooms = None
        self.bathrooms = None
        self.sitting_rooms = None
        self.property_type = None
        self.is_new_built = None
        self.short_description = None
        self.days_since_added_or_reduced = None
        self.sqm_surface_area = None
        self.keywords_found =[]

        self._get_property_details(self.url)

    def _get_property_details(self, detail_url):
        response = requests.get(detail_url, headers=HEADERS)
        otm_full_details = ""
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Parse basic details
            self.price = self._parse_price(soup)
            self.sqm_surface_area = self._parse_surface_from_key_fact(soup)

            # Parse javascript details
            script_content = soup.find_all("script", type='text/javascript')[2].string
            if script_content:
                otm_script_tag = "__OTM__.jsonData = "
                start_index = script_content.find(otm_script_tag)
                if start_index != -1:
                    end_index = script_content.find(';\n', start_index)
                    if end_index != -1:
                        otm_full_details = json.loads(
                            script_content[start_index + len(otm_script_tag):end_index])
            header_data_json = json.loads(otm_full_details["header-data"]["data-layer"])
            self.postcode = header_data_json.get("postcode")
            self.description = otm_full_details.get("description")
            self.bedrooms = otm_full_details.get("bedrooms")
            self.bathrooms = otm_full_details.get("bathrooms")
            self.sitting_rooms = otm_full_details.get("sitting-rooms")
            self.property_type = otm_full_details.get("humanised-property-type")
            if self.property_type not in OnTheMarketSearch.detailed_to_general_property_type_map.keys():
                logger.warning(f"Property type not known: {self.property_type} ({self.url})")
            self.is_new_built = otm_full_details.get("new-home-flag")
            self.short_description = otm_full_details.get("property-title")
            self.days_since_added_or_reduced = otm_full_details.get("days-since-added-reduced")
            # If we haven't found the surface in the key facts, try again in the description
            if not self.sqm_surface_area:
                self.sqm_surface_area = self.parse_sqm_surface_area(self.description)

    @property
    def has_potential(self):
        keyword_or_phrases_for_potential = ["STPP", "Potential to extend", "Potential to develop", ]
        for keyword in keyword_or_phrases_for_potential:
            if keyword in self.description:
                return True
        return False

    def parse_sqm_surface_area(self, text: str) -> int:
        sqm_surface_area = 0
        sqm_pattern = r"(\d{1,3}(,?\d{3})*(\.\d*)?).?sq.?m"
        sqm_matches = re.findall(sqm_pattern, text)
        if len(sqm_matches) == 1:
            sqm_surface_area = int(float(sqm_matches[0][0].replace(",", "")))
        else:
            # Looking for sq ft if sq m not found:
            sqft_pattern = r"(\d{1,3}(,?\d{3})*).?sq.?ft"
            sqft_matches = re.findall(sqft_pattern, text)
            if len(sqft_matches) == 1:
                sqm_surface_area = int(float(sqft_matches[0][0].replace(",", "")) * 0.09290304)
        if sqm_surface_area < 30 and sqm_surface_area > 0:
            pass
        return sqm_surface_area

    def _parse_price(self, result):
        price_str = result.find(id="container").find(
            "div", class_="main otm-new").find("div", class_="otm-Price").text
        price_pattern = r"£(\d{1,3}(,\d{3})*)"
        price_matches = re.findall(price_pattern, price_str)
        if len(price_matches) == 1:
            return int(price_matches[0][0].replace(",", ""))
        else:
            logger.error(f"Couldn't parse price for {self.url} - text was: {price_str}")

    def _parse_surface_from_key_fact(self, result):
        for div in result.find(class_="otm-IconFeatures md:order-3").find_all(
            "div", class_="flex items-center mr-6 py-0.5"):
            retrieved_surface = self.parse_sqm_surface_area(div.text)
            if retrieved_surface:
                return retrieved_surface

    @property
    def price_per_sqm(self):
        return int(self.price / self.sqm_surface_area) if self.sqm_surface_area > 0 else 0

    @property
    def stamp_duty(self):
        return int(max(self.price - 425000, 0) * 0.05)
