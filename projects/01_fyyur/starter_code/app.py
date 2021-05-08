#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
import sys
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# DONE:TODO: connect to a local postgresql database
migrate = Migrate(app, db)

#  Helper Functions:
#  ---------------------------------------------------------------------------#


def get_venue(venue_id):
    return Venue.query.get(venue_id)


def get_artist(artist_id):
    return Artist.query.get(artist_id)

#  Retornar todos los shows con fecha pasada:


def venue_past_shows(venue_id):
    return Show.query.filter(Show.start_time < datetime.now(), Show.venue_id == venue_id).all()

#  Retornar todos los shows con fecha a futuro:


def venue_upcoming_shows(venue_id):
    return Show.query.filter(Show.start_time > datetime.now(), Show.venue_id == venue_id).all()

#  Retornar los shows pasados del artista:


def artist_past_shows(artist_id):
    return Show.query.filter(Show.start_time < datetime.now(), Show.artist_id == artist_id).all()

#  Retornar los shows a futuro del artista:


def artist_upcoming_shows(artist_id):
    return Show.query.filter(Show.start_time > datetime.now(), Show.artist_id == artist_id).all()

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


class Show(db.Model):
    __tablename__ = 'shows'
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime())
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'))
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'))

    #  Usar las funciones helper para conseguir los datos de venue y artist:
    @property
    def upcoming(self):
        venue = get_venue(self.venue_id)
        artist = get_artist(seld.artist_id)
        #  Solo si el start_time es mayor a la hora actual, retornar valores:
        if self.start_time > datetime.now():
            return {
                "venue_id": self.venue_id,
                "venue_name": venue.name,
                "artist_id": self.artist_id,
                "artist_name": artist.name,
                "artist_image_link": artist.image_link,
                "start_time": self.start_time.strftime("%m/%d/%Y, %H:%M")

            }
        else:
            return None


class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=True)
    city = db.Column(db.String(), nullable=False)
    state = db.Column(db.String(), nullable=False)
    address = db.Column(db.String(), nullable=False)
    phone = db.Column(db.String(), nullable=False)
    image_link = db.Column(db.String(), nullable=False)
    genres = db.Column("genres", db.ARRAY(db.String()), nullable=True)
    website_link = db.Column(db.String(), nullable=True)
    facebook_link = db.Column(db.String(), nullable=True)
    seeking_talent = db.Column(db.Boolean, nullable=True, default=True)
    seeking_description = db.Column(db.String(
    ), nullable=False, default="We're looking for an exciting artist to perform here!!!")
    upcoming_shows = db.relationship('Show', backref='venue', lazy=True)
    test = db.Column(db.String(), nullable=True)

    def __repr__(self):
        return f'<<Venue Name: {self.name}, City: {self.city}, State: {self.state}, Seeking talent: {self.seeking_talent} >>'

    @property
    def city_state(self):
        return {'city': self.city, 'state': self.state}

    @property
    def full_details(self):
        past_shows = venue_past_shows(self.id)
        upcoming_shows = venue_upcoming_shows(self.id)

        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'phone': self.phone,
            'website_link': self.website_link,
            'facebook_link': self.facebook_link,
            'seeking_talent': self.seeking_talent,
            'seeking_description': self.seeking_description,
            'image_link': self.image_link,
            'past_shows': [{
                'artist_id': p.artist_id,
                'artist_name': p.artist.name,
                'artist_image_link': p.artist.image_link,
                'start_time': p.start_time.strftime("%m/%d/%Y, %H:%M")
            } for p in past_shows],
            'upcoming_shows': [{
                'artist_id': u.artist.id,
                'artist_name': u.artist.name,
                'artist_image_link': u.artist.image_link,
                'start_time': u.start_time.strftime("%m/%d/%Y, %H:%M")
            } for u in upcoming_shows],
            'past_shows_total': len(past_shows),
            'upcoming_shows_total': len(upcoming_shows)
        }

    # DONE:TODO: implement any missing fields, as a database migration using Flask-Migrate


