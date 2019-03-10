from django.db.models import Q
from django.shortcuts import render
from wagtail.admin.forms.search import SearchForm
from wagtail.admin.modal_workflow import render_modal_workflow
from wagtail.core import hooks
from wagtail.core.models import GroupCollectionPermission, Collection
from wagtail.images import get_image_model
from wagtail.images.forms import get_image_form
from wagtail.images.permissions import permission_policy
from wagtail.images.views.chooser import get_chooser_context, get_chooser_js_data
from wagtail.utils.pagination import paginate


def chooser(request):
    Image = get_image_model()
    # get collection permissions according to user groups
    collections = None
    groups = request.user.groups.all()

    if groups:
        collection_permissions = GroupCollectionPermission.objects.filter(group__in=groups)
        if collection_permissions:
            collections = [cp.collection for cp in collection_permissions.all()]

    if not collections:
        collections = Collection.objects.all()

    if permission_policy.user_has_permission(request.user, 'add'):
        ImageForm = get_image_form(Image)
        uploadform = ImageForm(user=request.user)
    else:
        uploadform = None

    images = None
    temp = None
    for collection in collections:
        images = Image.objects.filter(collection_id=collection.id)
        if temp != None:
            images = temp | images
        temp = images

    root_collection = Collection.objects.get(name="Root").id
    images = images | Image.objects.filter(collection_id=root_collection)
    images = images.distinct().order_by('-created_at')

    # allow hooks to modify the queryset
    for hook in hooks.get_hooks('construct_image_chooser_queryset'):
        images = hook(images, request)

    if (
            'q' in request.GET or 'p' in request.GET or 'tag' in request.GET or
            'collection_id' in request.GET
    ):
        # this request is triggered from search, pagination or 'popular tags';
        # we will just render the results.html fragment
        collection_id = request.GET.get('collection_id')
        if collection_id:
            images = images.filter(collection=collection_id)

        searchform = SearchForm(request.GET)
        if searchform.is_valid():
            q = searchform.cleaned_data['q']

            images = images.search(q)
            is_searching = True
        else:
            is_searching = False
            q = None

            tag_name = request.GET.get('tag')
            if tag_name:
                images = images.filter(tags__name=tag_name)

        # Pagination
        paginator, images = paginate(request, images, per_page=12)
        return render(request, "wagtailimages/chooser/results.html", {
            'images': images,
            'is_searching': is_searching,
            'query_string': q,
            'will_select_format': request.GET.get('select_format')
        })
    else:
        paginator, images = paginate(request, images, per_page=12)
        context = get_chooser_context(request)
        context.update({
            'images': images,
            'uploadform': uploadform,
        })
        return render_modal_workflow(
            request, 'wagtailimages/chooser/chooser.html', None, context,
            json_data=get_chooser_js_data()
        )
