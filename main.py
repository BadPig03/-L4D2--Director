import _thread
import atexit
import ctypes
import os
import re
import time
import tkinter
import tuples
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

import downloader
import utils

# 定义Director目前的版本号
__version__ = 'v0.1.4-alpha'


# 定义Window类
class Window(tkinter.Tk):
    def __init__(self):
        tkinter.Tk.__init__(self)
        self.title('Director by ty')
        self.geometry('1280x720')
        self.resizable(False, False)
        self.configure(bg='white')
        self.iconphoto(True, tkinter.PhotoImage(file='icon_small.png'))
        scale_factor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100
        if scale_factor == 1.24:
            self.tk.call('tk', 'scaling', self.tk.call('tk', 'scaling') / scale_factor)


# 定义修改可移动点实体种类的Toplevel类
class EntityWindow(tkinter.Toplevel):
    def __init__(self):
        tkinter.Toplevel.__init__(self)

        def destroy_window(window):
            window.destroy()

        index_list = [0, 0]
        self.title('设置点实体类型白名单')
        self.geometry('1120x632')
        self.resizable(False, False)
        self.focus_force()
        app.attributes('-disabled', True)
        self.move_frame = tkinter.LabelFrame(self, text='设置类型', font=('DengXian', 10))
        self.move_frame.place(relx=0.01, rely=0.01, relwidth=0.88, relheight=0.98)
        page_targetname.move_button.configure(state='disabled')
        ttk.Button(self, text='保存', command=lambda: destroy_window(self), width=10).place(relx=0.9045, rely=0.9)
        for name in move_criteria.items():
            if index_list[0] <= 23:
                ttk.Checkbutton(self.move_frame, text=name[0], variable=name[1]).grid(row=index_list[0], column=index_list[1], sticky='w', padx=1, pady=1)
                index_list[0] += 1
            else:
                index_list[0] = 0
                index_list[1] += 1
        page_targetname.move_button.wait_window(self)
        app.attributes('-disabled', False)
        page_targetname.move_button.configure(state='normal')
        app.focus_force()


# 定义选择脚本文件的Toplevel类
class ScriptWindow(tkinter.Toplevel):
    def __init__(self):
        tkinter.Toplevel.__init__(self)

        def choose_script_files(window):
            global script_file_path_list
            script_file_path_list = tkinter.filedialog.askopenfilenames(filetypes=[('NUT File', '*.nut')])
            window.text_box.configure(state='normal')
            window.text_box.delete('1.0', 'end')
            for script_file_path in script_file_path_list:
                window.text_box.insert('insert', '%s\n' % script_file_path)
            window.text_box.configure(state='disabled')
            script_string_var.set('(已选择%s个脚本文件)' % len(script_file_path_list))
            window.focus_force()

        def destroy_window(window):
            window.destroy()

        global script_file_path_list
        self.title('选择脚本文件')
        self.geometry('1000x600')
        self.resizable(False, False)
        self.focus_force()
        app.attributes('-disabled', True)
        self.file_frame = tkinter.LabelFrame(self, text='选择文件', font=('DengXian', 10))
        self.file_frame.place(relx=0.01, rely=0.01, relwidth=0.86, relheight=0.98)
        self.scrollbar_v = tkinter.Scrollbar(self.file_frame)
        self.scrollbar_v.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.scrollbar_h = tkinter.Scrollbar(self.file_frame, orient='horizontal')
        self.scrollbar_h.pack(side=tkinter.BOTTOM, fill=tkinter.X)
        self.text_box = tkinter.Text(self.file_frame, font=('Calibri', 12), wrap='none')
        self.text_box.pack(expand=tkinter.YES, fill=tkinter.BOTH)
        self.text_box.configure(xscrollcommand=self.scrollbar_h.set)
        self.text_box.configure(yscrollcommand=self.scrollbar_v.set)
        self.scrollbar_v.configure(command=self.text_box.yview)
        self.scrollbar_h.configure(command=self.text_box.xview)
        for script_path in script_file_path_list:
            self.text_box.insert('insert', '%s\n' % script_path)
        self.text_box.configure(state='disabled')
        page_targetname.script_select_button.configure(state='disabled')
        ttk.Button(self, text='选择文件', command=lambda: choose_script_files(self), width=10).place(relx=0.89, rely=0.83)
        ttk.Button(self, text='保存', command=lambda: destroy_window(self), width=10).place(relx=0.89, rely=0.9)
        page_targetname.script_select_button.wait_window(self)
        app.attributes('-disabled', False)
        page_targetname.script_select_button.configure(state='normal')
        app.focus_force()


# 定义选择黑名单文件的Toplevel类
class BlacklistWindow(tkinter.Toplevel):
    def __init__(self):
        tkinter.Toplevel.__init__(self)

        def destroy_window(window):
            global blacklist_string
            global blacklist_list
            temp_string = self.text_box.get('1.0', 'end')
            temp_list = utils.string_to_list(temp_string)
            if temp_string != '':
                blacklist_string = temp_string
                for item in temp_list:
                    if item in blacklist_list:
                        pass
                    else:
                        blacklist_list.append(item)
                for item in blacklist_list:
                    if item in temp_list:
                        pass
                    else:
                        blacklist_list.remove(item)
            window.destroy()

        global blacklist_string
        self.title('修改黑名单')
        self.geometry('1000x600')
        self.resizable(False, False)
        self.focus_force()
        app.attributes('-disabled', True)
        self.file_frame = tkinter.LabelFrame(self, text='修改黑名单', font=('DengXian', 10))
        self.file_frame.place(relx=0.01, rely=0.01, relwidth=0.86, relheight=0.98)
        self.scrollbar_v = tkinter.Scrollbar(self.file_frame)
        self.scrollbar_v.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.scrollbar_h = tkinter.Scrollbar(self.file_frame, orient='horizontal')
        self.scrollbar_h.pack(side=tkinter.BOTTOM, fill=tkinter.X)
        self.text_box = tkinter.Text(self.file_frame, font=('Calibri', 12), wrap='none')
        self.text_box.pack(expand=tkinter.YES, fill=tkinter.BOTH)
        self.text_box.configure(xscrollcommand=self.scrollbar_h.set)
        self.text_box.configure(yscrollcommand=self.scrollbar_v.set)
        self.text_box.insert('insert', '%s' % blacklist_string)
        self.scrollbar_v.configure(command=self.text_box.yview)
        self.scrollbar_h.configure(command=self.text_box.xview)
        page_targetname.blacklist_select_button.configure(state='disabled')
        ttk.Button(self, text='保存', command=lambda: destroy_window(self), width=10).place(relx=0.89, rely=0.9)
        page_targetname.blacklist_select_button.wait_window(self)
        app.attributes('-disabled', False)
        page_targetname.blacklist_select_button.configure(state='normal')
        app.focus_force()


