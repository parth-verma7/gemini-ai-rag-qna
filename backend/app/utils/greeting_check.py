from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Predefined greetings and concluding phrases
greetings = [
    "hello", 
    "how are you", 
    "what's up", 
    "how is it going"
]

concluding = [
    "thank you", 
    "thank you so much", 
    "it helped", 
    "thank you, it helped"
]

# Queries to compare
query1 = "What's up man?"
query2 = "Thanks, it worked"

# Combine predefined lists and queries into a single list
all_phrases = greetings + concluding + [query1, query2]

# Vectorize the text data
vectorizer = TfidfVectorizer()
vectors = vectorizer.fit_transform(all_phrases)

# Compute cosine similarity between all phrases
cos_sim = cosine_similarity(vectors)

# Define a helper function to find the most similar phrase
def find_most_similar(phrase_index, category_start, category_end, threshold=0.5):
    similarities = cos_sim[phrase_index, category_start:category_end]
    max_similarity = np.max(similarities)
    
    if max_similarity > threshold:
        max_index = np.argmax(similarities)
        return (max_index + category_start, max_similarity)
    
    return None

# Check if query1 is similar to greetings
similar_greeting = find_most_similar(len(greetings) + len(concluding), 0, len(greetings))

# Check if query2 is similar to concluding phrases
similar_concluding = find_most_similar(len(greetings) + len(concluding) + 1, len(greetings), len(greetings) + len(concluding))

# Output the result
if similar_greeting:
    print(f"Query1 ('{query1}') matches greeting: '{greetings[similar_greeting[0]]}' with similarity {similar_greeting[1]}")
else:
    print(f"Query1 ('{query1}') does not match any greeting.")

if similar_concluding:
    print(f"Query2 ('{query2}') matches concluding: '{concluding[similar_concluding[0] - len(greetings)]}' with similarity {similar_concluding[1]}")
else:
    print(f"Query2 ('{query2}') does not match any concluding phrase.")
