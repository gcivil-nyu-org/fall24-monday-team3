from django.shortcuts import render, redirect, get_object_or_404
from .forms import RoommatePostForm, RoommateImageForm, CommentForm
from .models import RoommateImage, RoommatePost, Comment
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q


@login_required(login_url="/users/login/")
def roommate_list(request):
    query = request.GET.get("q")
    if query:
        roommates = RoommatePost.objects.filter(
            Q(name__icontains=query)
            | Q(preferred_location__icontains=query)
            | Q(hobbies__icontains=query)
        )
    else:
        roommates = RoommatePost.objects.all()
    context = {"roommates": roommates, "search_query": query}
    return render(request, "roommates/roommate_list.html", context)


@login_required(login_url="/users/login/")
def roommate_detail(request, pk):
    roommate = get_object_or_404(RoommatePost, pk=pk)
    comments = roommate.comments.all()  # Load comments for display
    form = CommentForm()  # Empty form for the template

    context = {
        "roommate": roommate,
        "images": roommate.images.all(),
        "comments": comments,
        "form": form,
    }
    return render(request, "roommates/roommate_detail.html", context)


@login_required(login_url="/users/login/")
def update_roommate_post(request, pk):
    roommate_post = get_object_or_404(RoommatePost, pk=pk)

    # Check if the user is the owner
    if roommate_post.user != request.user:
        messages.error(request, "You don't have permission to edit this listing.")
        return redirect("roommate_detail", pk=roommate_post.pk)

    if request.method == "POST":
        form = RoommatePostForm(request.POST, request.FILES, instance=roommate_post)
        if form.is_valid():
            form.save()
            return redirect("roommate_detail", pk=roommate_post.pk)
    else:
        form = RoommatePostForm(instance=roommate_post)
    return render(
        request,
        "roommates/update_roommate_post.html",
        {"form": form, "post": roommate_post},
    )


@login_required(login_url="/users/login/")
def delete_roommate_post(request, pk):
    roommate_post = get_object_or_404(RoommatePost, pk=pk)

    # Check if the user is the owner
    if roommate_post.user != request.user:
        messages.error(request, "You don't have permission to delete this listing.")
        return redirect("roommate_detail", pk=roommate_post.pk)

    if request.method == "POST":
        roommate_post.delete()
        messages.success(request, "Roommate listing deleted successfully.")
        return redirect("roommate_list")
    return render(
        request,
        "roommates/delete_roommate_post.html",
        {"roommate_post": roommate_post},
    )


@login_required(login_url="/users/login/")
def create_roommate_post(request):
    if request.method == "POST":
        post_form = RoommatePostForm(request.POST)
        image_form = RoommateImageForm(request.POST, request.FILES)

        if post_form.is_valid() and image_form.is_valid():
            # Create roommate post but don't save to DB yet
            roommate_post = post_form.save(commit=False)
            # Set the user
            roommate_post.user = request.user
            # Now save to DB
            roommate_post.save()
            # Save many-to-many relationships
            post_form.save_m2m()

            images = request.FILES.getlist("image")
            for image in images:
                RoommateImage.objects.create(roommate=roommate_post, image=image)

            messages.success(request, "Roommate post created successfully!")
            return redirect("roommate_detail", pk=roommate_post.pk)
    else:
        post_form = RoommatePostForm()
        image_form = RoommateImageForm()

    context = {"post_form": post_form, "image_form": image_form}
    return render(request, "roommates/create_roommate_post.html", context)


@login_required(login_url="/users/login/")
def create_roommate_comment(request, pk):
    post = get_object_or_404(RoommatePost, pk=pk)
    parent_id = request.POST.get("parent_id")
    parent_comment = None

    # Check if this comment is a reply to another comment
    if parent_id:
        parent_comment = Comment.objects.get(id=parent_id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.parent = parent_comment  # Set parent if it's a reply
            comment.save()
            return redirect("roommate_detail", pk=post.pk)

    return redirect("roommate_detail", pk=pk)


@login_required(login_url="/users/login/")
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.user:  # Ensure only the comment author can delete
        comment.delete()
    return redirect("roommate_detail", pk=comment.post.pk)


@login_required(login_url="/users/login/")
def search_roommates(request):
    query = request.GET.get("q")
    if query:
        results = RoommatePost.objects.filter(
            Q(name__icontains=query)
            | Q(preferred_location__icontains=query)
            | Q(hobbies__icontains=query)
            | Q(description__icontains=query)
        )
    else:
        results = RoommatePost.objects.all()

    return render(
        request, "roommates/search_results.html", {"results": results, "query": query}
    )
