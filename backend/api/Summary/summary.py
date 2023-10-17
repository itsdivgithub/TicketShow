import matplotlib.pyplot as plt
from flask import request
from flask_restful import Resource
from app.models import *
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from api.Auth.AdminLogin import admin_required
from sqlalchemy import func
import io
import base64

class SummaryAPI(Resource):

    @jwt_required()
    @admin_required

    def get(self):

        venues = Venue.query.all()
        summary_data = []
        chart_images = []
        
        for venue in venues:
            venue_data = {
                'venue_name': venue.name,
                'shows_data': []
            }
            shows = Show.query.filter_by(venue_id=venue.id).all()
            for show in shows:
                total_seats_booked = db.session.query(func.sum(Bookings.seats_booked)).filter_by(show_id=show.id).scalar()
                if total_seats_booked is None:
                    total_seats_booked = 0

                show_data = {
                    'show_name': show.name,
                    'seats_booked': total_seats_booked
                }
                venue_data['shows_data'].append(show_data)
            
            summary_data.append(venue_data)

        for venue_data in summary_data:
            fig, ax = plt.subplots(figsize=(5,4)) 
            show_names = [show_data['show_name'] for show_data in venue_data['shows_data']]
            seats_booked = [show_data['seats_booked'] for show_data in venue_data['shows_data']]
            name= venue_data['venue_name']
            ax.bar(show_names, seats_booked)
            ax.set_xlabel('Show Name')
            ax.set_ylabel('Seats Booked')
            ax.set_title(f'Seats Booked at {name}')

            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
            plt.close()

            chart_images.append('data:image/png;base64,' + image_base64)

        return {
            'summary_data': summary_data,
            'chart_images': chart_images
        }, 200

