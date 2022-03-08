def menu_links(request):
    return {
        'menu_links': [
            {'url': 'main', 'name': 'домой'},
            {'url': 'products:index', 'name': 'продукты'},
            {'url': 'contact', 'name': 'контакты'},
        ]
    }