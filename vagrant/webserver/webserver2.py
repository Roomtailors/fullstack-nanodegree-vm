from flask import Flask, request, render_template, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from restaurants import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurants.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
    menuItem = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItem=menuItem.serialize)


@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    output = ''

    view = render_template('menu.html', items=items, restaurant=restaurant)

    return view

# Add menuitem
@app.route('/restaurants/<int:restaurant_id>/menuitem/add/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    output = ''

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        course = request.form['course']
        newEntry = MenuItem(name=name, description=description, price=price, course=course, restaurant_id=restaurant_id)
        session.add(newEntry)
        session.commit()
        flash('Menu item added')
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        output += "<form method='post' enctype='multipart/form-data'>"
        output += "<input type='text' name='name' placeholder='Enter item name'>"
        output += "<textarea name='description' placeholder='Enter description text'></textarea>"
        output += "<input type='text' name='price' placeholder='Price in Euro'>"
        output += "<input type='text' name='course' placeholder='Enter course'>"
        output += "<input type='submit' value='Add item'>"
        output += "</form>"
        return output

# Edit menuitem
@app.route('/restaurants/<int:restaurant_id>/menuitem/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    output = ''

    if request.method == 'POST':
        record = session.query(MenuItem).filter_by(id=menu_id).one()
        record.name = request.form['name']
        record.description = request.form['description']
        record.price = request.form['price']
        record.course = request.form['course']
        session.commit()
        flash('Menu item edited')
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))

    else:
        item = session.query(MenuItem).filter_by(id=menu_id).one()
        output += "<form method='post' enctype='multipart/form-data'>"
        output += "<input type='integer' name='id' value=" + str(item.id) + ">"
        output += "<input type='text' name='name' value=" + item.name + ">"
        output += "<textarea name='description' placeholder='Enter description text'>" + item.description + "</textarea>"
        output += "<input type='text' name='price' value=" + str(item.price) + ">"
        output += "<input type='text' name='course' value=" + item.course + ">"
        output += "<input type='submit' value='Add item'>"
        output += "</form>"
        return output

# Delete menuitem
@app.route('/restaurants/<int:restaurant_id>/menuitem/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    output = ''

    if request.method == 'POST':
        record = session.query(MenuItem).filter_by(id=menu_id).one()
        session.delete(record)
        session.commit()
        flash('Menu item deleted')
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        output += "<p>Are you sure you want to delete this item?</p>"
        output += "<form method='post' enctype='multipart/form-data'>"
        output += "<input type='submit' value='Delete item'>"
        output += "</form>"
        return output

if __name__ == '__main__':
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

