import customtkinter as ctk
import tkinter.ttk as ttk
from datetime import datetime
from process.process_transactions import process_get_all_transactions
from ui.add_transaction_popup import AddTransactionPopup


class DashboardView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        # Lưu tháng/năm hiện tại để lọc giao dịch
        self.current_month = datetime.now().month
        self.current_year = datetime.now().year

        self._build_ui()
        self.load_data()

    def _build_ui(self):
        # ======================================================
        # THANH TIÊU ĐỀ + NÚT THÊM GIAO DỊCH
        # ======================================================
        top_bar = ctk.CTkFrame(self, fg_color="transparent")
        top_bar.pack(fill="x", padx=15, pady=(15, 5))

        ctk.CTkLabel(
            top_bar, text="📊 Tổng Quan Chi Tiêu",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(side="left")

        ctk.CTkButton(
            top_bar, text="➕ Thêm Giao Dịch",
            width=160, height=35,
            fg_color="#28a745", hover_color="#218838",
            command=self.open_add_popup
        ).pack(side="right")

        # ======================================================
        # BỘ CHỌN THÁNG (Trái / Phải)
        # ======================================================
        month_bar = ctk.CTkFrame(self, fg_color="transparent")
        month_bar.pack(fill="x", padx=15, pady=5)

        ctk.CTkButton(
            month_bar, text="◀", width=35,
            command=self.prev_month
        ).pack(side="left")

        self.month_label = ctk.CTkLabel(
            month_bar, text="",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.month_label.pack(side="left", padx=10)

        ctk.CTkButton(
            month_bar, text="▶", width=35,
            command=self.next_month
        ).pack(side="left")

        # ======================================================
        # 3 THẺ THỐNG KÊ: THU / CHI / SỐ DƯ
        # ======================================================
        stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        stats_frame.pack(fill="x", padx=15, pady=10)
        stats_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # Tạo 3 thẻ và lưu lại label giá trị để cập nhật sau
        self.income_label = self._make_stat_card(stats_frame, "💰 Tổng Thu", "0 ₫", "#28a745", col=0)
        self.expense_label = self._make_stat_card(stats_frame, "💸 Tổng Chi", "0 ₫", "#dc3545", col=1)
        self.balance_label = self._make_stat_card(stats_frame, "📈 Số Dư", "0 ₫", "#1a73e8", col=2)

        # ======================================================
        # BẢNG GIAO DỊCH (Treeview)
        # ======================================================
        table_container = ctk.CTkFrame(self)
        table_container.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        # Áp style cho Treeview (để bảng nhìn đẹp hơn)
        style = ttk.Style()
        style.configure("Treeview", rowheight=28, font=("Arial", 10))
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))

        columns = ("ID", "Số tiền", "Danh mục", "Ghi chú", "Ngày", "Loại")
        self.tree = ttk.Treeview(
            table_container, columns=columns,
            show="headings", height=14
        )

        # Cài đặt từng cột
        col_config = {
            "ID":       50,
            "Số tiền":  120,
            "Danh mục": 130,
            "Ghi chú":  180,
            "Ngày":     100,
            "Loại":     80,
        }
        for col, width in col_config.items():
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor="center")

        # Thanh cuộn dọc
        scrollbar = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def _make_stat_card(self, parent, title, value, color, col):
        """Tạo một thẻ thống kê và trả về label giá trị để cập nhật sau"""
        card = ctk.CTkFrame(parent, corner_radius=10)
        card.grid(row=0, column=col, padx=5, sticky="ew", ipady=5)

        ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=12)).pack(pady=(8, 0))
        value_label = ctk.CTkLabel(
            card, text=value,
            font=ctk.CTkFont(size=17, weight="bold"),
            text_color=color
        )
        value_label.pack(pady=(0, 8))
        return value_label

    def load_data(self):
        """Tải dữ liệu từ DB, lọc theo tháng, cập nhật bảng và thẻ thống kê"""
        self.month_label.configure(text=f"Tháng {self.current_month} / {self.current_year}")

        all_data = process_get_all_transactions()

        # Nếu có lỗi (trả về string thay vì list)
        if not isinstance(all_data, list):
            return

        # Lọc giao dịch theo tháng/năm đang chọn
        filtered = []
        for row in all_data:
            try:
                date_val = row[4]  # Cột thứ 5 là ngày (spent_on)
                # DB trả về kiểu date hoặc string tuỳ driver
                if hasattr(date_val, 'month'):
                    match = (date_val.month == self.current_month and date_val.year == self.current_year)
                else:
                    parsed = datetime.strptime(str(date_val), "%Y-%m-%d")
                    match = (parsed.month == self.current_month and parsed.year == self.current_year)

                if match:
                    filtered.append(row)
            except Exception:
                pass

        # Xóa hết dữ liệu cũ trong bảng
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Tính tổng thu/chi và đổ dữ liệu vào bảng
        total_income = 0.0
        total_expense = 0.0

        for row in filtered:
            self.tree.insert("", "end", values=row)
            amount = float(row[1])
            type_name = str(row[5]).lower()  # Cột "Loại": "Thu" hoặc "Chi"
            if "thu" in type_name:
                total_income += amount
            else:
                total_expense += amount

        balance = total_income - total_expense

        # Cập nhật 3 thẻ thống kê
        self.income_label.configure(text=f"{total_income:,.0f} ₫")
        self.expense_label.configure(text=f"{total_expense:,.0f} ₫")
        self.balance_label.configure(
            text=f"{balance:,.0f} ₫",
            text_color="#28a745" if balance >= 0 else "#dc3545"
        )

    def open_add_popup(self):
        """Mở popup thêm giao dịch. Sau khi lưu xong, tự động reload bảng"""
        AddTransactionPopup(self, on_success=self.load_data)

    def prev_month(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.load_data()

    def next_month(self):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.load_data()
