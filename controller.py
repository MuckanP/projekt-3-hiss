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
    
    def run(self):
        while self.running:
            target = self.get_next_call()
            
            if target is None:
                time.sleep(1)
                continue
            
            if target > self.app.current_floor:
                self.move_up(target)
            else:
                self.move_down(target)
    
    def get_next_call(self):
        all_calls = list(self.up_calls | self.down_calls | self.internal_calls)
        return all_calls[0] if all_calls else None
    
    def move_up(self, target):
        while self.app.current_floor < target:
            time.sleep(1)
            
        #hoppa över våning 0, då entre är våning 1
        if self.app.current_floor == -1:
            self.app.current_floor = 1
        else:
            self.app.current_floor += 1
        
        self.app.update_indicator()
        
        if self.check_stop(): # detta är försök på AND logic,
            self.stop_at_floor() # vet ej om det funkar
            return
    
    def move_down(self, target):
        while self.app.current_floor > target:
            time.sleep(1)
            
        #hoppa över våning 0, då entre är våning 1
        if self.app.current_floor == 1:
            self.app.current_floor = -1
        else:
            self.app.current_floor -= 1
        
        self.app.update_indicator()
        
        if self.check_stop(): # detta är försök på AND logic,
            self.stop_at_floor() # vet ej om det funkar
            return
    
    def check_stop(self):
        floor = self.app.current_floor
        return (
            floor in self.up_calls 
            or floor in self.down_calls 
            or floor in self.internal_calls
        )
    
    def stop_at_floor(self):
        floor = self.app.current_floor
        print(f"Stopping at floor {floor}") #temporärt medan gui knappt funkaj
        
        # ta bort alla anrop för den aktuella våningen
        self.up_calls.discard(floor)
        self.down_calls.discard(floor)
        self.internal_calls.discard(floor)
        
        time.sleep(1)
    
    def btn_bind(self):
        for floor, button in app.buttons.items():
            button.configure(command=lambda f = floor: controller.add_call(f))
        
        
        
if __name__ == "__main__":
    app = ElevatorApp()
    controller = ElevatorController(app)
    
    controller.start()
    app.mainloop()