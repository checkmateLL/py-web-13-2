import os
import django
import pymongo
import sys
import psycopg2


os.environ.update({
    'DJANGO_SETTINGS_MODULE': 'quotes_site.settings',
    'DB_HOST': 'db', 
    'DB_PORT': '5432', 
})

django.setup()


from quotes.models import Author, Quote

# MongoDB connection settings
client = pymongo.MongoClient(
    "mongodb+srv://goitlearn:FvTP85uVCXJ8443r@cluster0.sdejq.mongodb.net/?retryWrites=true&w=majority")
db = client['homework']

def migrate_authors():
    authors_collection = db['authors']
    print("Starting author migration...")
    count = 0
    for author_data in authors_collection.find():
        try:
            
            author, created = Author.objects.get_or_create(
                mongo_id=str(author_data['_id']),  
                defaults={
                    'fullname': author_data['fullname'],
                    'born_date': author_data['born_date'],
                    'born_location': author_data['born_location'],
                    'description': author_data['description'],
                }
            )
            if not created:
                
                author.mongo_id = str(author_data['_id'])
                author.save()
            count += 1 if created else 0
            print(f"Processed author: {author.fullname} ({'created' if created else 'existing'})")
        except Exception as e:
            print(f"Error processing author {author_data['fullname']}: {str(e)}")
    print(f"Finished migrating authors. Created {count} new authors.")

def migrate_quotes():
    quotes_collection = db['quotes']
    print("Starting quote migration...")
    count = 0
    for quote_data in quotes_collection.find():
        try:
            # Find the author using mongo_id that matches quote_data['author']
            author = Author.objects.get(mongo_id=str(quote_data['author']))
            quote, created = Quote.objects.get_or_create(
                mongo_id=str(quote_data['_id']),  # Use MongoDB _id as mongo_id for quotes
                defaults={
                    'author': author,
                    'quote': quote_data['quote'],
                    'tags': ', '.join(quote_data['tags'])
                }
            )
            count += 1 if created else 0
            print(f"Processed quote by {author.fullname} ({'created' if created else 'existing'})")
        except Author.DoesNotExist:
            print(f"Warning: Author not found for quote: {quote_data['author']}")
        except Exception as e:
            print(f"Error processing quote: {str(e)}")
    print(f"Finished migrating quotes. Created {count} new quotes.")

def check_database_connection():
    from django.db import connections
    from django.db.utils import OperationalError

    print("Checking database connection...")
    try:
        db_conn = connections['default']
        db_conn.cursor()
        print("Successfully connected to the database!")
        return True
    except OperationalError as e:
        print(f"Database connection failed: {str(e)}")
        print("\nPlease ensure:")
        print("1. Docker containers are running (docker-compose up)")
        print("2. PostgreSQL port 5432 is exposed and accessible")
        print("3. Database credentials are correct")
        return False

if __name__ == '__main__':
    try:
        print("Starting migration process...")

        
        if not check_database_connection():
            sys.exit(1)

        migrate_authors()
        migrate_quotes()
        print("Migration completed successfully!")
    except Exception as e:
        print(f"Error during migration: {str(e)}")
        sys.exit(1)
