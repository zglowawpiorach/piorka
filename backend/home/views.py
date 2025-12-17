from django.http import JsonResponse
from wagtail.images.models import Image


def images_api(request):
    """
    API endpoint to get images filtered by tags.
    Usage: /api/images/?tag=one,two,three
    Returns list of image URLs matching any of the provided tags.
    """
    # Get tag parameter from query string
    tag_param = request.GET.get('tag', '')

    # Start with all images
    images = Image.objects.all()

    # Filter by tags if provided
    if tag_param:
        tags = [tag.strip() for tag in tag_param.split(',')]
        # Filter images that have any of the specified tags
        for tag in tags:
            images = images.filter(tags__name__iexact=tag)

    # Build response with image data
    image_list = []
    for img in images:
        image_list.append({
            'id': img.id,
            'title': img.title,
            'url': request.build_absolute_uri(img.file.url),
            'width': img.width,
            'height': img.height,
            'tags': [tag.name for tag in img.tags.all()],
        })

    return JsonResponse({
        'count': len(image_list),
        'images': image_list
    })
