from PySide6.QtCore import QThread, Signal


class CheckDavetliler(QThread):
    # Signal to send results back to the main UI (list of event IDs)
    result_signal = Signal(bool, list)

    def __init__(self, db_connection, kullanici_id):
        super().__init__()
        self.db_connection = db_connection
        self.kullanici_id = kullanici_id

    def run(self):
        try:
            cursor = self.db_connection.cursor()
            query = """
                SELECT e_idnum 
                FROM davetliler
                WHERE k_idnum = %s;
            """
            cursor.execute(query, (self.kullanici_id,))
            results = cursor.fetchall()

            if results:
                # Emit True and the list of event IDs if found
                event_ids = [row[0] for row in results]
                self.result_signal.emit(True, event_ids)
                print(f"Found event IDs: {event_ids}")
            else:
                # Emit False if no invitations found
                self.result_signal.emit(False, [])

        except Exception as e:
            print(f"Error checking davetliler table: {e}")
            self.result_signal.emit(False, [f"Error: {e}"])

        finally:
            cursor.close()