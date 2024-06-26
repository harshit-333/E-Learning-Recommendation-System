import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def recommend_courses(user_profile, threshold):
    course_ratings = pd.read_csv('C:/Users/91798/E-Learning Recommendation System/course_ratings.csv')
    all_items = course_ratings['item'].unique()
    user_data = pd.DataFrame(0, index=[user_profile.name], columns=user_profile.index)
    
    # Fill in the ratings provided and find common users
    user_data.loc[user_profile.name, user_profile.index] = user_profile.values
    common_users = course_ratings[course_ratings['item'].isin(user_profile.index)]['user'].unique()
    
    # Calculate cosine similarity
    similarity_scores = {}
    for user_id in common_users:
        user_ratings = course_ratings[course_ratings['user'] == user_id].set_index('item')['rating']
        user_ratings = user_ratings.reindex(user_data.columns, fill_value=0)
        temp = cosine_similarity([user_data.loc[user_profile.name]], [user_ratings])[0][0]
        if temp>threshold:
            similarity_scores[user_id] = temp
            
    sorted_users = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)
    
    # Generate recommendations
    recommended_courses = {}
    num_users_considered = {}
    for user_id, similarity_score in sorted_users:
        user_ratings = course_ratings[course_ratings['user'] == user_id].set_index('item')
        for item, rating in user_ratings.iterrows():
            if item not in user_profile.index: 
                if item not in recommended_courses:
                    recommended_courses[item] = 0
                    num_users_considered[item] = 0
                recommended_courses[item] += similarity_score * rating['rating']
                num_users_considered[item]+=1
    
    # Normalize the predicted scores between 0 and 3
    for item in recommended_courses:
        if num_users_considered[item] > 0:
            recommended_courses[item] /= num_users_considered[item]
    
    sorted_recommendations = sorted(recommended_courses.items(), key=lambda x: x[1], reverse=True)
    return sorted_recommendations

# Example
user_profile = pd.Series( {'BC0201EN': 3.0, 'BD0123EN': 3.0, 'TMP0105EN': 2.0}, name='target_user')
recommendations = recommend_courses(user_profile, 0.8)