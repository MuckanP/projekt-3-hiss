import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ElevatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Elevator Simulation")
        self.geometry("400x800")

        self.floors = [-2, -1] + list(range(1, 11))
        
        self.buttons = {}
        self.indicators = {}
        self.create_ui()

    def create_ui(self):
        frame = ctk.CTkFrame(self)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        for floor in reversed(self.floors): 
            row = ctk.CTkFrame(frame) 
            row.pack(fill="x", pady=2)
            
            
            btn = ctk.CTkButton(row, text=f"Floor {floor}") #knapp
            btn.pack(side="left", padx=5)

            
            indicator = ctk.CTkLabel(row, text="   ", width=40) #indikator
            indicator.pack(side="right", padx=5)

            self.buttons[floor] = btn
            self.indicators[floor] = indicator

if __name__ == "__main__":
    app = ElevatorApp()
    app.mainloop()


