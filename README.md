# Book Recommendation System

A recommendation system that suggests books based on user preferences using FAISS (Facebook AI Similarity Search) for efficient similarity search.

## Overview

This project implements a book recommendation system that uses text embeddings and similarity search to find relevant book suggestions. It includes:

- A dataset of 1000 books with metadata like title, author, category, ratings etc.
- Vector embeddings generation using LLaMA model
- Similarity search using FAISS
- Web interface for searching recommendations

## Requirements

- Python 3.10+
- Key dependencies:
  - pandas
  - numpy
  - faiss-cpu
  - requests
  - Flask

## Project Structure
├── app.py # Flask web application 
├── templates/│ 
              └── index.html # Web interface template 
├── books_1000.csv # Book dataset 
├── books.index # FAISS index file 
├── book_recommendations.ipynb # Main recommendation notebook 
└── amenities_recommendations.ipynb # Additional recommendation example


## Installation

1. Create a conda environment:
```bash
conda create -n bookrec python=3.10
conda activate bookrec

pip install pandas numpy faiss-cpu flask requests

##usage 

1-Run the Flask web application:
  python app.py

2-Open http://localhost:5000 in your browser

3-Enter search criteria like:
  Book title
  Author name
  Number of pages
  Category
  Rating

4-View recommended books based on your preferences


##Features
Text-based similarity search using FAISS
Filtering by multiple criteria
Web interface for easy interaction
Fast and efficient recommendations
Support for various book metadata fields
Data Source

The book dataset contains 1000 books with fields like:
ISBN
Title
Author
Category
Description
Published year
Ratings
Number of pages


