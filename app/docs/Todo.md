# TODO
1. Analyse what you did with the new Register, Login, Logout functions
1. Learn Authentication & Permissions


1. View test
2. API test
3. Serializer tests
4. API endpoint tests
- [ ] Plan for the Future and make a list of things this program shoud do
- [ ] Fix the home page
- [ ] ERD (Entity Relationship Diagram)
- [ ] For each employee you can see how much they earned and how much they are predicted to earn, add tax, add hours per week.
- [ ] Review that the website all makes sense and make a diagram
- [ ] Learn PostgreSQL properly

- [ ] Understand
- [ ] < @api_view(['POST'])
@permission_classes([AllowAny])
def create_post(request):
    try:
        user_id = request.headers.get('x-user-id')

        if not user_id:
            return Response(
                {'message': 'Not authenticated'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        data = request.data.copy()

        # Required fields
        title = data.get('title')
        content = data.get('content')
        category = data.get('category')

        if not title or not content or not category:
            return Response(
                {'message': 'Title, content, and category are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Auto excerpt
        if not data.get('excerpt'):
            data['excerpt'] = content[:150]

        # Tags fallback
        if data.get('tags') is None:
            data['tags'] = []

        # Read time auto calc
        data['read_time'] = max(1, len(content.split()) // 200)

        # Create post
        post = Post.objects.create(
            title=title,
            content=content,
            excerpt=data['excerpt'],
            category=category,
            tags=data['tags'],
            read_time=data['read_time'],
            author_id=user_id
        )

        return Response({
            'message': 'Post created successfully',
            'post': {
                'id': post.id,
                'title': post.title,
                'content': post.content,
                'excerpt': post.excerpt,
                'category': post.category,
                'tags': post.tags,
                'read_time': post.read_time,
                'published': post.published
            }
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        print(f'Create post error: {e}')
        return Response(
            {'message': 'Server error creating post'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        ) >