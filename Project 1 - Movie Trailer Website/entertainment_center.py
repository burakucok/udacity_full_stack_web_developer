import fresh_tomatoes
import media

# this code first creates list of movies and then open web page with these movies
movies = []
#add movies
movies.append(media.Movie("The Shawshank Redemption",
                          "https://images-na.ssl-images-amazon.com/images/M/MV5BODU4MjU4NjIwNl5BMl5BanBnXkFtZTgwMDU2MjEyMDE@._V1_SY1000_CR0,0,672,1000_AL_.jpg",
                          "https://www.youtube.com/watch?v=6hB3S9bIaco"))

movies.append(media.Movie("The Godfather",
                          "https://images-na.ssl-images-amazon.com/images/M/MV5BZTRmNjQ1ZDYtNDgzMy00OGE0LWE4N2YtNTkzNWQ5ZDhlNGJmL2ltYWdlL2ltYWdlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_SY1000_CR0,0,704,1000_AL_.jpg",
                          "https://www.youtube.com/watch?v=sY1S34973zA"))

movies.append(media.Movie("The Godfather: Part II",
                          "https://images-na.ssl-images-amazon.com/images/M/MV5BMjZiNzIxNTQtNDc5Zi00YWY1LThkMTctMDgzYjY4YjI1YmQyL2ltYWdlL2ltYWdlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_SY1000_CR0,0,702,1000_AL_.jpg",
                          "https://www.youtube.com/watch?v=qJr92K_hKl0"))

movies.append(media.Movie("The Dark Knight",
                          "https://images-na.ssl-images-amazon.com/images/M/MV5BMTMxNTMwODM0NF5BMl5BanBnXkFtZTcwODAyMTk2Mw@@._V1_SY1000_CR0,0,675,1000_AL_.jpg",
                          "https://www.youtube.com/watch?v=EXeTwQWrcwY"))

movies.append(media.Movie("12 Angry Men",
                          "https://images-na.ssl-images-amazon.com/images/M/MV5BODQwOTc5MDM2N15BMl5BanBnXkFtZTcwODQxNTEzNA@@._V1_SY1000_CR0,0,666,1000_AL_.jpg",
                          "https://www.youtube.com/watch?v=A7CBKT0PWFA"))
#open web page
fresh_tomatoes.open_movies_page(movies)
