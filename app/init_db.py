from app import models
from app.database import utworz_tabele


def main():
    utworz_tabele()
    print("Tabele bazy danych zostaly utworzone.")


if __name__ == "__main__":
    main()