# 定义救援脚本输入文本的Toplevel类
class ScriptInputWindow(tkinter.Toplevel):
    def __init__(self, title_text, size, text, button, dict_type):
        tkinter.Toplevel.__init__(self)

        def destroy_window(name, window):
            rescue_text[name] = window.text_box.get()
            window.destroy()

        self.title(title_text)
        self.geometry(size)
        self.resizable(False, False)
        self.focus_force()
        app.attributes('-disabled', True)
        button.configure(state='disabled')
        tkinter.Label(self, text=text, font=('DengXian', 12)).place(relx=0.02, rely=0.1)
        self.text_box = ttk.Entry(self, width=70, font=('DengXian', 12))
        self.text_box.pack(side='bottom', pady=5)
        ttk.Button(self, text='保存', command=lambda: destroy_window(dict_type, self), width=10).pack(side='bottom', pady=5)
        button.wait_window(self)
        app.attributes('-disabled', False)
        button.configure(state='normal')
        app.focus_force()


# 定义选择救援脚本阶段的Toplevel类
class StageWindow(tkinter.Toplevel):
    def __init__(self):
        tkinter.Toplevel.__init__(self)

        def anti_closing():
            pass

        def destroy_window(window):
            global update_rescue_stage_flag
            for list_index in range(1, int(rescue_text['stage_number']) + 1):
                if utils.is_text_valid(rescue_combobox_list[list_index].get(), rescue_entry_list[list_index].get()):
                    if rescue_combobox_list[list_index].get() == 'SCRIPTED':
                        rescue_value_dict[list_index] = rescue_combobox_list[list_index].get() + '\x1b' + utils.standardized_scripted(rescue_entry_list[list_index].get())
                    else:
                        rescue_value_dict[list_index] = rescue_combobox_list[list_index].get() + '\x1b' + rescue_entry_list[list_index].get()
                else:
                    messagebox.showerror('错误', '不合理的内容！')
                    self.focus_force()
                    return
            window.destroy()
            app.after(10, update_rescue_box)
            update_rescue_stage_flag = True

        if int(rescue_text['stage_number']) >= 16:
            return
        rescue_combobox_list.clear()
        rescue_entry_list.clear()
        rescue_value_dict.clear()
        update_rescue_stage_flag = False
        self.title('救援阶段详细设置')
        self.geometry('450x%s' % utils.get_window_y_size(rescue_text['stage_number']))
        self.resizable(False, False)
        self.focus_force()
        app.attributes('-disabled', True)
        page_rescue.stage_button.configure(state='disabled')
        ttk.Button(self, text='保存', command=lambda: destroy_window(self), width=10).grid(columnspan=3, column=0, row=int(rescue_text['stage_number']) + 1, padx=5, pady=5)
        for index in range(1, int(rescue_text['stage_number']) + 1):
            tkinter.Label(self, text='阶段 %s: ' % str(index).zfill(2), font=('DengXian', 12)).grid(column=0, row=index - 1, padx=5, pady=5, sticky='w')
            combobox = ttk.Combobox(self, width=12, state='readonly', textvariable=tkinter.StringVar())
            combobox['values'] = tuples.rescue_type_list
            combobox.current(0)
            combobox.grid(column=1, row=index - 1, padx=5, pady=5)
            entry = ttk.Entry(self, width=31, font=('DengXian', 12))
            entry.grid(column=2, row=index - 1, padx=5, pady=5)
            rescue_combobox_list[index] = combobox
            rescue_entry_list[index] = entry
        self.protocol('WM_DELETE_WINDOW', anti_closing)
        page_rescue.stage_button.wait_window(self)
        app.attributes('-disabled', False)
        page_rescue.stage_button.configure(state='normal')
        app.focus_force()


# 初始化窗口并定义notebook变量和style
app = Window()
notebook = ttk.Notebook(app)
page_targetname = tkinter.Frame(app)
page_second = tkinter.Frame(app)
page_third = tkinter.Frame(app)
page_resources = tkinter.Frame(app)
page_rescue = tkinter.Frame(app)
page_options = tkinter.Frame(app)
page_update = tkinter.Frame(app)
style = ttk.Style(app)
style.theme_settings('xpnative', settings={
    'TLabel': {'configure': {'font': ('DengXian', 12)}},
    'TCheckbutton': {'configure': {'font': ('DengXian', 12)}},
    'TButton': {'configure': {'font': ('DengXian', 12)}},
    'TEntry': {'configure': {'font': ('DengXian', 10)}},
    'TNotebook': {'configure': {'background': 'white', 'font': ('DengXian', 12)}},
    'TNotebook.Tab': {'configure': {'font': ('DengXian', 12)}}})
style.theme_use('xpnative')

# 定义需要使用到的tkinter variables
move_checkbutton_flag = tkinter.IntVar()
script_checkbutton_flag = tkinter.IntVar()
log_checkbutton_flag = tkinter.IntVar()
blacklist_checkbutton_flag = tkinter.IntVar()
msg_checkbutton_flag = tkinter.IntVar()
prohibit_bosses_checkbutton_flag = tkinter.IntVar()
qc_nop4_checkbutton_flag = tkinter.IntVar()
script_string_var = tkinter.StringVar()
script_string_var.set('')
blacklist_string = ''

# 定义需要使用到的boolean
update_rescue_stage_flag = True

# 定义需要使用到的list
blacklist_list = []
script_file_path_list = []

