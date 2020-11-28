from flask import render_template, url_for, flash, redirect, request, abort
import secrets
import os
from PIL import Image
from my_app.models import User, Post
from my_app import app, db, bcrypt
from my_app.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flask_login import login_user, current_user, logout_user, login_required
from geopy import Nominatim, distance
from sqlalchemy import any_
import geocoder

class Location:
    def __init__(self, title, longitud, latitud, price):
        self.title = title
        self.longitud = longitud
        self.latitud = latitud
        self.price = price


#  @app.route('/home')
@app.route('/SearchNotFound')
def search_this():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    q = request.args.get('q', type=str)
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    if q:
        posts = Post.query.filter(Post.title.contains(str(q)))
        posts_else = Post.query.filter(Post.content.contains(str(q)))
        if len(list(posts)) == 0 and len(list(posts_else)) == 0:
            return render_template('SearchNotFound.html', title='Not found')
        else:
            posts = Post.query.filter(Post.title.contains(q) | Post.content.contains(q)).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
            return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)
    else:
        return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/', methods=['GET', 'POST'])
def landing_page():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list_title_and_content = []
    q = request.args.get('q', type=str)
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    if q:
        posts = Post.query.filter(Post.title.contains(str(q)))
        posts_else = Post.query.filter(Post.content.contains(str(q)))

        post = Post.query.filter(Post.title.contains(str(q)))

        titleListTitle = []
        longiListTitle = []
        latiListTitle = []
        priceListTitle = []
        for x in post:
            titleListTitle.append(x.title)
            longiListTitle.append(x.longitud)
            latiListTitle.append(x.latitud)
            priceListTitle.append(x.price)
        for x in range(len(longiListTitle)):
            list_title_and_content.append(Location(titleListTitle[x], longiListTitle[x], latiListTitle[x], priceListTitle[x]))

        post = Post.query.filter(Post.content.contains(str(q)))
        titleListTitle = []
        longiListContent = []
        latiListContent = []
        priceListContent = []

        for x in post:
            titleListTitle.append(x.title)
            longiListContent.append(x.longitud)
            latiListContent.append(x.latitud)
            priceListContent.append(x.price)
        for x in range(len(longiListContent)):
            list_title_and_content.append(Location(titleListTitle[x], longiListContent[x], latiListContent[x], priceListContent[x]))


        if len(list(posts)) == 0 and len(list(posts_else)) == 0:
            return render_template('SearchNotFound.html', title='Not found')
        else:
            posts = Post.query.filter(Post.title.contains(q) | Post.content.contains(q)).order_by(
                Post.date_posted.desc()).paginate(page=page, per_page=5)
            return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list_title_and_content)
    else:
        return render_template('index.html', title='Welcome')

    # return render_template('index.html', title='Welcome')


