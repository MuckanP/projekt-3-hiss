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
        self.floor_positions = {}
        
        self.gui()
        self.elevator_box()

    def gui(self):
        frame = ctk.CTkFrame(self)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        for i, floor in reversed(self.floors): 
            row = ctk.CTkFrame(frame) 
            row.pack(fill="x", pady=2)
            
            btn = ctk.CTkButton(row, text=f"Floor {floor}") #knapp
            btn.pack(side="left", padx=5)
            
            indicator = ctk.CTkLabel(row, text="   ", width=40) #indikator
            indicator.pack(side="right", padx=5)

            self.buttons[floor] = btn
            self.indicators[floor] = indicator
            
            self.floor_positions[floor] = i 
            
    def elevator_box(self):
        self.canvas = ctk.CTkCanvas(self, width= 60, height= 550, bg= "black", highlightthickness=0)
        self.canvas.place(x= 230, y= 25) # canvas för animation
        
        self.box = self.canvas.create_rectangle(10,10,50,40, fill= "green")
        self.current_y = 10
        
    def update_indicator(self, current_floor):
        for floor, label in self.indicators.items():
            if floor == current_floor: 
                label.configure(text= "#", fg_color= "green")
            else: label.configure(text="", fg_color= "transparent")
    
    def animate(self, floor):
        target_index = self.floor_positions[floor]
        target_y = 10 + target_index * 40
        #detta konverterar index till pixlar/position
        self.animate_step(target_y)
        
    def animate_step(self, target_y):
        if abs (self.current_y - target_y) < 2:
            return
        
        direction = 1 if target_y > self.current_y else -1
        self.current_y += direction * 2
        
        self.canvas.move(self.box, 0, direction * 2)
        self.after(10, lambda: self.animate_step(target_y))
        
        

if __name__ == "__main__":
    app = ElevatorApp()
    app.mainloop()


