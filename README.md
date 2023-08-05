## Scrapy it

Extracting vacancies *(on the example of vacancies containing the word 'Python')* from a job search site.

### Getting Started

* сlone repository
* install requirements:  
`pip install -r requirements.txt`
* run spider *(may need this command first: `cd workua`)*:  
`scrapy crawl vacancies -o <filename>.jsonl`,  
where `<filename>` - file name to save  

Example of found vacancies: `vacancies.jsonl`.  

You can change the `start_urls` in the file `workua/workua/spiders/workua.py`, 
but the job search site must be the same.