# TripAdvisorSpider
A Scrapy spider that scraps restaurants information in London 


### About
The RestoReviewSpider will scrap top rated restaurants in London, as listed on https://www.tripadvisor.co.uk/Restaurants-g186338-London_England.html


### Command line parameters

* max_resto: maximum number of restaurants to scrap
* max_review: maximum number of reviews to scrap per restaurants

sample command: 
scrapy RestoReviewSpider -a max_resto=100 -a max_review=200

