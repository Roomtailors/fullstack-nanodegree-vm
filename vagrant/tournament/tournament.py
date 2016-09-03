#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

# DATABASE contains all shared functions for database operations
class Database(object):
    """ Open and close database connection """
    con = object
    cur = object

    def __enter__(self):
        """ Create connection and cursor """
        self.con = psycopg2.connect("dbname=tournament")
        self.cur = self.con.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """ Terminate connection """
        self.con.close()

def deleteMatches():
    """Remove all records """
    with Database() as db:
        db.cur.execute("DELETE FROM matches")
        db.con.commit()

def deletePlayers():
    """Remove all records """
    with Database() as db:
        db.cur.execute("DELETE FROM players")
        db.con.commit()

def countPlayers():
    # Select player count
    with Database() as db:
        db.cur.execute("SELECT count(*) FROM players")
        result = db.cur.fetchone()

    # Return empty result if no players found
    if not result:
        return 0

    # Return count result
    return result[0]

def registerPlayer(name):

    # Insert player name into the database, auto-assign serial
    with Database() as db:
        db.cur.execute("INSERT INTO players (name) VALUES (%s)", (name,))
        db.con.commit()

def playerStandings():

    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    # Run query using the views wincounts and totalmatches
    with Database() as db:
        db.cur.execute("SELECT wincounts.id, wincounts.name, wincounts.wins, totalmatches.total_matches FROM wincounts JOIN totalmatches ON wincounts.id = totalmatches.id ORDER BY wincounts.wins DESC")
        result = db.cur.fetchall()

    return result

def reportMatch(winner, loser):

    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    with Database() as db:
        db.cur.execute("INSERT INTO matches (winner, loser) VALUES (%s, %s)", (winner, loser,))
        db.con.commit()
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    # Get players by rank
    with Database() as db:
        db.cur.execute("SELECT wincounts.id, wincounts.name FROM wincounts ORDER BY wincounts.wins DESC")
        opponents = db.cur.fetchall()

    # Prepare pairing variables
    index = 0
    pairings = []
    player_count = len(opponents)

    # Create pairings
    while (index < player_count):
        pair = opponents[index] + opponents[index+1]
        pairings.append(pair)
        index = index +2

    return pairings
