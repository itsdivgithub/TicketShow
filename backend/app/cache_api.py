from app.models import *
from app.cache import cache
from flask_jwt_extended import jwt_required


@jwt_required()
@cache.cached(timeout=10, key_prefix='get_all_venues')
def get_all_venues():
    venues = Venue.query.all()
    return venues

@jwt_required()
@cache.memoize(10)
def get_shows_by_venue(venue_id):
    shows = Show.query.filter_by(venue_id=venue_id)
    return shows.all()

@jwt_required()
@cache.memoize(10)
def get_venue(venue_id):
    venue = Venue.query.get(venue_id)
    return venue

@jwt_required()
@cache.memoize(10)
def get_show_by_showvenue(venue_id, show_id):
    show = Show.query.filter_by(id=show_id, venue_id=venue_id)
    return show.first()

