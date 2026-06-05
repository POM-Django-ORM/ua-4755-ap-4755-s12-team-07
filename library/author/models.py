from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=20, blank=False)
    surname = models.CharField(max_length=20, blank=False)
    patronymic = models.CharField(max_length=20, blank=False)

    def __str__(self):
        # Рядок без фігурних дужок на початку та в кінці під шаблон тесту
        return f"'id': {self.id}, 'name': '{self.name}', 'surname': '{self.surname}', 'patronymic': '{self.patronymic}'"

    def __repr__(self):
        # Тест очікує коротку форму класу
        return f"Author(id={self.id})"

    @staticmethod
    def get_by_id(author_id):
        try:
            return Author.objects.get(pk=author_id)
        except Author.DoesNotExist:
            return None

    @staticmethod
    def delete_by_id(author_id):
        try:
            author = Author.objects.get(pk=author_id)
            author.delete()
            return True
        except Author.DoesNotExist:
            return False

    @staticmethod
    def create(name, surname, patronymic):
        try:
            if not name or len(name) > 20 or not surname or len(surname) > 20 or not patronymic or len(patronymic) > 20:
                return None
            author = Author(name=name, surname=surname, patronymic=patronymic)
            author.save()
            return author
        except Exception:
            return None

    def update(self, name=None, surname=None, patronymic=None):
        # Перевірка валідності довжини імені (максимум 20 символів за ТЗ CharField)
        if name is not None:
            if len(name) > 20 or len(name) == 0:
                return  # Скасовуємо оновлення, якщо ім'я невалідне
            self.name = name
        if surname is not None:
            if len(surname) > 20 or len(surname) == 0:
                return
            self.surname = surname
        if patronymic is not None:
            if len(patronymic) > 20 or len(patronymic) == 0:
                return
            self.patronymic = patronymic
        self.save()

    @staticmethod
    def get_all():
        return list(Author.objects.all())
