# TripAdvisorSpider
A Scrapy spider that scraps restaurants information in London 


### About
The RestoReviewSpider will scrap top rated restaurants in London, as listed on https://www.tripadvisor.co.uk/Restaurants-g186338-London_England.html

The results will be written as a Reviews.csv file. This can be changed in settings.py. Here are a few columns from the result file:


| name           | score | date             | title                  | text                                              |   
|----------------|-------|------------------|------------------------|---------------------------------------------------|
| Taste Of Nawab | 50    | 27 December 2020 | Consistently wonderful | Taste of Nawab never disappoints. I’ve been go... |   
| Figo Stratford | 50    | 3 January 2021   | Lovely environment     | This is a really good restaurant. Excellent se... |   
| The Gojk       | 50    | 28 August 2020   | Great                  | Great place, very cozzy and friendly.2 levels ... |   


Note that:
* Each review will have its own entry and there will be no assumed ordering.
* 'text' field will contain the full review. '...' are used here for display purpose.


### Command line parameters

* max_resto: maximum number of restaurants to scrap
* max_review: maximum number of reviews to scrap per restaurants

sample command: 
scrapy RestoReviewSpider -a max_resto=100 -a max_review=200

