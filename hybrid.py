def hybrid_recommendation(collaborative_rec, content_rec):
    collaborative_rec_dict = {}
    for course, score in collaborative_rec[:5]:
        collaborative_rec_dict[course] = score
    for course, rating_info in content_rec:
        collaborative_rec_dict[course] = rating_info[0] * collaborative_rec_dict[rating_info[1]]
    sorted_recommendations = sorted(collaborative_rec_dict.items(), key=lambda item: item[1], reverse=True)
    return sorted_recommendations