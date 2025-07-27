import tkinter as tk
import time

store = {}

def set_key():
    key = entry_key.get()
    value = entry_value.get()
    ttl = entry_ttl.get()
    if not key or not value:
        result_var.set("Key and value required.")
        return
    try:
        ttl = int(ttl) if ttl else None
    except ValueError:
        result_var.set("TTL must be a number.")
        return
    expire_at = time.time() + ttl if ttl else None
    store[key] = {'value': value, 'expire_at': expire_at}
    result_var.set(f"Key '{key}' set successfully.")

def get_key():
    key = entry_key.get()
    data = store.get(key)
    if not data:
        result_var.set("Key not found.")
        return
    if data['expire_at'] and data['expire_at'] <= time.time():
        del store[key]
        result_var.set("Key expired.")
        return
    result_var.set(f"Value: {data['value']}")

def delete_key():
    key = entry_key.get()
    data = store.pop(key, None)
    if data:
        result_var.set(f"Deleted: {data}")
    else:
        result_var.set("Key not found.")

def ttl_key():
    key = entry_key.get()
    data = store.get(key)
    if not data or not data['expire_at']:
        result_var.set("TTL: -1 (no expiry)")
        return
    remaining = int(data['expire_at'] - time.time())
    if remaining < 0:
        del store[key]
        result_var.set("Key expired.")
        return
    result_var.set(f"TTL: {remaining} seconds")

def show_all():
    output = ""
    for k, v in store.items():
        status = "expired" if v['expire_at'] and v['expire_at'] <= time.time() else "active"
        output += f"{k}: {v['value']} (status: {status})\n"
    result_var.set(output or "No keys found.")

# GUI Setup
root = tk.Tk()
root.title("Mini Redis Clone")

tk.Label(root, text="Key:").grid(row=0, column=0)
entry_key = tk.Entry(root)
entry_key.grid(row=0, column=1)

tk.Label(root, text="Value:").grid(row=1, column=0)
entry_value = tk.Entry(root)
entry_value.grid(row=1, column=1)

tk.Label(root, text="TTL (seconds):").grid(row=2, column=0)
entry_ttl = tk.Entry(root)
entry_ttl.grid(row=2, column=1)

tk.Button(root, text="SET", width=10, command=set_key).grid(row=3, column=0)
tk.Button(root, text="GET", width=10, command=get_key).grid(row=3, column=1)
tk.Button(root, text="DEL", width=10, command=delete_key).grid(row=4, column=0)
tk.Button(root, text="TTL", width=10, command=ttl_key).grid(row=4, column=1)
tk.Button(root, text="SHOW ALL", width=22, command=show_all).grid(row=5, column=0, columnspan=2)

result_var = tk.StringVar()
tk.Label(root, textvariable=result_var, fg="blue", wraplength=400, justify="left").grid(row=6, column=0, columnspan=2)

root.mainloop()