# 定义需要使用到的dict
move_criteria = {'ai_speechfilter': tkinter.IntVar(value=1), 'ambient_music': tkinter.IntVar(value=1), 'color_correction': tkinter.IntVar(value=1), 'env_credits': tkinter.IntVar(value=1), 'env_detail_controller': tkinter.IntVar(value=1),
                 'env_dof_controller': tkinter.IntVar(value=1), 'env_effectscript': tkinter.IntVar(value=1), 'env_fade': tkinter.IntVar(value=1), 'env_fog_controller': tkinter.IntVar(value=1), 'env_global': tkinter.IntVar(value=1),
                 'env_hudhint': tkinter.IntVar(value=1), 'env_message': tkinter.IntVar(value=1), 'env_outtro_stats': tkinter.IntVar(value=1), 'env_particle_performance_monitor': tkinter.IntVar(value=1),
                 'env_particlescript': tkinter.IntVar(value=1), 'env_player_surface_trigger': tkinter.IntVar(value=1), 'env_screeneffect': tkinter.IntVar(value=1), 'env_screenoverlay': tkinter.IntVar(value=1),
                 'env_texturetoggle': tkinter.IntVar(value=1), 'env_tonemap_controller': tkinter.IntVar(value=1), 'env_tonemap_controller_ghost': tkinter.IntVar(value=1), 'env_tonemap_controller_infected': tkinter.IntVar(value=1),
                 'env_wind': tkinter.IntVar(value=1), 'env_zoom': tkinter.IntVar(value=1), 'filter_activator_class': tkinter.IntVar(value=1), 'filter_activator_context': tkinter.IntVar(value=1),
                 'filter_activator_infected_class': tkinter.IntVar(value=1), 'filter_activator_mass_greater': tkinter.IntVar(value=1), 'filter_activator_model': tkinter.IntVar(value=1), 'filter_activator_name': tkinter.IntVar(value=1),
                 'filter_activator_team': tkinter.IntVar(value=1), 'filter_damage_type': tkinter.IntVar(value=1), 'filter_health': tkinter.IntVar(value=1), 'filter_melee_damage': tkinter.IntVar(value=1),
                 'filter_multi': tkinter.IntVar(value=1), 'func_timescale': tkinter.IntVar(value=1), 'game_end': tkinter.IntVar(value=1), 'game_gib_manager': tkinter.IntVar(value=1), 'game_player_equip': tkinter.IntVar(value=1),
                 'game_player_team': tkinter.IntVar(value=1), 'game_ragdoll_manager': tkinter.IntVar(value=1), 'game_scavenge_progress_display': tkinter.IntVar(value=1), 'game_score': tkinter.IntVar(value=1),
                 'game_text': tkinter.IntVar(value=1), 'game_weapon_manager': tkinter.IntVar(value=1), 'hammer_updateignorelist': tkinter.IntVar(value=1), 'info_camera_link': tkinter.IntVar(value=1),
                 'info_director': tkinter.IntVar(value=1), 'info_gamemode': tkinter.IntVar(value=1), 'info_map_parameters': tkinter.IntVar(value=1), 'info_map_parameters_versus': tkinter.IntVar(value=1),
                 'info_no_dynamic_shadow': tkinter.IntVar(value=1), 'light_directional': tkinter.IntVar(value=1), 'light_environment': tkinter.IntVar(value=1), 'logic_active_autosave': tkinter.IntVar(value=1),
                 'logic_auto': tkinter.IntVar(value=1), 'logic_autosave': tkinter.IntVar(value=1), 'logic_branch': tkinter.IntVar(value=1), 'logic_branch_listener': tkinter.IntVar(value=1), 'logic_case': tkinter.IntVar(value=1),
                 'logic_choreographed_scene': tkinter.IntVar(value=1), 'logic_collision_pair': tkinter.IntVar(value=1), 'logic_compare': tkinter.IntVar(value=1), 'logic_director_query': tkinter.IntVar(value=1),
                 'logic_game_event': tkinter.IntVar(value=1), 'logic_multicompare': tkinter.IntVar(value=1), 'logic_navigation': tkinter.IntVar(value=1), 'logic_playerproxy': tkinter.IntVar(value=1), 'logic_relay': tkinter.IntVar(value=1),
                 'logic_scene_list_manager': tkinter.IntVar(value=1), 'logic_script': tkinter.IntVar(value=1), 'logic_timer': tkinter.IntVar(value=1), 'logic_versus_random': tkinter.IntVar(value=1),
                 'material_modify_control': tkinter.IntVar(value=1), 'math_colorblend': tkinter.IntVar(value=1), 'math_counter': tkinter.IntVar(value=1), 'math_remap': tkinter.IntVar(value=1),
                 'phys_constraintsystem': tkinter.IntVar(value=1), 'phys_convert': tkinter.IntVar(value=1), 'phys_keepupright': tkinter.IntVar(value=1), 'player_speedmod': tkinter.IntVar(value=1),
                 'player_weaponstrip': tkinter.IntVar(value=1), 'point_angularvelocitysensor': tkinter.IntVar(value=1), 'point_bonusmaps_accessor': tkinter.IntVar(value=1), 'point_broadcastclientcommand': tkinter.IntVar(value=1),
                 'point_clientcommand': tkinter.IntVar(value=1), 'point_gamestats_counter': tkinter.IntVar(value=1), 'point_posecontroller': tkinter.IntVar(value=1), 'point_servercommand': tkinter.IntVar(value=1),
                 'point_surroundtest': tkinter.IntVar(value=1), 'point_template': tkinter.IntVar(value=1), 'point_velocitysensor': tkinter.IntVar(value=1), 'postprocess_controller': tkinter.IntVar(value=1),
                 'shadow_control': tkinter.IntVar(value=1), 'sound_mix_layer': tkinter.IntVar(value=1), 'tanktrain_ai': tkinter.IntVar(value=1), 'target_changegravity': tkinter.IntVar(value=1), 'vgui_screen': tkinter.IntVar(value=1),
                 'vgui_slideshow_display': tkinter.IntVar(value=1), 'water_lod_control': tkinter.IntVar(value=1)}
paths_dict = {'move_coordinate': '', 'vmf_path': '', 'dict_path': '', 'game_path': '', 'rescue_path': '', 'qc_dir_path': '', 'qc_output_path': ''}
rescue_text = {'msg': '', 'stage_number': '0'}
entities_dict = {}
move_entities_dict = {}
rescue_value_dict = {}
rescue_combobox_list = {}
rescue_entry_list = {}


