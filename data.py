import requests
from datetime import datetime



def getcurrentSeason():
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

def getcurrentYear():
    today = datetime.now()
    return today.year

def getAnime(season,year):
    query = '''
query getAiringAnime (
  $page: Int,
  $perPage: Int,
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
    Page(page: $page, perPage: $perPage ){
			pageInfo {
        total
        perPage 
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
      season
      seasonYear
      title {
        english
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
        'season' : str(season),
        'seasonYear' : str(year),
        'perPage' : 1000,
        'Page' : 1
     
    }

    url = 'https://graphql.anilist.co'
    response = requests.post(url, json={'query': query, 'variables': variables})
    data = response.json()
    data = data['data']['Page']['media']
    # data is a list of dicts
    data = sorted(data, key=lambda anime: anime['popularity'],reverse=True) 
    data = data[:10]
    return data

print(getAnime('FALL','2022'))
