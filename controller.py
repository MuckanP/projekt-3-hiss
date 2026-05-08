import time
import threading

from elevatorgui import ElevatorApp


class ElevatorController:

    def __init__(self, app):

        self.app = app

        self.up_calls = set()
        self.down_calls = set()
        self.internal_calls = set()

        self.running = False

        self.bind_buttons()

    def add_call(self, floor):

        print(f"Call added for floor {floor}")

        if floor > self.app.current_floor:
            self.up_calls.add(floor)

        elif floor < self.app.current_floor:
            self.down_calls.add(floor)

        else:
            self.internal_calls.add(floor)

    def bind_buttons(self):

        for floor, button in self.app.buttons.items():

            button.configure(
                command=lambda f=floor: self.add_call(f)
            )

    def start(self):

        self.running = True

        threading.Thread(
            target=self.run,
            daemon=True
        ).start()

    def run(self):

        while self.running:

            target = self.get_next_call()

            if target is None:
                time.sleep(0.2)
                continue

            if target > self.app.current_floor:
                self.move_up(target)

            elif target < self.app.current_floor:
                self.move_down(target)

            else:
                self.stop_at_floor()

    def get_next_call(self):

        all_calls = list(
            self.up_calls
            | self.down_calls
            | self.internal_calls
        )

        return all_calls[0] if all_calls else None

    def move_up(self, target):

        while self.app.current_floor < target:

            time.sleep(1)

            if self.app.current_floor == -1:
                self.app.current_floor = 1

            else:
                self.app.current_floor += 1

            print("Moving up:", self.app.current_floor)

            self.app.update_indicator(
                self.app.current_floor
            )

            self.app.animate_to_floor(
                self.app.current_floor
            )

        self.stop_at_floor()

    def move_down(self, target):

        while self.app.current_floor > target:

            time.sleep(1)

            if self.app.current_floor == 1:
                self.app.current_floor = -1

            else:
                self.app.current_floor -= 1

            print("Moving down:", self.app.current_floor)

            self.app.update_indicator(
                self.app.current_floor
            )

            self.app.animate_to_floor(
                self.app.current_floor
            )

        self.stop_at_floor()

    def stop_at_floor(self):

        floor = self.app.current_floor

        print(f"Stopping at floor {floor}")

        self.up_calls.discard(floor)
        self.down_calls.discard(floor)
        self.internal_calls.discard(floor)

        time.sleep(1)


if __name__ == "__main__":

    app = ElevatorApp()

    controller = ElevatorController(app)

    controller.start()

    app.mainloop()