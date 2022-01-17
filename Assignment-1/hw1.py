#Task 1.1
def read_ratings_data(f):

    movie_ratings_dict = {}

    for line in f:

        data = line.rstrip().split('|')
        
        if data[0] in movie_ratings_dict:
            
            movie_ratings_dict[data[0]].append(data[1])
        else:
            movie_ratings_dict[data[0]] = [data[1]]

    
    return movie_ratings_dict

#Task 1.2
def read_movie_genre(f):

    movies = {}

    for line in f:

        data = line.rstrip().split('|')

        movies[data[2]] = data[0]
    
    return movies

#Task 2.1
def create_genre_dict(movie_to_genre):

    genre_to_movie = {}
    
    for key, item in movie_to_genre.items():
        genre_to_movie[item] = genre_to_movie.get(item, []) + [key]
    
    return genre_to_movie

#Task 2.2
def calculate_average_rating(movie_ratings_dict):

    average_rating = {}

    for key, value in movie_ratings_dict.items():

        value = list(map(float, value))

        avg = lambda x : sum(x) / len(x)

        average_rating[key] = avg(value)
    
    return average_rating

#Task 3.1
def get_popular_movies(average_rating, n = 10):

    top_n_movies = {}

    top_movies = {key: value for key, value in sorted(average_rating.items(), reverse = True, key = lambda item: item[1])}

    top_n_movies = dict(list(top_movies.items())[:n])

    return top_n_movies

#Task 3.2
def filter_movies(average_rating, threshold_rating = 3):

    top_movies = {key: value for key, value in average_rating.items() if value >= threshold_rating}

    top_movies_sorted = {key: value for key, value in sorted(top_movies.items(), reverse = True, key = lambda item: item[1])}

    return top_movies_sorted

#Task 3.3
def get_popular_in_genre(genre, genre_to_movies, movie_average_rating, n = 5):

    popular_genre = {}
    
    target_genre = genre_to_movies[genre]

    for item in target_genre:

        popular_genre[item] = movie_average_rating[item]
    
    popular_genre_sorted = {key: value for key, value in sorted(popular_genre.items(), reverse = True, key = lambda item: item[1])}

    top_popular_genre_n = dict(list(popular_genre_sorted.items())[:n])

    return top_popular_genre_n

#Task 3.4
def get_genre_rating(genre, genre_to_movies, movie_average_rating):

    target_genre = genre_to_movies[genre]

    total_ratings = 0

    for item in target_genre:

        total_ratings += movie_average_rating[item]
    
    genre_average = total_ratings / len(target_genre)

    return genre_average

#Task 3.5
def genre_popularity(genre_to_movies, movie_average_rating, n = 5):

    genre_ratings = {}

    for key, value in genre_to_movies.items():
        
        movie_average_rating_temp = {}

        for item in value:

            movie_average_rating_temp[item] = movie_average_rating[item]

        genre_ratings[key] = get_genre_rating(key, {key: genre_to_movies[key]}, movie_average_rating_temp)
    
    popular_genre_sorted = {key: value for key, value in sorted(genre_ratings.items(), reverse = True, key = lambda item: item[1])}

    top_popular_genre_n = dict(list(popular_genre_sorted.items())[:n])


    return top_popular_genre_n

#Task 4.1
def read_user_ratings(f):

    user_ratings_dict = {}

    for line in f:

        data = line.rstrip().split('|')
        
        if data[2] in user_ratings_dict:

            user_ratings_dict[data[2]].append((data[0], data[1]))
        
        else:

            user_ratings_dict[data[2]] = [(data[0], data[1])]


    return user_ratings_dict

