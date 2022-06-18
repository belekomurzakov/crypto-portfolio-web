from flask import Flask
from views import home, prices, wallet, history
from database import database

# from views.auth import login_manager

app = Flask(__name__)

# config
app.config.from_object('config')
database.init_app(app)
# login_manager.init_app(app)

# views
app.register_blueprint(home.bp)
app.register_blueprint(prices.bp)
app.register_blueprint(wallet.bp)
app.register_blueprint(history.bp)

if __name__ == '__main__':
    app.run()

# matplotlib
