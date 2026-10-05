import customtkinter as ctk
from tkcalendar import DateEntry
from tkinter import messagebox
from db.category_db import get_all_categories
from db.transaction_type_db import get_all_transaction_type
from process.process_transactions import process_add_transaction


class AddTransactionPopup(ctk.CTkToplevel):
    def __init__(self, master, on_success=None):
        super().__init__(master)
        self.title("Thêm Giao Dịch Mới")
        self.geometry("420x520")
        self.resizable(False, False)
        self.grab_set()  # Khoá cửa sổ cha lại, bắt buộc phải xử lý popup này trước

        self.on_success = on_success  # Hàm callback - gọi sau khi lưu thành công để cập nhật bảng

        # ---------- Load dữ liệu từ Database ----------
        categories = get_all_categories()           # [(category_id, category_name), ...]
        transaction_types = get_all_transaction_type()  # [(type_id, type_name), ...]

        # Tạo từ điển: tên hiển thị -> id (để khi người dùng chọn tên, ta lấy đúng id gửi xuống DB)
        self.category_map = {row[1]: row[0] for row in categories}
        self.type_map = {row[1]: row[0] for row in transaction_types}

        # ---------- TIÊU ĐỀ ----------
        ctk.CTkLabel(
            self, text="➕ Thêm Giao Dịch",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=15)

        # ---------- LOẠI GIAO DỊCH (Thu / Chi) ----------
        ctk.CTkLabel(self, text="Loại giao dịch:").pack(anchor="w", padx=30)
        self.type_var = ctk.StringVar(
            value=list(self.type_map.keys())[0] if self.type_map else ""
        )
        ctk.CTkOptionMenu(
            self, values=list(self.type_map.keys()), variable=self.type_var
        ).pack(fill="x", padx=30, pady=(2, 10))

        # ---------- DANH MỤC ----------
        ctk.CTkLabel(self, text="Danh mục:").pack(anchor="w", padx=30)
        self.category_var = ctk.StringVar(
            value=list(self.category_map.keys())[0] if self.category_map else ""
        )
        ctk.CTkOptionMenu(
            self, values=list(self.category_map.keys()), variable=self.category_var
        ).pack(fill="x", padx=30, pady=(2, 10))

        # ---------- SỐ TIỀN ----------
        ctk.CTkLabel(self, text="Số tiền (VNĐ):").pack(anchor="w", padx=30)
        self.amount_entry = ctk.CTkEntry(self, placeholder_text="Ví dụ: 150000")
        self.amount_entry.pack(fill="x", padx=30, pady=(2, 10))

        # ---------- NGÀY GIAO DỊCH (Lịch) ----------
        ctk.CTkLabel(self, text="Ngày giao dịch:").pack(anchor="w", padx=30)
        # DateEntry là widget tkinter thường, cần để trong Frame để tương thích
        date_frame = ctk.CTkFrame(self, fg_color="transparent")
        date_frame.pack(fill="x", padx=30, pady=(2, 10))
        self.date_picker = DateEntry(
            date_frame,
            width=30,
            date_pattern="yyyy-mm-dd",
            font=("Arial", 11)
        )
        self.date_picker.pack(fill="x", ipady=5)

        # ---------- GHI CHÚ ----------
        ctk.CTkLabel(self, text="Ghi chú (không bắt buộc):").pack(anchor="w", padx=30)
        self.note_entry = ctk.CTkEntry(self, placeholder_text="Ví dụ: Mua cà phê buổi sáng")
        self.note_entry.pack(fill="x", padx=30, pady=(2, 10))

        # ---------- NÚT BẤM ----------
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=30, pady=15)

        ctk.CTkButton(
            btn_frame, text="Huỷ",
            fg_color="gray", hover_color="#555",
            command=self.destroy
        ).pack(side="left", expand=True, padx=(0, 5))

        ctk.CTkButton(
            btn_frame, text="✔ Xác nhận",
            fg_color="#28a745", hover_color="#218838",
            command=self.save
        ).pack(side="right", expand=True, padx=(5, 0))

    def save(self):
        """Lấy dữ liệu từ form, gọi tầng Process để kiểm tra và lưu xuống DB"""
        amount_str = self.amount_entry.get()
        category_id = self.category_map.get(self.category_var.get())
        transaction_type_id = self.type_map.get(self.type_var.get())
        note = self.note_entry.get()
        spent_on = self.date_picker.get_date().strftime("%Y-%m-%d")

        result = process_add_transaction(amount_str, category_id, note, spent_on, transaction_type_id)

        if "Thành công" in result:
            messagebox.showinfo("✅ Thành công", result)
            if self.on_success:
                self.on_success()  # Gọi callback để reload bảng dữ liệu bên ngoài
            self.destroy()
        else:
            messagebox.showerror("❌ Lỗi", result)
