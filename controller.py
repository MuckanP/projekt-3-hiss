import time
import threading

from elevatorgui import ElevatorApp


class ElevatorController:

    def __init__(self, app):

        self.app = app

        self.requests = set()

        self.direction = "up"

        self.running = False

        self.bind_buttons()
    
    def update_debug_terminal(self, target=None):

        queue = sorted(list(self.requests))
        debug_text = (
            f"Current Floor : {self.app.current_floor}\n"
            f"Direction     : {self.direction}\n"
            f"Current Target: {target}\n"
            f"Queue         : {queue}\n"
            f"Queue Length  : {len(queue)}\n"
            )

        self.app.update_debug(debug_text)

    def bind_buttons(self):

        # Outside buttons
        for floor, button in self.app.buttons.items():

            button.configure(
                command=lambda f=floor: self.add_request(f)
            )

        # Inside buttons
        for floor, button in self.app.internal_buttons.items():

            button.configure(
                command=lambda f=floor: self.add_request(f)
            )

    def add_request(self, floor):

        print(f"Request added: {floor}")

        self.requests.add(floor)

    def start(self):

        self.running = True

        threading.Thread(
            target=self.run,
            daemon=True
        ).start()

    def run(self):

        while self.running:

            if not self.requests:
                time.sleep(0.2)
                continue

            next_floor = self.get_next_floor_scan()

            if next_floor is None:
                continue

            self.move_to_floor(next_floor)

    def get_next_floor_scan(self):
        
        current = self.app.current_floor

        higher = sorted(
            [f for f in self.requests if f > current]
        )

        lower = sorted(
            [f for f in self.requests if f < current],
            reverse=True
        )

        if self.direction == "up":

            if higher:
                return higher[0]

            self.direction = "down"

            if lower:
                return lower[0]

        else:

            if lower:
                return lower[0]

            self.direction = "up"

            if higher:
                return higher[0]

        return None

    def move_to_floor(self, target):

        while self.app.current_floor != target:
            
            next_floor = self.get_next_step(target)
            print(f"Moving from {self.app.current_floor} -> {next_floor}")
            self.app.animate_to_floor(next_floor)

            time.sleep(1) #tid mellan våningar

            self.app.current_floor = next_floor
            print("Current floor:", self.app.current_floor)
            self.app.update_indicator(self.app.current_floor)

        self.stop_at_floor()

    def stop_at_floor(self):

        floor = self.app.current_floor

        print(f"Stopping at floor {floor}")

        self.requests.discard(floor)

        time.sleep(2)
    
    def get_next_step(self, target):

        if target > self.app.current_floor:

            if self.app.current_floor == -1:
               return 1

            return self.app.current_floor + 1

        else:
            if self.app.current_floor == 1:
                return -1

            return self.app.current_floor - 1


if __name__ == "__main__":

    app = ElevatorApp()

    controller = ElevatorController(app)

    controller.start()

    app.mainloop()