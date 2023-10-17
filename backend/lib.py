from flask import Flask, render_template, send_file, request, Response
from flask_jwt_extended import JWTManager
from flask_restful import Api, Resource
from flask_cors import CORS
import app.config as config
from datetime import datetime, timedelta
from app.workers import make_celery
from celery.result import AsyncResult
from app.security import user_datastore, security
from app.models import *
import os, time
from sqlalchemy import func
import requests
from celery.schedules import crontab
from app.cache import cache

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Template



from api.Auth.SignupAPI import SignupAPI
from api.Auth.LoginAPI import LoginAPI
from api.Auth.AdminLogin import AdminLoginAPI
from api.AddTheatre.addvenue import AdminAddTheatreAPI
from api.AddTheatre.addvenue import AdminGetTheatreAPI
from api.EditTheater.editvenue import AdminEditTheatreAPI
from api.AddShow.addshow import AdminAddShowAPI
from api.AddShow.addshow import AdminGetShowAPI
from api.EditShow.editshow import AdminEditShowAPI
from api.DeleteShow.deleteshow import AdminDeleteShowAPI
from api.DeleteTheater.deletevenue import AdminDeleteVenueAPI
from api.Auth.AdminSignup import AdminSignupAPI
from api.User.postedvenues import PostedVenuesAPI
from api.User.postedshows import  PostedShowsAPI
from api.User.getvenuedetail import VenueDetailAPI
from api.User.getshowdetail import ShowDetailAPI
from api.User.showbook import BookShowAPI
from api.User.getavailableseats import GetSeatsAPI
from api.User.bookdash import BookDashAPI
from api.User.search import SearchVenuesAPI
from api.Summary.summary import SummaryAPI