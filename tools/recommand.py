from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import numpy as np

class ContentBasedRecommender:
    def __init__(self, items_df):
        self.item_ids = items_df['id'].tolist()
        self.tfidf_matrix = self._create_tf_idf_matrix(items_df['flavor_title'])
        self.item_similarities = linear_kernel(self.tfidf_matrix, self.tfidf_matrix)

    def _create_tf_idf_matrix(self, texts):
        vectorizer = TfidfVectorizer(analyzer='word', stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(texts)
        return tfidf_matrix

    def recommend_items(self, item_ids, num):
        item_indices = [self.item_ids.index(item_id) for item_id in item_ids]
        similarity_scores = np.mean([self.item_similarities[i] for i in item_indices], axis=0)
        similarity_scores = list(enumerate(similarity_scores))
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
        similarity_scores = similarity_scores[0:num]

        # 获取推荐的内容id
        recommend_item_indices = [i[0] for i in similarity_scores]
        recommend_item_ids = [self.item_ids[i] for i in recommend_item_indices]

        return recommend_item_ids
