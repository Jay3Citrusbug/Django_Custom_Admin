from django.db.models import Q, Count
from rest_framework import serializers
from core.models import Comments
from datetime import datetime
from datetime import datetime, timedelta, timezone
from django.utils.timesince import timesince


class CommentSerializer(serializers.ModelSerializer):
    replied_comments = serializers.SerializerMethodField('child_comments')
    upvote_count = serializers.SerializerMethodField('comment_upvote_count')
    name = serializers.SerializerMethodField('name_check')
    create_at = serializers.SerializerMethodField('create_at_date')
    
    class Meta:
        model = Comments
        fields =  ['id', 'name', 'email', 'description', 'parent_id', 'upvote_count', 'create_at', 'replied_comments']
        
    def child_comments(request, obj):
        child_comment = Comments.objects.filter(parent_id=obj.id, is_approved=True).annotate(upvote_count=Count('upvote__comment_id')).order_by('-upvote_count')
        replied_comments = []
        for comment in child_comment:
            serializers = CommentSerializer(comment)
            replied_comments.append(serializers.data)
        return replied_comments
    
    def comment_upvote_count(request, obj):
        return obj.upvote_count

    def name_check(self, obj):
        if obj.name in [None, '', ' ']:
            name = 'Anonymous'
        else:
            name = obj.name
        return name

    def create_at_date(self, obj):
        now = datetime.now(timezone.utc)
        try:
            difference = now - obj.create_at
        except:
            return obj.create_at

        if difference <= timedelta(minutes=1):
            return 'just now'
        return '%(time)s ago' % {'time': timesince(obj.create_at).split(', ')[0]}
