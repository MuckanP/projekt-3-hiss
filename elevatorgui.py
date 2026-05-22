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

    def create_layout(self):

        # =========================
        # OUTSIDE PANEL
        # =========================

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

        # =========================
        # ELEVATOR SHAFT
        # =========================

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

        # =========================
        # INSIDE ELEVATOR PANEL
        # =========================

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

        target_y = 10 + target_index * 42

        self.animate_step(target_y)

    def animate_step(self, target_y):

        if abs(self.current_y - target_y) < 1:
            return

        direction = 1 if target_y > self.current_y else -1

        self.current_y += direction * 1

        self.canvas.move(
            self.box,
            0,
            direction * 1
        )

        # MUCH slower animation
        self.after(
            25,
            lambda: self.animate_step(target_y)
        )


if __name__ == "__main__":

    app = ElevatorApp()
    app.mainloop()