# 作用：在程序正常退出时保存entry、checkbutton、text等内容，以便下次启动程序时可以使用上次的设置
# 注意：配置文件储存在Appdata\Roaming\Director\director.ini里
def exit_save():
    temp_string = ['', '', '']
    with open(os.getenv('APPDATA') + '\\Director\\director.ini', mode='w', encoding='utf-8') as settings_log:
        settings_log.write('move_coordinate = %s\n' % paths_dict['move_coordinate'].replace('\n', ''))
        settings_log.write('move_checkbutton_flag = %s\n' % move_checkbutton_flag.get())
        settings_log.write('script_checkbutton_flag = %s\n' % script_checkbutton_flag.get())
        settings_log.write('log_checkbutton_flag = %s\n' % log_checkbutton_flag.get())
        settings_log.write('blacklist_checkbutton_flag = %s\n' % blacklist_checkbutton_flag.get())
        settings_log.write('msg_checkbutton_flag = %s\n' % msg_checkbutton_flag.get())
        settings_log.write('prohibit_bosses_checkbutton_flag = %s\n' % prohibit_bosses_checkbutton_flag.get())
        settings_log.write('vmf_path = %s\n' % paths_dict['vmf_path'].replace('\n', ''))
        settings_log.write('dict_path = %s\n' % paths_dict['dict_path'].replace('\n', ''))
        settings_log.write('game_path = %s\n' % paths_dict['game_path'].replace('\n', ''))
        settings_log.write('rescue_path = %s\n' % paths_dict['rescue_path'].replace('\n', ''))
        settings_log.write('blacklist_list = %s\n' % blacklist_string.replace('\n', '\x1b'))
        settings_log.write('script_file_path_list = ')
        for file_path in script_file_path_list:
            temp_string[1] += (file_path.replace('\n', '') + ' \x1b ')
        settings_log.write(temp_string[1].removesuffix(' \x1b ') + '\n')
        settings_log.write('move_criteria = ')
        for move_item in move_criteria.items():
            temp_string[2] += '%s: %s \x1b ' % (move_item[0], move_item[1].get())
        settings_log.write(temp_string[2].removesuffix(' \x1b '))


# 作用：在vmf文件中寻找可移动点实体并将其hammer id(key)和origin(value)保存进move_entities_dict
# 注意：需要先搜索id后再匹配classname，防止乱套
def get_id_and_origin():
    temp_flag = False
    entity_id = 0
    with open(paths_dict['vmf_path'], mode='r', encoding='utf-8') as vmf_file:
        for move_row in vmf_file:
            if temp_flag is False and re.match('\t\"id\" \"[0-9]*\"', move_row):
                entity_id = move_row.split('\" \"')[1].replace('\"', '').replace('\n', '')
            if temp_flag is False and re.match('\t\"classname\" \".*?\"', move_row):
                entity_classname = move_row.split('\" \"')[1].replace('\"', '').replace('\n', '')
                if entity_classname in move_criteria:
                    if move_criteria[entity_classname].get():
                        temp_flag = True
                    else:
                        continue
                else:
                    continue
            if temp_flag is True and re.match('\t\"origin\" \".*?\"', move_row):
                move_entities_dict[entity_id] = move_row.split('\" \"')[1].replace('\"', '').replace('\n', '')
                temp_flag = False


# 作用：调用选择文件(夹)的窗口并保存其路径
# 注意：无
def select_file(selection_index):
    global script_file_path_list
    match selection_index:
        case 0:
            paths_dict['vmf_path'] = tkinter.filedialog.askopenfilename(filetypes=[('Valve Map Format', '*.vmf')])
            page_options.vmf_box.configure(state='normal')
            page_options.vmf_box.delete(0, 'end')
            page_options.vmf_box.insert(0, paths_dict['vmf_path'])
            page_options.vmf_box.configure(state='readonly')
        case 1:
            paths_dict['dict_path'] = tkinter.filedialog.askopenfilename(filetypes=[('Director Dict File', '*.dict')])
            page_options.dict_box.configure(state='normal')
            page_options.dict_box.delete(0, 'end')
            page_options.dict_box.insert(0, paths_dict['dict_path'])
            page_options.dict_box.configure(state='readonly')
        case 2:
            paths_dict['game_path'] = tkinter.filedialog.askopenfilename(filetypes=[('left4dead2.exe', 'left4dead2.exe')])
            page_options.game_box.configure(state='normal')
            page_options.game_box.delete(0, 'end')
            page_options.game_box.insert(0, paths_dict['game_path'])
            page_options.game_box.configure(state='readonly')
        case 3:
            paths_dict['rescue_path'] = tkinter.filedialog.askopenfilename(filetypes=[('NUT File', '*_finale.nut')])
            page_options.rescue_box.configure(state='normal')
            page_options.rescue_box.delete(0, 'end')
            page_options.rescue_box.insert(0, paths_dict['rescue_path'])
            page_options.rescue_box.configure(state='readonly')
        case 4:
            paths_dict['qc_dir_path'] = tkinter.filedialog.askdirectory()
            page_resources.qc_box.configure(state='normal')
            page_resources.qc_box.delete(0, 'end')
            page_resources.qc_box.insert(0, paths_dict['qc_dir_path'])
            page_resources.qc_box.configure(state='readonly')
            if paths_dict['qc_dir_path'] != '' and paths_dict['qc_output_path'] != '':
                page_resources.qc_compile_button.configure(state='normal')
            else:
                page_resources.qc_compile_button.configure(state='disabled')
        case 5:
            paths_dict['qc_output_path'] = tkinter.filedialog.askdirectory()
            page_resources.qc_output_box.configure(state='normal')
            page_resources.qc_output_box.delete(0, 'end')
            page_resources.qc_output_box.insert(0, paths_dict['qc_output_path'])
            page_resources.qc_output_box.configure(state='readonly')
            if paths_dict['qc_dir_path'] != '' and paths_dict['qc_output_path'] != '':
                page_resources.qc_compile_button.configure(state='normal')
            else:
                page_resources.qc_compile_button.configure(state='disabled')


# 作用：备份脚本文件并替换里面的targetname
# 注意：备份文件的后缀名为.bak
def edit_script_files():
    for script_path in script_file_path_list:
        try:
            os.rename(script_path, '%s.bak' % script_path)
        except OSError:
            if messagebox.askquestion('确认', '检测到.bak备份文件！\n若继续则会删除该备份文件！\n是否继续？') == 'yes':
                os.remove('%s.bak' % script_path)
                os.rename(script_path, '%s.bak' % script_path)
            else:
                return
        finally:
            pass
        with open('%s.bak' % script_path, mode='r', encoding='utf-8') as old_file, open(script_path, mode='w', encoding='utf-8') as new_file:
            for file_row in old_file:
                for entities_item in entities_dict.items():
                    if entities_item[0] in file_row:
                        file_row = file_row.replace(entities_item[0], entities_item[1])
                new_file.write(file_row)


