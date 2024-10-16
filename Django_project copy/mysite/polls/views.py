from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Avg
from .models import Post, Rating

def post_detail(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        return render(request, 'polls/post_detail.html', {'post': post})
    except Post.DoesNotExist:
        return render(request, 'post_not_found.html', {'post_id': post_id}, status=404)

def rate_post(request, post_id):
    if request.method == 'POST':
        try:
            post = Post.objects.get(id=post_id)
            rating_value = int(request.POST.get('rating'))
            
            Rating.objects.create(post=post, value=rating_value)
            
            # Recalculate average rating
            avg_rating = post.ratings.aggregate(Avg('value'))['value__avg']
            post.average_rating = round(avg_rating, 2) if avg_rating else 0
            post.save()
            
            return JsonResponse({'success': True, 'average_rating': post.average_rating})
        except Post.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Post not found'}, status=404)
        except ValueError:
            return JsonResponse({'success': False, 'error': 'Invalid rating value'}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)