from ui.app import App
from auth.login import Login_System

if __name__ == "__main__":
    app = App()
    app.show_page(Login_System)
    app.mainloop()