class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=True)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column("genres", db.ARRAY(db.String()), nullable=False)
    image_link = db.Column(db.String(), nullable=False)
    website_link = db.Column(db.String(), nullable=True)
    facebook_link = db.Column(db.String(), nullable=True)
    seeking_venue = db.Column(db.Boolean, nullable=False, default=True)
    seeking_description = db.Column(
        db.String(), nullable=False, default="Looking to perform at an exciting venue!")
    shows = db.relationship('Show', backref='artist', lazy=True)

    def __repr__(self):
        return f'<<Artist Name: {self.name}, City: {self.city}, State: {self.state} >>'

    @property
    def details(self):
        return {'id': self.id, 'name': self.name}

    @property
    def full_details(self):
        past_shows = artist_past_shows(self.id)
        upcoming_shows = artist_upcoming_shows(self.id)

        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'state': self.state,
            'phone': self.phone,
            'genres': self.genres,
            'website_link': self.website_link,
            'facebook_link': self.facebook_link,
            'seeking_venue': self.seeking_venue,
            'seeking_description': self.seeking_description,
            'image_link': self.image_link,
            'past_shows': [{
                'venue_id': p.venue_id,
                'venue_name': p.venue.name,
                'venue_image_link': p.venue.image_link,
                'start_time': p.start_time.strftime("%m/%d/%Y, %H:%M")
            } for p in past_shows],
            'upcoming_shows': [{
                'venue_id': u.venue.id,
                'venue_name': u.venue.name,
                'venue_image_link': u.venue.image_link,
                'start_time': u.start_time.strftime("%m/%d/%Y, %H:%M")
            } for u in upcoming_shows],
            'past_shows_count': len(past_shows),
            'upcoming_shows_count': len(upcoming_shows)
        }

    # DONE-TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():

    try:
        # areas = [ven.city_state for ven in Venue.query.distinct(Venue.city, Venue.state).all()]
        # areas = Venue.query.all()

        # for a in areas:
        #     a['venues'] = [{'id': ven.id, 'name': ven.name, 'num_upcoming_shows': ven.shows}
        #                    for ven in Venue.query.filter_by(city=a['city']).all()]

        # return render_template('pages/venues.html', areas=areas)
        data = []

        # get all venues
        venues = Venue.query.all()

        # Use set so there are no duplicate venues
        locations = set()

        for venue in venues:
            # add city/state tuples
            locations.add((venue.city, venue.state))

        # for each unique city/state, add venues
        for location in locations:
            data.append({
                "city": location[0],
                "state": location[1],
                "venues": []
            })

        for venue in venues:
            num_upcoming_shows = 0

            shows = Show.query.filter_by(venue_id=venue.id).all()

            # get current date to filter num_upcoming_shows
            current_date = datetime.now()

            for show in shows:
                if show.start_time > current_date:
                    num_upcoming_shows += 1

            for venue_location in data:
                if venue.state == venue_location['state'] and venue.city == venue_location['city']:
                    venue_location['venues'].append({
                        "id": venue.id,
                        "name": venue.name,
                        "num_upcoming_shows": num_upcoming_shows
                    })
        return render_template('pages/venues.html', areas=data)

    except:
        flash('Error: no hay venues para mostrar ahora mismo.')
        return redirect(url_for('index'))

        # TODO: replace with real venues data.
        #       num_shows should be aggregated based on number of upcoming shows per venue.

    # return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # DONE-TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    try:
        search_text = request.form.get('search_term', '')
        # Para buscar entre varias venues:
        results = Venue.query.filter(
            Venue.name.ilike(f'%{search_text}%')).all()
        print(results)
        response = {
            "count": len(results),
            "data": results
        }

        return render_template('pages/search_venues.html', results=response, search_term=search_text)
    except:
        flash('Un error ha ocurrido en la búsqueda, por favor intente de nuevo.')
        return redirect(url_for('venues'))


