## School Scraper
#### 

install
```
git clone https://github.com/matthewhatch/school-scraper.git
cd school-scraper
pip install -r requirements.txt
```

Create SQL database
1. Create a local or remote database and store the connection information in database.ini (see example)
2. Run the SQL scripts in the `sql` folder

Create OpenSearch
1. Create new instance of OpenSearch in AWS
2. Store Connection information in opensearch.ini (see example)
usage
```
# scrape schools in Alaska
python ./school-scraper.py --scraper school --state AK

# scrape colleges in Rhode Island
python ./school-scraper.py --scraper college --state RI

#scrape all colleges in all states
python ./school-scraper.py --scraper college
```