# 作用：按下checkbutton后更新对应的button、box和variables状态
# 注意：所有相关的都会被一同更新
def update_flags():
    if move_checkbutton_flag.get():
        page_targetname.move_box.configure(state='normal')
        page_targetname.move_button.configure(state='normal')
    else:
        page_targetname.move_box.configure(state='disabled')
        page_targetname.move_button.configure(state='disabled')
    if script_checkbutton_flag.get():
        page_targetname.script_select_button.configure(state='normal')
        script_string_var.set('(已选择%s个脚本文件)' % len(script_file_path_list))
    else:
        page_targetname.script_select_button.configure(state='disabled')
        script_string_var.set('')
    if blacklist_checkbutton_flag.get():
        page_targetname.blacklist_select_button.configure(state='normal')
    else:
        page_targetname.blacklist_select_button.configure(state='disabled')
    if msg_checkbutton_flag.get():
        page_rescue.msg_button.configure(state='normal')
    else:
        page_rescue.msg_button.configure(state='disabled')


# 作用：备份vmf并读取所有targetname，生成混淆后的字符串，然后准备混淆targetname
# 注意：备份文件的后缀名为.bak
def do_obfuscate():
    if paths_dict['vmf_path'] == '':
        messagebox.showerror('错误', '请选择文件！')
        return
    if move_checkbutton_flag.get() and not check_coordinate_rationality():
        messagebox.showerror('错误', '不合理的地图坐标！')
        return
    if messagebox.askquestion('确认', '确认要混淆vmf文件吗？\n将会覆盖源文件并创建.bak备份文件！') == 'yes':
        file_path = paths_dict['vmf_path'].replace('\\', '/')
        generate_obfuscate_targetname(open(file_path, mode='r', encoding='utf-8'))
        try:
            os.rename(file_path, '%s.bak' % file_path)
        except OSError:
            if messagebox.askquestion('确认', '检测到.bak备份文件！\n若继续则会删除该备份文件！\n是否继续？') == 'yes':
                os.remove('%s.bak' % file_path)
                os.rename(file_path, '%s.bak' % file_path)
            else:
                return
        finally:
            pass
        with open('%s.bak' % file_path, mode='r', encoding='utf-8') as old_file, open(file_path, mode='w', encoding='utf-8') as new_file:
            replace_string(old_file, new_file, file_path)


# 作用：检查用户输入的坐标是否合理，合理则返回True，反之返回False
# 注意：若合理，会将坐标标准化后储存进paths_dict里
def check_coordinate_rationality():
    if move_checkbutton_flag.get():
        temp_coordinates = page_targetname.move_box.get()
        if re.fullmatch('^(-?[0-9]+)(.[0-9]+)?([^0-9]+)(-?[0-9]+)(.[0-9]+)?([^0-9]+)(-?[0-9]+)(.[0-9]+)?$', temp_coordinates):
            paths_dict['move_coordinate'] = re.sub('[^0-9.-]+', ' ', temp_coordinates)
            return True
        else:
            return False


# 作用：替换vmf里的targetname(包括I/O里的targetname)
# 注意：若勾选了保存混淆字典，会保存targetname一一对应的日志文件
#      若勾选了移动点实体到指定位置，则一并移动可移动点实体到指定位置
def replace_string(old_file, new_file, file_path):
    temp_flag = False
    for old_file_row in old_file:
        if re.search("\"[A-Za-z0-9]+\" \"", old_file_row):
            criteria = re.search("\"[A-Za-z0-9]+\" \"", old_file_row).group()[1:-3]
            if criteria in tuples.replace_criteria:
                for entities_item in entities_dict.items():
                    old_file_row = old_file_row.replace('\"' + criteria + '\" \"' + entities_item[0] + '\"', '\"' + criteria + '\" \"' + entities_item[1] + '\"')
        if re.search("[A-Za-z0-9]+\x1b", old_file_row):
            for entities_item in entities_dict.items():
                old_file_row = old_file_row.replace(entities_item[0] + '\x1b', entities_item[1] + '\x1b')
        if temp_flag is False and re.match('\t\"id\" \"[0-9]*\"', old_file_row):
            entity_id = old_file_row.split('\" \"')[1].replace('\"', '').replace('\n', '')
            if entity_id in move_entities_dict.keys():
                temp_flag = True
            else:
                continue
        if temp_flag is True and re.match('\t\"origin\" \".*?\"', old_file_row):
            old_file_row = '\t\"origin\" \"%s\"\n' % paths_dict['move_coordinate']
            temp_flag = False
        new_file.write(old_file_row)
    if log_checkbutton_flag.get():
        with open('%s.log' % file_path, mode='w', encoding='utf-8') as log_file:
            for entities_item in entities_dict.items():
                log_file.write('%s -> %s\n' % (entities_item[0], entities_item[1]))
            for entities_item in list(set(blacklist_list)):
                log_file.write('%s\n' % entities_item)
            log_file.write('!%s' % time.strftime('%Y-%m-%d %H:%M:%S'))
    messagebox.showinfo('提示', 'vmf已混淆完成！\n.bak备份文件已创建！')


# 作用：生成混淆后的字符串并储存进entities_dict
# 注意：若勾选了移动点实体到指定位置，则同时获取可移动点实体的hammer id
def generate_obfuscate_targetname(file):
    if move_checkbutton_flag.get():
        get_id_and_origin()
    for file_row in file:
        if '*' in file_row:
            blacklist_list.append(file_row.split('*')[0].split('\"')[-1].split('\x1b')[-1])
        if re.findall('\"targetname\" \".*?\"', file_row):
            file_row = file_row.split("\" \"")[1][:-2]
            if not utils.is_startswith_in_list(file_row, blacklist_list):
                entities_dict[file_row] = utils.generate_random_string()


