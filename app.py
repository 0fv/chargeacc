from flask import Flask,request,render_template,url_for,redirect,flash,Blueprint
from werkzeug.utils import secure_filename
from config import DevConfig
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_uploads import UploadSet,configure_uploads
from wtforms import SelectMultipleField,SubmitField,SelectField
import misc
import os


app = Flask(__name__)
app.config.from_object(DevConfig)
db = SQLAlchemy(app)
ALLOWED_EXTENSIONS = set(['csv'])
doc = UploadSet(extensions=('xlsx','xls'))
configure_uploads(app, (doc,))

manage_blueprint=Blueprint(
    'manage',
    __name__,
    template_folder='templates/manage',
    url_prefix='/manage'
)
#flask-wtf
class Select2MultipleField(SelectMultipleField):

    def pre_validate(self, form):
        # Prevent "not a valid choice" error
        pass

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = ",".join(valuelist)
        else:
            self.data = ""

class ChoiceForm(FlaskForm):
    single_select = SelectField(u"选择对应关系", [],
        choices = misc.find_id(),
        description=u"选择",
        render_kw={})
    multi_select = Select2MultipleField(u"删除关系文件", [],
        choices= misc.find_id(),
        description=u"可多选",
        render_kw={"multiple": "multiple"})
    submit = SubmitField('删除')

class Relation(db.Model):
    a = db.Column(db.Integer(),primary_key=True)
    phone_num = db.Column(db.String(255))
    depart = db.Column(db.String(255))
    id = db.Column(db.String(255))

class Data(db.Model):
    a = db.Column(db.Integer(), primary_key=True)
    depart = db.Column(db.String(255))
    price = db.Column(db.Float())
    date = db.Column(db.String(255))
    relation = db.Column(db.String(255))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/manage')
def redirect_to_upload():
    return redirect(url_for('manage.upload_file'))

@manage_blueprint.route('/upload', methods=['GET', 'POST'])
def upload_file():
    form= ChoiceForm(request.form)
    if request.method == 'POST':
        doc.save(request.files['input-b2'])
        return redirect(request.url)
    else:
        pass
    return render_template(
        'upload.html',
        form = form
    )

@manage_blueprint.route('/relation', methods=['GET', 'POST'])
def relation_file():
    relations = Relation.query.all()
    form = ChoiceForm(request.form)
    if request.method == 'POST':
        if form.submit():
            dellist=form.data['multi_select']
            dellist1=dellist.split(',')
            for file in dellist1:
                delelements = Relation.query.filter_by(id = file).all()
                for delelement in delelements:
                    db.session.delete(delelement)
                db.session.commit()
        # check if the post request has the file part
        if 'input-b2' not in request.files:
            flash('No file part')
            return redirect(request.url)
        else:
            file = request.files['input-b2']
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            else:
                pass
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                misc.relation_to_database(filename)
                return redirect(request.url)
            else:
                pass
    return render_template(
        'relation.html',
        relations = relations,
        form = form
    )

app.register_blueprint(manage_blueprint)

if __name__ == '__main__':
    app.run(DEBUG = True)
