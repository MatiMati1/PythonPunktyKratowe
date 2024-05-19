import tkinter as tk
from ctypes import windll


class Gui:
    def __init__(self):
        self.window = tk.Tk()

        self.width = self.window.winfo_screenwidth()
        self.height = self.window.winfo_screenheight()

        self.xAxisCenter = 0
        self.yAxisCenter = 0

        self.window.geometry("%dx%d+0+0" % (self.width, self.height))
        self.window.state('zoomed')
        self.window.title('Obliczanie punktów kratowych')

        self.canvas = tk.Canvas(self.window, background='white')
        self.canvas.pack(side=tk.LEFT, fill="both", expand=True)

        self.mainFrame = tk.Frame(self.window)
        self.mainFrame.pack(side=tk.RIGHT, fill="y")

        self.label1 = tk.Label(self.mainFrame, text='Podaj współrzędne środka koła', font=('Arial', 15))
        self.label1.pack(padx=15, pady=15)

        self.xInputFrame = tk.Frame(self.mainFrame)
        self.xInputFrame.pack(side=tk.TOP, pady=10)
        self.xInputLabel = tk.Label(self.xInputFrame, text="X=", font=('Arial', 13))
        self.xInputLabel.pack(side=tk.LEFT)
        self.xInputEntry = tk.Entry(self.xInputFrame)
        self.xInputEntry.pack(side=tk.LEFT)

        self.yInputFrame = tk.Frame(self.mainFrame)
        self.yInputFrame.pack(side=tk.TOP, pady=10)
        self.yInputLabel = tk.Label(self.yInputFrame, text="Y=", font=('Arial', 13))
        self.yInputLabel.pack(side=tk.LEFT)
        self.yInputEntry = tk.Entry(self.yInputFrame)
        self.yInputEntry.pack(side=tk.LEFT)

        self.label2 = tk.Label(self.mainFrame, text='Podaj promień koła', font=('Arial', 15))
        self.label2.pack(padx=15, pady=15)

        self.rInputFrame = tk.Frame(self.mainFrame)
        self.rInputFrame.pack(side=tk.TOP, pady=10)
        self.rInputLabel = tk.Label(self.rInputFrame, text="R=", font=('Arial', 13))
        self.rInputLabel.pack(side=tk.LEFT)
        self.rInputEntry = tk.Entry(self.rInputFrame)
        self.rInputEntry.pack(side=tk.LEFT)

        self.button = tk.Button(self.mainFrame, text="Oblicz", font=('Arial', 15), command=self.calculate)
        self.button.pack(pady=15)

        self.answersFrame = tk.Frame(self.mainFrame)
        self.answersFrame.pack(pady=20)

        self.errorLabel = tk.Label(self.answersFrame, font=('Arial', 15))
        self.answersLabel = tk.Label(self.answersFrame, font=('Arial', 15))

        self.drawGrid()

        self.window.mainloop()

    def drawGrid(self):
        self.canvas.delete("all")

        self.canvas.update()

        self.xAxisCenter = (int((self.canvas.winfo_width() / 20) / 2) + 2) * 20
        self.yAxisCenter = int((self.canvas.winfo_height() / 20) / 2) * 20

        for i in range(0, int(self.canvas.winfo_width() / 20) + 1):
            self.canvas.create_line(20 * i, 0, 20 * i, self.canvas.winfo_height(), fill='black', width=1)
        for i in range(0, int(self.canvas.winfo_height() / 20)):
            self.canvas.create_line(0, 20 * i, self.canvas.winfo_width(), 20 * i, fill='black', width=1)

        self.canvas.create_line(self.xAxisCenter, 0, self.xAxisCenter, self.canvas.winfo_height(), fill='black',
                                width=3)
        self.canvas.create_line(0, self.yAxisCenter, self.canvas.winfo_width(), self.yAxisCenter, fill='black', width=3)

    def calculate(self):
        x = int(self.xInputEntry.get())
        y = int(self.yInputEntry.get())
        r = int(self.rInputEntry.get())

        if r <= 0:
            if self.answersLabel.winfo_exists():
                self.answersLabel.pack_forget()
            self.drawGrid()
            self.errorLabel.config(text="Promień nie może być\n mniejszy lub równy 0")
            self.errorLabel.pack()
        else:
            if self.errorLabel.winfo_exists():
                self.errorLabel.pack_forget()
            self.drawGrid()
            self.canvas.create_oval(self.xAxisCenter + (20 * (x - r)), self.yAxisCenter - (20 * (y - r)), self.xAxisCenter + (20 * (x + r)), self.yAxisCenter - (20 * (y + r)), width=3)

            points = set()

            for i in range(y - r, y + r + 1):
                for j in range(x - r, x + r + 1):
                    if ((j - x) * (j - x)) + ((i - y) * (i - y)) <= (r * r):
                        points.add((j, i))
                        self.canvas.create_oval(self.xAxisCenter + (20 * (j - 0.15)), self.yAxisCenter - (20 * (i - 0.15)), self.xAxisCenter + (20 * (j + 0.15)), self.yAxisCenter - (20 * (i + 0.15)), width=1, fill="black")

            counter = 0
            formattedPoints = "Punkty Kratowe to:\n\n"

            for point in points:
                formattedPoints += f"{str(point[0])}, {str(point[1])} ; "

                counter += 1

                if counter == 5:
                    formattedPoints += "\n"
                    counter = 0

            formattedPoints = formattedPoints[:-2]

            self.answersLabel.config(text=formattedPoints)
            self.answersLabel.pack()


windll.shcore.SetProcessDpiAwareness(1)

gui = Gui()
