#from django.shortcuts import render
from django.shortcuts import render
from .models import UserProfile
from django.shortcuts import render, redirect
from .models import Expense, UserProfile, ExpenseSplit
from .form import ExpenseForm, UserProfileForm

def create_user_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            return redirect('profile')
    else:
        form = UserProfileForm()
    return render(request, 'expenses/create_user_profile.html', {'form': form})

def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.creator = request.user
            expense.save()
            form.save_m2m()
            split_type = request.POST.get('split_type')
            split_details = request.POST.get('split_details')
            expense.split_expense(split_type, split_details)
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'expenses/add_expense.html', {'form': form})

def view_balance_sheet(request):
    user_profile = UserProfile.objects.get(user=request.user)
    balance_sheet = user_profile.generate_balance_sheet()
    return render(request, 'expenses/balance_sheet.html', {'balance_sheet': balance_sheet})

def expense_list(request):
    expenses = Expense.objects.all()
    return render(request, 'expenses/expense_list.html', {'expenses': expenses})


