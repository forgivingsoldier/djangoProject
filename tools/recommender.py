from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import numpy as np

class ContentBasedRecommender:
    def __init__(self, items_df):
        self.items = items_df[['id', 'title']].values.tolist()  # change 'flavor_title' to 'title'
        self.tfidf_matrix = self._create_tf_idf_matrix(items_df['title'])  # change 'flavor_title' to 'title'
        self.item_similarities = linear_kernel(self.tfidf_matrix, self.tfidf_matrix)

    def _create_tf_idf_matrix(self, texts):
        vectorizer = TfidfVectorizer(analyzer='word', stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(texts)
        return tfidf_matrix

    def recommend_items(self, item_ids, num):
        item_id_list = [item[0] for item in self.items]  # 提取所有的'id'
        item_indices = [item_id_list.index(item_id) for item_id in item_ids]
        similarity_scores = np.mean([self.item_similarities[i] for i in item_indices], axis=0)
        similarity_scores = list(enumerate(similarity_scores))
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
        similarity_scores = similarity_scores[0:num]

        # 获取推荐的内容id
        recommend_item_indices = [i[0] for i in similarity_scores]
        recommend_item_ids = [self.items[i][0] for i in recommend_item_indices]  # change this line to get the id from the item

        return recommend_item_ids
