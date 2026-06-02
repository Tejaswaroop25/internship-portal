import os
import sys
from flask import Flask, render_template
from flask_login import LoginManager
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from backend.models import db
from backend.models.user import User
from backend.models.internship import Internship
from backend.models.application import Application
from backend.config import Config

def create_app():
    app = Flask(
        __name__, 
        template_folder=os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'frontend', 'templates'),
        static_folder=os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'frontend', 'static')
    )
    app.config.from_object(Config)


    db_dir = os.path.dirname(app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', ''))

    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    from backend.routes.auth import auth_bp
    from backend.routes.internships import internships_bp
    from backend.routes.applications import applications_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(internships_bp)
    app.register_blueprint(applications_bp)

    @app.context_processor
    def inject_helpers():
        return dict(
            str=str,
            len=len,
            isinstance=isinstance,
        )

    with app.app_context():
        db.create_all()
        seed_data()

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('base.html', error_code=404, error_message="The page you are looking for does not exist."), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('base.html', error_code=500, error_message="An internal server error occurred."), 500

    return app

def seed_data():
    if User.query.first() is not None:
        return

    print("Seeding initial mock data...")


    admin = User(username="admin", email="admin@portal.com", role="admin")
    admin.set_password("admin123")
    db.session.add(admin)
    techcorp = User(
        username="techcorp", 
        email="jobs@techcorp.com", 
        role="company",
        company_name="TechCorp Inc.",
        company_website="https://techcorp.example.com",
        bio="Leading global provider of cloud, AI, and enterprise software solutions."
    )
    techcorp.set_password("company123")
    db.session.add(techcorp)

    designlab = User(
        username="designlab", 
        email="careers@designlab.co", 
        role="company",
        company_name="DesignLab Studio",
        company_website="https://designlab.example.com",
        bio="A boutique digital agency specializing in premium branding, UX design, and visual styling."
    )
    designlab.set_password("company123")
    db.session.add(designlab)

    john = User(
        username="john_doe",
        email="john@student.edu",
        role="student",
        skills="Python, Flask, SQLite, HTML, CSS",
        experience="Built a personal portfolio site. Contributed to open-source Python CLI tools.",
        resume_link="https://drive.google.com/example-resume-john",
        bio="Aspiring full-stack engineer and backend Python developer. Eager to learn modern web frameworks."
    )
    john.set_password("student123")
    db.session.add(john)

    alice = User(
        username="alice_smith",
        email="alice@student.edu",
        role="student",
        skills="Figma, UI/UX, CSS, JavaScript, React",
        experience="Designed wireframes and interactive prototypes for 3 mobile app hackathons.",
        resume_link="https://behance.net/example-portfolio-alice",
        bio="Creative UI/UX designer and frontend enthusiast. Loves clean typography and seamless micro-animations."
    )
    alice.set_password("student123")
    db.session.add(alice)

    db.session.commit()

    backend_intern = Internship(
        title="Backend Developer Intern",
        description="Join our engineering team to construct robust REST APIs and database connectors. You will work with Flask, SQLite, and cloud deployments.",
        requirements="Python, Flask, SQLite, Git",
        location="Remote",
        stipend="$1,500/month",
        duration="3 Months",
        company_id=techcorp.id
    )
    db.session.add(backend_intern)

    frontend_intern = Internship(
        title="Frontend & UI Design Intern",
        description="Help us design and craft pixel-perfect, responsive web interfaces. You will translate wireframes into interactive, responsive frontend builds.",
        requirements="HTML, CSS, JavaScript, React, Figma",
        location="San Francisco, CA (Hybrid)",
        stipend="$2,000/month",
        duration="6 Months",
        company_id=designlab.id
    )
    db.session.add(frontend_intern)

    python_intern = Internship(
        title="Python Software Intern",
        description="Work closely with data analysts to construct web crawlers, write automation scripts, and build backend prototypes with Python.",
        requirements="Python, Git, SQL",
        location="Remote",
        stipend="$1,200/month",
        duration="3 Months",
        company_id=techcorp.id
    )
    db.session.add(python_intern)

    db.session.commit()
    print("Mock data seeded successfully!")

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