# 作用：更新救援预览内容
# 注意：目前为手动更新
def update_rescue_box():
    global update_rescue_stage_flag
    stage_number = rescue_text['stage_number']
    page_rescue.text_box.configure(state='normal')
    page_rescue.text_box.delete('1.0', 'end')
    if msg_checkbutton_flag.get():
        page_rescue.text_box.insert('insert', 'Msg(\"%s\");\n\n' % rescue_text['msg'])
    page_rescue.text_box.insert('insert', 'PANIC <- 0\nTANK <- 1\nDELAY <- 2\nSCRIPTED <- 3\nCLEAROUT <- 4\nSETUP <- 5\nESCAPE <- 7\nRESULTS <- 8\nNONE <- 9\n\nDirectorOptions <-\n{\n')
    if stage_number.isnumeric() and int(stage_number) > 0 and update_rescue_stage_flag:
        page_rescue.text_box.insert('insert', '\tA_CustomFinale_StageCount = %s\n\n' % stage_number)
        for index in range(1, int(stage_number) + 1):
            page_rescue.text_box.insert('insert', '\tA_CustomFinale%s = %s\n' % (index, rescue_value_dict[index].split('\x1b')[0]))
            page_rescue.text_box.insert('insert', '\tA_CustomFinaleValue%s = %s\n\n' % (index, rescue_value_dict[index].split('\x1b')[1]))
    if prohibit_bosses_checkbutton_flag.get():
        page_rescue.text_box.insert('insert', '\tProhibitBosses = true\n')
    page_rescue.text_box.insert('insert', '}\n')
    page_rescue.text_box.configure(state='disabled')


# 作用：自动更新救援预览窗口的内容
# 注意：0.1s递归己函数
def auto_refresh_rescue_window():
    global update_rescue_stage_flag
    rescue_text['stage_number'] = page_rescue.stage_box.get()
    if rescue_text['stage_number'].isnumeric() and 0 < int(rescue_text['stage_number']) < 16:
        page_rescue.stage_button.configure(state='normal')
    else:
        page_rescue.stage_button.configure(state='disable')
    app.after(100, auto_refresh_rescue_window)


# 作用：批量编译qc文件
# 注意：使用多线程方法编译
def walk_through_qc_files(raw_path, mdl_path):
    gameinfo_path = mdl_path.removesuffix('bin/studiomdl.exe') + 'left4dead2/'
    for dir_path, dir_names, file_names in os.walk(raw_path):
        for file_name in file_names:
            if file_name.endswith('.qc'):
                _thread.start_new_thread(os.system, ('""%s" -game "%s" -nop4 "%s/%s""' % (mdl_path, gameinfo_path, dir_path, file_name),))


# 作用：获取Director最新版本并加以比较，输出更新结果
# 注意：若一直尝试获取，会导致短时间被禁止访问
def update_version_check():
    new_version = downloader.get_latest_version()
    if new_version is None:
        return
    if new_version == __version__:
        page_update.update_frame.version_box.configure(state='normal')
        page_update.update_frame.version_box.delete(0, 'end')
        page_update.update_frame.version_box.insert(0, 'Director处于最新版本！')
        page_update.update_frame.version_box.configure(state='readonly')
    elif new_version == 'ERROR':
        page_update.update_frame.version_box.configure(state='normal')
        page_update.update_frame.version_box.delete(0, 'end')
        page_update.update_frame.version_box.insert(0, '网络连接失败！')
        page_update.update_frame.version_box.configure(state='readonly')
    else:
        page_update.update_frame.version_box.configure(state='normal')
        page_update.update_frame.version_box.delete(0, 'end')
        page_update.update_frame.version_box.insert(0, 'Director有新版本可供升级！最新版本号：%s！' % new_version)
        page_update.update_frame.version_box.configure(state='readonly')


# 定义全部tkinter组件
page_targetname.option_frame = tkinter.LabelFrame(page_targetname, text='选项', font=('DengXian', 10))
page_targetname.option_frame.place(relx=0.01, rely=0.01, relwidth=0.48, relheight=0.48)
page_targetname.move_checkbutton = ttk.Checkbutton(page_targetname.option_frame, text='将指定点实体移动到指定位置:', command=lambda: update_flags(), variable=move_checkbutton_flag)
page_targetname.move_checkbutton.grid(column=0, row=0, padx=5, pady=5, sticky='w')
page_targetname.move_box = ttk.Entry(page_targetname.option_frame, width=28, state='readonly', font=('Calibri', 10))
page_targetname.move_box.grid(column=1, row=0, padx=5, pady=5)
page_targetname.move_button = ttk.Button(page_targetname.option_frame, text='指定实体类型', command=lambda: EntityWindow(), width=15)
page_targetname.move_button.grid(column=2, row=0, padx=5)
page_targetname.script_checkbutton = ttk.Checkbutton(page_targetname.option_frame, text='同时对指定脚本文件进行混淆:', command=lambda: update_flags(), variable=script_checkbutton_flag)
page_targetname.script_checkbutton.grid(column=0, row=1, padx=5, pady=5, sticky='w')
page_targetname.text_third = ttk.Label(page_targetname.option_frame, textvariable=script_string_var)
page_targetname.text_third.grid(column=1, row=1, padx=5, pady=5, sticky='w')
page_targetname.script_select_button = ttk.Button(page_targetname.option_frame, text='选择脚本文件', command=lambda: ScriptWindow(), width=15, state='disabled')
page_targetname.script_select_button.grid(column=2, row=1, padx=5, pady=5)
page_targetname.blacklist_checkbutton = ttk.Checkbutton(page_targetname.option_frame, text='启用targetname黑名单', command=lambda: update_flags(), variable=blacklist_checkbutton_flag)
page_targetname.blacklist_checkbutton.grid(column=0, row=2, padx=5, pady=5, sticky='w')
page_targetname.blacklist_select_button = ttk.Button(page_targetname.option_frame, text='修改黑名单', command=lambda: BlacklistWindow(), width=15, state='disabled')
page_targetname.blacklist_select_button.grid(column=2, row=2, padx=5, pady=5)
page_targetname.log_checkbutton = ttk.Checkbutton(page_targetname.option_frame, text='保存混淆字典', command=lambda: update_flags(), variable=log_checkbutton_flag)
page_targetname.log_checkbutton.grid(column=0, row=3, padx=5, pady=5, sticky='w')
page_targetname.execute_button = ttk.Button(page_targetname, text='混淆', command=lambda: do_obfuscate(), width=9)
page_targetname.execute_button.place(relx=0.8, rely=0.83)
page_targetname.test_button = ttk.Button(page_targetname, text='测试', command=lambda: edit_script_files(), width=9)
page_targetname.test_button.place(relx=0.6, rely=0.83)
page_targetname.text_second = tkinter.Label(page_targetname, text='仅用于求生之路2的vmf文件！', font=('DengXian', 12), fg='red')
page_targetname.text_second.place(relx=0.05, rely=0.835)

