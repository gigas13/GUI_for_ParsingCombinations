from tkinter import *
from tkinter import filedialog, messagebox, ttk, Entry
import pandas as pd
import numpy as np
from itertools import combinations
from csv import writer
from os import getcwd

root = Tk()
root.title('Self Remittance APP')
root.iconbitmap(r'C:\Users\XMHC4749\Desktop\Py\SelfRemittance-APP\tree.ico')
#root.configure(background='#00FFFF')
#root.geometry("1000x500")

df_loaded = pd.DataFrame()
def min_max(num):
#get a number num, range it from 1 to num+1 and alternate the values min - max
    lst = list(range(1,num+1))
    lst2 = []
    if len(lst)==1:
        return lst
    else:
        while len(lst)>=2:
            lst2.append(min(lst))
            lst2.append(max(lst))
            lst.remove(min(lst))
            lst.remove(max(lst))
            if len(lst) == 1:
                lst2.append(lst[0])
    return lst2
### identify the possible combinations (mathematically) and return the first combination found
def get_subset(numbers, target, error):
    check_negatives = [number for number in numbers if number<0] #if all numbers are positive, we can remove numbers bigger than target (trying to reduce the combinations)
    if len(check_negatives)==0:
        numbers = [number for number in numbers if number<=(target+error)]
    check=0
    outcome = ()
    for L in min_max(len(numbers)):
        if check == 0:
            for subset in combinations(numbers, L):
                if (target-error) <= sum(subset) <= (target+error):
                    outcome = list(subset)
                    check=1
                    break
        else:
            break
    return outcome
def df_generator(lst, df):
    df_construct = pd.DataFrame(columns=["Invoice", "Value"])
    for i, row in df.iterrows():
        for j, value in enumerate(lst):
            if row.Value == value:
                df_construct = pd.concat([df_construct,pd.DataFrame(row).T])
                del lst[j]
                break
    return df_construct

def loadCSV(): ##command to browse csv file
    clear_data(tv1)
    filename = filedialog.askopenfile(initialdir="/Desktop", title="Select a File",
                                        filetype=(('csv files', '*.csv'),('all files', '*.*')))
    file_path = filename.name
    try:
        df = pd.read_csv(file_path)
    except ValueError:
        messagebox.showerror("Information", "The file you have chosen is invalid")
        return None
    except FileNotFoundError:
        tk.messagebox.showerror("Information", "File Not Found")
        return None
    global df_loaded
    df_loaded = df
    label_file['text'] = 'Loaded'
    label4a['text'] = 'Invoices Loaded: {}'.format(df.shape[0])
    df = add_total(df)
    display_df(tv1, df)
    tv1.column('Invoice', anchor=W, width=100, minwidth=40)
    tv1.column('Value', anchor=CENTER, width=100, minwidth=40)
    return None
def clear_data(tv):
    try: ##clear a Treeview object
        tv.delete(*tv.get_children())
    except:
        pass
def display_df(tv, df): ##display a pandas df in a Treeview object
    tv['column'] = list(df.columns)
    tv['show'] = "headings"
    for column in tv['columns']:
        tv.heading(column, text=column)
    df_rows = df.to_numpy().tolist()
    for row in df_rows:
        tv.insert("", "end", values=row)
    return None
def display_df_final(df_loaded):
    if df_loaded.size == 0:
        messagebox.showerror("Data Not Imported", "Load .csv file first!")
    else:
        clear_data(tv2)
        clear_data(tv3)
        values = df_loaded.Value.to_list()
        target_string = input_payment.get()
        if target_string == "" : target_string=0
        target_range = input_range.get()
        if target_range == "" : target_range=0
        try:
            target = float(target_string)
            error = float(target_range)
        except:
            messagebox.showerror("Payment or Range not numeric", "Insert numeric values (use '.' as delimiter)")
            return
        combination = get_subset(values, target=target, error=0)
        df_filtered = df_generator(combination, df_loaded)
        df_final_exact = add_total(df_filtered)
        display_df(tv2, df_final_exact)
        tv2.column('Invoice', anchor=W, width=100, minwidth=40)
        tv2.column('Value', anchor=CENTER, width=100, minwidth=40)
        if df_final_exact.iloc[-1,-1] == 0:
            combination = get_subset(values, target=target, error=error)
            df_filtered = df_generator(combination, df_loaded)
            df_final_loose = add_total(df_filtered)
            display_df(tv3, df_final_loose)
            tv3.column('Invoice', anchor=W, width=100, minwidth=40)
            tv3.column('Value', anchor=CENTER, width=100, minwidth=40)
        else:
            df_final_loose = pd.DataFrame()
        global dfs_final
        dfs_final = [df_final_exact, df_final_loose]
    return None
