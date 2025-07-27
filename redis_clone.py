import time
store = {}
ttl_store = {}

def set_key(key,value,ttl=None):
    expire_at=time.time() + ttl if ttl else None
    store[key] = {'value':value,'expire_at':expire_at}

def get_key(key):
    data=store.get(key)
    if not data:
        return None
    if data['expire_at'] and time.time() > data['expire_at']:
        del_key(key)
        return None
    return data['value']

def del_key(key):
    return store.pop(key, None)

def ttl_key(key):
    data = store.get(key)
    if not data or not data['expire_at']:
        return -1
    remaining = int(data['expire_at']-time.time())
    if remaining <0:
        del_key(key)
        return -1
    return remaining
    
#Command line workssssss

while True:
    cmd = input(">> ").strip().split()
    if not cmd:
        continue

    op = cmd[0].upper()

    if op == "SET":
        key, val = cmd[1], cmd[2]
        ttl = int(cmd[3]) if len(cmd) == 4 else None
        set_key(key, val, ttl)

    elif op == "GET":
        result = get_key(cmd[1])
        print(result if result else "Key not found or expired.")

    elif op == "DEL":
        deleted = del_key(cmd[1])
        print(deleted if deleted else "Key not found.")

    elif op == "TTL":
        print(ttl_key(cmd[1]))

    elif op == "EXIT":
        break
    
    else:
        print("Unknown command.")