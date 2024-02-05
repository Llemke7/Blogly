from app import app, db
from models import User, Post


app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'

def test_homepage():
    with app.test_client() as client:
        resp = client.get('/')
        assert resp.status_code == 200

def test_new_user():
    with app.test_client() as client:
        resp = client.post('/', data={'first_name': 'John', 'last_name': 'Doe', 'image_url': 'test.jpg'})
        assert resp.status_code == 302

        user = User.query.filter_by(first_name='John').first()
        assert user is not None
        assert user.last_name == 'Doe'

def test_show_user():
    with app.test_client() as client:
        user = User(first_name='Jane', last_name='Doe', image_url='test.jpg')
        db.session.add(user)
        db.session.commit()

        resp = client.get(f'/user/{user.id}')
        assert resp.status_code == 200
        assert b'Jane Doe' in resp.data

def test_edit_user():
    with app.test_client() as client:
        user = User(first_name='Jack', last_name='Smith', image_url='test.jpg')
        db.session.add(user)
        db.session.commit()

        resp = client.post(f'/user/{user.id}/edit', data={'first_name': 'Updated', 'last_name': 'User', 'image_url': 'updated.jpg'})
        assert resp.status_code == 302

        updated_user = User.query.get(user.id)
        assert updated_user.first_name == 'Updated'
        assert updated_user.last_name == 'User'

def test_delete_user():
    with app.test_client() as client:
        user = User(first_name='ToDelete', last_name='User', image_url='test.jpg')
        db.session.add(user)
        db.session.commit()

        resp = client.post(f'/user/{user.id}/delete')
        assert resp.status_code == 302

        deleted_user = User.query.get(user.id)
        assert deleted_user is None


def test_new_post():
    with app.test_client() as client:
        user = User(first_name='John', last_name='Doe', image_url='test.jpg')
        db.session.add(user)
        db.session.commit()

        resp = client.post(f'/users/{user.id}/posts/new', data={'title': 'New Post', 'content': 'This is a new post.'})
        assert resp.status_code == 302

        post = Post.query.filter_by(title='New Post').first()
        assert post is not None
        assert post.content == 'This is a new post.'
        assert post.user_id == user.id

def test_show_post():
    with app.test_client() as client:
        user = User(first_name='Jane', last_name='Doe', image_url='test.jpg')
        db.session.add(user)
        db.session.commit()

        post = Post(title='Test Post', content='This is a test post.', user_id=user.id)
        db.session.add(post)
        db.session.commit()

        resp = client.get(f'/posts/{post.id}')
        assert resp.status_code == 200
        assert b'Test Post' in resp.data
        assert b'This is a test post.' in resp.data
        assert b'Jane Doe' in resp.data