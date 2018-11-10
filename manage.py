from flask_script import Manager,Server
from app import app,db,Relation,Data

manager = Manager(app)

manager.add_command('server',Server())
@manager.shell
def make_shell_context():
    return dict(app=app,db=db,Relation=Relation,Data=Data)

if __name__ == '__main__':
    manager.run()