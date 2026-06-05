from django.db import models
from authentication.models import CustomUser
from book.models import Book
from django.utils import timezone

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    end_at = models.DateTimeField(null=True, blank=True)
    plated_end_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        created_str = f"'{self.created_at.strftime('%Y-%m-%d %H:%M:%S+00:00')}'" if self.created_at else "None"
        end_str = f"'{self.end_at.strftime('%Y-%m-%d %H:%M:%S+00:00')}'" if self.end_at else "None"
        plated_str = f"'{self.plated_end_at.strftime('%Y-%m-%d %H:%M:%S+00:00')}'" if self.plated_end_at else "None"

        # ПОВЕРТАЄМО РЯДОК БЕЗ ФІГУРНИХ ДУЖОК НА ПОЧАТКУ ТА В КІНЦІ!
        return f"'id': {self.id}, 'user': CustomUser(id={self.user_id}), 'book': Book(id={self.book_id}), 'created_at': {created_str}, 'end_at': {end_str}, 'plated_end_at': {plated_str}"

    def __repr__(self):
        # Тест чітко очікує рядок виду 'Order(id=102)'
        return f"Order(id={self.id})"


    @staticmethod
    def get_by_id(order_id):
        try:
            return Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            return None

    @staticmethod
    def delete_by_id(order_id):
        try:
            order = Order.objects.get(pk=order_id)
            order.delete()
            return True
        except Order.DoesNotExist:
            return False

    @staticmethod
    def create(user, book, plated_end_at=None):
        try:
            if not user or user.id is None or not book:
                return None
            if book.count <= 0:
                return None
            if plated_end_at and plated_end_at < timezone.now():
                return None
            if Order.objects.filter(user=user, book=book, end_at__isnull=True).exists():
                return None

            order = Order(user=user, book=book, plated_end_at=plated_end_at, end_at=None)
            order.save()

            book.count -= 1
            book.save()
            return order
        except Exception:
            return None

    def update(self, end_at=None, plated_end_at=None):
        if end_at is not None:
            self.end_at = end_at
        if plated_end_at is not None:
            self.plated_end_at = plated_end_at
        self.save()

    @staticmethod
    def get_all():
        return list(Order.objects.all())

    @staticmethod
    def get_not_returned_books():
        # Повертає список усіх замовлень, у яких книга ще не повернута (end_at є порожнім)
        return list(Order.objects.filter(end_at__isnull=True))
