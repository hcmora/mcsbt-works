import movies_module.movies

all_movies = movies_module.movies.MovieServices()

forest_gump = all_movies.search_movie_in_platforms(movie="the fifth element")

print(forest_gump)
