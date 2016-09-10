from flask import Flask, request, render_template, redirect, url_for, flash, jsonify, json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from restaurants import Base, Restaurant, MenuItem
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

engine = create_engine('sqlite:///restaurants.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# List all restaurants
@app.route('/restaurants/')
def showRestaurants():
    restaurants = session.query(Restaurant).all()
    view = render_template('restaurants.html', restaurants=restaurants)
    return view

# Create new restaurant
@app.route('/restaurant/new', methods=['GET', 'POST'])
def addRestaurant():

    # Process posted data
    if request.method == 'POST':
        name = request.form['name']
        newEntry = Restaurant(name=name)
        session.add(newEntry)
        session.commit()
        flash('Restaurant added')
        return redirect(url_for('viewRestaurantMenu', restaurant_id=newEntry.id))

    # Render form
    else:
        view = render_template('newrestaurant.html')
        return view

# Edit restaurant
@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    if request.method == 'POST':
        record = session.query(Restaurant).filter_by(id=restaurant_id).one()
        record.name = request.form['name']
        session.commit()
        flash('Restaurant edited')
        return redirect(url_for('viewRestaurantMenu', restaurant_id=restaurant_id))

    else:
        restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
        view = render_template('editrestaurant.html', restaurant = restaurant)
        return view

# Delete restaurant
@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    if request.method == 'POST':
        record = session.query(Restaurant).filter_by(id=restaurant_id).one()
        session.delete(record)
        session.commit()
        flash('Restaurant and related menu deleted')
        return redirect(url_for('showRestaurants'))
    else:
        view = render_template('deleterestaurant.html', restaurant_id=restaurant_id)
        return view

# List restaurant menu
@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def viewRestaurantMenu(restaurant_id):
    # Receive data
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()

    # Create view
    view = render_template('menu.html', restaurant=restaurant, items=items)

    return view

# Edit restaurant menu item
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET', 'POST'])
def editRestaurantMenu(restaurant_id, menu_id):
    record = session.query(MenuItem).filter_by(id=menu_id).one()

    if request.method == 'POST':
        record.name = request.form['name']
        record.description = request.form['description']
        record.price = request.form['price']
        record.course = request.form['course']
        session.commit()
        flash('Menu item edited')
        return redirect(url_for('viewRestaurantMenu', restaurant_id=restaurant_id))

    else:
        view = render_template('editmenuitem.html', restaurant_id=restaurant_id, item=record)
        return view

# Delete restaurant menu item
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET', 'POST'])
def deleteRestaurantMenu(restaurant_id, menu_id):
    if request.method == 'POST':
        record = session.query(MenuItem).filter_by(id=menu_id).one()
        session.delete(record)
        session.commit()
        flash('Menu item deleted')
        return redirect(url_for('viewRestaurantMenu', restaurant_id=restaurant_id))
    else:
        view = render_template('deletemenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id)
        return view

# Add restaurant menu item
@app.route('/restaurant/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):

    # Process posted data
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        course = request.form['course']
        newEntry = MenuItem(name=name, description=description, price=price, course=course, restaurant_id=restaurant_id)
        session.add(newEntry)
        session.commit()
        flash('Menu item added')
        return redirect(url_for('viewRestaurantMenu', restaurant_id=restaurant_id))

    # Render form
    else:
        view = render_template('newmenuitem.html', restaurant_id=restaurant_id)
        return view


# API ENDPOINTS

@app.route('/restaurants/JSON')
def restaurantsJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurants=[restaurant.serialize for restaurant in restaurants])

@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def restaurantMenuItemJSON(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItems=[item.serialize])


# Run app as main
if __name__ == '__main__':
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.debug = True
    toolbar = DebugToolbarExtension(app)
    app.run(host= '0.0.0.0', port = 5000)