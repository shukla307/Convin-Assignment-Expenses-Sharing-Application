from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username

    def generate_balance_sheet(self):
        balance_sheet = {}
        user_expenses = ExpenseSplit.objects.filter(user=self.user)
        for split in user_expenses:
            creditor = split.expense.creator
            if creditor != self.user:
                balance_sheet[creditor] = balance_sheet.get(creditor, 0) + split.amount
        return balance_sheet

class Expense(models.Model):
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_expenses')
    participants = models.ManyToManyField(User, through='ExpenseSplit')

    def __str__(self):
        return self.description

    def split_expense(self, split_type, split_details=None):
        if split_type == 'equal':
            split_amount = self.amount / self.participants.count()
            for participant in self.participants.all():
                ExpenseSplit.objects.create(expense=self, user=participant, amount=split_amount)
        elif split_type == 'exact' and split_details:
            for participant, amount in split_details.items():
                ExpenseSplit.objects.create(expense=self, user=participant, amount=amount)
        elif split_type == 'percentage' and split_details:
            for participant, percentage in split_details.items():
                amount = self.amount * (percentage / 100)
                ExpenseSplit.objects.create(expense=self, user=participant, amount=amount)

class ExpenseSplit(models.Model):
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.user.username} owes {self.amount} for {self.expense.description}'