page_resources.qc_frame = tkinter.LabelFrame(page_resources, text='qc批量编译', font=('DengXian', 10))
page_resources.qc_frame.place(relx=0.005, rely=0.005, relwidth=0.49, relheight=0.24)
ttk.Label(page_resources.qc_frame, text='选择文件夹：').grid(column=0, row=0, padx=5, pady=6, sticky='w')
page_resources.qc_box = ttk.Entry(page_resources.qc_frame, width=62, state='readonly')
page_resources.qc_box.grid(column=1, row=0, padx=5, pady=6)
ttk.Button(page_resources.qc_frame, text='浏览', command=lambda: select_file(4), width=9).grid(column=2, row=0, padx=5, pady=6)
ttk.Label(page_resources.qc_frame, text='选择输出位置：').grid(column=0, row=1, padx=5, pady=6, sticky='w')
page_resources.qc_output_box = ttk.Entry(page_resources.qc_frame, width=62, state='readonly')
page_resources.qc_output_box.grid(column=1, row=1, padx=5, pady=6)
ttk.Button(page_resources.qc_frame, text='浏览', command=lambda: select_file(5), width=9).grid(column=2, row=1, padx=5, pady=6)
page_resources.qc_nop4_checkbutton = ttk.Checkbutton(page_resources.qc_frame, text='-nop4', command=lambda: update_flags(), variable=qc_nop4_checkbutton_flag)
page_resources.qc_nop4_checkbutton.grid(column=0, row=2, padx=5, pady=5, sticky='w')
page_resources.qc_compile_button = ttk.Button(page_resources.qc_frame, text='编译', command=lambda: walk_through_qc_files(paths_dict['qc_dir_path'], paths_dict['game_path'].removesuffix('left4dead2.exe') + 'bin/studiomdl.exe'), width=9, state='disabled')
page_resources.qc_compile_button.grid(column=2, row=3, padx=5, pady=6)

page_rescue.option_necessary_frame = tkinter.LabelFrame(page_rescue, text='必选设置', font=('DengXian', 10))
page_rescue.option_necessary_frame.place(relx=0.005, rely=0.005, relwidth=0.24, relheight=0.09)
ttk.Label(page_rescue.option_necessary_frame, text='救援阶段数:').grid(column=0, row=0, padx=5, pady=5, sticky='w')
page_rescue.stage_box = ttk.Entry(page_rescue.option_necessary_frame, width=6)
page_rescue.stage_box.grid(column=1, row=0, padx=5, pady=5, sticky='w')
page_rescue.stage_button = ttk.Button(page_rescue.option_necessary_frame, text='详细设置', command=lambda: StageWindow(), width=10, state='disabled')
page_rescue.stage_button.grid(column=2, row=0, padx=5, pady=5, sticky='w')
ttk.Button(page_rescue.option_necessary_frame, text='?', command=lambda: messagebox.showinfo('提示', '救援阶段数：救援持续的总波数\n\nPANIC：进入该阶段后刷新尸潮的波数\n\nTANK：进入该阶段后生成Tank的个数\n\nDELAY：进入下一阶段之前等待的秒数\n\nSCRIPTED：进入该阶段时执行的尸潮脚本名字\n\n脚本应直接位于scripts\\vscript文件夹下且不带.nut后缀名'), width=3).grid(column=3, row=0, padx=5, pady=5, sticky='w')
page_rescue.option_additional_frame = tkinter.LabelFrame(page_rescue, text='额外设置', font=('DengXian', 10))
page_rescue.option_additional_frame.place(relx=0.255, rely=0.005, relwidth=0.24, relheight=0.88)
page_rescue.msg_checkbutton = ttk.Checkbutton(page_rescue.option_additional_frame, text='', command=lambda: update_flags(), variable=msg_checkbutton_flag)
page_rescue.msg_checkbutton.grid(column=0, row=0, padx=5, pady=5, sticky='w')
page_rescue.msg_button = ttk.Button(page_rescue.option_additional_frame, text='自定义消息设置', command=lambda: ScriptInputWindow('自定义消息设置', '600x100', '请输入自定义消息内容：', page_rescue.msg_button, 'msg'), width=15)
page_rescue.msg_button.place(x=24, y=3)
page_rescue.prohibit_bosses_checkbutton = ttk.Checkbutton(page_rescue.option_additional_frame, text='禁止Tank与Witch', command=lambda: update_flags(), variable=prohibit_bosses_checkbutton_flag)
page_rescue.prohibit_bosses_checkbutton.grid(column=0, row=1, padx=5, pady=5, sticky='w')
page_rescue.preview_frame = tkinter.LabelFrame(page_rescue, text='预览', font=('DengXian', 10))
page_rescue.preview_frame.place(relx=0.505, rely=0.005, relwidth=0.49, relheight=0.98)
page_rescue.scrollbar_v = tkinter.Scrollbar(page_rescue.preview_frame)
page_rescue.scrollbar_v.pack(side=tkinter.RIGHT, fill=tkinter.Y)
page_rescue.scrollbar_h = tkinter.Scrollbar(page_rescue.preview_frame, orient='horizontal')
page_rescue.scrollbar_h.pack(side=tkinter.BOTTOM, fill=tkinter.X)
page_rescue.text_box = tkinter.Text(page_rescue.preview_frame, font=('DengXian', 12), wrap='none')
page_rescue.text_box.pack(expand=tkinter.YES, fill=tkinter.BOTH)
page_rescue.text_box.configure(xscrollcommand=page_rescue.scrollbar_h.set)
page_rescue.text_box.configure(yscrollcommand=page_rescue.scrollbar_v.set)
page_rescue.scrollbar_v.configure(command=page_rescue.text_box.yview)
page_rescue.scrollbar_h.configure(command=page_rescue.text_box.xview)
ttk.Button(page_rescue, text='更新预览', command=lambda: update_rescue_box(), width=9).place(relx=0.25, rely=0.94, anchor='center')

