# discussions/forms.py
from django import forms
from .models import Discussion, Reply

class DiscussionForm(forms.ModelForm):
    class Meta:
        model = Discussion
        fields = ['title', 'content', 'topic']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
        }

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
        }

# discussions/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from django.http import JsonResponse
from django.urls import reverse
from .models import Discussion, Topic, Reply, Vote
from .forms import DiscussionForm, ReplyForm

def discussion_list(request):
    topics = Topic.objects.annotate(discussion_count=Count('discussions'))
    discussions = Discussion.objects.select_related('author', 'topic')\
        .annotate(reply_count=Count('replies'),
                 vote_score=Count('votes__value'))\
        .order_by('-created_at')
    
    topic_slug = request.GET.get('topic')
    if topic_slug:
        discussions = discussions.filter(topic__slug=topic_slug)
    
    context = {
        'topics': topics,
        'discussions': discussions,
        'selected_topic': topic_slug,
    }
    return render(request, 'discussions/discussion_list.html', context)

@login_required
def discussion_create(request):
    if request.method == 'POST':
        form = DiscussionForm(request.POST)
        if form.is_valid():
            discussion = form.save(commit=False)
            discussion.author = request.user
            discussion.save()
            return redirect(reverse('discussions:discussion_detail', args=[discussion.pk]))
    else:
        form = DiscussionForm()
    
    return render(request, 'discussions/discussion_form.html', {'form': form})

def discussion_detail(request, pk):
    discussion = get_object_or_404(Discussion.objects.select_related('author', 'topic'), pk=pk)
    replies = discussion.replies.select_related('author').order_by('created_at')
    
    if request.user.is_authenticated:
        user_vote = discussion.votes.filter(user=request.user).first()
    else:
        user_vote = None
    
    if request.method == 'POST' and request.user.is_authenticated:
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.discussion = discussion
            reply.author = request.user
            reply.save()
            messages.success(request, 'Reply posted successfully!')
            return redirect('discussion_detail', pk=pk)
    else:
        form = ReplyForm()
    
    # Increment view count
    discussion.views += 1
    discussion.save()
    
    context = {
        'discussion': discussion,
        'replies': replies,
        'form': form,
        'user_vote': user_vote,
    }
    return render(request, 'discussions/discussion_detail.html', context)

@login_required
def vote_discussion(request, pk):
    if request.method == 'POST':
        discussion = get_object_or_404(Discussion, pk=pk)
        vote_type = request.POST.get('vote_type')
        
        if vote_type not in ['upvote', 'downvote']:
            return JsonResponse({'error': 'Invalid vote type'}, status=400)
            
        value = Vote.UPVOTE if vote_type == 'upvote' else Vote.DOWNVOTE
        
        vote, created = Vote.objects.get_or_create(
            user=request.user,
            discussion=discussion,
            defaults={'value': value}
        )
        
        if not created:
            if vote.value == value:
                vote.delete()
            else:
                vote.value = value
                vote.save()
        
        vote_count = discussion.votes.aggregate(
            score=Count('value')
        )['score']
        
        return JsonResponse({'vote_count': vote_count})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def discussion_edit(request, pk):
    discussion = get_object_or_404(Discussion, pk=pk)
    
    if request.method == 'POST':
        form = DiscussionForm(request.POST, instance=discussion)
        if form.is_valid():
            form.save()
            messages.success(request, 'Discussion updated successfully!')
            return redirect('discussions:discussion_detail', pk=discussion.pk)
    else:
        form = DiscussionForm(instance=discussion)
    
    return render(request, 'discussions/discussion_form.html', {'form': form})

@login_required
def discussion_delete(request, pk):
    discussion = get_object_or_404(Discussion, pk=pk)

    if discussion.author != request.user:
        messages.error(request, "You are not authorized to delete this discussion.")
        return redirect('discussions:discussion_detail', pk=pk)

    if request.method == 'POST':
        discussion.delete()
        messages.success(request, 'Discussion deleted successfully!')
        return redirect('discussions:discussion_list')

    return render(request, 'discussions/discussion_confirm_delete.html', {'discussion': discussion})