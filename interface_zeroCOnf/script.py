import socket
import tkinter as tk
from tkinter import ttk

import GPUtil
from zeroconf import ServiceBrowser, ServiceInfo, Zeroconf


class GPUServer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GPU Monitor Server")
        self.ip = socket.gethostbyname(socket.gethostname())
        self.port = 12345
        self.zeroconf = Zeroconf()
        self.setup_gui()
        self.start_service()

    def setup_gui(self):
        self.geometry("300x200")
        
        ttk.Label(self, text="GPU Monitor Server", font=('Helvetica', 14)).pack(pady=10)
        ttk.Label(self, text=f"IP: {self.ip}").pack()
        ttk.Label(self, text=f"Port: {self.port}").pack()
        
        self.status_label = ttk.Label(self, text="Status: Running")
        self.status_label.pack(pady=10)
        
        ttk.Button(self, text="Stop", command=self.stop).pack()

    def get_gpu_info(self):
        gpus = GPUtil.getGPUs()
        if not gpus:
            return {"status": "No GPU found"}
        
        gpu = gpus[0]
        return {
            "name": gpu.name,
            "load": f"{gpu.load * 100:.1f}",
            "memory_used": str(gpu.memoryUsed),
            "memory_total": str(gpu.memoryTotal),
            "temperature": str(gpu.temperature)
        }

    def start_service(self):
        gpu_info = self.get_gpu_info()
        properties = {k: str(v).encode('utf-8') for k, v in gpu_info.items()}
        
        service_info = ServiceInfo(
            "_gpumonitor._tcp.local.",
            f"GPU-{socket.gethostname()}._gpumonitor._tcp.local.",
            addresses=[socket.inet_aton(self.ip)],
            port=self.port,
            properties=properties
        )
        self.zeroconf.register_service(service_info)

    def stop(self):
        self.zeroconf.close()
        self.quit()

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
        
        # Frame para a lista de GPUs
        self.gpu_frame = ttk.Frame(self)
        self.gpu_frame.pack(fill='both', expand=True, padx=10)
        
        # Botões
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
        # Limpa o frame atual
        for widget in self.gpu_frame.winfo_children():
            widget.destroy()

        # Adiciona as informações de cada GPU
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

def run_server():
    app = GPUServer()
    app.mainloop()

def run_client():
    app = GPUClient()
    app.mainloop()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2 or sys.argv[1] not in ['-s', '-c']:
        print("Usage: python script.py [-s|-c]")
        print("  -s: run as server")
        print("  -c: run as client")
        sys.exit(1)

    if sys.argv[1] == '-s':
        run_server()
    else:
        run_client()