page_options.option_frame = tkinter.LabelFrame(page_options, text='文件路径', font=('DengXian', 10))
page_options.option_frame.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.48)
ttk.Label(page_options.option_frame, text='vmf文件路径：').grid(column=0, row=0, padx=5, pady=6, sticky='w')
page_options.vmf_box = ttk.Entry(page_options.option_frame, width=165, state='readonly')
page_options.vmf_box.grid(column=1, row=0, padx=5, pady=10)
ttk.Button(page_options.option_frame, text='浏览', command=lambda: select_file(0), width=9).grid(column=2, row=0, padx=5, pady=6)
ttk.Label(page_options.option_frame, text='混淆字典路径：').grid(column=0, row=1, padx=5, pady=6, sticky='w')
page_options.dict_box = ttk.Entry(page_options.option_frame, width=165, state='readonly')
page_options.dict_box.grid(column=1, row=1, padx=5, pady=6)
ttk.Button(page_options.option_frame, text='浏览', command=lambda: select_file(1), width=9).grid(column=2, row=1, padx=5, pady=6)
ttk.Label(page_options.option_frame, text='游戏本体路径：').grid(column=0, row=2, padx=5, pady=6, sticky='w')
page_options.game_box = ttk.Entry(page_options.option_frame, width=165, state='readonly')
page_options.game_box.grid(column=1, row=2, padx=5, pady=6)
ttk.Button(page_options.option_frame, text='浏览', command=lambda: select_file(2), width=9).grid(column=2, row=2, padx=5, pady=6)
ttk.Label(page_options.option_frame, text='救援脚本路径：').grid(column=0, row=3, padx=5, pady=6, sticky='w')
page_options.rescue_box = ttk.Entry(page_options.option_frame, width=165, state='readonly')
page_options.rescue_box.grid(column=1, row=3, padx=5, pady=6)
ttk.Button(page_options.option_frame, text='浏览', command=lambda: select_file(3), width=9).grid(column=2, row=3, padx=5, pady=6)

page_update.update_frame = tkinter.LabelFrame(page_update, text='当前版本：%s' % __version__, font=('DengXian', 10))
page_update.update_frame.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.98)
ttk.Button(page_update.update_frame, text='检查更新', command=lambda: update_version_check(), width=9).grid(column=0, row=1, padx=5, pady=5)
page_update.update_frame.version_box = ttk.Entry(page_update.update_frame, width=94, state='readonly')
page_update.update_frame.version_box.grid(column=1, row=1, pady=5)
ttk.Button(page_update.update_frame, text='手动更新', state='disabled', command=lambda: update_version_check(), width=9).grid(column=2, row=1, padx=5, pady=5)

# notebook里添加新页
notebook.add(page_targetname, text='地图混淆')
notebook.add(page_second, text='贴图')
notebook.add(page_third, text='脚本')
notebook.add(page_resources, text='资源提取器')
notebook.add(page_rescue, text='自定义救援')
notebook.add(page_options, text='路径设置')
notebook.add(page_update, text='版本更新')
notebook.pack(padx=10, pady=5, fill='both', expand=True)

# 作用：初始化时自动读取储存好的配置文件，若没有，则生成新的配置文件
try:
    with open(os.getenv('APPDATA') + '\\Director\\director.ini', mode='a+', encoding='utf-8') as director_settings:
        director_settings.seek(0)
        for row in director_settings:
            if row.startswith('move_coordinate ='):
                paths_dict['move_coordinate'] = row.split(' = ')[1].replace('\n', '')
                page_targetname.move_box.configure(state='normal')
                page_targetname.move_box.insert(0, paths_dict['move_coordinate'])
                page_targetname.move_box.configure(state='readonly')
            if row.startswith('move_checkbutton_flag ='):
                if int(row.split(' = ')[1]) == 1:
                    page_targetname.move_checkbutton.invoke()
            if row.startswith('script_checkbutton_flag ='):
                if int(row.split(' = ')[1]) == 1:
                    page_targetname.script_checkbutton.invoke()
            if row.startswith('log_checkbutton_flag ='):
                if int(row.split(' = ')[1]) == 1:
                    page_targetname.log_checkbutton.invoke()
            if row.startswith('blacklist_checkbutton_flag ='):
                if int(row.split(' = ')[1]) == 1:
                    page_targetname.blacklist_checkbutton.invoke()
            if row.startswith('msg_checkbutton_flag ='):
                if int(row.split(' = ')[1]) == 1:
                    page_rescue.msg_checkbutton.invoke()
            if row.startswith('prohibit_bosses_checkbutton_flag ='):
                if int(row.split(' = ')[1]) == 1:
                    page_rescue.prohibit_bosses_checkbutton.invoke()
            if row.startswith('vmf_path ='):
                paths_dict['vmf_path'] = row.split(' = ')[1].replace('\n', '')
                page_options.vmf_box.configure(state='normal')
                page_options.vmf_box.insert(0, paths_dict['vmf_path'])
                page_options.vmf_box.configure(state='readonly')
            if row.startswith('dict_path ='):
                paths_dict['dict_path'] = row.split(' = ')[1].replace('\n', '')
                page_options.dict_box.configure(state='normal')
                page_options.dict_box.insert(0, paths_dict['dict_path'])
                page_options.dict_box.configure(state='readonly')
            if row.startswith('game_path ='):
                paths_dict['game_path'] = row.split(' = ')[1].replace('\n', '')
                page_options.game_box.configure(state='normal')
                page_options.game_box.insert(0, paths_dict['game_path'])
                page_options.game_box.configure(state='readonly')
            if row.startswith('rescue_path ='):
                paths_dict['rescue_path'] = row.split(' = ')[1].replace('\n', '')
                page_options.rescue_box.configure(state='normal')
                page_options.rescue_box.insert(0, paths_dict['rescue_path'])
                page_options.rescue_box.configure(state='readonly')
            if row.startswith('blacklist_list ='):
                blacklist_string = row.split(' = ')[1].replace('\x1b', '\n')
                blacklist_list = utils.string_to_list(blacklist_string)
            if row.startswith('script_file_path_list ='):
                if row != 'script_file_path_list = \n':
                    for path in row.split(' = ')[1].split(' \x1b '):
                        if path != '':
                            script_file_path_list.append(path)
                    script_string_var.set('(已选择%s个脚本文件)' % len(script_file_path_list))
            if row.startswith('move_criteria = '):
                for move_list in row.split(' = ')[1].split(' \x1b '):
                    move_criteria[move_list.split(': ')[0]] = tkinter.IntVar(value=int(move_list.split(': ')[1]))
            update_flags()
except FileNotFoundError:
    director_settings = open(os.getenv('APPDATA') + '\\Director\\director.ini', mode='x', encoding='utf-8')
    director_settings.close()
finally:
    pass

# 正式执行
atexit.register(exit_save)
app.after(100, auto_refresh_rescue_window)
app.mainloop()