#  @app.route('/', methods=['GET'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list_title_and_content = []
    q = request.args.get('q', type=str)
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)

    if q:
        posts = Post.query.filter(Post.title.contains(str(q)))
        posts_else = Post.query.filter(Post.content.contains(str(q)))

        post = Post.query.filter(Post.title.contains(str(q)))
        titleListTitle = []
        longiListContent = []
        latiListContent = []
        priceListTitle = []

        for x in post:
            titleListTitle.append(x.title)
            longiListContent.append(x.longitud)
            latiListContent.append(x.latitud)
            priceListTitle.append(x.price)
        for x in range(len(longiListContent)):
            list_title_and_content.append(Location(titleListTitle[x], longiListContent[x], latiListContent[x], priceListTitle[x]))

        post = Post.query.filter(Post.content.contains(str(q)))
        titleListTitle = []
        longiListContent = []
        latiListContent = []
        priceListTitle = []

        for x in post:
            titleListTitle.append(x.title)
            longiListContent.append(x.longitud)
            latiListContent.append(x.latitud)
            priceListTitle.append(x.price)
        for x in range(len(longiListContent)):
            list_title_and_content.append(Location(titleListTitle[x], longiListContent[x], latiListContent[x], priceListTitle[x]))

        if len(list(posts)) == 0 and len(list(posts_else)) == 0:
            return render_template('SearchNotFound.html', title='Not found')
        else:
            posts = Post.query.filter(Post.title.contains(q) | Post.content.contains(q)).order_by(
                Post.date_posted.desc()).paginate(page=page, per_page=5)
            return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token,
                                   locations=list_title_and_content)
    else:
        listAll = []
        post = Post.query.all()
        titleList = []
        longiList = []
        latiList = []
        priceList = []
        for x in post:
            titleList.append(x.title)
            longiList.append(x.longitud)
            latiList.append(x.latitud)
            priceList.append(x.price)
        for x in range(len(longiList)):
            listAll.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
        page = request.args.get('page', 1, type=int)
        posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
        return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=listAll)


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))  # home is the name of the function home()
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('landing_page'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('landing_page'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('landing_page'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, file_extension = os.path.splitext(form_picture.filename)
    picture_file_name = random_hex + file_extension
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_file_name)
    image = Image.open(form_picture)
    image.save(picture_path, quality=95)
    return picture_file_name


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.profile_picture.data:
            picture_file = save_picture(form.profile_picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


def save_picture_post(form_picture):
    random_hex = secrets.token_hex(8)
    _, file_extension = os.path.splitext(form_picture.filename)
    picture_file_name = random_hex + file_extension
    picture_path = os.path.join(app.root_path, 'static/house_pictures', picture_file_name)
    output_size = (250, 250)
    image = Image.open(form_picture)
    image.thumbnail(output_size)
    image.save(picture_path)
    return picture_file_name


@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    form = PostForm()
    if form.validate_on_submit():
        if form.master_bedroom.data:
            _, file_extension = os.path.splitext(form.master_bedroom.data.filename)
            bedroom_name = str(save_picture_post(form.master_bedroom.data))
        else:
            bedroom_name = 'default_house.jpg'
        if form.master_bathroom.data:
            _, file_extension = os.path.splitext(form.master_bathroom.data.filename)
            bathroom_name = str(save_picture_post(form.master_bathroom.data))
        else:
            bathroom_name = 'default_house.jpg'
        if form.kitchen.data:
            _, file_extension = os.path.splitext(form.kitchen.data.filename)
            kitchen_name = str(save_picture_post(form.kitchen.data))
        else:
            kitchen_name = 'default_house.jpg'
        if form.outside_view.data:
            _, file_extension = os.path.splitext(form.outside_view.data.filename)
            outside_view_name = str(save_picture_post(form.outside_view.data))
        else:
            outside_view_name = 'default_house.jpg'
        optional_pics = [form.house_pictures.data]
        outer_array = optional_pics[0]
        inside_array = str(outer_array[0])
        string_to_check = "<FileStorage: ''"
        if string_to_check in inside_array:
            placeholder = str('default_house.jpg')
            optional_pics = [placeholder]
        else:
            optional_pics.clear()
            for pic in form.house_pictures.data:
                _, file_extension = os.path.splitext(pic.filename)
                optional_pics.append(str(save_picture_post(pic)))
        zipcode = ''
        if form.zip_postal_code.data:
            if len(form.zip_postal_code.data) == 3:
                zipcode = '00' + form.zip_postal_code.data
            elif len(form.zip_postal_code.data) == 4:
                zipcode = '0' + form.zip_postal_code.data
            else:
                zipcode = form.zip_postal_code.data

        if form.address_line_2.data:
            locator = Nominatim(user_agent="myGeocoder")
            testString = str(form.address_line_1.data) + ', ' + str(form.address_line_2.data) + ', ' + str(
                form.city.data) + ', ' + 'Puerto Rico, ' + zipcode + ', US'
            locationFound = locator.geocode(testString)
            longi = str(locationFound.longitude)
            lati = str(locationFound.latitude)
            floatLati = locationFound.latitude
            floatLongi = locationFound.longitude
        else:
            locator = Nominatim(user_agent="myGeocoder")
            testString = str(form.address_line_1.data) + ', ' + str(form.city.data) + ', ' + 'Puerto Rico, ' + zipcode + ', US'
            locationFound = locator.geocode(testString)
            longi = str(locationFound.longitude)
            lati = str(locationFound.latitude)
            floatLati = locationFound.latitude
            floatLongi = locationFound.longitude

        post = Post(title=form.title.data, buy_or_rent=form.buy_or_rent.data, content=form.content.data, amenities=form.amenities.data,
                    master_bedroom=bedroom_name, master_bathroom=bathroom_name, kitchen=kitchen_name,
                    outside_view=outside_view_name, house_pictures=optional_pics,
                    address_line_1=form.address_line_1.data, address_line_2=form.address_line_2.data,
                    city=form.city.data, state_province_region=form.state_province_region.data,
                    zip_postal_code=zipcode, number_of_bedrooms=form.number_of_bedrooms.data,
                    number_of_bathrooms=form.number_of_bathrooms.data, price=form.price.data,
                    longitud=longi, latitud=lati, floatLati=floatLati, floatLongi=floatLongi, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post', mapbox_access_token=mapbox_access_token)

@app.route('/post/<int:post_id>')
def post(post_id):
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.get_or_404(post_id)
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    titleList.append(post.title)
    longiList.append(post.longitud)
    latiList.append(post.latitud)
    priceList.append(post.price)
    list.append(Location(titleList[0],longiList[0], latiList[0],priceList[0]))
    return render_template('post.html', title=post.title, post=post, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.amenities = form.amenities.data
        zipcode = ''
        if form.zip_postal_code.data:
            if len(form.zip_postal_code.data) == 3:
                zipcode = '00' + form.zip_postal_code.data
            elif len(form.zip_postal_code.data) == 4:
                zipcode = '0' + form.zip_postal_code.data
            else:
                zipcode = form.zip_postal_code.data
        post.zip_postal_code = zipcode
        db.session.commit()
        flash('Your post has been updated successfully!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.amenities.data = post.amenities
        form.price.data = post.price
        form.number_of_bathrooms.data = post.number_of_bathrooms
        form.number_of_bedrooms.data = post.number_of_bedrooms
        form.zip_postal_code.data = post.zip_postal_code
        form.state_province_region.data = post.state_province_region
        form.city.data = post.city
        form.address_line_1.data = post.address_line_1
        form.address_line_2.data = post.address_line_2
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')


@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route('/user/<string:username>')
def user_posts(username):
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    user1 = User.query.filter_by(username=username).first_or_404()
    post = Post.query.filter_by(author=user1)
    titleList = []
    longiList = []
    latiList = []
    priceList =[]
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))

    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('user_post.html', posts=posts, user=user, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/filter_search', methods=['GET', 'POST'])
def search_this_filter():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    titleList =[]
    longiList = []
    latiList = []
    priceList =[]
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    if request.method == 'POST':
        array = request.form.getlist('mycheckbox')
        if len(array) != 0:
            for x in array:
                posts = Post.query.filter(Post.amenities.any(x)).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)

                post = Post.query.filter(Post.amenities.any(str(x)))
                for p in post:
                    titleList.append(p.title)
                    longiList.append(p.longitud)
                    latiList.append(p.latitud)
                    priceList.append(p.price)
                for r in range(len(longiList)):
                    list.append(Location(titleList[r], longiList[r], latiList[r], priceList[r]))

            if len(posts.items) != 0:
                return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)
            else:
                return render_template('SearchNotFound.html', title='Not found')
        else:
            post = Post.query.all()
            for x in post:
                titleList.append(x.title)
                longiList.append(x.longitud)
                latiList.append(x.latitud)
                priceList.append(x.price)
            for x in range(len(longiList)):
                list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))

            return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)
    else:
        return render_template('SearchNotFound.html', title='Not found')


