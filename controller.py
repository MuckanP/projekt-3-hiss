import time
import threading
from elevatorgui import ElevatorApp

class ElevatorController:
    def __init__ (self, app):
        self.app = app
        self.up_calls = set()
        self.down_calls = set()
        self.internal_calls = set()
        self.running = False
    
    def add_call(self, floor):
        if floor > self.app.current_floor:
            self.up_calls.add(floor)
        elif floor < self.app.current_floor:
            self.down_calls.add(floor)
        else:
            self.internal_calls.add(floor)
    
    def start(self):
        self.running = True
        threading.Thread(target=self.run).start()
    
    
        
        
        
if __name__ == "__main__":
    app = ElevatorApp()
    controller = ElevatorController(app)
    controller.start()
    app.mainloop()