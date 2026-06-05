from django.db import models

class Book(models.Model):
    # Збільшуємо max_length до 128 згідно з вимогами тестів
    name = models.CharField(max_length=128, blank=False)
    description = models.CharField(max_length=256, blank=True)
    count = models.IntegerField(default=10)
    authors = models.ManyToManyField('author.Author', related_name='books')

    def __str__(self):
        authors_ids = [author.id for author in self.authors.all()]
        return f"'id': {self.id}, 'name': '{self.name}', 'description': '{self.description}', 'count': {self.count}, 'authors': {authors_ids}"

    def __repr__(self):
        return f"Book(id={self.id})"

    @staticmethod
    def create(name, description, count=10, authors=None):
        try:
            # Строгий ліміт тесту: повертаємо None тільки якщо назви немає або вона ДОЛША ЗА 128 символів
            if not name or len(name) > 128:
                return None
                
            if count is None:
                count = 10
                
            book = Book(name=name, description=description, count=count)
            book.save()
            
            if authors:
                for author in authors:
                    book.authors.add(author)
            return book
        except Exception:
            return None

    @staticmethod
    def get_by_id(book_id):
        try:
            return Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return None

    @staticmethod
    def delete_by_id(book_id):
        try:
            book = Book.objects.get(pk=book_id)
            book.delete()
            return True
        except Book.DoesNotExist:
            return False

    def add_authors(self, authors):
        if authors:
            for author in authors:
                if author not in self.authors.all():
                    self.authors.add(author)

    def remove_authors(self, authors):
        if authors:
            for author in authors:
                if author in self.authors.all():
                    self.authors.remove(author)

    def update(self, name=None, description=None, count=None):
        if name is not None:
            # Для оновлення ліміт залишаємо гнучким (до 128 символів), або прибираємо мінімум
            if len(name) > 128 or len(name) < 2:
                return
            self.name = name
        if description is not None:
            self.description = description
        if count is not None:
            self.count = count
        self.save()

    @staticmethod
    def get_all():
        return list(Book.objects.all())
