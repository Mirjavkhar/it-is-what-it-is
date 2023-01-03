from flask_security import UserMixin, RoleMixin
from flask_login import AnonymousUserMixin
from slugify import slugify
from hashlib import md5
from app import db
import datetime

# === Relationship tables === #

community_category = db.Table('community_category',
    db.Column('community_id', db.Integer(), db.ForeignKey('community.id')),
    db.Column('category_id', db.Integer(), db.ForeignKey('category.id'))
)

post_community = db.Table('post_community',
    db.Column('post_id', db.Integer(), db.ForeignKey('post.id')),
    db.Column('community_id', db.Integer(), db.ForeignKey('community.id'))
)

post_comment = db.Table('post_comment',
    db.Column('post_id', db.Integer(), db.ForeignKey('post.id')),
    db.Column('comment_id', db.Integer(), db.ForeignKey('comment.id'))
)

post_media = db.Table('post_media',
    db.Column('post_id', db.Integer(), db.ForeignKey('post.id')),
    db.Column('media_id', db.Integer(), db.ForeignKey('media.id'))
)

user_post = db.Table('user_post',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('post_id', db.Integer(), db.ForeignKey('post.id'))
)

user_community = db.Table('user_community',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('community_id', db.Integer(), db.ForeignKey('community.id'))
)

save_post = db.Table('save_post',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('post_id', db.Integer(), db.ForeignKey('post.id'))
)

