from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from sqlite3 import *
import pandas as pd
import matplotlib.pyplot as plt

def open_add():
	mw.withdraw()
	aw.deiconify()

def close_add():
	aw.withdraw()
	mw.deiconify()

def open_view():
	mw.withdraw()
	vw.deiconify()
	vw_st_data.delete(1.0, END)
	info = ""
	con = None
	try:
		con = connect("emp.db")
		cursor = con.cursor()
		sql = "select * from emp"
		cursor.execute(sql)
		data = cursor.fetchall()
		for d in data:
			info = info + " Id = " + str(d[0]) + "  Name = " + str(d[1]) + "  Salary = " + str(d[2]) + "\n"
		vw_st_data.insert(INSERT, info)
	except Exception as e:
		showerror("issue", e)
	finally:
		if con is not None:
			con.close()

def close_view():
	vw.withdraw()
	mw.deiconify()

def open_charts():
	con = None
	try:
		con = connect("emp.db")
		cursor = con.cursor()
		sql = "select name, salary from emp"
		data = pd.read_sql(sql, con)
		plt.bar(data.name, data.salary)
		plt.title("Performance")
		plt.show()
		con.commit()
	except Exception as e:
		showerror("issue", e)
		con.rollback()
	finally:
		if con is not None:
			con.close()

def insert_record():
	check_counter=0
	if aw_ent_id.get() == "":
		showerror("Error", "Id can't be empty")
	else:
		check_counter += 1

	if int(aw_ent_id.get()) < 0:
		showerror("Error", "Id should be positive only")
	else:
		check_counter += 1
	        
	if aw_ent_name.get() == "":
		showerror("Error", "Name can't be empty")
	else:
		check_counter += 1
	
	if (aw_ent_name.get() >="a" and aw_ent_name.get() <="z") or (aw_ent_name.get() >="A" and aw_ent_name.get() <= "z"):
		check_counter += 1
	else:
		showerror("Error", "Name should contain only alphabets")

	if len(aw_ent_name.get()) < 2:
		showerror("Error", "Name should contain min 2 letters")
	else:
		check_counter += 1

	if aw_ent_salary.get() == "":
		showerror("Error", "Salary can't be empty")
	else:
		check_counter += 1

	if float(aw_ent_salary.get()) < 8000:
		showerror("Error", "Salary should be at least 8000")
	else:
		check_counter += 1
  
	if check_counter == 7:        
		try:
			con = connect("emp.db")
			cursor = con.cursor()
			sql = "insert into emp values ('%d','%s','%f')"
			id = int(aw_ent_id.get())
			name = aw_ent_name.get()
			salary = float(aw_ent_salary.get())
			cursor.execute(sql%(id, name, salary))
			con.commit()
			showinfo("Success", "Record Added")
		except Exception as e:
			showerror("issue", e)
			con.rollback()
		finally:
			if con is not None:
				con.close()
		aw_ent_id.delete(0, END)
		aw_ent_name.delete(0, END)
		aw_ent_salary.delete(0, END)

def update_record():
	check_counter=0
	if uw_ent_id.get() == "":
		showerror("Error", "Id can't be empty")
	else:
		check_counter += 1

	if int(uw_ent_id.get()) < 0:
		showerror("Error", "Id should be positive only")
	else:
		check_counter += 1
        
	if uw_ent_name.get() == "":
		showerror("Error", "Name can't be empty")
	else:
		check_counter += 1

	if (uw_ent_name.get() >="a" and uw_ent_name.get() <="z") or (uw_ent_name.get() >="A" and uw_ent_name.get() <= "z"):
		check_counter += 1
	else:
		showerror("Error", "Name should contain only alphabets")

	if len(uw_ent_name.get()) < 2:
		showerror("Error", "Name should contain min 2 letters")
	else:
		check_counter += 1

	if uw_ent_salary.get() == "":
		showerror("Error", "Salary can't be empty")
	else:
		check_counter += 1

	if float(uw_ent_salary.get()) < 8000:
		showerror("Error", "Salary should be at least 8000")
	else:
		check_counter += 1
  
	if check_counter == 7:        
		try:
			con = connect("emp.db")
			cursor = con.cursor()
			sql = "update emp set name= '%s', salary = '%f' where id= '%d' "
			id = int(uw_ent_id.get())
			name = uw_ent_name.get()
			salary = float(uw_ent_salary.get())
			cursor.execute(sql % (name, salary, id))
			if cursor.rowcount == 1:
				con.commit()
				showinfo("Success", "Record Updated")
			else:
				showerror("Error", "Id Does Not Exists")
		except ValueError:
			showerror("Error", "Invalid Input")
			con.rollback()
		except Exception as e:
			showerror("issue", e)
			con.rollback()
		finally:
			if con is not None:
				con.close()
		uw_ent_id.delete(0, END)
		uw_ent_name.delete(0, END)
		uw_ent_salary.delete(0, END)


