# -*- coding: utf-8 -*-
"""
Created on Sun Jun 25 20:36:34 2017

@author: pmullapudy
"""
import pywinauto
import time as ti
import pandas as pd

# Declaratoions
clipboard_df = pd.DataFrame()
main_data_df = pd.DataFrame()

#Connect to the application
app = pywinauto.application.Application(backend="uia").connect(title="Scanner: MySignalAPP", auto_id="frmPopoutChart", control_type="Window")
dlg_spec = app.window(title='Scanner: MySignalAPP')
#print (dlg_spec.print_control_identifiers()) # Test this with only 2 or 3 symbols loaded on Scanner
#dlg_spec_wrapper = dlg_spec.wrapper_object() #Actual window lookup is performed by wrapper_object()

#child controls
dlg_ctlScanner = dlg_spec.child_window(auto_id="ctlScanner", control_type="Pane")
dlg_DataGridView = dlg_ctlScanner.child_window(title="DataGridView", auto_id="grdResults", control_type="Table")
dlg_Row_0 = dlg_DataGridView.child_window(title="Row 0", control_type="Custom")
dlg_Trade_Time = dlg_Row_0.child_window(title="Trade Time Row 0", control_type="DataItem")
dlg_Symbol = dlg_Row_0.child_window(title="Symbol Row 0", control_type="DataItem")

dlg_spec.set_focus() # makes the window active.

#print (" the corect wrapper for this UIA element", pywinauto.controls.uiawrapper.UiaMeta.find_wrapper(dlg_spec))
#print ("No of CONTROLS in datagrid view is: ", pywinauto.controls.uia_controls.ListViewWrapper.control_count(dlg_DataGridView))
row_cnt = pywinauto.controls.uia_controls.ListViewWrapper.control_count(dlg_DataGridView) # This includes the header
#row_cnt = len(pywinauto.controls.uia_controls.ListViewWrapper.children_texts(dlg_DataGridView)) # This includes the header

for x in range(0, (row_cnt -1)):
    pywinauto.keyboard.SendKeys('{UP}')
#
#pywinauto.keyboard.SendKeys('{PGUP 10}') # on a 14 inch screen, pressing 10 times on pageup makes it faster if less than 200 stocks are scanned.
pywinauto.controls.uiawrapper.UIAWrapper.draw_outline(dlg_Row_0)
pywinauto.controls.hwndwrapper.HwndWrapper.set_keyboard_focus(dlg_DataGridView)
#
loop_start_time = ti.time()
#
for row_number in range(0, (row_cnt -2)):
    pywinauto.keyboard.SendKeys('^c')
    pywinauto.keyboard.SendKeys('{ENTER}')
    clipboard_df = pd.read_clipboard(header=None)
    main_data_df = main_data_df.append(clipboard_df)
#
main_data_df['Trade Time'] = main_data_df[0] + ' ' + main_data_df[1]
main_data_df['Alert Time'] = main_data_df[5] + ' ' + main_data_df[6]
main_data_df['Trade Time'] =  pd.to_datetime(main_data_df['Trade Time'])
main_data_df['Alert Time'] =  pd.to_datetime(main_data_df['Alert Time'])
main_data_df = main_data_df[['Trade Time',2, 3, 4, 'Alert Time']]
main_data_df.columns = ['Trade Time', 'Symbol', 'Last', 'Volume', 'Alert Time']
main_data_df = main_data_df.reset_index(drop=True)
#
print("------- %s seconds for one full cycle of data retreival & write------" % (ti.time() - loop_start_time) , "@", ti.strftime("%H:%M:%S")) #