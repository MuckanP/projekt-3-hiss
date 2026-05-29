from turtle import distance

import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class ElevatorApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("SCAN Elevator Simulation")
        self.geometry("900x700")

        self.floors = [-2, -1] + list(range(1, 11))

        self.current_floor = 1

        self.buttons = {}
        self.internal_buttons = {}
        self.indicators = {}
        self.floor_positions = {}

        self.create_layout()

        self.update_indicator(self.current_floor)
        
        self.animation_job = None
        self.target_y = None

    def create_layout(self):

        outside_frame = ctk.CTkFrame(self)
        outside_frame.pack(side="left", padx=20, pady=20)

        title = ctk.CTkLabel(
            outside_frame,
            text="Hall Calls",
            font=("Arial", 20)
        )
        title.pack(pady=10)

        for i, floor in enumerate(reversed(self.floors)):

            row = ctk.CTkFrame(outside_frame)
            row.pack(fill="x", pady=3)

            btn = ctk.CTkButton(
                row,
                text=f"Floor {floor}",
                width=100
            )

            btn.pack(side="left", padx=5)

            indicator = ctk.CTkLabel(
                row,
                text="",
                width=40
            )

            indicator.pack(side="right")

            self.buttons[floor] = btn
            self.indicators[floor] = indicator

            self.floor_positions[floor] = i

        shaft_frame = ctk.CTkFrame(self)
        shaft_frame.pack(side="left", padx=40)

        shaft_label = ctk.CTkLabel(
            shaft_frame,
            text="Elevator Shaft",
            font=("Arial", 20)
        )

        shaft_label.pack(pady=10)

        self.canvas = ctk.CTkCanvas(
            shaft_frame,
            width=120,
            height=600,
            bg="black",
            highlightthickness=0
        )

        self.canvas.pack()

        self.box = self.canvas.create_rectangle(
            20,
            10,
            100,
            60,
            fill="green"
        )

        self.current_y = 10

        inside_frame = ctk.CTkFrame(self)
        inside_frame.pack(side="right", padx=20, pady=20)

        inside_title = ctk.CTkLabel(
            inside_frame,
            text="Inside Elevator",
            font=("Arial", 20)
        )

        inside_title.pack(pady=10)

        for floor in reversed(self.floors):

            btn = ctk.CTkButton(
                inside_frame,
                text=f"{floor}",
                width=80
            )

            btn.pack(pady=3)

            self.internal_buttons[floor] = btn
            
        debug_frame = ctk.CTkFrame(self)
        debug_frame.pack(side="bottom", pady=20)

        debug_title = ctk.CTkLabel(debug_frame, text="Controller Debug", font=("Consolas", 18))

        debug_title.pack(pady=5)

        self.debug_box = ctk.CTkTextbox(debug_frame, width=500, height=180, font=("Consolas", 14))

        self.debug_box.pack(padx=10, pady=10)
    
    def update_debug(self, text):

        self.debug_box.delete("0.0", "end")
        self.debug_box.insert("0.0", text)

    def update_indicator(self, current_floor):

        for floor, label in self.indicators.items():

            if floor == current_floor:
                label.configure(
                    text="⬅",
                    fg_color="green"
                )

            else:
                label.configure(
                    text="",
                    fg_color="transparent"
                )

    def animate_to_floor(self, floor):

        target_index = self.floor_positions[floor]

        self.target_y = 10 + target_index * 42

        if self.animation_job is None: # detta fixar att animationen hakar4
            self.animate_step()

    def animate_step(self):

        if self.target_y is None:
            self.animation_job = None
            return

        distance = self.target_y - self.current_y

        if abs(distance) < 0.5:

            move_amount = self.target_y - self.current_y

            self.canvas.move(self.box, 0, move_amount)

            self.current_y = self.target_y

            self.animation_job = None
            return

        movement = distance * 0.05 #mjukare animation

        if abs(movement) < 0.2: #minimal hastighet
            movement = 0.2 if movement > 0 else -0.2

        self.current_y += movement

        self.canvas.move(self.box, 0, movement)

        self.animation_job = self.after(16, self.animate_step)


if __name__ == "__main__":

    app = ElevatorApp()
    app.mainloop()