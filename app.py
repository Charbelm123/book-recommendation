from flask import Flask, render_template, request
import pandas as pd
import requests
import faiss
import numpy as np


app = Flask(__name__)
books = pd.read_csv('books_1000.csv')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods = ['POST'])
def search():
    input = request.get_json()
    title = input.get('title')
    author = input.get('author')
    num_pages = input.get('num_pages')
    category = input.get('category')
    rating = input.get('rating')
    results = []
    if title:
        book = books[books['title'].str.contains(title.strip(), case=False)]
        if not book.empty:
            textual_representation = f"""   Title: {book['title']}
                                    Subtitle: {book['subtitle']}
                                    Authors: {book['authors']}
                                    Categories: {book['categories']}
                                    Description: {book['description']}
                                    Published Year: {book['published_year']}
                                    Average Rating: {book['average_rating']}
                                    Num Pages: {book['num_pages']}
                                    Rating Count: {book['ratings_count']}
                                    """
            req = requests.post("http://localhost:11434/api/embeddings",json={
                    "model" : "llama3.2",
                    "prompt" : textual_representation
                })
            embedding = req.json()['embedding']
            embedding = np.array(embedding).reshape(1, -1)
            index = faiss.read_index('books.index')
            distance, indices = index.search(embedding, 10)
            indices = indices.flatten()
            
            results = books['textual_representation'].iloc[indices].tolist()
        else:
            print("No book title found")
            if author:
                print(author)
                book = books[books['authors'].str.contains(author.strip(), case=False)]
                if not book.empty:
                    results = books[books['authors'].str.contains(author, case=False)].head(1)
                    results =  results['textual_representation'].tolist()
            else:
                print("No author found")
                if num_pages and not category and not rating:
                    results = books[books['num_pages'] == int(num_pages)].head(10)
                    results =  results['textual_representation'].tolist()
                elif category and not num_pages and not rating:
                    results = books[books['categories']== category].head(10)    
                    results =  results['textual_representation'].tolist()
                elif rating and not num_pages and not category:
                    results = books[books['average_rating'] == float(rating)].head(10)
                    results =  results['textual_representation'].tolist()
                elif num_pages and category and not rating:
                    results = books[(books['num_pages'] == int(num_pages)) & (books['categories']==category)].head(10)
                    results =  results['textual_representation'].tolist()  
                elif num_pages and rating and not category:
                    results = books[(books['num_pages'] == int(num_pages)) & (books['average_rating'] == float(rating))].head(10)
                    results =  results['textual_representation'].tolist()
                elif category and rating and not num_pages:
                    results = books[(books['categories']==category) & (books['average_rating'] == float(rating))].head(10)
                    results =  results['textual_representation'].tolist()
                elif num_pages and category and rating:
                    results = books[(books['num_pages'] == int(num_pages)) & (books['categories']==category) & (books['average_rating'] == float(rating))].head(10)
                    results =  results['textual_representation'].tolist()

    elif author:
        print("Author found")
        print(author)
        book = books[books['authors'].str.contains(author, case=False)]
        print(book)
        if not book.empty:
            results = books[books['authors'].str.contains(author, case=False)]
            results =  results['textual_representation'].tolist()
        else:
            print("No author found")
            if num_pages and not category and not rating:
                results = books[books['num_pages'] == int(num_pages)].head(10)
                results =  results['textual_representation'].tolist()
            elif category and not num_pages and not rating:
                results = books[books['categories']== category].head(10)    
                results =  results['textual_representation'].tolist()
            elif rating and not num_pages and not category:
                results = books[books['average_rating'] == float(rating)].head(10)
                results =  results['textual_representation'].tolist()
            elif num_pages and category and not rating:
                results = books[(books['num_pages'] == int(num_pages)) & (books['categories']==category)].head(10)
                results =  results['textual_representation'].tolist()  
            elif num_pages and rating and not category:
                results = books[(books['num_pages'] == int(num_pages)) & (books['average_rating'] == float(rating))].head(10)
                results =  results['textual_representation'].tolist()
            elif category and rating and not num_pages:
                results = books[(books['categories']==category) & (books['average_rating'] == float(rating))].head(10)
                results =  results['textual_representation'].tolist()
            elif num_pages and category and rating:
                results = books[(books['num_pages'] == int(num_pages)) & (books['categories']==category) & (books['average_rating'] == float(rating))].head(10)
                results =  results['textual_representation'].tolist()
    elif num_pages or category or rating:
        print("No title or author found")
        if num_pages and not category and not rating:
            results = books[books['num_pages'] == int(num_pages)].head(10)
            results =  results['textual_representation'].tolist()
        elif category and not num_pages and not rating:
            results = books[books['categories']== category].head(10)    
            results =  results['textual_representation'].tolist()
        elif rating and not num_pages and not category:
            results = books[books['average_rating'] == float(rating)].head(10)
            results =  results['textual_representation'].tolist()
        elif num_pages and category and not rating:
            results = books[(books['num_pages'] == int(num_pages)) & (books['categories']==category)].head(10)
            results =  results['textual_representation'].tolist()  
        elif num_pages and rating and not category:
            results = books[(books['num_pages'] == int(num_pages)) & (books['average_rating'] == float(rating))].head(10)
            results =  results['textual_representation'].tolist()
        elif category and rating and not num_pages:
            results = books[(books['categories']==category) & (books['average_rating'] == float(rating))].head(10)
            results =  results['textual_representation'].tolist()
        elif num_pages and category and rating:
            results = books[(books['num_pages'] == int(num_pages)) & (books['categories']==category) & (books['average_rating'] == float(rating))].head(10)
            results =  results['textual_representation'].tolist()
    else:
        results = books[(books['average_rating'] >= 4.0) & (books['ratings_count'].astype(float) >= 1000)].head(10)
        results =  results['textual_representation'].tolist()


    if results:
        return results
    return ["No results found for this query"]



if __name__=='__main__':
    app.run(debug=True) 