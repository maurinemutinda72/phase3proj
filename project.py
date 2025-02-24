class Author:
    def __init__(self, name):
        if type(name) != str or len(name) == 0:
            raise Exception("Name must be a non-empty string")
        
        self._name = getattr(self, "_name", name)


    @property
    def name(self):
        return self._name

    def articles(self):
        return [article for article in Article._all_articles if article.author == self]

    def magazines(self):
        return list(set([article.magazine for article in self.articles()]))

    def add_article(self, magazine, title):
        return Article(self, magazine, title)

    def topic_areas(self):
        if len(self.articles()) == 0:
            return None
        return list(set([magazine.category for magazine in self.magazines()]))


class Magazine:
    _all_magazines = []

    def __init__(self, name, category):
        if type(name) != str or not (2 <= len(name) <= 16):
            raise Exception("Name must be a string between 2 and 16 characters")
        if type(category) != str or len(category) == 0:
            raise Exception("Category must be a non-empty string")

        self._name = name
        self._category = category
        Magazine._all_magazines.append(self)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        if type(new_name) != str or not (2 <= len(new_name) <= 16):
            raise Exception("New name must be a string between 2 and 16 characters")
        self._name = new_name

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, new_category):
        if type(new_category) != str or len(new_category) == 0:
            raise Exception("Category must be a non-empty string")
        self._category = new_category

    def articles(self):
        return [article for article in Article._all_articles if article.magazine == self]

    def contributors(self):
        return list(set([article.author for article in self.articles()]))

    def article_titles(self):
        if len(self.articles()) == 0:
            return None
        return [article.title for article in self.articles()]

    def contributing_authors(self):
        author_counts = {}
        for article in self.articles():
            author = article.author
            author_counts[author] = author_counts.get(author, 0) + 1

        frequent_authors = [author for author, count in author_counts.items() if count > 2]
        return frequent_authors if frequent_authors else None

    @classmethod
    def top_publisher(cls):
        if not Article._all_articles:
            return None
        return max(cls._all_magazines, key=lambda mag: len(mag.articles()), default=None)


class Article:
    _all_articles = []

    def __init__(self, author, magazine, title):
        if type(title) != str or not (5 <= len(title) <= 50):
            raise Exception("Title must be a string between 5 and 50 characters")

        self._author = author
        self._magazine = magazine
        self._title = title

        Article._all_articles.append(self)

    @property
    def title(self):
        return self._title

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, new_author):
        self._author = new_author

    @property
    def magazine(self):
        return self._magazine

    @magazine.setter
    def magazine(self, new_magazine):
        self._magazine = new_magazine
#Testing One-to-Many and Many-to-Many Relationships
# Create authors
author1 = Author("Alice")
author2 = Author("Bob")
author3 = Author("Charlie")

# Create magazines
mag1 = Magazine("Tech Times", "Technology")
mag2 = Magazine("Nature Weekly", "Science")
mag3 = Magazine("Health Digest", "Health")

# Create articles (establishing relationships)
article1 = author1.add_article(mag1, "Moringa tech expoze")
article2 = author1.add_article(mag2, "Quantum Computing")
article3 = author2.add_article(mag1, "Cybersecurity Trends")
article4 = author2.add_article(mag3, "Fitness ")
article5 = author3.add_article(mag1, "Robotics Future")
article6 = author1.add_article(mag1, "Machine Learning Breakthroughs")
article7 = author2.add_article(mag1, "SQL Gurus")
article8 = author2.add_article(mag1, "Tech Innovations")

# ONE-TO-MANY (One Author to Many Articles)
print(f"Articles by {author1.name}: {[a.title for a in author1.articles()]}")

# ONE-TO-MANY (One Magazine to Many Articles)
print(f"Articles in {mag1.name}: {[a.title for a in mag1.articles()]}")

# MANY-TO-MANY (One Author Writes for Multiple Magazines)
print(f"Magazines where {author2.name} has published: {[m.name for m in author2.magazines()]}")

# MANY-TO-MANY (One Magazine Has Multiple Authors)
print(f"Contributors to {mag1.name}: {[a.name for a in mag1.contributors()]}")

# Topic areas of an author
print(f"{author1.name}'s topic areas: {author1.topic_areas()}")

# Most active magazine (Top Publisher)
print(f"Top publisher: {Magazine.top_publisher().name}")
