import tkinter as tk
from tkinter import ttk, messagebox
import json
import time
import os

DATA_FILE = "redis_clone_data.json"

# ---------------------- Core Store ----------------------
class RedisClone:
    def __init__(self):
        self.store = {}
        self.load_data()

    def set(self, key, value, ttl=None):
        expiry = time.time() + int(ttl) if ttl else None
        self.store[key] = {"value": value, "expiry": expiry}
        self.save_data()

    def get(self, key):
        data = self.store.get(key)
        if data:
            if data['expiry'] and time.time() > data['expiry']:
                del self.store[key]
                self.save_data()
                return None
            return data['value']
        return None

    def delete(self, key):
        if key in self.store:
            del self.store[key]
            self.save_data()

    def keys(self):
        return [k for k in self.store if not self.is_expired(k)]

    def is_expired(self, key):
        data = self.store.get(key)
        if data and data['expiry'] and time.time() > data['expiry']:
            del self.store[key]
            self.save_data()
            return True
        return False

    def get_all_data(self):
        # Clean up expired keys
        for key in list(self.store):
            self.is_expired(key)
        return self.store

    def save_data(self):
        with open(DATA_FILE, 'w') as f:
            json.dump(self.store, f)

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                try:
                    self.store = json.load(f)
                except json.JSONDecodeError:
                    self.store = {}

# ---------------------- GUI ----------------------
class RedisGUI:
    def __init__(self, master, redis):
        self.redis = redis
        self.master = master
        master.title("Redis Clone GUI")

        # Entry Frame
        self.key_entry = tk.Entry(master, width=30)
        self.value_entry = tk.Entry(master, width=30)
        self.ttl_entry = tk.Entry(master, width=10)
        self.key_entry.grid(row=0, column=1, padx=5, pady=5)
        self.value_entry.grid(row=0, column=3, padx=5, pady=5)
        self.ttl_entry.grid(row=0, column=5, padx=5, pady=5)

        tk.Label(master, text="Key").grid(row=0, column=0)
        tk.Label(master, text="Value").grid(row=0, column=2)
        tk.Label(master, text="TTL (s)").grid(row=0, column=4)

        tk.Button(master, text="Set", command=self.set_key).grid(row=0, column=6, padx=5)
        tk.Button(master, text="Refresh", command=self.refresh_table).grid(row=0, column=7, padx=5)

        # Treeview Table
        self.tree = ttk.Treeview(master, columns=("Key", "Value", "Expiry"), show="headings", height=10)
        self.tree.heading("Key", text="Key")
        self.tree.heading("Value", text="Value")
        self.tree.heading("Expiry", text="Expires At")
        self.tree.grid(row=1, column=0, columnspan=8, padx=10, pady=10)

        # Delete Button
        tk.Button(master, text="Delete Selected", command=self.delete_selected).grid(row=2, column=0, columnspan=8)

        # Start refreshing table every 3 seconds
        self.auto_refresh()

    def set_key(self):
        key = self.key_entry.get().strip()
        value = self.value_entry.get().strip()
        ttl = self.ttl_entry.get().strip()
        if not key or not value:
            messagebox.showwarning("Missing Fields", "Key and Value are required!")
            return
        self.redis.set(key, value, ttl if ttl else None)
        self.key_entry.delete(0, tk.END)
        self.value_entry.delete(0, tk.END)
        self.ttl_entry.delete(0, tk.END)
        self.refresh_table()

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for key, data in self.redis.get_all_data().items():
            expiry = data['expiry']
            expires_at = time.strftime('%H:%M:%S', time.localtime(expiry)) if expiry else "-"
            self.tree.insert("", "end", values=(key, data['value'], expires_at))

    def delete_selected(self):
        selected = self.tree.selection()
        for item in selected:
            key = self.tree.item(item, "values")[0]
            self.redis.delete(key)
        self.refresh_table()

    def auto_refresh(self):
        self.refresh_table()
        self.master.after(3000, self.auto_refresh)

# ---------------------- Run ----------------------
if __name__ == "__main__":
    root = tk.Tk()
    redis = RedisClone()
    app = RedisGUI(root, redis)
    root.mainloop()
