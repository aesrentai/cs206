from urllib.parse import urlparse
import json
import os
import requests
import re

'''
Given a fact, retrieves a list of related sources
'''

WHITELIST = [
    r"(www\.)?cdc\.gov",
    r"(www\.)?who\.int",
    r"(www\.)?cancer\.org",
    r"(www\.)?cancer\.gov",
    r"(www\.)?ncbi.nlm.nih\.gov",
    r"(www\.)?nhs\.uk",
    r"(www\.)?webmd\.com",
    r"(www\.)?sciencedirect\.com",
    r"(www\.)?hopkinsmedicine\.org",
]

APIKEY=os.environ['BING_SEARCH_V7_SUBSCRIPTION_KEY']
ENDPOINT="https://api.bing.microsoft.com/v7.0/search"

#NOREQUEST=False
NOREQUEST=False
REQUEST=[
    {'id': 'https://api.bing.microsoft.com/api/v7/#WebPages.0', 
     'name': "COVID-19: Who's at higher risk of serious symptoms?", 
     'url': 'https://www.mayoclinic.org/diseases-conditions/coronavirus/in-depth/coronavirus-who-is-at-risk/art-20483301', 'isFamilyFriendly': True, 'displayUrl': 'https://www.mayoclinic.org/.../in-depth/coronavirus-who-is-at-risk/art-20483301', 'snippet': 'The risk of developing dangerous symptoms of COVID-19 may be increased in people who are older. The risk may also be increased in people of any age who have other serious health problems — such as heart or lung conditions, weakened immune systems, obesity, or diabetes.', 'dateLastCrawled': '2023-03-04T03:12:00.0000000Z', 'language': 'en', 'isNavigational': False}, {'id': 'https://api.bing.microsoft.com/api/v7/#WebPages.1', 'name': 'Factors That Affect Your Risk of Getting Very Sick from COVID-19', 'url': 'https://www.cdc.gov/coronavirus/2019-ncov/your-health/risks-getting-very-sick.html', 'isFamilyFriendly': True, 'displayUrl': 'https://www.cdc.gov/coronavirus/2019-ncov/your-health/risks-getting-very-sick.html', 'snippet': 'Certain underlying health conditions you have (for example, obesity or chronic obstructive pulmonary disorder) may affect your risk of becoming very sick if youget COVID-19. Often, the more health conditions you have, the higher your risk. Certain conditions increase your risk more than others.', 'dateLastCrawled': '2023-03-05T06:56:00.0000000Z', 'language': 'en', 'isNavigational': False}, {'id': 'https://api.bing.microsoft.com/api/v7/#WebPages.2', 'name': 'Coronavirus disease 2019 (COVID-19) - Symptoms and causes', 'url': 'https://www.mayoclinic.org/diseases-conditions/coronavirus/symptoms-causes/syc-20479963', 'isFamilyFriendly': True, 'displayUrl': 'https://www.mayoclinic.org/diseases-conditions/coronavirus/symptoms-causes/syc-20479963', 'snippet': 'Certain medical conditions that may increase the risk of serious illness from COVID-19 include: Serious heart diseases, such as heart failure, coronary artery disease or cardiomyopathy Cancer Chronic obstructive pulmonary disease (COPD) Type 1 or type 2 diabetes Overweight, obesity or severe obesity High blood pressure Smoking', 'dateLastCrawled': '2023-03-05T11:36:00.0000000Z', 'language': 'en', 'isNavigational': False}, {'id': 'https://api.bing.microsoft.com/api/v7/#WebPages.3', 'name': 'Understanding Risk | CDC', 'url': 'https://www.cdc.gov/coronavirus/2019-ncov/your-health/understanding-risk.html', 'isFamilyFriendly': True, 'displayUrl': 'https://www.cdc.gov/coronavirus/2019-ncov/your-health/understanding-risk.html', 'snippet': 'Risk of Getting COVID-19 Risk of Getting Very Sick Information for Specific Groups Older Adults People Who Are Immunocompromised People with Medical Conditions People with Asthma Pregnant and Recently Pregnant People Risk for COVID-19 Infection, Hospitalization, and Death Age Group Rate Ratios Race and Ethnicity Rate Ratios', 'dateLastCrawled': '2023-03-06T03:44:00.0000000Z', 'language': 'en', 'isNavigational': False}, {'id': 'https://api.bing.microsoft.com/api/v7/#WebPages.4', 'name': 'COVID-19 Risk Factors: A Comprehensive List - Healthline', 'url': 'https://www.healthline.com/health/covid-risk-factors', 'isFamilyFriendly': True, 'displayUrl': 'https://www.healthline.com/health/covid-risk-factors', 'snippet': 'According to the National Institutes of Health (NIH), COVID-19 can increase the risk of blood clots and other complications. People with blood clotting disorders may be at a higher risk of...', 'dateLastCrawled': '2023-03-06T11:56:00.0000000Z', 'language': 'en', 'isNavigational': False}, {'id': 'https://api.bing.microsoft.com/api/v7/#WebPages.5', 'name': 'Who is Most at Risk for Coronavirus (COVID-19)? - WebMD', 'url': 'https://www.webmd.com/covid/whos-at-risk-covid-19','isFamilyFriendly': True, 'displayUrl': 'https://www.webmd.com/covid/whos-at-risk-covid-19', 'snippet': 'But kids with one or more other health conditions have a higher risk of severe COVID-19. These include: Long-term lung disease, including moderate to severe asthma Diabetes Heart disease or...', 'dateLastCrawled': '2023-03-06T05:55:00.0000000Z', 'language': 'en', 'isNavigational': False}, {'id': 'https://api.bing.microsoft.com/api/v7/#WebPages.6', 'name': 'People with Long COVID Have Higher Risk of Early Death | Time', 'url': 'https://time.com/6260071/long-covid-health-risks/', 'isFamilyFriendly': True, 'displayUrl': 'https://time.com/6260071/long-covid-health-risks', 'snippet': 'In the year after their COVID-19 diagnoses, people with Long COVID were significantly more likely to seek care for health problems including irregular heartbeats, blood clots, strokes, heart...', 'dateLastCrawled': '2023-03-07T13:44:00.0000000Z', 'language': 'en', 'isNavigational': False}, {'id': 'https://api.bing.microsoft.com/api/v7/#WebPages.7', 'name': 'How badis COVID-19 in the Sacramento area? Here’s latest | The ...', 'url': 'https://www.sacbee.com/news/coronavirus/article272707395.html', 'isFamilyFriendly': True, 'displayUrl': 'https://www.sacbee.com/news/coronavirus/article272707395.html', 'snippet': 'According to the state’s COVID dashboard, Sacramento County has a seven-day average case rate of 6.8 cases per 100,000. Nearby counties Placer, Yolo and El Dorado are also at the medium ...', 'dateLastCrawled': '2023-03-05T15:28:00.0000000Z', 'language': 'en', 'isNavigational': False}, {'id': 'https://api.bing.microsoft.com/api/v7/#WebPages.8', 'name': 'Where do I need a mask in IL? See latest CDC COVID-19 data | Belleville ...', 'url': 'https://www.bnd.com/news/coronavirus/article272723305.html', 'isFamilyFriendly': True, 'displayUrl': 'https://www.bnd.com/news/coronavirus/article272723305.html', 'snippet': 'IDPH continues to monitor COVID-19 and other respiratory diseases closely throughout Illinois, with extra attention towards those most at-risk. Treatments continue to be effective, but timingis ...', 'dateLastCrawled': '2023-03-07T02:28:00.0000000Z', 'language': 'en', 'isNavigational': False}, {'id': 'https://api.bing.microsoft.com/api/v7/#WebPages.9', 'name': 'COVID-19 advice - High risk groups | WHO Western Pacific', 'url': 'https://www.who.int/westernpacific/emergencies/covid-19/information/high-risk-groups', 'thumbnailUrl': 'https://www.bing.com/th?id=OIP.TTm_TfFq_ktwnXzV8Quq5AHaEO&w=80&h=80&c=1&pid=5.1', 'isFamilyFriendly': True, 'displayUrl': 'https://www.who.int/westernpacific/emergencies/covid-19/information/high-risk-groups', 'snippet': 'COVID-19 is often more severe in people who are older than 60 years or who have health conditions like lung or heart disease, diabetes or conditions that affect their immune system. If you’re at high risk, know what to do, and take the right actions now to protect yourself. If you’re not at high risk, do your part to prevent the spread of ...', 'dateLastCrawled': '2023-03-05T09:33:00.0000000Z', 'language': 'en', 'isNavigational': False}]
