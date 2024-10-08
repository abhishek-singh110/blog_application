# Blog Application

## Overview

This is a simple blog application built using Django. It allows users to sign up, log in, write blogs from the Django admin interface, and engage with blog content through comments and likes. The application also features advanced search functionality, including tagging, full-text search, stemming, ranking, and trigram similarity.

## Features

- **User Authentication**: 
  - Users can sign up and log in to their accounts.

- **Blog Management**: 
  - Blogs are created through the Django admin dashboard.

- **Blog List and Detail Views**: 
  - Users can view a list of blogs and click on individual blogs for detailed views.

- **Pagination**: 
  - The application displays 5 blogs per page for easy navigation.

- **Tagging Functionality**: 
  - users can search for blogs based on tags.

- **Full-Text Search**: 
  - Users can perform full-text searches on blog data.

- **Stemming and Ranking**: 
  - Search results are stemmed and ranked for better relevance.

- **Trigram Similarity Search**: 
  - Implemented search functionality that utilizes trigram similarity for improved search capabilities.

- **Comment System**: 
  - Users can leave comments on blog posts, and there is an option to like comments.

- **Email Sharing**: 
  - Users can share blog posts via email.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/blog-application.git
   cd blog-application


2. Create the Virtual environment:
   - python -m venv env
   - source env/bin/activate  # On Windows use `env\Scripts\activate`

3. Create the .env file (for reference i have shared the .env.example file):
   - put the valid credentials for email and database in the .env file.

4. Install the requirement.txt file:
   - pip install -r requirements.txt

5. Run the migrations:
   - python manage.py makemigrations
   - python manage.py migrate

6. Run the server: 
   - python manage.py runserver

## Usage
   - Navigate to the login/signup page to create an account or log in.
   - Access the Django admin interface at http://127.0.0.1:8000/admin/ to create and manage blogs.
   - View the list of blogs, read detailed blog posts, leave comments, and like comments.
