from taipy.gui import Gui
from frontend.pages.home import home_page
from frontend.pages.dashboard import dashboard_page
from frontend.pages.data import data_page

pages = {
    "home": home_page,
    "dashboard": dashboard_page,
    "data": data_page
}

if __name__ == "__main__":
    Gui(pages=pages, css_file="assets/style.css").run(
        use_navigation=True,
        use_reloader=True,
        port=5050
    )


