import PySimpleGUI as sg
import funcs
import plotting
import json
import time
from PIL import Image, ImageTk


case_stats = "case_stats_n"
case_lib = "case_lib_n"
tot = "tot_n"

headings = ["Name","Amount","Market Value (€)","Inventory Value (€)","Diff from last (%)"]
case_table_info = []
version = "v1.0"
add = ""


layout = [
    [sg.Text(f"Case Storage Manager {version} {add}")],
    [sg.Button("Display Case Inventory", tooltip='Click on a case!', key = "displayButton"),sg.Text("Current TIV: --", key = "tivText"),sg.Button("Refresh", key = "tivButton"),sg.Text("Both Operations take about 15s.")],
    [sg.Table(values=case_table_info,headings = headings, auto_size_columns = False, justification = "middle", key = "Table", row_height = 35,enable_events=True), sg.Image("defaultcase_qm.png",key="-IMAGE-")],
    [sg.Button("Add Case", key="addButton", tooltip="Check whether your case already exists!"),sg.Input(key = "addInput"),sg.Input(key = "addInput2")],
    [sg.Text("Input Case Name and CSGO Stash Link"), sg.Text("", key="AddConfirmation")],
    [sg.Button("Remove Case", key="removeButton",tooltip="Case Name exactly as in Inventory List!"),sg.Input(key = "removeInput")],
    [sg.Text("Input Case Name"), sg.Text("", key="RemoveInfo")],
    [sg.Button("Update Amount", key="amountUpdate", tooltip='Refresh after Updating!'),sg.Input(key = "caseAmount"),sg.Input(key = "amountAmount")],
    [sg.Text("Input Case Name and Amount to change to")],
    [sg.Button("Display Barchart", key="barchart"),sg.Button("Display Pieplot", key="pieplot"),sg.Spin(["1","2","3","4","5","6"], key="spinnerPie"),sg.Button("Display TIV over Time", key="tot"),sg.Spin(["1","2","3","4","5","6"],key="spinnerLine")]
]

window = sg.Window("Case Storage Manager", layout)

while True:

    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

    if event == "tivButton":
        tiv = funcs.get_total_inv_value()
        updatetext = "Current TIV: " + str(round(tiv,2)) + " €"
        window['tivText'].update(updatetext)

    if event == "displayButton":
        allinfo = funcs.get_all_info()
        case_table_info = []
        if window["displayButton"].get_text() == "Display Case Inventory":
            f = open(case_stats, "r")
            data = json.load(f)
            for case in allinfo:
                am = case["amount"]
                pr = funcs.price_from_website(case["link"])
                try:
                    rel_diff = str(round(100*(data["dates"][-1][case["name"]] - data["dates"][-2][case["name"]]) / data["dates"][-2][case["name"]],2))
                except:
                    if am == 0:
                        rel_diff = 0.0
                case_table_info.append([case["name"],str(am),str(pr),str(round(pr * am,2)),rel_diff])
            window["Table"].update(case_table_info)
            window["displayButton"].update("Hide Case Inventory")
            f.close()
        else:
            window["displayButton"].update("Display Case Inventory")
            case_table_info = []
            window["Table"].update(case_table_info)
            window['-IMAGE-'].update("defaultcase_qm.png")

    if event == "addButton":
        if values["addInput"] != "":
            case_to_add = values["addInput"]
            link_to_add = values["addInput2"]
            funcs.add_case(case_to_add, 0, link_to_add)
            sg.Popup(f"{case_to_add} succesfully added!")

    if event == "removeButton":
        case = values["removeInput"]
        deletion = funcs.delete_case(case)
        if deletion:
            sg.Popup(f"{case} succesfully deleted!")
        else:
            sg.Popup(f"{case} does not exist in the database.")

    if event == "amountUpdate":
        case = values["caseAmount"]
        amount = int(values["amountAmount"])
        funcs.alter_amount(case, amount)
        sg.Popup(f"{case} succesfully updated!")

    if event == "pieplot":
        cutoff = int(values["spinnerPie"])
        plotting.pieplot(cutoff)

    if event == "barchart":
        plotting.barchart()

    if event == "tot":
        cutoff = int(values["spinnerLine"])
        plotting.plot_tot(cutoff)

    if event == 'Table':
        selected_name = case_table_info[values[event][0]][0]
        img = funcs.get_im_from_site(selected_name)
        window['-IMAGE-'].update(data=img)


window.close()