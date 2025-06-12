from .models import Page, PageCategory

def toc_context(request):
    """Add Table of Contents to all template contexts"""
    categories = PageCategory.objects.prefetch_related(
        'page_set'
    ).filter(
        page__is_published=True,
        page__show_in_toc=True
    ).distinct()
    
    toc_data = []
    for category in categories:
        pages = category.page_set.filter(
            is_published=True, 
            show_in_toc=True
        ).order_by('toc_order', 'title')
        
        if pages.exists():
            toc_data.append({
                'category': category,
                'pages': pages
            })
    
    # Also get uncategorized pages
    uncategorized_pages = Page.objects.filter(
        is_published=True,
        show_in_toc=True,
        category__isnull=True
    ).order_by('toc_order', 'title')
    
    if uncategorized_pages.exists():
        toc_data.append({
            'category': None,
            'pages': uncategorized_pages
        })
    
    return {
        'toc_data': toc_data
    }