import time

from PySide6.QtCore import QThread, Signal


class UpdateData(QThread):
    data_updated = Signal(int)
    film_load = Signal(object)

    def __init__(self, main, db_connection, kullanici_id, event_id):
        super().__init__()
        self.main = main
        self.db_connection = db_connection
        self.kullanici_id = kullanici_id
        self.event_id = event_id
    def run(self):
        print("Update data thread started!")
        loaded_films= set()
        while True:
            try:
                cursor = self.db_connection.cursor()

                if self.main.stackedWidget.currentWidget() == self.main.mainmenu:
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
            
                    
                if self.main.stackedWidget.currentWidget() == self.main.roomPage:
                    select_query = """
                    SELECT f.f_id, f.f_adi, f.f_resim, f.fragman_url, ef.oylar
                    FROM e_film_liste ef, filmler f
                    WHERE ef.e_idf = %s and ef.f_idf = f.f_id;
                    """
                    cursor.execute(select_query, (self.event_id,))
                    films = cursor.fetchall()

                    new_film_ids = {film[0] for film in films}
                    new_ids_to_add = new_film_ids - loaded_films
                    loaded_films.update(new_ids_to_add)

                    new_films = [film  for film in films if film[0] in new_ids_to_add]

                    if new_films:  
                        self.film_load.emit(new_films)

                self.db_connection.commit()
            except Exception as e:
                print(f"Error updating user data: {e}")
            finally:
                cursor.close()

            QThread.sleep(1)
