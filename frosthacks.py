import tkinter as tk
from tkinter import ttk
import openai

class RDBMS:
    def __init__(self, master):
        self.master = master
        self.master.title("Excel Input GUI")
        self.selected_options = {}
        self.api_key=""

        # Create and configure widgets
        self.create_widgets()
        self.text = ""

    def create_widgets(self):
        # Multiline Text Entry
        label1=ttk.Label(self.master,text="ENTER THE OPENAI API KEY TO PROCEED")
        label1.grid(row=0,column=0,pady=10)

        self.label1_in=ttk.Entry(self.master)
        self.label1_in.grid(row=0,column=1,pady=10)

        

        text_entry_label = ttk.Label(self.master, text="Input query:")
        text_entry_label.grid(row=1, column=0, pady=10, padx=5, sticky=tk.W)

        self.text_entry = tk.Text(self.master, wrap=tk.NONE, height=10, width=70)
        self.text_entry.grid(row=2, column=0, pady=5, padx=5, sticky=tk.W + tk.E + tk.N + tk.S)

        entry_scrollbar_y = tk.Scrollbar(self.master, command=self.text_entry.yview)
        entry_scrollbar_y.grid(row=2, column=1)
        entry_scrollbar_x = tk.Scrollbar(self.master, command=self.text_entry.xview, orient=tk.HORIZONTAL)
        entry_scrollbar_x.grid(row=3, column=0, sticky=tk.W + tk.E)
        self.text_entry.config(yscrollcommand=entry_scrollbar_y.set, xscrollcommand=entry_scrollbar_x.set)

                # Output Text
        text_out_label = ttk.Label(self.master, text="Output:")
        text_out_label.grid(row=1, column=2, pady=5, padx=10, sticky=tk.W)

        self.text_out = tk.Text(self.master, wrap=tk.NONE, height=10, width=70)
        self.text_out.grid(row=2, column=2, pady=5, padx=10, sticky=tk.W + tk.E + tk.N + tk.S)

        # Check buttons
        options_label = ttk.Label(self.master, text="Select Options:")
        options_label.grid(row=4, column=0, pady=10, padx=10, sticky=tk.W)

        options = ["MySQL", "PostgreSQL", "Oracle Database", "Microsoft SQL Server", "SQLite"]

        for i, option in enumerate(options):
            var = tk.BooleanVar()
            check_button = ttk.Checkbutton(self.master, text=option, variable=var,
                                           command=lambda opt=option, v=var: self.toggle_option(opt, v))
            check_button.grid(row=i+5, column=0, pady=5, padx=10, sticky=tk.W)
            self.selected_options[option] = var  # Store the BooleanVar in the dictionary



        output_scrollbar_y = tk.Scrollbar(self.master, command=self.text_out.yview)
        output_scrollbar_y.grid(row=2, column=3, sticky=tk.W + tk.E + tk.N + tk.S)
        output_scrollbar_x = tk.Scrollbar(self.master, command=self.text_out.xview, orient=tk.HORIZONTAL)
        output_scrollbar_x.grid(row=3, column=2, sticky=tk.W + tk.E)
        self.text_out.config(yscrollcommand=output_scrollbar_y.set, xscrollcommand=output_scrollbar_x.set)

        # Submit button
        submit_button = ttk.Button(self.master, text="Submit", command=self.submit_form)
        submit_button.grid(row=len(options)+5, column=0, columnspan=3, pady=20, padx=10, sticky=tk.W)

    def toggle_option(self, option, var):
        self.selected_options[option] = var.get()

    def submit_form(self):
        #print(self.selected_options)
        self.api_key=self.label1_in.get()
        chosen_options = [option for option, state in self.selected_options.items() if state==True]
        #print(chosen_options)
        input_query = self.text_entry.get("1.0", tk.END).strip()
        self.chat(input_query, chosen_options)

    def update_text(self, new_text):
        self.text_out.delete(1.0, tk.END)
        self.text_out.insert(tk.END, new_text)

    def chat(self, input_query, chosen_options):
        query_options = " ".join(chosen_options)
        full_query = f"{input_query} Convert the above code/query into only in {query_options} dbms platform-oriented code"

        openai.api_key = self.api_key
        messages = [{"role": "system", "content": "You are an intelligent assistant."}]

        user_message = {"role": "user", "content": full_query}
        messages.append(user_message)

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        assistant_reply = response.choices[0].message.content
        print(assistant_reply)
        self.update_text(assistant_reply)

if __name__ == "__main__":
    root = tk.Tk()
    app = RDBMS(root)
    root.mainloop()
