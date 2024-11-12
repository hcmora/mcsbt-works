
from movies import MovieServices

movie_services = MovieServices()

# Search for movie platform

movie_services.search_movie_in_platforms("Forrest Gump")

movie_services.show_amount_of_movies_per_country(country="US")
