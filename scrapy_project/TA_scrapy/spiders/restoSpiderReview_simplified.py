# Logging packages
import logging
import logzero
from logzero import logger

import math

# Scrapy packages
import scrapy
from TA_scrapy.items import ReviewRestoItem    
from TA_scrapy.spiders import get_info         

NAME = 'a.HEADING::text'
SCORE = '//*[@id="HEADING"]/div[2]/span[1]/span/@class'
DATE = "span.ratingDate.relativeDate::attr(title)"
TITLE = "span.noQuotes::text"
REVIEW_TEXT = "p.partial_entry::text"
REVIEW_LANG = "div.prw_reviews_google_translate_button_hsx"


class RestoReviewSpider(scrapy.Spider):
    name = "RestoReviewSpider"

    def __init__(self, *args, **kwargs): 
        super(RestoReviewSpider, self).__init__(*args, **kwargs)

        # Set logging level
        logzero.loglevel(logging.WARNING)
        
        # Mmax number of review and resto
        self.resto_per_page = 30
        self.review_per_page = 10
    
        max_resto = kwargs.get('max_resto')
        if max_resto:
            self.max_resto_page = math.ceil(int(max_resto)/self.resto_per_page)
        else:
            self.max_resto_page = None
        
        
        max_review = kwargs.get('max_review')
        if max_review:
            self.max_review_page = math.ceil(int(max_review)/self.review_per_page)
        else:
            self.max_review_page = None
        
        logger.info("max_resto: {}".format(max_resto))
        logger.info("max_resto_page: {}".format(self.max_resto_page))
        logger.info("max_review: {}".format(max_review))
        logger.info("max_review_page: {}".format(self.max_review_page))
        


        # To track the evolution of scrapping
        self.main_nb = 0
        self.resto_nb = 0
        self.review_nb = 0
        

    def start_requests(self):
        """ Give the urls to follow to scrapy
        - function automatically called when using "scrapy crawl my_spider"
        """

        # Basic restaurant page on TripAdvisor GreaterLondon
        url = 'https://www.tripadvisor.co.uk/Restaurants-g186338-London_England.html'
        yield scrapy.Request(url=url, callback=self.parse)

   
    def parse(self, response):
        """MAIN PARSING : Start from a classical reastaurant page
            - Usually there are 30 restaurants per page
            - 
        """

        # Display a message in the console
        logger.warn(' > PARSING NEW MAIN PAGE OF RESTO ({})'.format(self.main_nb))
        self.main_nb += 1

        # Get the list of the 30 restaurants of the page
        restaurant_urls = get_info.get_urls_resto_in_main_search_page(response)
        
        # For each url : follow restaurant url to get the reviews
        for restaurant_url in restaurant_urls:
            logger.warn('> New restaurant detected : {}'.format(restaurant_url))
            yield response.follow(url=restaurant_url, callback=self.parse_resto)

        
        
        # Get next page information
        next_page, next_page_number = get_info.get_urls_next_list_of_restos(response)
        
        # Follow the page if we decide to
        if get_info.go_to_next_page(next_page, next_page_number, max_page=self.max_resto_page):
            yield response.follow(next_page, callback=self.parse)


    def parse_resto(self, response):
        """SECOND PARSING : Given a restaurant, get each review url and get to parse it
            - Usually there are 10 comments per page
        """
        logger.warn(' > PARSING NEW RESTO PAGE ({})'.format(self.resto_nb))
        self.resto_nb += 1

        # Get the list of reviews on the restaurant page

        urls_review = get_info.get_urls_review(response)
        

        # For each review open the link and parse it into the parse_review method
        for url_review in urls_review:
             yield response.follow(url=url_review, callback=self.parse_review)

        
        # Get next page information
        next_page, next_page_number = get_info.get_urls_next_list_of_reviews(response)
        
  
        # Follow the page if we decide to
        if get_info.go_to_next_page(next_page, next_page_number, max_page=self.max_review_page):
            yield response.follow(next_page, callback=self.parse_resto)

        



    def parse_review(self, response):
        """FINAL PARSING : Open a specific page with review and client opinion
            - Read these data and store them
            - Get all the data you can find and that you believe interesting
        """

        # Count the number of review scrapped
        self.review_nb += 1

        review_item = {}
        
        name = response.css(NAME).extract_first().strip()
        score = response.xpath(SCORE).extract_first().split("_")[-1]
        date = response.css(DATE).extract_first()
        title = response.css(TITLE).extract_first()
        text = response.css(REVIEW_TEXT).extract_first().replace("\n", "")

        
        review_item['name'] = name
        review_item['score'] = score
        review_item['date'] = date
        review_item['title'] = title
        review_item['text'] = text

        
        yield review_item 



