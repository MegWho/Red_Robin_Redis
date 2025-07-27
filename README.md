# Red Robin Redis
Hi!
I'm tiny Redis clone written in Python by meg (python because she's..ykw).  
She's (still working on making me better and) is building for to learning and experimentation, I'm just a mimic of core Redis behavior — including in-memory storage, basic command parsing, and persistence so when you close a file, i forgive, but not forget.

## Features
1. Key-Value Storage: Mimics basic Redis functionalities like setting and getting keys.
2. Data Persistence: Stores data in `redis_clone_data.json` for reuse.
3. GUI Interfaces: Two versions (`redis_GUI.py` and `redis_GUI2.py`) to interact with data without a terminal.

## How to Run
1. Clone the repo:
    git clone https://github.com/MegWho/Red_Robin_Redis.git
    cd Red_Robin_Redis

2. Run the core logic:
    python redis_clone.py

3. Launch GUI:
    python redis_GUI.py 
    or
    python redis_GUI2.py

```text
Project Structure

Red_Robin_Redis/
├── redis_clone.py         # Core logic for the in-memory database.
├── redis_clone_data.json  # Stores the persistent key-value data.
├── redis_GUI.py           # First version of GUI interface using Tkinter.
├── redis_GUI2.py          # Alternative GUI with improved layouts in in table.
├── .gitignore             # Specifies files to exclude from version control.
└── LICENSE 
```

This project is licensed under the MIT License.
