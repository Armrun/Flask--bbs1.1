from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from routes import current_user

from models.topic import Topic


main = Blueprint('topic', __name__)


@main.route("/")
def index():
    ms = Topic.all()
    u = current_user()
    return render_template("topic/index.html", ms=ms, user=u)


@main.route('/<int:id>')
# /topic/1
# @main.route('/')
# /topic?id=1
# zhihu.com/question/1/answer/2/comment/3/xxx/y
def detail(id):
    m = Topic.get(id)
    u = current_user()
    return render_template("topic/detail.html", topic=m, user=u)


@main.route("/add", methods=["POST"])
def add():
    form = request.form.to_dict()
    u = current_user()
    m = Topic.add(form, user_id=u.id)
    return redirect(url_for('.detail', id=m.id))


@main.route("/new")
def new():
    u = current_user()
    return render_template("topic/new.html", user=u)

