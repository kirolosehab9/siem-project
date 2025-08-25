import customtkinter as ctk
from tkinter import filedialog
import re
import pandas as pd
from tkinter import scrolledtext
def parse_logs(file_path):
    logs = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            pattern = r"^(.*?)\s+(INFO|TRACE|WARNING)\s+(.*)$"
            match = re.match(pattern, line)
            if match:
                timestamp, severity, message = match.groups()
                logs.append((timestamp, severity, message))
    return logs
def display_logs(df_to_display):
    log_text.config(state='normal')
    log_text.delete(1.0, 'end') 
    for _, row in df_to_display.iterrows():
        log_text.insert('end', f"{row['Timestamp']} {row['Severity']} {row['Message']}\n")
    log_text.config(state='disabled') 
if __name__ == "__main__":
    ctk.set_appearance_mode("light")  
    ctk.set_default_color_theme("blue")  

    root = ctk.CTk()  
    root.title("Log File Viewer")
    root.geometry("800x600")
    
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if not file_path:
        print("No file selected")
        exit()

    logs = parse_logs(file_path)
    
    df = pd.DataFrame(logs, columns=["Timestamp","Severity","Message"])
    print(df)
    
    failed_logins = df[df['Message'].str.contains("Failed login")]
    if len(failed_logins) >= 3:
        print("ALERT: Multiple failed logins detected")
    
    df.to_csv("parsed_logs.csv", index=False)
    
    
    log_text = scrolledtext.ScrolledText(root)
    log_text.pack(fill="both", expand=True, padx=10, pady=10)
    log_text.config(state='disabled')

    button_frame = ctk.CTkFrame(root)
    button_frame.pack(fill="x", padx=10, pady=5)

    def show_all():
        display_logs(df)
    
    def show_warnings():
        display_logs(df[df['Severity'] == "TRACE"])
    
    def show_errors():
        display_logs(df[df['Severity'] == "WARNING"])

    ctk.CTkButton(button_frame, text="Show All", command=show_all).pack(side="left", padx=5)
    ctk.CTkButton(button_frame, text="Show Warnings", command=show_warnings).pack(side="left", padx=5)
    ctk.CTkButton(button_frame, text="Show Errors", command=show_errors).pack(side="left", padx=5)

    display_logs(df)

    root.mainloop()