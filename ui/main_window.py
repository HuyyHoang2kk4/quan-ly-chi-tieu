import customtkinter as ctk
from ui.dashboard_view import DashboardView

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Quản Lý Chi Tiêu")
        self.geometry("950x600")

        # Chia cửa sổ thành 2 cột: Sidebar (trái) + Nội dung (phải)
        self.grid_columnconfigure(0, weight=0)  # Cột trái - cố định
        self.grid_columnconfigure(1, weight=1)  # Cột phải - co giãn
        self.grid_rowconfigure(0, weight=1)

        # ============================
        # SIDEBAR (Cột trái)
        # ============================
        self.sidebar = ctk.CTkFrame(self, width=160, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)  # Giữ nguyên width=160

        ctk.CTkLabel(
            self.sidebar, text="💰\nChi Tiêu",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=25)

        ctk.CTkButton(
            self.sidebar, text="📊 Dashboard",
            command=self.show_dashboard
        ).pack(fill="x", padx=10, pady=5)

        # ============================
        # KHU VỰC NỘI DUNG (Cột phải)
        # ============================
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=0, column=1, sticky="nsew")

        # Mặc định hiển thị Dashboard
        self.show_dashboard()

    def show_dashboard(self):
        """Xoá nội dung cũ và hiển thị màn hình Dashboard"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        DashboardView(self.content_frame).pack(fill="both", expand=True)
