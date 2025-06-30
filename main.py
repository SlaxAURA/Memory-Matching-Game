import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw
import random

CARD_NAMES = ["apple", "banana", "burger", "cake", "donut", "fries", "pizza", "sushi"]
CARD_PATH = "images/"
CARD_SIZE = (100, 100)
GRID_SIZE = 4

class MemoryGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🍎 MEMORY MATCH GAME")
        self.root.geometry("620x720")
        self.root.configure(bg="#e0f7fa")

        self.first_card = None
        self.second_card = None
        self.lock = False
        self.score = 0
        self.matched = 0
        self.timer = 0
        self.running = False

        self.load_images()
        self.create_ui()
        self.reset_game()

    def create_rounded_back(self):
        """Create a rounded pastel blue card back image"""
        img = Image.new("RGBA", CARD_SIZE, (179, 229, 252, 255))
        mask = Image.new("L", CARD_SIZE, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle((0, 0) + CARD_SIZE, radius=20, fill=255)
        img.putalpha(mask)
        return ImageTk.PhotoImage(img)

    def load_images(self):
        self.card_images = {}
        for name in CARD_NAMES:
            img = Image.open(CARD_PATH + name + ".png").resize(CARD_SIZE)
            self.card_images[name] = ImageTk.PhotoImage(img)
        self.back_image = self.create_rounded_back()

    def create_ui(self):
        tk.Label(self.root, text="👑 MEMORY GAME", font=("Comic Sans MS", 24, "bold"),
                 bg="#e0f7fa", fg="#004d40").pack(pady=20)

        self.stats = tk.Label(self.root, text="Time: 0s | Score: 0", font=("Arial", 14),
                              bg="#e0f7fa", fg="#006064")
        self.stats.pack(pady=10)

        self.grid_frame = tk.Frame(self.root, bg="#e0f7fa")
        self.grid_frame.pack()

        self.buttons = []
        for i in range(GRID_SIZE * GRID_SIZE):
            btn = tk.Button(self.grid_frame, image=self.back_image,
                            command=lambda i=i: self.flip_card(i),
                            bd=0, bg="#e0f7fa", activebackground="#e0f7fa",
                            relief="flat", highlightthickness=0)
            btn.grid(row=i//GRID_SIZE, column=i%GRID_SIZE, padx=8, pady=8)
            self.buttons.append(btn)

        # ✅ Flutter-style Gradient Restart Button
        self.restart_canvas = tk.Canvas(self.root, width=200, height=50,
                                        bd=0, highlightthickness=0, bg="#e0f7fa")
        self.restart_canvas.pack(pady=20)

        # Create gradient
        gradient = tk.PhotoImage(width=200, height=50)
        r1, g1, b1 = (0, 242, 255)
        r2, g2, b2 = (79, 172, 254)
        for y in range(50):
            r = int(r1 + (r2 - r1) * y / 50)
            g = int(g1 + (g2 - g1) * y / 50)
            b = int(b1 + (b2 - b1) * y / 50)
            gradient.put(f"#{r:02x}{g:02x}{b:02x}", to=(0, y, 200, y+1))
        self.restart_canvas.create_image(0, 0, anchor="nw", image=gradient)
        self.restart_canvas.image = gradient

        rect = self.restart_canvas.create_oval(10, 5, 190, 45, fill="", outline="")
        text = self.restart_canvas.create_text(100, 25, text="🔁 Restart", font=("Segoe UI", 14, "bold"), fill="white")

        self.restart_canvas.tag_bind(rect, "<Button-1>", lambda e: self.reset_game())
        self.restart_canvas.tag_bind(text, "<Button-1>", lambda e: self.reset_game())

    def reset_game(self):
        self.card_values = CARD_NAMES * 2
        random.shuffle(self.card_values)
        self.card_states = [False] * len(self.card_values)
        for btn in self.buttons:
            btn.config(image=self.back_image)
        self.first_card = None
        self.second_card = None
        self.lock = False
        self.score = 0
        self.matched = 0
        self.timer = 0
        self.stats.config(text="Time: 0s | Score: 0")
        self.running = True
        self.update_timer()

    def update_timer(self):
        if self.running:
            self.timer += 1
            self.stats.config(text=f"Time: {self.timer}s | Score: {self.score}")
            self.root.after(1000, self.update_timer)

    def flip_card(self, index):
        if self.lock or self.card_states[index]:
            return
        self.buttons[index].config(image=self.card_images[self.card_values[index]])
        if self.first_card is None:
            self.first_card = index
            return
        self.second_card = index
        self.lock = True
        self.root.after(600, self.check_match)

    def check_match(self):
        if self.card_values[self.first_card] == self.card_values[self.second_card]:
            self.card_states[self.first_card] = True
            self.card_states[self.second_card] = True
            self.matched += 1
            self.score += 10
        else:
            self.buttons[self.first_card].config(image=self.back_image)
            self.buttons[self.second_card].config(image=self.back_image)
        self.first_card = None
        self.second_card = None
        self.lock = False
        self.stats.config(text=f"Time: {self.timer}s | Score: {self.score}")
        if self.matched == len(CARD_NAMES):
            self.running = False
            messagebox.showinfo("🎉 You Won!", f"Time: {self.timer}s\nScore: {self.score}")

if __name__ == "__main__":
    root = tk.Tk()
    MemoryGame(root)
    root.mainloop()
