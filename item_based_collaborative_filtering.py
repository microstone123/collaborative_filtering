

######################
# 1. Data Preprocessing
######################

# imports and display settings
import pandas as pd
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 500)
pd.set_option('display.expand_frame_repr', False)

# uploading data
movie = pd.read_csv('datasets/movie_lens_dataset/movie.csv')
rating = pd.read_csv('datasets/movie_lens_dataset/rating.csv')
df = movie.merge(rating, how="left", on="movieId")
df.head()


######################
# 2. Creating User-Movie Dataframe
######################

# Selecting movies with more than 1000 ratings

# number of ratings for movies
comment_counts = pd.DataFrame(df["title"].value_counts())

# movies with less tahn 1000 ratings
rare_movies = comment_counts[comment_counts["title"] <= 1000].index

# movies with more than 1000 ratings
common_movies = df[~df["title"].isin(rare_movies)]

common_movies.head()

# user-movie df
user_movie_df = common_movies.pivot_table(index=["userId"],
                                          columns=["title"],
                                          values="rating")
user_movie_df.columns


######################
# 3. Item-Based 电影推荐
######################

"""
- 电影名称作为列，用户作为行。
- 此时，当我们看一部电影与其他电影的相关性时，就好像在看相关性在两个变量之间，我们发现电影的相似性。
"""

# 手动选择电影
movie_name = 'Limitless (2011)'

# 检查相关性
movie_name = user_movie_df[movie_name]
user_movie_df.corrwith(movie_name).sort_values(ascending=False).head(10)

# 随机选择电影
movie_name = pd.Series(user_movie_df.columns).sample(1).values[0]
movie_name = user_movie_df[movie_name]
user_movie_df.corrwith(movie_name).sort_values(ascending=False).head(10)


# 用关键字检查电影名称
def check_film(keyword, user_movie_df):
    return [col for col in user_movie_df.columns if keyword in col]

check_film("Limit", user_movie_df)
