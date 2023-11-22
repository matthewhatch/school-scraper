PUBLIC_SCHOOL_URL = 'https://nces.ed.gov/ccd/schoolsearch/school_list.asp?Search=1&SpecificSchlTypes=all&IncGrade=-1&LoGrade=-1&HiGrade=-1'
PRIVATE_SCHOOL_URL = 'https://nces.ed.gov/surveys/pss/privateschoolsearch/school_list.asp?Search=1&NumOfStudentsRange=more&IncGrade=13&LoGrade=-1&HiGrade=-1'
COLLEGE_URL = 'https://nces.ed.gov/collegenavigator/'
COLLEGE_HOST = 'nces.ed.gov'
REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", 
    "Accept-Encoding": "gzip, deflate, br", 
    "Accept-Language": "en-US,en;q=0.5", 
    "Referer": "https://www.google.com/", 
    "Upgrade-Insecure-Requests": "1", 
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
    "Sec-Fetch-Dest": "document", 
    "Sec-Fetch-Mode": "navigate", 
    "Sec-Fetch-Site": "cross-site", 
    "Sec-Fetch-User": "?1", 
    "Upgrade-Insecure-Requests": "1"
}