def close_update():
	uw.withdraw()
	mw.deiconify()

def open_update():
	mw.withdraw()
	uw.deiconify()

def open_delete():
	mw.withdraw()
	dw.deiconify()

def close_delete():
	dw.withdraw()
	mw.deiconify()

def delete_record():
	con = None
	try:
		con = connect("emp.db")
		cursor = con.cursor()
		sql = "delete from emp where id = '%d' "
		id = int(dw_ent_id.get())
		cursor.execute(sql % (id))
		if cursor.rowcount == 1:
			con.commit()
			showinfo("Success", "Record Deleted")
		else:
			showerror("Error", "Id Does Not Exists")
	except ValueError:
		showerror("Error", "Id should be integer only")
		con.rollback()
	except Exception as e:
		showerror("issue", e)
		con.rollback()
	finally:
		if con is not None:
			con.close()
	dw_ent_id.delete(0, END)
		
mw = Tk()
mw.title("E.M.S")
mw.geometry("600x600+100+100")

f = ("Curlz MT", 20, "bold")
y = 10
mw_btn_add = Button(mw, text = "Add", font = f, command = open_add)
mw_btn_view = Button(mw, text = "View", font = f, command = open_view)
mw_btn_update = Button(mw, text = "Update", font = f, command = open_update)
mw_btn_delete = Button(mw, text = "Delete", font = f, command = open_delete)
mw_btn_charts = Button(mw, text = "Charts", font = f, command = open_charts)
mw_btn_add.pack(pady = y)
mw_btn_view.pack(pady = y)
mw_btn_update.pack(pady = y)
mw_btn_delete.pack(pady = y)
mw_btn_charts.pack(pady = y)

aw = Toplevel(mw)
aw.title("Add Emp")
aw.geometry("600x600+100+100")

aw_lab_id = Label(aw, text = "Enter Id:", font = f)
aw_ent_id = Entry(aw, bd = 4, font = f)
aw_lab_name = Label(aw, text = "Enter Name:", font = f)
aw_ent_name = Entry(aw, bd = 4, font = f)
aw_lab_salary = Label(aw, text = "Enter Salary:", font = f)
aw_ent_salary = Entry(aw, bd = 4, font = f)
aw_btn_save = Button(aw, text = "Save", font = f, command = insert_record)
aw_btn_back = Button(aw, text = "Back", font = f, command = close_add)

aw_lab_id.pack(pady = y)
aw_ent_id.pack(pady = y)
aw_lab_name.pack(pady = y)
aw_ent_name.pack(pady = y)
aw_lab_salary.pack(pady = y)
aw_ent_salary.pack(pady = y)
aw_btn_save.pack(pady = y)
aw_btn_back.pack(pady = y)
aw.withdraw()

vw = Toplevel(mw)
vw.title("View Emp")
vw.geometry("600x600+100+100")

vw_st_data = ScrolledText(vw, width = 50, height = 10, font = f)
vw_btn_back = Button(vw, text = "Back", font = f, command = close_view)
vw_st_data.pack(pady = y)
vw_btn_back.pack(pady = y)
vw.withdraw()

uw = Toplevel(mw)
uw.title("Update Emp")
uw.geometry("600x600+100+100")

uw_lab_id = Label(uw, text = "Enter Id:", font = f)
uw_ent_id = Entry(uw, bd = 4, font = f)
uw_lab_name = Label(uw, text = "Enter Name:", font = f)
uw_ent_name = Entry(uw, bd = 4, font = f)
uw_lab_salary = Label(uw, text = "Enter Salary:", font = f)
uw_ent_salary = Entry(uw, bd = 4, font = f)
uw_btn_save = Button(uw, text = "Save", font = f, command = update_record)
uw_btn_back = Button(uw, text = "Back", font = f, command = close_update)

uw_lab_id.pack(pady = y)
uw_ent_id.pack(pady = y)
uw_lab_name.pack(pady = y)
uw_ent_name.pack(pady = y)
uw_lab_salary.pack(pady = y)
uw_ent_salary.pack(pady = y)
uw_btn_save.pack(pady = y)
uw_btn_back.pack(pady = y)
uw.withdraw()

dw = Toplevel(mw)
dw.title("Delete Emp")
dw.geometry("600x600+100+100")

dw_lab_id = Label(dw, text = "Enter Id:", font = f)
dw_ent_id = Entry(dw, bd = 4, font = f)
dw_btn_save = Button(dw, text = "Save", font = f, command = delete_record)
dw_btn_back = Button(dw, text = "Back", font = f, command = close_delete)

dw_lab_id.pack(pady = y)
dw_ent_id.pack(pady = y)
dw_btn_save.pack(pady = y)
dw_btn_back.pack(pady = y)
dw.withdraw()


mw.mainloop()