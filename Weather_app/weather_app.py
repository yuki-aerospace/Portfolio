import tkinter as tk
from PIL import ImageTk, Image
import get_weather
import requests
from io import BytesIO

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.city = "Geneseo"
        self.weather, self.temp, self.humidity, self.icon = get_weather.get_weather(self.city) # call from a module

        self.master.geometry("450x450")
        self.master.title("Weather App")
        self.create_widgets()
    
    #! make show_error method 
    
    #! This doen't work
    # This function Clears label
    def clear_label(self):
        self.location_label = tk.Label(self, text="City:"  , font= ('Helvetica', 20), padx=10, pady=20)
        self.weather_label = tk.Label(self, text="Weather:" , font= ('Helvetica', 20), padx=10, pady=20)
        self.temp_label = tk.Label(self, text="Temprature:" + "  " + "°C", font= ('Helvetica', 20), padx=10, pady=20)
        self.humidity_label = tk.Label(self, text="Humidity:" + "  " + "%", font= ('Helvetica', 20), padx=10, pady=20)
        
    # This function gets value from entry
    def lookup(self):
        self.city = self.entry.get()
        self.weather, self.temp, self.humidity, self.icon = get_weather.get_weather(self.city)
        self.clear_label()
        self.create_widgets()
        self.entry.delete(0,tk.END)
        
    def create_widgets(self):
        color = "#FFFFFF"
        
        # Define labels
        self.location_label = tk.Label(self, text="City:" + "  " + self.city, font= ('Helvetica', 20), padx=10, pady=20, background=color)
        self.weather_label = tk.Label(self, text="Weather:" + "  " + self.weather, font= ('Helvetica', 20), padx=10, pady=20, background=color)
        self.temp_label = tk.Label(self, text="Temprature:" + "  " + str(self.temp)+  "  " + "°C", font= ('Helvetica', 20), padx=10, pady=20, background=color)
        self.humidity_label = tk.Label(self, text="Humidity:" + "  " + str(self.humidity)+  "  " + "%", font= ('Helvetica', 20), padx=10, pady=20, background=color)
        self.enter_label = tk.Label(self, text="ex) Los Angeles", font= ('Helvetica', 15), padx=10, fg="#3A3B3C", bg=color)
        
        # Place lables 
        self.location_label.grid(row=0,column=0, sticky=tk.W)
        self.weather_label.grid(row=2,column=0, sticky=tk.W)
        self.temp_label.grid(row=3,column=0, sticky=tk.W)
        self.humidity_label.grid(row=4,column=0, sticky=tk.W)
        self.enter_label.grid(row=6, column=0, sticky=tk.W+tk.N, columnspan=2)
        
        # Place weather icon image
        im = Image.open((BytesIO(requests.get('http://openweathermap.org/img/wn/'+str(self.icon)+'@2x.png').content))) # get icon from web API
        self.img = ImageTk.PhotoImage(im) 
        size = im.size
        self.frame = tk.Canvas(self, width=size[0], height=size[1])
        self.frame.create_image(0,0,anchor='nw',image=self.img)
        
        self.frame.grid(row=1, column=0)
        
        # Difine buttons
        button_exit = tk.Button(self,text="Exit",command=self.quit)
        self.enter_btn = tk.Button(self, text="Look Up City", command=self.lookup) 
        
        # Place buttons
        button_exit.grid(row=5, column=2,padx=(30,1), sticky=tk.W+tk.E+tk.S+tk.N, columnspan=2)
        self.enter_btn.grid(row=5, column=1, sticky=tk.W+tk.E+tk.S+tk.N)
        
        # Place serach box
        self.entry = tk.Entry(self, font=('Helvetica', 15))
        self.entry.insert(tk.END, u'New York')
        self.entry.grid(row=5, column=0, sticky=tk.W+tk.E+tk.S+tk.N, padx=(10,0))
        
        self.grid()
    
        

def main():
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()

if __name__ == "__main__":
    main()  
    
