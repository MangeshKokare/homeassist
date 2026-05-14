from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Message
from .forms import MessageForm


@login_required
def chat_view(request, user_id):

    receiver = get_object_or_404(
        User,
        id=user_id
    )

    chats = (
        Message.objects.filter(
            sender=request.user,
            receiver=receiver
        ) |
        Message.objects.filter(
            sender=receiver,
            receiver=request.user
        )
    ).order_by('timestamp')

    form = MessageForm()

    if request.method == 'POST':

        form = MessageForm(request.POST)

        if form.is_valid():

            msg = form.save(commit=False)

            msg.sender = request.user
            msg.receiver = receiver

            msg.save()

            return redirect(
                'chat',
                user_id=receiver.id
            )

    # =========================
    # DYNAMIC BASE TEMPLATE
    # =========================
    if request.user.profile.role == 'provider':

        base_template = 'layout/provider_base.html'

    else:

        base_template = 'layout/resident_base.html'

    return render(
        request,
        'messages/chat.html',
        {
            'chats': chats,
            'receiver': receiver,
            'form': form,
            'base_template': base_template,
        }
    )