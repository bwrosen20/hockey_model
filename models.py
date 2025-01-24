from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
# from sqlalchemy.ext.associationproxy import association_proxy

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Game(db.Model, SerializerMixin):
    # __tablename__ = 'games'

    # serialize_rules = ('-players.game',)

    id = db.Column(db.Integer, primary_key=True)
    visitor = db.Column(db.String)
    home = db.Column(db.String)
    location = db.Column(db.String)
    home_score = db.Column(db.Integer)
    away_score = db.Column(db.Integer)
    home_even_corsi = db.Column(db.Integer)
    away_even_corsi = db.Column(db.Integer)
    home_even_hits = db.Column(db.Integer)
    away_even_hits = db.Column(db.Integer)
    home_even_blocks = db.Column(db.Integer)
    away_even_blocks = db.Column(db.Integer)

    home_pp_corsi = db.Column(db.Integer)
    away_pp_corsi = db.Column(db.Integer)
    home_pp_hits = db.Column(db.Integer)
    away_pp_hits = db.Column(db.Integer)
    home_pp_blocks = db.Column(db.Integer)
    away_pp_blocks = db.Column(db.Integer)

    away_penalty_mins = db.Column(db.Integer)
    home_penalty_mins = db.Column(db.Integer)


    date = db.Column(db.DateTime)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    players = db.relationship('PlayerGame', back_populates="game", cascade='all, delete-orphan')
    goalies = db.relationship('GoalieGame', back_populates="game", cascade='all, delete-orphan')
    # teams = db.relationship('Team', backref=backref('game'))

    def __repr__(self):
        return f'<{self.visitor} at {self.home} {self.date}>'

class Player(db.Model, SerializerMixin):
    # __tablename__ = 'players'

    # serialize_rules = ('-game.players', '-team.players',)
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    position = db.Column(db.Integer)
    side = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    games = db.relationship('PlayerGame', back_populates='player')
    final_bets = db.relationship('FinalBet', back_populates='player')

    

    def __repr__(self):
        return f'<{self.name}>'


class Goalie(db.Model, SerializerMixin):
    # __tablename__ = 'players'

    # serialize_rules = ('-game.players', '-team.players',)
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    games = db.relationship('GoalieGame', back_populates='goalie')

    

    def __repr__(self):
        return f'<{self.name}>'

# class FinalBet(db.Model, SerializerMixin):
#     # __tablename__ = 'players'

#     # serialize_rules = ('-game.players', '-team.players',)
    
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     category = db.Column(db.String)
#     category_value = db.Column(db.Integer)
#     date = db.Column(db.DateTime)
#     prop = db.Column(db.String)
#     line = db.Column(db.Integer)
#     algorithm = db.Column(db.String)
#     created_at = db.Column(db.DateTime, server_default=db.func.now())
#     updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    

#     def __repr__(self):
#         return f'<{self.category} {self.category_value} ({self.date}): {self.name} {self.line} {self.prop}>'


class PlayerGame(db.Model, SerializerMixin):
    # __tablename__ = 'player_games'

    id = db.Column(db.Integer, primary_key=True)
    team = db.Column(db.String)
    minutes = db.Column(db.Float)
    shots = db.Column(db.Integer)
    points = db.Column(db.Integer)
    assists = db.Column(db.Integer)
    goals = db.Column(db.Integer)
    pp_goals = db.Column(db.Integer)
    pp_assists = db.Column(db.Integer)
    penalty_minutes = db.Column(db.Integer)
    home = db.Column(db.Boolean)
    shot_stdev = db.Column(db.Integer)

    pp_corsi = db.Column(db.Integer)
    even_corsi = db.Column(db.Integer)
    even_on_ice_corsi = db.Column(db.Integer)
    pp_on_ice_corsi = db.Column(db.Integer)
    even_on_ice_against_corsi = db.Column(db.Integer)
    pp_on_ice_against_corsi = db.Column(db.Integer)
    pp_hits = db.column(db.Integer)
    even_hits = db.Column(db.Integer)
    pp_blocks = db.Column(db.Integer)
    even_blocks = db.Column(db.Integer)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    player_id = db.Column('player_id',db.Integer, db.ForeignKey('player.id'))
    game_id = db.Column('game_id',db.Integer, db.ForeignKey('game.id'))

    player = db.relationship('Player', back_populates='games')
    game = db.relationship('Game', back_populates='players')


    def __repr__(self):
        return f"<{self.player.name} on {self.game.date}>"


class GoalieGame(db.Model, SerializerMixin):
    # __tablename__ = 'players'

    # serialize_rules = ('-game.players', '-team.players',)
    
    id = db.Column(db.Integer, primary_key=True)
    saves = db.Column(db.Integer)
    goals = db.Column(db.Integer)
    minutes = db.Column(db.Float)
    penalty_minutes = db.Column(db.Integer)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    goalie_id = db.Column('goalie_id',db.Integer, db.ForeignKey('goalie.id'))
    game_id = db.Column('game_id',db.Integer, db.ForeignKey('game.id'))

    goalie = db.relationship('Goalie', back_populates='games')
    game = db.relationship('Game', back_populates='goalies')

    

    def __repr__(self):
        return f'<{self.goalie.name} on {self.game.date}>'


class FinalBet(db.Model, SerializerMixin):
    # __tablename__ = 'players'

    # serialize_rules = ('-game.players', '-team.players',)
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    prop = db.Column(db.String)
    line = db.Column(db.String)
    date = db.Column(db.DateTime)
    daily_index = db.Column(db.Integer)
    result = db.Column(db.Integer)
    over = db.Column(db.Boolean)
    arrays = db.Column(db.Integer)
    low_stdev = db.Column(db.Float)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    player_id = db.Column('player_id',db.Integer, db.ForeignKey('player.id'))
    player = db.relationship('Player',back_populates='final_bets')
    

    def __repr__(self):
        return f'<{self.name}>'

# class Team(db.Model, SerializerMixin):
#     __tablename__ = 'teams'

#     serialize_rules = ('-.user',)

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
    
#     created_at = db.Column(db.DateTime, server_default=db.func.now())
#     updated_at = db.Column(db.DateTime, onupdate=db.func.now())

#     players = db.relationship('Players', backref='team')
#     games = db.relationship('Games', backref='team')
