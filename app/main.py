from app import app, db
from auth.auth import auth
from profiles.profile import profiles
from communities.community import community
from leaderboards.leaderboard import leaderboard
from posts.post import posts
from chats.chat import chats
import view

# ===== Blueprints ===== #

app.register_blueprint(auth)
app.register_blueprint(profiles, url_prefix='/profile')
app.register_blueprint(community, url_prefix='/community')
app.register_blueprint(leaderboard, url_prefix='/leaderboard')
app.register_blueprint(posts, url_prefix='/posts')
app.register_blueprint(chats, url_prefix='/chat')

# ===== Run ===== #

if __name__ == '__main__':
    app.run()