@app.route('/venues/<int:venue_id>', methods=['GET'])
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # DONE-TODO: replace with real venue data from the venues table, using venue_id
    try:
        # print(Venue.query.get(venue_id))

        data = Venue.query.filter_by(id=venue_id).all()[0]
        print(data.full_details)
        # data = list(filter(lambda d: d['id'] == venue_id, datas))[0]
        return render_template('pages/show_venue.html', venue=data.full_details)
    except:
        flash('La venue con el id {venue_id} no existe.')
        return redirect(url_for('index'))

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # DONE-TODO: insert form data as a new Venue record in the db, instead
    # DONE-TODO: modify data to be the data object returned from db insertion
    error = False

    try:
        form = VenueForm()
        seeking_talent = request.form.get('seeking_talent')

        new_venue = Venue(
            name=request.form.get('name'),
            city=request.form.get('city'),
            state=request.form.get('state'),
            address=request.form.get('address'),
            genres=form.genres.data,
            phone=request.form.get('phone'),
            facebook_link=request.form.get('facebook_link'),
            image_link=request.form.get('image_link'),
            website_link=request.form.get('website_link'),
            seeking_talent=request.form.get('seeking_talent'),
            seeking_description=request.form.get('seeking_description')
        )
        db.session.add(new_venue)
        db.session.commit()
        # on successful db insert, flash success
        flash('Venue ' + request.form['name'] + ' was successfully listed!')

    except:
        error = True
        # DONE-TODO: on unsuccessful db insert, flash an error instead.
        flash('An error occurred. Venue could not be listed.')
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if not error:
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    else:
        flash('An error occurred. Venue could not be listed.')

    # e.g.,
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return redirect(url_for('index'))


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # DONE-TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    error = None

    try:
        Venue.query.filter_by(id=venue_id).delete()
        db.session.commit()
    except:
        error = True
        db.session.rollback()
    finally:
        db.session.close()
    if error:
        flash('An error occurred, the venue cannot be deleted')
        return redirect(url_for('index'))
    else:
        flash('Venue ' + request.form['name'] + ' is deleted!')
        return redirect(url_for('index'))

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    # DONE-TODO: replace with real data returned from querying the database
    # artists = [art.details for art in Artist.query.all()]
    # print(artists)
    try:
        artists = [art.details for art in Artist.query.all()]
        return render_template('pages/artists.html', artists=artists)
    except:
        flash('An error occurred, No artist to display right now.')
        return redirect(url_for('index'))


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # DONE-TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    # response = {
    #     "count": 1,
    #     "data": [{
    #         "id": 4,
    #         "name": "Guns N Petals",
    #         "num_upcoming_shows": 0,
    #     }]
    # }
    try:
        search_text = request.form.get('search_term', '')
        # result = Artist.query.filter(Artist.name === search_text).all()
        #  Search filter that matches the text:
        results = Artist.query.filter(
            Artist.name.ilike(f'%{search_text}%')).all()

        def getData(self, res):
            for r in res:
                return {
                    'id': r.id,
                    'name': r.name,
                    'num_upcoming_shows': len(r.shows)
                }

        response = {
            'count': len(results),
            'data': [getData(results)]
        }
        return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))
    except:
        flash('An error occurred while searching, please try again')
        return redirect(url_for('artists'))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the artist page with the given artist_id
    # DONE-TODO: replace with real artist data from the artist table, using artist_id
    datas = Artist.query.filter_by(id=artist_id).all()[0]
    print(datas.full_details)
    try:
        datas = Artist.query.filter_by(id=artist_id).all()[0]

        # data = list(filter(lambda d: d['id'] ==
        #                    artist_id, [datas]))[0]
        return render_template('pages/show_artist.html', artist=datas.full_details)
    except:
        flash('Sorry, that Artist does not exists.')
        return redirect(url_for('index'))

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    artist = Artist.query.filter_by(id=artist_id).all()[0]
    print(artist)

    form = ArtistForm(
        name=artist.name,
        city=artist.city,
        state=artist.state,
        genres=artist.genres,
        phone=artist.phone,
        facebook_link=artist.facebook_link,
        website_link=artist.website_link,
        image_link=artist.image_link,
        seeking_venue=artist.seeking_venue,
        seeking_description=artist.seeking_description
    )
    print(request.form.get('seeking_venue'))
    # DONE-TODO: populate form with fields from artist with ID <artist_id>
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes
    try:
        artist = Artist.query.filter_by(id=artist_id).all()[0]

        artist.name = request.form.get('name')
        artist.city = request.form.get('city')
        artist.state = request.form.get('state')
        artist.phone = request.form.get('phone')
        artist.genres = request.form.getlist('genres')
        artist.facebook_link = request.form.get('facebook_link')
        artist.website_link = request.form.get('website_link')
        artist.image_link = request.form.get('image_link')
        artist.seeking_venue = request.form.get('seeking_venue') == 'True'
        artist.seeking_description = request.form.get('seeking_description')

        db.session.commit()
    except:
        db.session.rollback()
        flash('An error occurred. Artist could not be updated')
    finally:
        db.session.close()

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):

    venue = Venue.query.filter_by(id=venue_id).all()[0]

    form = VenueForm(
        name=venue.name,
        city=venue.city,
        state=venue.state,
        address=venue.address,
        phone=venue.phone,
        facebook_link=venue.facebook_link,
        website_link=venue.website_link,
        image_link=venue.image_link,
        seeking_talent=venue.seeking_talent,
        seeking_description=venue.seeking_description
    )
    # DONE-TODO: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    try:
        venue = Venue.query.filter_by(id=venue_id).all()[0]

        venue.name = request.form.get('name')
        venue.city = request.form.get('city')
        venue.state = request.form.get('state')
        venue.address = request.form.get('address')
        venue.phone = request.form.get('phone')
        venue.facebook_link = request.form.get('facebook_link')
        venue.website_link = request.form.get('website_link')
        venue.image_link = request.form.get('image_link')
        venue.seeking_talent = request.form.get('seeking_talent')  # == 'True'
        venue.seeking_description = request.form.get('seeking_description')

        db.session.commit()
    except:
        db.session.rollback()
        flash('An error occurred. Venue could not be updated')
    finally:
        db.session.close()

    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():

    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
    error = False

    try:
        form = ArtistForm()

        new_artist = Artist(
            name=request.form.get('name'),
            city=request.form.get('city'),
            state=request.form.get('state'),
            phone=request.form.get('phone'),
            genres=request.form.getlist('genres'),
            facebook_link=request.form.get('facebook_link'),
            image_link=request.form.get('image_link'),
            website_link=request.form.get('website_link'),
            seeking_venue=request.form.get('seeking_venue') == 'True',
            seeking_description=request.form.get('seeking_description')
        )

        db.session.add(new_artist)
        db.session.commit()

    except:
        error = True
        db.session.rollback()

    finally:
        db.session.close()

    if not error:
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    else:
        flash('An error occurred. Artist ' +
              new_artist.name + ' could not be listed.')

    return redirect(url_for('index'))


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # DONE-TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.

    try:
        shows = Show.query.order_by(db.desc(Show.start_time))
        dataShows = []

        for show in shows:
            dataShows.append({
                "venue_id": show.venue_id,
                "venue_name": show.venue.name,
                "artist_id": show.artist_id,
                "artist_name": show.artist.name,
                "artist_image_link": show.artist.image_link,
                "start_time": format_datetime(str(show.start_time))
            })

        return render_template('pages/shows.html', shows=dataShows)
    except:
        flash('Error. No shows to display currently')
        return redirect(url_for('index'))


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # DONE-TODO: insert form data as a new Show record in the db, instead

    # on successful db insert, flash success
    error = False

    try:
        new_show = Show(
            start_time=request.form.get('start_time'),
            venue_id=request.form.get('venue_id'),
            artist_id=request.form.get('artist_id')
        )
        db.session.add(new_show)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
    finally:
        db.session.close()
    if not error:
        flash('Show was successfully listed!')
    else:
        flash('An error occurred. Show could not be listed.')

    return redirect(url_for('shows'))
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