user_role = db.Table('user_role',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

user_rank = db.Table('user_rank',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('rank_id', db.Integer(), db.ForeignKey('rank.id'))
)

user_comment = db.Table('user_comment',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('comment_id', db.Integer(), db.ForeignKey('comment.id'))
)

user_report = db.Table('user_report',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('report_id', db.Integer(), db.ForeignKey('report.id'))
)

members = db.Table('members',
    db.Column('community_id', db.Integer(), db.ForeignKey('community.id')),
    db.Column('member_id', db.Integer(), db.ForeignKey('user.id'))
)

followers = db.Table('followers',
    db.Column('follower_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer(), db.ForeignKey('user.id'))
)

like = db.Table('like',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('post_id', db.Integer(), db.ForeignKey('post.id'))
)

dislike = db.Table('dislike',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('post_id', db.Integer(), db.ForeignKey('post.id'))
)

# === Classes === #

class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    created_on = db.Column(db.DateTime(), default=datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f%Z"))
    creator_id = db.Column(db.Integer())
    title = db.Column(db.String(100), unique=True)
    slug = db.Column(db.String(100), unique=True)
    content = db.Column(db.String(10000))
    likes = db.Column(db.Integer())
    dislikes = db.Column(db.Integer())
    stats = db.Column(db.Integer())
    updated = db.Column(db.Boolean, default=False)
    updated_on = db.Column(db.DateTime(), default=datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f%Z"))
    
    # === Relationships === #

    community = db.relationship('Community', secondary='post_community', backref=db.backref('posts', lazy='dynamic'), lazy='dynamic')
    comments = db.relationship('Comment', secondary='post_comment', backref=db.backref('post', lazy='dynamic'), lazy='dynamic')
    medias = db.relationship('Media', secondary='post_media', backref=db.backref('post', lazy='dynamic'), lazy='dynamic')

    # === Functions === #

    def rating(self):
        if self.likes is None:
            self.likes = 0
        if self.dislikes is None:
            self.dislikes = 0
        return self.likes - self.dislikes

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)
        return self.generate_slug()

    def generate_slug(self):
        if self.title:
            self.slug = slugify(self.title)

    def __repr__(self):
        return '<Post ID: {}, Title: {}>'.format(self.id, self.title)


class Media(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), unique=True)


class Category(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), unique=True)
    slug = db.Column(db.String(100), unique=True)
    about = db.Column(db.String(500))

    # === Functions === #

    def __init__(self, *args, **kwargs):
        super(Category, self).__init__(*args, **kwargs)
        self.slug = slugify(self.name)

    def __repr__(self):
        return '<Category ID: {}, Name: {}>'.format(self.id, self.name)


class Community(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    creator_id = db.Column(db.Integer())
    created_on = db.Column(db.DateTime(), default=datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f%Z"))
    name = db.Column(db.String(100), unique=True)
    slug = db.Column(db.String(100), unique=True)
    about = db.Column(db.String(500))
    color = db.Column(db.String())
    img = db.Column(db.String())
    bgimg = db.Column(db.String())
    com_members = db.Column(db.Integer())
    confirm = db.Column(db.Boolean(), default=False)

    # === Relationships === #

    category = db.relationship('Category', secondary='community_category', backref=db.backref('communities', lazy='dynamic'), lazy='dynamic')

    # === Functions === #

    def __init__(self, *args, **kwargs):
        super(Community, self).__init__(*args, **kwargs)
        self.slug = slugify(self.name)

    def __repr__(self):
        return '<Community ID: {}, Name: {}>'.format(self.id, self.name)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    created_on = db.Column(db.DateTime(), default=datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f%Z"))
    name = db.Column(db.String(100), unique=True)
    slug = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))
    about = db.Column(db.String(200))
    points = db.Column(db.Integer())
    last_seen = db.Column(db.DateTime(), default=datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f%Z"))
    active = db.Column(db.Boolean(), nullable=False, default=True)
    official = db.Column(db.Boolean(), nullable=False, default=False)
    confirm = db.Column(db.Boolean(), nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime(), default=datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f%Z"))
    avatar = db.Column(db.String())
    blocked = db.Column(db.Boolean(), default=False)
    
    # === Relationships === #

    posts = db.relationship('Post', secondary='user_post', backref=db.backref('creator', lazy='dynamic'), lazy='dynamic')
    roles = db.relationship('Role', secondary='user_role', backref=db.backref('users', lazy='dynamic'), lazy='dynamic')
    rank = db.relationship('Rank', secondary='user_rank', backref=db.backref('users', lazy='dynamic'), lazy='dynamic')
    comments = db.relationship('Comment', secondary='user_comment', backref=db.backref('creator', lazy='dynamic'), lazy='dynamic')
    reports = db.relationship('Report', secondary='user_report', backref=db.backref('creator', lazy='dynamic'), lazy='dynamic')
    communities = db.relationship('Community', secondary='user_community', backref=db.backref('creator', lazy='dynamic'), lazy='dynamic')
    saved_posts = db.relationship('Post', secondary='save_post', primaryjoin=(save_post.c.user_id == id), secondaryjoin=(save_post.c.post_id == Post.id), backref=db.backref('users', lazy='dynamic'), lazy='dynamic')
    followed_community = db.relationship('Community', secondary='members', primaryjoin=(members.c.member_id == id), secondaryjoin=(members.c.community_id == Community.id), backref=db.backref('members', lazy='dynamic'), lazy='dynamic')
    followed = db.relationship('User', secondary='followers', primaryjoin=(followers.c.follower_id == id), secondaryjoin=(followers.c.followed_id == id), backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
    liked = db.relationship('Post', secondary='like', primaryjoin=(like.c.user_id == id), secondaryjoin=(like.c.post_id == Post.id), backref=db.backref('like', lazy='dynamic'), lazy='dynamic')
    disliked = db.relationship('Post', secondary='dislike', primaryjoin=(dislike.c.user_id == id), secondaryjoin=(dislike.c.post_id == Post.id), backref=db.backref('dislike', lazy='dynamic'), lazy='dynamic')

    # === Functions === #

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self

    def is_following(self, users):
        return self.followed.filter(followers.c.followed_id == users.id).count() > 0

    def followers_list(self):
        return db.session.query(followers).filter(followers.c.followed_id == self.id).all()

    def following_list(self):
        return db.session.query(followers).filter(followers.c.follower_id == self.id).all()

    def save_unsave(self, post):
        if not self.is_post_saved(post):
            self.saved_posts.append(post)
            return self
        if self.is_post_saved(post):
            self.saved_posts.remove(post)
            return self

    def is_post_saved(self, post):
        return self.saved_posts.filter(save_post.c.post_id == post.id).count() > 0

    def join(self, community):
        if not self.is_member(community):
            self.followed_community.append(community)
            if not community.com_members or community.com_members < 0:
                community.com_members = 0
            community.com_members += 1
            return self

    def leave(self, community):
        if self.is_member(community):
            self.followed_community.remove(community)
            if not community.com_members or community.com_members < 0:
                community.com_members = 0
            community.com_members -= 1
            return self

    def is_member(self, community):
        return self.followed_community.filter(members.c.community_id == community.id).count() > 0

    def like(self, post):
        if not self.is_liked(post):
            if post.likes == None:
                post.likes = 0  
            else: 
                post.likes = int(post.likes)
            post.likes += 1
            self.liked.append(post)
            post.stats = post.rating()
            return self
        if self.is_liked(post):
            post.likes = int(post.likes)
            post.likes -= 1
            self.liked.remove(post)
            post.stats = post.rating()
            return self

    def is_liked(self, post):
        return self.liked.filter(like.c.post_id == post.id).count() > 0

    def dislike(self, post):
        if not self.is_disliked(post):
            if post.dislikes == None:
                post.dislikes = 0  
            else: 
                post.dislikes = int(post.dislikes)
            post.dislikes += 1
            self.disliked.append(post)
            post.stats = post.rating()
            return self
        if self.is_disliked(post):
            post.dislikes = int(post.dislikes)
            post.dislikes -= 1
            self.disliked.remove(post)
            post.stats = post.rating()
            return self

    def is_disliked(self, post):
        return self.disliked.filter(dislike.c.post_id == post.id).count() > 0

    def followed_posts(self):
        followed = Post.query.join(followers, (followers.c.followed_id == Post.creator_id)).filter(followers.c.follower_id == self.id)
        own = Post.query.filter_by(creator_id=self.id)
        return followed.union(own).order_by(Post.created_on.desc())

    def karma(self):
        self.points = 0
        if self.points is None:
            self.points = 0
        posts = self.posts
        for post in posts:
            point = post.rating()
            self.points += point
        db.session.commit()
        return int(self.points)

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        return self.generate_slug()

    def generate_slug(self):
        if self.name:
            self.slug = slugify(self.name)

    def __repr__(self):
        return '<User ID: {}, Name: {}>'.format(self.id, self.name)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(500))

    # === Functions === #

    def __repr__(self):
        return '<Role ID: {}, Name: {}>'.format(self.id, self.name)


class Rank(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(500))

    # === Functions === #

    def __repr__(self):
        return '<Rank ID: {}, Name: {}>'.format(self.id, self.name)


class Comment(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    creator_id = db.Column(db.Integer())
    created_on = db.Column(db.DateTime(), default=datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f%Z"))
    comment = db.Column(db.String(500))
    likes = db.Column(db.Integer())
    dislikes = db.Column(db.Integer())


class Report(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    creator_id = db.Column(db.Integer())
    created_on = db.Column(db.DateTime(), default=datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f%Z"))
    title = db.Column(db.String(100))
    content = db.Column(db.String(1000))
    rType = db.Column(db.String(100))


class MyAnonymousUser(AnonymousUserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), default="anonymous")

    # === Functions === #

    def follow(self, user):
        return False

    def unfollow(self, user):
        return False

    def is_following(self, users):
        return False

    def followers_list(self):
        return False

    def join(self, community):
        return False

    def leave(self, community):
        return False

    def is_member(self, community):
        return False

    def is_post_saved(self, post):
        return False

    def like(self, post):
        return False

    def is_liked(self, post):
        return False

    def dislike(self, post):
        return False

    def is_disliked(self, post):
        return False

    def followed_posts(self):
        return False

    def __repr__(self):
        return '<User id: {}, name {}>'.format(self.id, self.name)