def add_total(df):
    df_blank = pd.DataFrame(['Total', np.nan], index=['Invoice','Value']).T
    df_final = pd.concat([df, df_blank])
    df_final.iloc[-1,-1] = df.Value.sum()
    return df_final

#Row 0 / 1
lab0a = Label(root, text="App for SelfRemittance", font=('Arial', 18), fg='blue').grid(row=0, column=1, pady=5)
lab0b = Label(root, text="Payment").grid(row=1, column=1, pady=10)
lab0c = Label(root, text="Range Allowed").grid(row=1, column=2, pady=10)
#Row2
button_load = Button(root, width=20, text='Load .csv file', command=loadCSV).grid(row=2, column=0)
input_payment = Entry(root, width=25, borderwidth=5)
input_payment.grid(row=2, column=1, padx=10, pady=5)
input_range = Entry(root, width=25, borderwidth=5)
input_range.grid(row=2, column=2, padx=10, pady=5)
img = PhotoImage(file=r'C:\Users\XMHC4749\Desktop\Py\SelfRemittance-APP\start-button-png-4.png')
start_button = Button(root, borderwidth='0', image=img, padx=20, command=lambda: display_df_final(df_loaded)).grid(row=2, column=19)
#row3
label_file = Label(root, text="No File Selected")
label_file.grid(row=3, column=0)

#row4
label4a = Label(root, text="Invoices Loaded")
label4a.grid(row=4, column=0, pady=10)
label4b = Label(root, text="Exact Match")
label4b.grid(row=4, column=1, pady=10)
label4c = Label(root, text="Loose Match")
label4c.grid(row=4, column=2, pady=10)
#row5
tv1 = ttk.Treeview(root)
tv1.grid(row=5, column=0, padx=20)
tv2 = ttk.Treeview(root)
tv2.grid(row=5, column=1)
tv3 = ttk.Treeview(root)
tv3.grid(row=5, column=2)
tresscrolly1 = Scrollbar(root, orient='vertical', command=tv1.yview)
tresscrolly1.grid(row=5, column=0)
tresscrolly2 = Scrollbar(root, orient='vertical', command=tv2.yview)
tresscrolly2.grid(row=5, column=1)
tresscrolly3 = Scrollbar(root, orient='vertical', command=tv3.yview)
tresscrolly3.grid(row=5, column=2)
def clean_all():
    global df_loaded
    df_loaded = pd.DataFrame()
    clear_data(tv1)
    clear_data(tv2)
    clear_data(tv3)
    input_payment.delete(0, 'end')
    input_range.delete(0, 'end')
    return None
clean_button = Button(root, text="Clean All", command=clean_all)
clean_button.grid(row=5, column=19)

#row6
def save1(df):
    fln = filedialog.asksaveasfile(initialdir=getcwd(), title="Save CSV",
                            filetypes = (('csv files', '*.csv'), ('All Files', '*.*')),
                            initialfile = 'outcome',
                            defaultextension=".csv")
    with open(fln.name, mode='w', newline='') as myfile:
        exp_writer = writer(myfile, delimiter=',')
        exp_writer.writerow(list(df.columns))
        for i, row in df.iterrows():
            exp_writer.writerow(row)
    messagebox.showinfo("Data Exported", "Your data has been exported to CSV")
btn_save1 = ttk.Button(root, text = 'Save to CSV', command = lambda: save1(dfs_final[0]))
btn_save1.grid(row=6, column=1, pady=10)
btn_save2 = ttk.Button(root, text = 'Save to CSV', command = lambda: save1(dfs_final[1]))
btn_save2.grid(row=6, column=2, pady=10)

#row7
def template():
        fln = filedialog.asksaveasfile(initialdir=getcwd(), title="Generate Template",
                                filetypes = (('csv files', '*.csv'), ('All Files', '*.*')),
                                initialfile = 'invoices',
                                defaultextension=".csv")
        with open(fln.name, mode='w', newline='') as myfile:
            exp_writer = writer(myfile, delimiter=',')
            exp_writer.writerow(['Invoice','Value'])
        return None
btn_template = ttk.Button(root, text = 'Template', command = template)
btn_template.grid(row=7, column=0, pady=10)

exit = Button(root, text = "Exit Program", command=root.destroy)
exit.grid(row=7, column=20)
root.mainloop()