@app.route('/SearchNotFound')
def search_not_found():
    return render_template('SearchNotFound.html', title='Not found')


@app.route('/Rent', methods=['GET'])
def filter_rent():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.buy_or_rent.contains('Rent'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.buy_or_rent.contains('Rent')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Buy', methods=['GET'])
def filter_buy():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.buy_or_rent.contains('Buy'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.buy_or_rent.contains('Buy')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)

@app.route('/nearby', methods=['GET', 'POST'])
def nearby():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.all()
    titleList =[]
    longiList = []
    latiList = []
    priceList =[]
    for x in post:
        titleList.append(x.title)
        longiList.append(x.floatLongi)
        latiList.append(x.floatLati)
        priceList.append(x.price)
    g = geocoder.ip('me')
    my_location = g.latlng
    myLocation = [float(my_location[0]), float(my_location[1])]
    for x in range(len(longiList)):
        tempArray = [latiList[x], longiList[x]]
        if distance.distance(myLocation, tempArray) <= 32.1869:
            list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    latListForQuery = []
    for x in list:
        latListForQuery.append(x.latitud)
    stringList = []
    for x in latListForQuery:
        stringList.append(str(x))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.latitud.like(any_(stringList))).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)

@app.route('/Adjuntas', methods=['GET'])
def city_filter_Adjuntas():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Adjuntas'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Adjuntas')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Aguada', methods=['GET'])
def city_filter_Aguada():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Aguada'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Aguada')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Aguadilla', methods=['GET'])
def city_filter_Aguadilla():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Aguadilla'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Aguadilla')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Aguas%Buenas', methods=['GET'])
def city_filter_Aguas_Buenas():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Aguas Buenas'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Aguas Buenas')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Aibonito', methods=['GET'])
def city_filter_Aibonito():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Aibonito'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Aibonito')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Añasco', methods=['GET'])
def city_filter_Anasco():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Añasco'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Añasco')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Arecibo', methods=['GET'])
def city_filter_Arecibo():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Arecibo'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Arecibo')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Arroyo', methods=['GET'])
def city_filter_Arroyo():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Arroyo'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Arroyo')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Barceloneta', methods=['GET'])
def city_filter_Barceloneta():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Barceloneta'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Barceloneta')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token)