#Task 4.2
def get_user_genre(user_id, user_ratings_dict, movie_to_genre):
    
    user_id = str(user_id)

    data = user_ratings_dict[user_id]
    
    user_genre_ratings = {}

    for item in data:

        genre = movie_to_genre[item[0]]

        if genre in user_genre_ratings:

            temp = user_genre_ratings[genre][1]
            
            user_genre_ratings[genre][1] += 1
            user_genre_ratings[genre][0] = ((user_genre_ratings[genre][0] * temp) + float(item[1])) / user_genre_ratings[genre][1]
        
        else:

            user_genre_ratings[genre] = [float(item[1]), 1]
    
    user_genre_ratings_cleaned = {}
    
    for key, value in user_genre_ratings.items():

        user_genre_ratings_cleaned[key] = value[0]
   
    return max(user_genre_ratings_cleaned, key = user_genre_ratings_cleaned.get)

#Task 4.3
def recommend_movies(user_id, user_ratings_dict, movie_to_genre, movie_to_average):

    user_id = str(user_id)
    
    top_genre = get_user_genre(user_id, user_ratings_dict, movie_to_genre)
    
    recommended_movies = {}

    for key, value in movie_to_genre.items():
        
        if value == top_genre:
            
            recommended_movies[key] = movie_to_average[key]
        
    user_movies = user_ratings_dict[user_id]

    for item in user_movies:

        if item[0] in recommended_movies:

            del recommended_movies[item[0]]
    
    recommended_movies_sorted = {key: value for key, value in sorted(recommended_movies.items(), reverse = True, key = lambda item: item[1])}

    top_3_recommended_movies = dict(list(recommended_movies_sorted.items())[:3])

    return top_3_recommended_movies

#Task1.1

#f = open('movieRatingSample.txt', 'r')
#print(read_ratings_data(f))

#Task1.2

#f = open('genreMovieSample.txt', 'r')
#print(read_movie_genre(f))

#Task 2.1

#f = open('genreMovieSample.txt', 'r')
#print(create_genre_dict(read_movie_genre(f)))

#Task 2.2 - Does number of decimal places matter?

#f = open('movieRatingSample.txt', 'r')
#print(calculate_average_rating(read_ratings_data(f)))

#Task 3.1

#f = open('movieRatingSample.txt', 'r')
#print(get_popular_movies(calculate_average_rating(read_ratings_data(f)),1000000))

#Task 3.2

#f = open('movieRatingSample.txt', 'r')
#print(filter_movies(calculate_average_rating(read_ratings_data(f)),1))

#Task 3.3

#f = open('genreMovieSample.txt', 'r')
#f1 = open('movieRatingSample.txt', 'r')
#print(get_popular_in_genre('Adventure', create_genre_dict(read_movie_genre(f)), calculate_average_rating(read_ratings_data(f1))))

#Task 3.4 - Does number of decimal places matter?

#f = open('genreMovieSample.txt', 'r')
#f1 = open('movieRatingSample.txt', 'r')
#print(get_genre_rating('Adventure', create_genre_dict(read_movie_genre(f)), calculate_average_rating(read_ratings_data(f1))))

#Task 3.5

#f = open('genreMovieSample.txt', 'r')
#f1 = open('movieRatingSample.txt', 'r')
#print(genre_popularity(create_genre_dict(read_movie_genre(f)), calculate_average_rating(read_ratings_data(f1))))

#Task 4.1

#f = open('movieRatingSample.txt', 'r')
#print(read_user_ratings(f))

#Task 4.2

#f = open('movieRatingSample.txt', 'r')
#f1 = open('genreMovieSample.txt', 'r')
#print(get_user_genre(6, read_user_ratings(f), read_movie_genre(f1)))

#Task 4.3

f = open('movieRatingSample.txt', 'r')
user_movie_ratings = read_user_ratings(f)
f.close()

f1 = open('genreMovieSample.txt', 'r')

f = open('movieRatingSample.txt', 'r')
movie_to_average = calculate_average_rating(read_ratings_data(f))
f.close()

print(recommend_movies(1, user_movie_ratings, read_movie_genre(f1), movie_to_average))