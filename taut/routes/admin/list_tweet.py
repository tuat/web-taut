from flask import Blueprint
from flask import render_template, request
from ...models import ListTweet
from ...helpers.account import require_admin
from ...helpers.value import force_integer, fill_with_users

blueprint = Blueprint('admin_list_tweet', __name__)

@blueprint.route('/index')
@require_admin
def index():
    page        = force_integer(request.args.get('page', 1), 0)
    list_tweets = ListTweet.query.order_by(ListTweet.create_at.desc()).paginate(page)

    list_tweets.items = fill_with_users(list_tweets.items)

    return render_template('admin/list_tweet/index.html', list_tweets=list_tweets)
