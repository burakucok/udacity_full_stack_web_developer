from flask import (Flask,
                   render_template,
                   request,
                   redirect, 
                   jsonify, 
                   url_for, 
                   flash, 
                   make_response)
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog Application"

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/login')
def showLogin():
    """Show login page"""
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    """Connects via google acount"""
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


def createUser(login_session):
    """create user record in db"""
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    """get user info"""
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


@app.route('/gdisconnect')
def gdisconnect():
    """Disconnects from google acount"""
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response



def getItems(category_id):
    """Returns all items in the given category
    args:
        category_id: category id which items will be get
    """
    return session.query(Item).filter_by(category_id=category_id).all()


@app.route('/JSON')
def categoryJSON():
    """JSON APIs to view Category Information"""
    categories = session.query(Category).all()
    return jsonify(Catalog=[c.serialize(getItems(c.id)) for c in categories])


@app.route('/')
def showCategories():
    """Shows all categories and latest items as list"""
    categories = session.query(Category).order_by(asc(Category.name))
    items = session.query(Item).order_by(Item.create_time.desc())
    return render_template('categories.html', categories = categories, items = items)


@app.route('/category/<int:category_id>/')
@app.route('/category/<int:category_id>/items/')
def showItems(category_id):
    """Shows Items in category as list
    Args:
        category_id: category id which items will be shown
    """
    category = session.query(Category).filter_by(id = category_id).one()
    items = session.query(Item).filter_by(category_id = category_id).all()
    return render_template('items.html', items = items, category = category)


@app.route('/category/<int:category_id>/item/<int:item_id>/', methods=['GET','POST'])
def showItem(category_id, item_id):
    """Shows Item
    Args:
        item_id: item id which will be shown
    """
    item = session.query(Item).filter_by(id = item_id).one()
    category = session.query(Category).filter_by(id = category_id).one()
    return render_template('item.html', item = item, category = category, 
                           isAuthenticatedUser = isAuthenticatedUser(item.user_id))


def isAuthenticatedUser(item_user_id):
    """Check whether items user is authenticated for item
    Args:
        item_user_id: user_id which will be checked with the logged in user_id
    """

    isAuthenticatedUser = False
    if ('user_id' in login_session and login_session['user_id'] == item_user_id):
        isAuthenticatedUser = True;
    return isAuthenticatedUser


@app.route('/category/<int:category_id>/item/new/',methods=['GET','POST'])
def newItem(category_id):
    """creates new item from post request
    Args:
        category_id: category id which item will be belongs to
    """
    if 'username' not in login_session:
        return redirect('/login')

    category = session.query(Category).filter_by(id = category_id).one()
    if request.method == 'POST':
        newItem = Item(title = request.form['title'], description = request.form['description'], 
                       category = category, user_id = login_session['user_id'])
        session.add(newItem)
        session.commit()
        return showItems(category_id)
    else:
        return render_template('newItem.html', category_id = category_id)


@app.route('/category/<int:category_id>/item/<int:item_id>/edit', methods=['GET','POST'])
def editItem(category_id, item_id):
    """edits item from post request
    Args:
        category_id: category id which item will be edited
        item_id: category id which will be edited
    """
    category = session.query(Category).filter_by(id = category_id).one()
    editedItem = session.query(Item).filter_by(id = item_id).one()
    if not isAuthenticatedUser(editedItem.user_id):
      return redirect('/login')

    if request.method == 'POST':
        if request.form['title']:
            editedItem.title = request.form['title']
        if request.form['description']:
            editedItem.description = request.form['description']
        session.add(editedItem)
        session.commit() 
        return redirect(url_for('showItems', category_id = category_id))
    else:
        return render_template('editItem.html', category_id = category_id, 
                               item_id = item_id, item = editedItem)


@app.route('/category/<int:category_id>/item/<int:item_id>/delete', methods = ['GET','POST'])
def deleteItem(category_id, item_id):
    """delete item from post request
    Args:
        category_id: category id which item will be deleted
        item_id: category id which will be deleted
    """
    category = session.query(Category).filter_by(id = category_id).one()
    itemToDelete = session.query(Item).filter_by(id = item_id).one() 
    if not isAuthenticatedUser(itemToDelete.user_id):
      return redirect('/login')

    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('showItems', category_id = category_id))
    else:
        return render_template('deleteItem.html', item = itemToDelete)


if __name__ == '__main__':
  app.secret_key = 'super_secret_key'
  app.debug = True
  app.run(host = '0.0.0.0', port = 5000)
