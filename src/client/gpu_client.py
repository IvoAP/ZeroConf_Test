import tkinter as tk
from tkinter import ttk

from zeroconf import ServiceBrowser, Zeroconf


class GPUClient(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GPU Monitor Client")
        self.geometry("400x300")
        self.services = {}
        self.zeroconf = Zeroconf()
        self.setup_gui()
        self.start_browser()

    def setup_gui(self):
        ttk.Label(self, text="Available GPUs", font=('Helvetica', 14)).pack(pady=10)
        
        # Frame to list GPU
        self.gpu_frame = ttk.Frame(self)
        self.gpu_frame.pack(fill='both', expand=True, padx=10)
        
        # Button
        button_frame = ttk.Frame(self)
        button_frame.pack(fill='x', padx=10, pady=5)
        ttk.Button(button_frame, text="Refresh", command=self.update_gui).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Exit", command=self.stop).pack(side='left')

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        if info:
            self.services[name] = info
            self.update_gui()

    def remove_service(self, zeroconf, type, name):
        if name in self.services:
            del self.services[name]
            self.update_gui()

    def update_gui(self):
        # Clear current frame
        for widget in self.gpu_frame.winfo_children():
            widget.destroy()

        # Add information of gpu
        for name, info in self.services.items():
            frame = ttk.LabelFrame(self.gpu_frame, text=name)
            frame.pack(fill='x', pady=5)
            
            try:
                props = {k.decode('utf-8'): v.decode('utf-8') 
                        for k, v in info.properties.items()}
                
                ttk.Label(frame, text=f"GPU: {props.get('name', 'N/A')}").pack()
                ttk.Label(frame, text=f"Load: {props.get('load', 'N/A')}%").pack()
                ttk.Label(frame, text=f"Memory: {props.get('memory_used', 'N/A')}/{props.get('memory_total', 'N/A')} MB").pack()
                ttk.Label(frame, text=f"Temperature: {props.get('temperature', 'N/A')}°C").pack()
            except Exception as e: 
                ttk.Label(frame, text=f"Error reading device: {str(e)}").pack()

    def start_browser(self):
        self.browser = ServiceBrowser(self.zeroconf, "_gpumonitor._tcp.local.", self)

    def stop(self):
        self.zeroconf.close()
        self.quit()

def run_client():
    app = GPUClient()
    app.mainloop()