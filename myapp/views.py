from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth import decorators, forms, authenticate, login, get_user_model

from .models import Message
from .forms import MessageForm


User = get_user_model()


@decorators.login_required
def index(request):
  users = User.objects.exclude(pk=request.user.pk)
  return render(request, 'index.html', {'users': users})


@decorators.login_required
def create_message(request):
  if request.method != 'POST':
    return redirect('index')
  form = MessageForm(request.POST)
  if form.is_valid():
    message = form.save(commit=False)
    message.author = request.user
    message.save()

  return redirect('dialog', pk=form.cleaned_data['user'].pk)


@decorators.login_required
def get_dialog(request, pk):
  dialog_user = get_object_or_404(User, pk=pk)
  messages = Message.objects.filter(
    Q(author=request.user, user=dialog_user) 
    | Q(author=dialog_user, user=request.user)
  ).order_by('created_at')
  return render(
    request,
    'dialog.html',
    {
      'messages': messages,
      'author': dialog_user,
    }
  )


def registration_view(request):
  if request.method != 'POST':
    return render(request, 'registration/registration.html',
                  {'form': forms.UserCreationForm()})
  form = forms.UserCreationForm(request.POST)
  if form.is_valid():
    form.save()
    user = authenticate(
      request=request,
      username=form.cleaned_data['username'],
      password=form.cleaned_data['password1']
    )
    login(request, user)
    
    return redirect('index')

  return render(request, 'registration/registration.html', {'form': form})
