import time

from PySide6.QtCore import QThread, Signal


class UpdateData(QThread):
    data_updated = Signal(int)

    def __init__(self, main, database, kullanici_id):
        super().__init__()
        self.main = main
        self.database = database
        self.kullanici_id = kullanici_id

    def run(self):
        print("Update data thread started!")
        while True:
            try:
                cursor = self.database.cursor()

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
                    pass

                cursor.execute(query, (self.kullanici_id,))
                self.database.commit()
            except Exception as e:
                print(f"Error updating user data: {e}")
            finally:
                cursor.close()

            QThread.sleep(1)
