# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Message

# from .forms import MessageForm
from users.models import User
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import Q
from django.utils.timezone import now


@login_required
def inbox(request):
    # Get distinct users who have either sent or received messages with the logged-in user
    distinct_users = User.objects.filter(
        id__in=Message.objects.filter(sender=request.user).values("receiver")
    ).union(
        User.objects.filter(
            id__in=Message.objects.filter(receiver=request.user).values("sender")
        )
    )
    return render(request, "dm/inbox.html", {"distinct_users": distinct_users})


@login_required
def conversation(request, username):
    other_user = get_object_or_404(User, username=username)
    messages = Message.objects.filter(
        (Q(sender=request.user) & Q(receiver=other_user))
        | (Q(sender=other_user) & Q(receiver=request.user))
    ).order_by("sent_at")

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        messages_html = render_to_string(
            "partials/messages.html", {"messages": messages, "user": request.user}
        )
        return JsonResponse({"messages_html": messages_html})

    return render(
        request,
        "dm/conversation.html",
        {"messages": messages, "other_user": other_user},
    )


@login_required
def send_message(request):
    if request.method == "POST":
        message_text = request.POST.get("message_text")
        receiver_id = request.POST.get("receiver")
        receiver = get_object_or_404(User, id=receiver_id)

        message = Message.objects.create(
            sender=request.user,
            receiver=receiver,
            message_text=message_text,
            sent_at=now(),
        )

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse(
                {
                    "message_text": message.message_text,
                    "sent_at": message.sent_at.strftime("%Y-%m-%d %H:%M:%S"),
                }
            )

        return redirect("conversation", username=receiver.username)
