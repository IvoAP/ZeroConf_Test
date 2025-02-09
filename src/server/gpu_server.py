import socket
import tkinter as tk
from tkinter import ttk

import GPUtil
from zeroconf import ServiceInfo, Zeroconf


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

def run_server():
    app = GPUServer()
    app.mainloop()