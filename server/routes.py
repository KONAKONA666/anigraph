from aiohttp.web import Application


def setup_routes(app: Application, handler, static_root):
    router = app.router
    router.add_get('/', handler.index, name='index')
    router.add_get('/get_closest_anime/{title}/{top}', handler.get_closest_anime, name='get_closest_anime')
    router.add_get('/get_analogy/{base_title}/{rel_title}/{req_title}', handler.get_analogy, name='get_analogy')
    router.add_get('/autocomplete/{prefix}', handler.autocomplete, name='title_autocomplete')
    router.add_get('/get_points', handler.get_all_points, name='get_points')
    router.add_get('/get_neighbours/{title}/{margin}', handler.get_neighbours, name='get_neighbours')
    router.add_static(
        '/static/', path=str(static_root), name='static'
    )
