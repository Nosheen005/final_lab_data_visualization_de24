from taipy.gui import Gui
from frontend.pages.home import home_page
from frontend.pages.dashboard import dashboard_page
from frontend.pages.data import data_page
from frontend.pages.storytelling import storytelling_page


# Define the page routing dictionary
pages = {
    "/": home_page,
    "dashboard": dashboard_page,
    "data": data_page,
    "storytelling": storytelling_page
}

if __name__ == "__main__":
    Gui(pages=pages).run(
        use_navigation=True,
        use_reloader=True,
        port="auto"
    )



