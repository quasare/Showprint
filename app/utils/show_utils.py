from flask import Blueprint, render_template, session,  \
    redirect, url_for, flash, jsonify, request
from ..models import db, Search, Show, Season, Episode, \
    Watched_episode, Watched_show, Watched_season

# Function to mark episode watched in DB
def toggle_ep(ep_id, username):
    in_db = Watched_episode.query.filter(
        Watched_episode.ep_id == ep_id, Watched_episode.user_id == username).first()
    if not in_db:
        new_watched_ep = Watched_episode(
            user_id=username, ep_id=ep_id, finished=True)
        db.session.add(new_watched_ep)
        db.session.commit()
    elif in_db:
        db.session.delete(in_db)
        db.session.commit()
    return    

# Marke season watched in DB 
def toggle_season(s_id, username):
    in_db = Watched_season.query.filter(
        Watched_season.season_id == s_id, Watched_season.user_id == username).first()
    if not in_db:
        new_watched_ep = Watched_season(
            user_id=username, season_id=s_id, finished=True)
        db.session.add(new_watched_ep)
        db.session.commit()
    elif in_db:
        db.session.delete(in_db)
        db.session.commit()
    return