class SearchResult:
    def __init__(self, url, title, description):
        self.url = url
        self.title = title
        self.description = description

    def __repr__(self):
        return f"SearchResult(Title={self.title}, URL={self.url}, Description={self.description})"

def _filter_sources(sources: list[SearchResult]) -> list[SearchResult]:
    ret = []
    for source in sources:
        parts = urlparse(source.url)
        if any(re.match(pattern, parts.netloc) is not None for pattern in WHITELIST):
            ret.append(source)
    return ret

def _make_request(query: str) -> list[SearchResult]:
    params = { 'q': query }
    headers = { 'Ocp-Apim-Subscription-Key': APIKEY }

    ret = []
    if NOREQUEST:
        for page in REQUEST:
            ret.append(SearchResult(page["url"], page["name"], page["snippet"]))
        return ret

    try:
        response = requests.get(ENDPOINT, headers=headers, params=params)

        data = json.loads(response.text)
        pages = data["webPages"]["value"]
        for page in pages:
            ret.append(SearchResult(page["url"], page["name"], page["snippet"]))
    # TODO, ADDRESS THIS
    except Exception as ex:
        print(data)
        raise ex
    return ret

def get_sources(query: str):
    sources = _make_request(query)
    return _filter_sources(sources)

if __name__ == '__main__':
    sources = get_sources("Risk for COVID 19")
    preliminary_sources = []
    if NOREQUEST:
        for source in REQUEST:
            preliminary_sources.append(SearchResult(source["url"], source["name"], source["snippet"]))
    else:
        preliminary_sources = sources
    filtered = _filter_sources(preliminary_sources)
    print(filtered)
    print(len(filtered))