@app.route('/Barranquitas', methods=['GET'])
def city_filter_Barranquitas():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Barranquitas'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Barranquitas')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Bayamón', methods=['GET'])
def city_filter_Bayamon():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Bayamón'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Bayamón')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Cabo%Rojo', methods=['GET'])
def city_filter_Cabo_Rojo():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Cabo Rojo'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Cabo Rojo')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Caguas', methods=['GET'])
def city_filter_Caguas():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Caguas'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Caguas')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Camuy', methods=['GET'])
def city_filter_Camuy():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Camuy'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Camuy')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Canovanas', methods=['GET'])
def city_filter_Canovanas():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Canovanas'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Canóvanas')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Carolina', methods=['GET'])
def city_filter_Carolina():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Carolina'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Carolina')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Cataño', methods=['GET'])
def city_filter_Catano():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Cataño'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Cataño')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Cayey', methods=['GET'])
def city_filter_Cayey():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Cayey'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Cayey')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Ceiba', methods=['GET'])
def city_filter_Ceiba():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Ceiba'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Ceiba')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Ciales', methods=['GET'])
def city_filter_Ciales():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Ciales'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Ciales')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Cidra', methods=['GET'])
def city_filter_Cidra():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Cidra'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Cidra')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Coamo', methods=['GET'])
def city_filter_Coamo():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Coamo'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Coamo')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Comerío', methods=['GET'])
def city_filter_Comerio():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Comerío'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Comerío')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Corozal', methods=['GET'])
def city_filter_Corozal():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Corozal'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Corozal')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Culebra', methods=['GET'])
def city_filter_Culebra():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Culebra'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Culebra')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Dorado', methods=['GET'])
def city_filter_Dorado():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Dorado'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Dorado')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Fajardo', methods=['GET'])
def city_filter_Fajardo():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Fajardo'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Fajardo')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Florida', methods=['GET'])
def city_filter_Florida():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Florida'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Florida')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Guánica', methods=['GET'])
def city_filter_Guanica():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Guánica'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Guánica')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Guayama', methods=['GET'])
def city_filter_Guayama():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Guayama'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Guayama')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Guayanilla', methods=['GET'])
def city_filter_Guayanilla():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Guayanilla'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Guayanilla')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Guaynabo', methods=['GET'])
def city_filter_Guaynabo():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Guaynabo'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Guaynabo')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Gurabo', methods=['GET'])
def city_filter_Gurabo():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Gurabo'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Gurabo')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Hatillo', methods=['GET'])
def city_filter_Hatillo():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Hatillo'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Hatillo')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Hormigueros', methods=['GET'])
def city_filter_Hormigueros():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Hormigueros'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Hormigueros')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Humacao', methods=['GET'])
def city_filter_Humacao():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Humacao'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Humacao')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Isabela', methods=['GET'])
def city_filter_Isabela():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Isabela'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Isabela')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Jayuya', methods=['GET'])
def city_filter_Jayuya():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Jayuya'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Jayuya')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Juana%Díaz', methods=['GET'])
def city_filter_Juana_Diaz():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Juana Díaz'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Juana Díaz')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Juncos', methods=['GET'])
def city_filter_Juncos():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Juncos'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Juncos')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Lajas', methods=['GET'])
def city_filter_Lajas():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Lajas'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Lajas')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Lares', methods=['GET'])
def city_filter_Lares():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Lares'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Lares')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Las%Marías', methods=['GET'])
def city_filter_Las_Marias():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Las Marías'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Las Marías')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Las%Piedras', methods=['GET'])
def city_filter_Las_Piedras():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Las Piedras'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Las Piedras')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Loíza', methods=['GET'])
def city_filter_Loiza():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Loíza'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Loíza')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Luquillo', methods=['GET'])
def city_filter_Luquillo():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Luquillo'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Luquillo')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Manatí', methods=['GET'])
def city_filter_Manati():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Manatí'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Manatí')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Maricao', methods=['GET'])
def city_filter_Maricao():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Maricao'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Maricao')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Maunabo', methods=['GET'])
def city_filter_Maunabo():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Maunabo'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Maunabo')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Mayagüez', methods=['GET'])
def city_filter_Mayaguez():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Mayagüez'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Mayagüez')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Moca', methods=['GET'])
def city_filter_Moca():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Moca'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Moca')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Morovis', methods=['GET'])
def city_filter_Morovis():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Morovis'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Morovis')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Naguabo', methods=['GET'])
def city_filter_Naguabo():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Naguabo'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Naguabo')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Naranjito', methods=['GET'])
def city_filter_Naranjito():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Naranjito'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Naranjito')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Orocovis', methods=['GET'])
def city_filter_Orocovis():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Orocovis'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Orocovis')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Patillas', methods=['GET'])
def city_filter_Patillas():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Patillas'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Patillas')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Peñuelas', methods=['GET'])
def city_filter_Penuelas():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Peñuelas'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Peñuelas')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Ponce', methods=['GET'])
def city_filter_Ponce():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Ponce'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Ponce')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Quebradillas', methods=['GET'])
def city_filter_Quebradillas():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Quebradillas'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Quebradillas')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Rincón', methods=['GET'])
def city_filter_Rincon():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Rincón'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Rincón')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Río%Grande', methods=['GET'])
def city_filter_Rio_Grande():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Río Grande'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Río Grande')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Sabana%Grande', methods=['GET'])
def city_filter_Sabana_Grande():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Sabana Grande'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Sabana Grande')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Salinas', methods=['GET'])
def city_filter_Salinas():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Salinas'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Salinas')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/San%Germán', methods=['GET'])
def city_filter_San_German():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('San Germán'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('San German')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/San%Juan', methods=['GET'])
def city_filter_San_Juan():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('San Juan'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('San Juan')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/San%Lorenzo', methods=['GET'])
def city_filter_San_Lorenzo():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('San Lorenzo'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('San Lorenzo')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/San%Sebastián', methods=['GET'])
def city_filter_San_Sebastian():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('San Sebastián'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('San Sebastián')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


#fixed
@app.route('/Santa%Isabel', methods=['GET'])
def city_filter_Santa_Isabel():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Santa Isabel'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Santa Isabel')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Toa%Baja', methods=['GET'])
def city_filter_Toa_Baja():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Toa Baja'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Toa Baja')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Toa%Alta', methods=['GET'])
def city_filter_Toa_Alta():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Toa Alta'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Toa Alta')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Trujillo%Alto', methods=['GET'])
def city_filter_Trujillo_Alto():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Trujillo Alto'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Trujillo Alto')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Utuado', methods=['GET'])
def city_filter_Utuado():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Utuado'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Utuado')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Vega%Alta', methods=['GET'])
def city_filter_Vega_Alta():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Vega Alta'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Vega Alta')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Vega%Baja', methods=['GET'])
def city_filter_Vega_Baja():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Vega Baja'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Vega Baja')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Vieques', methods=['GET'])
def city_filter_Vieques():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Vieques'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Vieques')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Villalba', methods=['GET'])
def city_filter_Villalba():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Villalba'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Villalba')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Yabucoa', methods=['GET'])
def city_filter_Yabucoa():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Yabucoa'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Yabucoa')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)


@app.route('/Yauco', methods=['GET'])
def city_filter_Yauco():
    mapbox_access_token = 'pk.eyJ1Ijoiam9zZS1zYW50aWFnbzkwIiwiYSI6ImNraGlpaHlzMTFienAzMHBmdms1ODNjcTEifQ.mA4WMGbNBOQgaKcXy2FoPg'
    list = []
    post = Post.query.filter(Post.city.contains('Yauco'))
    titleList = []
    longiList = []
    latiList = []
    priceList = []
    for x in post:
        titleList.append(x.title)
        longiList.append(x.longitud)
        latiList.append(x.latitud)
        priceList.append(x.price)
    for x in range(len(longiList)):
        list.append(Location(titleList[x], longiList[x], latiList[x], priceList[x]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.city.contains('Yauco')).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, mapbox_access_token=mapbox_access_token, locations=list)