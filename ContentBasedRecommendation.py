import numpy as np
import pandas as pd

def generate_recommendations(enrolled_course_ids, threshold, include):
    if include==0:
        course_df = pd.read_csv('C:/Users/91798/E-Learning Recommendation System/filtered_courses.csv')
    else:
        course_df = pd.read_csv('C:/Users/91798/E-Learning Recommendation System/courses.csv')
        
    bows_df = pd.read_csv('C:/Users/91798/E-Learning Recommendation System/bows_df.csv')
    sim_matrix = pd.read_csv('C:/Users/91798/E-Learning Recommendation System/sim.csv').to_numpy()

    # Create index-id dictionaries
    grouped_df = bows_df.groupby(['doc_index', 'doc_id']).max().reset_index(drop=False)
    idx_id_dict = grouped_df[['doc_id']].to_dict()['doc_id']
    id_idx_dict = {v: k for k, v in idx_id_dict.items()}

    # Extract selected and unselected courses
    all_courses = set(course_df['COURSE_ID'])
    unselected_course_ids = all_courses.difference(enrolled_course_ids)

    # Generate recommendations
    res = {}
    for enrolled_course in enrolled_course_ids:
        for unselect_course in unselected_course_ids:
            if enrolled_course in id_idx_dict and unselect_course in id_idx_dict:
                idx1 = id_idx_dict[enrolled_course]
                idx2 = id_idx_dict[unselect_course]
                sim = sim_matrix[idx1][idx2]
                if sim > threshold:
                    if unselect_course not in res:
                        res[unselect_course] = (sim,enrolled_course)
                    else:
                        if sim >= res[unselect_course][0]:
                            res[unselect_course] = (sim,enrolled_course)
    sorted_recommendations = sorted(res.items(), key=lambda item: item[1][0], reverse=True)
    return sorted_recommendations

enrolled_course_ids = ['BC0201EN', 'BD0123EN', 'TMP0105EN']
threshold = 0.5
recommendations = generate_recommendations(enrolled_course_ids, threshold, 1)