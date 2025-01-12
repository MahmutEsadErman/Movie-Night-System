import time

from PySide6.QtCore import QThread, Signal


class UpdateData(QThread):
    data_updated = Signal(int)
    film_load = Signal(object)
    film_update = Signal(object)
    info_dialog = Signal(str)
    exit_room = Signal()

    def __init__(self, main, db_connection, kullanici_id, event_id):
        super().__init__()
        self.main = main
        self.db_connection = db_connection
        self.kullanici_id = kullanici_id
        self.event_id = event_id

    def run(self):
        print("Update data thread started!")
        loaded_films = set()  # Initialize as an empty set
        loaded_film_oys = {}

        while True:
            try:
                cursor = self.db_connection.cursor()

                if self.main.stackedWidget.currentWidget() == self.main.mainmenu:
                    loaded_films.clear()
                    query = """
                        SELECT e_idnum
                        FROM davetliler
                        WHERE k_idnum = %s;
                    """
                    cursor.execute(query, (self.kullanici_id,))
                    results = cursor.fetchall()

                    if results:
                        # Emit True and the list of event IDs if found
                        for row in results:
                            print(f"Found event IDs: {row[0]}")
                            self.data_updated.emit(row[0])

                elif self.main.stackedWidget.currentWidget() == self.main.roomPage:
                    check_query = """
                    SELECT 1
                    FROM katilimci
                    WHERE e_idnum = %s AND k_idnum = %s;
                    """
                    cursor.execute(check_query, (self.event_id, self.kullanici_id))
                    result = cursor.fetchone()
                    if not result:
                        self.exit_room.emit()
                        self.info_dialog.emit("Oda sahibi çıktığı için oda kapatıldı!")
                        continue

                    select_query = """
                    SELECT f.f_id, f.f_adi, f.f_resim, f.fragman_url, ef.oylar
                    FROM e_film_liste ef, filmler f
                    WHERE ef.e_idf = %s and ef.f_idf = f.f_id;
                    """
                    cursor.execute(select_query, (self.event_id,))
                    films = cursor.fetchall()

                    # List to hold films with updated `oy` values
                    new_films = []
                    updated_films = []

                    for film in films:
                        film_id = film[0]  # Film ID
                        oy_value = film[-1]  # Oy value

                        # Check if the film is new or its oy value has changed
                        if film_id not in loaded_films:
                            loaded_films.add(film_id)  # Add the film ID to the set
                            loaded_film_oys[film_id] = oy_value
                            new_films.append(film)  # Add the film to updated list

                        elif loaded_film_oys[film_id] != oy_value:
                            loaded_film_oys[film_id] = oy_value  # Update the oy value
                            updated_films.append((film_id, oy_value))

                    if updated_films:
                        self.film_update.emit(updated_films)

                    # Emit all updated films in a single emit
                    if new_films:
                        self.film_load.emit(new_films)

                self.db_connection.commit()
            except Exception as e:
                print(f"Error updating user data: {e}")
            finally:
                cursor.close()

            QThread.sleep(1)
