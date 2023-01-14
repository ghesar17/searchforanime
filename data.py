import requests
from datetime import datetime


def getSeason():
    today = datetime.now()
    month = today.month
    if 1 <= month <= 3:
        return 'WINTER'
    if 4 <= month <= 6:
        return 'SPRING'
    if 7 <= month <= 9:
        return 'SUMMER'
    else:
        return 'FALL'

def getYear():
    today = datetime.now()
    return today.year

def getAnime():
    query = '''
query (
  $page: Int,
  $type: MediaType,
  $format: MediaFormat,
  $season: MediaSeason,
  $seasonYear: Int,
  $status: MediaStatus
  $genres: [String],
  $genresExclude: [String],
  $isAdult: Boolean = false, # Assign default value if isAdult is not included in our query variables 
  $sort: [MediaSort],
)

{
    Page(page: $page){
			pageInfo {
        total
        currentPage
        perPage
        lastPage
        hasNextPage 
      }      
    
    media (
      season: $season,
      seasonYear: $seasonYear
      status: $status
      type: $type,
      format: $format,
      genre_in: $genres,
      genre_not_in: $genresExclude,
      isAdult: $isAdult,
      sort: $sort,
    ) {
      id
      season
      seasonYear
      title {
        romaji
      }
      type
      format
      episodes
      genres
      averageScore
      popularity
      startDate {
        year
        month
        day
      }
      endDate {
        year
        month
        day
      }
      nextAiringEpisode {
        airingAt
        timeUntilAiring
        episode
      }
      coverImage {
        extraLarge
        large
        medium
        color
      }
  	}
	}
}
'''

    variables = {
        'type': 'ANIME',
        'season' : getSeason(),
        'seasonYear' : getYear(),
        'status' : 'RELEASING'
    }

    url = 'https://graphql.anilist.co'
    response = requests.post(url, json={'query': query, 'variables': variables})
    data = response.json()
    return data

print(getAnime())
