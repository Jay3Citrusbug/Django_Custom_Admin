from frontend.serializers import CommentSerializer
from frontend.utils import comment_check
from core.models import (UpVote, Comments, User, VisitorHistory)
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, Count


@csrf_exempt
def add_new_comment(request):
    if request.method == 'POST':
        print(request.POST)
        name = request.POST.get("name", None)
        email = request.POST.get("email", None)
        description = request.POST.get("description")
        is_notification = request.POST.get("is_notification").title()
        comment_type_id = request.POST.get('comment_type_id')
        comment_type = request.POST.get('comment_type')
        parent_id = request.POST.get('parent_id', None)
        user_ip = request.POST['user_ip']
        is_spam = comment_check(user_ip, request.META['HTTP_USER_AGENT'], name, email, description)

        if name.isspace():
            name = "Anonymous"
        print(description, '-*****************', is_notification)
        if description != ' ':
            Comments.objects.create(
                ip=user_ip, name=name, email=email, description=description, comment_type=comment_type,
                comment_type_id=comment_type_id, is_notification=is_notification, is_spam=is_spam,
                parent_id_id=parent_id
            )
    return JsonResponse({'data':'Done'}, safe=False)


def display_comments(request):
    comment_type = request.GET.get('comment_type')
    comment_type_id = request.GET.get('comment_type_id')
    upvote_comment = request.GET.get('upvote_comment')
    all_comments = request.GET.get('all_comments', 'False')
    is_upvoted = request.GET.get('is_upvoted')
    comment_filter = request.GET.get('comment_filter', 'newest_first')
    user_ip = request.GET.get('ip')

    # review_obj = Review.objects.get(slug=review_brand_and_slug[1],brands__slug=review_brand_and_slug[0])
    qry_main_review_comments = Comments.objects.filter(
        comment_type=comment_type, is_approved=True, comment_type_id=comment_type_id
    ).annotate(upvote_count=Count('upvote__comment_id'))
    if comment_filter == 'most_valuable':
        qry_main_review_comments = qry_main_review_comments.order_by('-upvote_count')
    else:
        qry_main_review_comments = qry_main_review_comments.order_by('-create_at')

    if is_upvoted == 'true':
        add_comment_upvote = UpVote.objects.create(comment_id_id=upvote_comment, ip=user_ip)
    if is_upvoted == 'false':
        remove_comment_upvote = UpVote.objects.filter(comment_id_id=upvote_comment, ip=user_ip).delete()

    upvoted_comments = list(UpVote.objects.filter(ip=user_ip).values_list('comment_id', flat=True))

    comments = []

    total_comment = len(qry_main_review_comments.filter(parent_id=None))
    if all_comments != 'True' and all_comments == 'False':
        for replied_comments in qry_main_review_comments.filter(parent_id=None)[:2]:
            serializer = CommentSerializer(replied_comments)
            comments.append(serializer.data)

    if all_comments == 'True' and all_comments != 'False':
        for replied_comments in qry_main_review_comments.filter(parent_id=None):
            serializer = CommentSerializer(replied_comments)
            comments.append(serializer.data)

    qry_user_admin = list(User.objects.values_list('email', flat=True))

    context = {
        'review_comments': comments,
        'upvoted_comments': upvoted_comments,
        'admin_emails': qry_user_admin,
        'total_comment': total_comment,
        'comment_type_id': comment_type_id
    }

    return render(request, 'frontend/include/main_comment.html', context)


def display_sub_comments(request):
    parentid = request.GET.get('parent_comment_id')
    is_sub_comment = request.GET.get('is_sub_comment')
    user_ip = request.GET.get('ip')
    qry_comments = Comments.objects.filter(is_approved=True, parent_id=parentid)
    comments = []
    for replied_comments in qry_comments.annotate(upvote_count=Count('upvote__comment_id')).order_by('-upvote_count'):
        serializer = CommentSerializer(replied_comments)
        comments.append(serializer.data)

    # user_ip = json.loads(requests.get('https://api.ipify.org/?format=json').text)['ip']
    upvoted_comments = list(UpVote.objects.filter(ip=user_ip).values_list('comment_id', flat=True))

    if is_sub_comment == 'True':
        comments = comments
    if is_sub_comment == 'False':
        comments = comments[2:]

    qry_user_admin = list(User.objects.values_list('email', flat=True))
    context = {
       'comments': comments,
       'upvoted_comments': upvoted_comments,
       'is_sub_comment': is_sub_comment,
       'admin_emails': qry_user_admin,
    }

    return render(request, 'frontend/include/show_child_comment.html', context)
