import atexit
import re
import os
import tkinter
import time
import _thread
import downloader
import utils
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

__version__ = 'v0.1.3-alpha'

if __name__ != '__main__':
    exit(0)

window = tkinter.Tk()
window.title('Director by ty')
window.geometry('1280x720')
window.resizable(False, False)
window.configure(bg='white')
window.iconphoto(True, tkinter.PhotoImage(file='icon_small.png'))

# messagebox.showinfo('提示', 'vmf混淆器的作用：\n1.将所有实体的targetname重命名为无意义字符串\n2.IO里对应的targetname也会随之更改\n3.(可选)将对位置无要求的点实体移动到指定位置\n4.(可选)将指定脚本文件里的targetname也一并混淆\n5.(可选)保存一个targetname被混淆前后的日志文件')

replace_criteria = ('targetname', 'parentname', 'target', 'PSName', 'SourceEntityName', 'DestinationGroup', 'TemplateName', 'RenameNPC', 'panelname', 'LightningStart', 'LightningEnd', 'filtername', 'ignoredEntity', 'lightingorigin',
                    'LaserTarget', 'directionentityname', 'targetentityname', 'MainSoundscapeName', 'position0', 'position1', 'position2', 'position3', 'position4', 'position5', 'position6', 'position7', 'master', 'ApplyEntity',
                    'referencename', 'm_SourceEntityName', 'cpoint1', 'cpoint2', 'cpoint3', 'cpoint4', 'cpoint5', 'cpoint6', 'cpoint7', 'cpoint8', 'cpoint9', 'cpoint10', 'cpoint11', 'cpoint12', 'cpoint13', 'cpoint14', 'cpoint15',
                    'cpoint16', 'cpoint17', 'cpoint18', 'cpoint19', 'cpoint20', 'cpoint21', 'cpoint22', 'cpoint23', 'cpoint24', 'cpoint25', 'cpoint26', 'cpoint27', 'cpoint28', 'cpoint29', 'cpoint30', 'cpoint31', 'cpoint32', 'cpoint33',
                    'cpoint34', 'cpoint35', 'cpoint36', 'cpoint37', 'cpoint38', 'cpoint39', 'cpoint40', 'cpoint41', 'cpoint42', 'cpoint43', 'cpoint44', 'cpoint45', 'cpoint46', 'cpoint47', 'cpoint48', 'cpoint49', 'cpoint50', 'cpoint51',
                    'cpoint52', 'cpoint53', 'cpoint54', 'cpoint55', 'cpoint56', 'cpoint57', 'cpoint58', 'cpoint59', 'cpoint60', 'cpoint61', 'cpoint62', 'cpoint63', 'globalname', 'slavename', 'NextKey', 'moveto', 'PropName', 'Branch01',
                    'Branch02', 'Branch03', 'Branch04', 'Branch05', 'Branch06', 'Branch07', 'Branch08', 'Branch09', 'Branch10', 'Branch11', 'Branch12', 'Branch13', 'Branch14', 'Branch15', 'Branch16', 'IgnoredName01', 'IgnoredName02',
                    'IgnoredName03', 'IgnoredName04', 'IgnoredName05', 'IgnoredName06', 'IgnoredName07', 'IgnoredName08', 'IgnoredName09', 'IgnoredName10', 'IgnoredName11', 'IgnoredName12', 'IgnoredName13', 'IgnoredName14',
                    'IgnoredName15', 'IgnoredName16', 'attach1', 'attach2', 'SpeakerName', 'ListenFilter', 'source', 'lookatname', 'Filter01', 'Filter02', 'Filter03', 'Filter04', 'Filter05', 'Filter06', 'Filter07', 'Filter08',
                    'Filter09', 'Filter10', 'EntityTemplate', 'Template01', 'Template02', 'Template03', 'Template04', 'Template05', 'Template06', 'Template07', 'Template08', 'Template09', 'Template10', 'Template11', 'Template12',
                    'Template13', 'Template14', 'Template15', 'Template16', 'DamageTarget', 'constraintsystem', 'newtarget', 'damagefilter', 'InitialOwner', 'altpath', 'PointCamera', 'MeasureTarget', 'MeasureReference', 'Target',
                    'TargetReference', 'enemyfilter', 'squadname', 'cameraname', 'spawnpositionname', 'scene0', 'scene1', 'scene2', 'scene3', 'scene4', 'scene5', 'scene6', 'scene7', 'scene8', 'scene9', 'scene10', 'scene11', 'scene12',
                    'scene13', 'scene14', 'scene15', 'target1', 'target2', 'target3', 'target4', 'target5', 'target6', 'target7', 'target8', 'target_entity', 'hint_target', 'nozzle', 'RockTargetName', 'model', 'ColorCorrectionName',
                    'FogName', 'PostProcessName', 'glow', 'train', 'toptrack', 'bottomtrack', 'landmark', 'measuretarget', 'soundscape', 'TonemapName')
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
rescue_text = {'msg': '', 'stage_number': '0'}

move_checkbutton_flag = tkinter.IntVar()
script_checkbutton_flag = tkinter.IntVar()
log_checkbutton_flag = tkinter.IntVar()
wildcard_checkbutton_flag = tkinter.IntVar()
msg_checkbutton_flag = tkinter.IntVar()
prohibit_bosses_checkbutton_flag = tkinter.IntVar()
qc_nop4_checkbutton_flag = tkinter.IntVar()
update_rescue_stage_flag = True

entities_dict = {}
move_entities_dict = {}
rescue_value_dict = {}
rescue_combobox_list = {}
rescue_entry_list = {}
blacklist_list = []
script_file_path_list = []
rescue_type_list = ['PANIC', 'TANK', 'DELAY', 'SCRIPTED', 'CLEAROUT', 'SETUP', 'ESCAPE', 'RESULTS', 'NONE']

script_string_var = tkinter.StringVar()
script_string_var.set('')
move_coordinate = ''
vmf_path = ''
dict_path = ''
game_path = ''
rescue_path = ''
qc_dir_path = ''
qc_output_path = ''

notebook = ttk.Notebook(window)
page_first = tkinter.Frame(window)
page_second = tkinter.Frame(window)
page_third = tkinter.Frame(window)
page_resources = tkinter.Frame(window)
page_rescue = tkinter.Frame(window)
page_options = tkinter.Frame(window)
page_update = tkinter.Frame(window)

style = ttk.Style(window)
style.theme_settings('xpnative', settings={
    'TLabel': {'configure': {'font': ('DengXian', 12)}},
    'TCheckbutton': {'configure': {'font': ('DengXian', 12)}},
    'TButton': {'configure': {'font': ('DengXian', 12)}},
    'TEntry': {'configure': {'font': ('Calibri', 10)}},
    'TNotebook': {'configure': {'background': 'white', 'font': ('DengXian', 12)}},
    'TNotebook.Tab': {'configure': {'font': ('DengXian', 12)}}})
style.theme_use('xpnative')


def save_settings_before_exit():
    global script_file_path_list
    temp_string = ['', '', '']
    with open(os.getenv('APPDATA') + '\\Director\\director.ini', 'w') as settings_log:
        settings_log.write('move_coordinate = %s\n' % move_coordinate.replace('\n', ''))
        settings_log.write('move_checkbutton_flag = %s\n' % move_checkbutton_flag.get())
        settings_log.write('script_checkbutton_flag = %s\n' % script_checkbutton_flag.get())
        settings_log.write('log_checkbutton_flag = %s\n' % log_checkbutton_flag.get())
        settings_log.write('wildcard_checkbutton_flag = %s\n' % wildcard_checkbutton_flag.get())
        settings_log.write('msg_checkbutton_flag = %s\n' % msg_checkbutton_flag.get())
        settings_log.write('prohibit_bosses_checkbutton_flag = %s\n' % prohibit_bosses_checkbutton_flag.get())
        settings_log.write('vmf_path = %s\n' % vmf_path.replace('\n', ''))
        settings_log.write('dict_path = %s\n' % dict_path.replace('\n', ''))
        settings_log.write('game_path = %s\n' % game_path.replace('\n', ''))
        settings_log.write('rescue_path = %s\n' % rescue_path.replace('\n', ''))
        settings_log.write('script_file_path_list = ')
        for file_path in script_file_path_list:
            temp_string[1] += (file_path.replace('\n', '') + ' \x1b ')
        settings_log.write(temp_string[1].removesuffix(' \x1b ') + '\n')
        settings_log.write('move_criteria = ')
        for move_item in move_criteria.items():
            temp_string[2] += '%s: %s \x1b ' % (move_item[0], move_item[1].get())
        settings_log.write(temp_string[2].removesuffix(' \x1b '))


def manually_update():
    new_version = downloader.get_latest_version()
    if new_version is None:
        return
    if new_version == __version__:
        page_update.update_frame.version_box.configure(state='normal')
        page_update.update_frame.version_box.delete(0, tkinter.END)
        page_update.update_frame.version_box.insert(0, 'Director处于最新版本！')
        page_update.update_frame.version_box.configure(state='readonly')
    else:
        page_update.update_frame.version_box.configure(state='normal')
        page_update.update_frame.version_box.delete(0, tkinter.END)
        page_update.update_frame.version_box.insert(0, 'Director有新版本可供升级！最新版本号：%s！' % new_version)
        page_update.update_frame.version_box.configure(state='readonly')


def move_entities():
    flag = False
    entity_id = 0
    with open(vmf_path, 'r', -1, 'utf-8') as vmf_file:
        for move_row in vmf_file:
            if flag is False and re.match('\t\"id\" \"[0-9]*\"', move_row):
                entity_id = move_row.split('\" \"')[1].replace('\"', '').replace('\n', '')
            if flag is False and re.match('\t\"classname\" \".*?\"', move_row):
                entity_classname = move_row.split('\" \"')[1].replace('\"', '').replace('\n', '')
                if entity_classname in move_criteria:
                    flag = True
                else:
                    continue
            if flag is True and re.match('\t\"origin\" \".*?\"', move_row):
                move_entities_dict[entity_id] = move_row.split('\" \"')[1].replace('\"', '').replace('\n', '')
                flag = False


def choose_move_entity_type():
    index_list = [0, 0]
    move_entity_window = tkinter.Toplevel(window)
    move_entity_window.title('设置点实体类型白名单')
    move_entity_window.geometry('1120x632')
    move_entity_window.resizable(False, False)
    move_entity_window.focus_force()
    window.attributes('-disabled', True)
    page_first.move_button.configure(state='disabled')
    move_entity_window.move_frame = tkinter.LabelFrame(move_entity_window, text='设置类型', font=('DengXian', 10))
    move_entity_window.move_frame.place(relx=0.01, rely=0.01, relwidth=0.88, relheight=0.98)

    def destroy_window():
        move_entity_window.destroy()

    ttk.Button(move_entity_window, text='保存', command=lambda: destroy_window(), width=10).place(relx=0.9045, rely=0.9)
    for name in move_criteria.items():
        if index_list[0] <= 23:
            ttk.Checkbutton(move_entity_window.move_frame, text=name[0], variable=name[1]).grid(row=index_list[0], column=index_list[1], sticky='w', padx=1, pady=1)
            index_list[0] += 1
        else:
            index_list[0] = 0
            index_list[1] += 1
    page_first.move_button.wait_window(move_entity_window)
    window.attributes('-disabled', False)
    page_first.move_button.configure(state='normal')
    window.focus_force()


def check_coordinate():
    global move_coordinate
    if move_checkbutton_flag.get():
        temp_coordinates = page_first.move_box.get()
        if re.fullmatch('^(-?[0-9]+)(.[0-9]+)?([^0-9]+)(-?[0-9]+)(.[0-9]+)?([^0-9]+)(-?[0-9]+)(.[0-9]+)?$', temp_coordinates):
            move_coordinate = re.sub('[^0-9.-]+', ' ', temp_coordinates)
            return True
        else:
            return False


def choose_script_file():
    script_file_window = tkinter.Toplevel(window)
    script_file_window.title('选择脚本文件')
    script_file_window.geometry('1000x600')
    script_file_window.resizable(False, False)
    script_file_window.focus_force()
    window.attributes('-disabled', True)
    page_first.script_select_button.configure(state='disabled')
    script_file_window.file_frame = tkinter.LabelFrame(script_file_window, text='选择文件', font=('DengXian', 10))
    script_file_window.file_frame.place(relx=0.01, rely=0.01, relwidth=0.86, relheight=0.98)
    script_file_window.scrollbar_v = tkinter.Scrollbar(script_file_window.file_frame)
    script_file_window.scrollbar_v.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    script_file_window.scrollbar_h = tkinter.Scrollbar(script_file_window.file_frame, orient='horizontal')
    script_file_window.scrollbar_h.pack(side=tkinter.BOTTOM, fill=tkinter.X)
    script_file_window.text_box = tkinter.Text(script_file_window.file_frame, font=('Calibri', 12), wrap='none')
    script_file_window.text_box.pack(expand=tkinter.YES, fill=tkinter.BOTH)
    script_file_window.text_box.configure(xscrollcommand=script_file_window.scrollbar_h.set)
    script_file_window.text_box.configure(yscrollcommand=script_file_window.scrollbar_v.set)
    script_file_window.scrollbar_v.configure(command=script_file_window.text_box.yview)
    script_file_window.scrollbar_h.configure(command=script_file_window.text_box.xview)
    for script_path in script_file_path_list:
        script_file_window.text_box.insert('insert', '%s\n' % script_path)
    script_file_window.text_box.configure(state='disabled')

    def destroy_window():
        script_file_window.destroy()

    ttk.Button(script_file_window, text='选择文件', command=lambda: select_file(3, script_file_window), width=10).place(relx=0.89, rely=0.83)
    ttk.Button(script_file_window, text='保存', command=lambda: destroy_window(), width=10).place(relx=0.89, rely=0.9)
    page_first.script_select_button.wait_window(script_file_window)
    window.attributes('-disabled', False)
    page_first.script_select_button.configure(state='normal')
    window.focus_force()


def select_file(selection_index, script_file_window):
    global vmf_path
    global dict_path
    global game_path
    global rescue_path
    global qc_dir_path
    global qc_output_path
    global script_file_path_list
    match selection_index:
        case 0:
            vmf_path = tkinter.filedialog.askopenfilename(filetypes=[('Valve Map Format', '*.vmf')])
            page_options.vmf_box.configure(state='normal')
            page_options.vmf_box.delete(0, tkinter.END)
            page_options.vmf_box.insert(0, vmf_path)
            page_options.vmf_box.configure(state='readonly')
        case 1:
            dict_path = tkinter.filedialog.askopenfilename(filetypes=[('Director Dict File', '*.dict')])
            page_options.dict_box.configure(state='normal')
            page_options.dict_box.delete(0, tkinter.END)
            page_options.dict_box.insert(0, dict_path)
            page_options.dict_box.configure(state='readonly')
        case 2:
            game_path = tkinter.filedialog.askopenfilename(filetypes=[('left4dead2.exe', 'left4dead2.exe')])
            page_options.game_box.configure(state='normal')
            page_options.game_box.delete(0, tkinter.END)
            page_options.game_box.insert(0, game_path)
            page_options.game_box.configure(state='readonly')
        case 3:
            script_file_path_list = tkinter.filedialog.askopenfilenames(filetypes=[('NUT File', '*.nut')])
            script_file_window.text_box.configure(state='normal')
            script_file_window.text_box.delete('1.0', 'tkinter.END.0')
            for script_path in script_file_path_list:
                script_file_window.text_box.insert('insert', '%s\n' % script_path)
            script_file_window.text_box.configure(state='disabled')
            script_string_var.set('(已选择%s个脚本文件)' % len(script_file_path_list))
            script_file_window.focus_force()
        case 4:
            rescue_path = tkinter.filedialog.askopenfilename(filetypes=[('NUT File', '*_finale.nut')])
            page_options.rescue_box.configure(state='normal')
            page_options.rescue_box.delete(0, tkinter.END)
            page_options.rescue_box.insert(0, rescue_path)
            page_options.rescue_box.configure(state='readonly')
        case 5:
            qc_dir_path = tkinter.filedialog.askdirectory()
            page_resources.qc_box.configure(state='normal')
            page_resources.qc_box.delete(0, tkinter.END)
            page_resources.qc_box.insert(0, qc_dir_path)
            page_resources.qc_box.configure(state='readonly')
            if qc_dir_path != '' and qc_output_path != '':
                page_resources.qc_compile_button.configure(state='normal')
            else:
                page_resources.qc_compile_button.configure(state='disabled')
        case 6:
            qc_output_path = tkinter.filedialog.askdirectory()
            page_resources.qc_output_box.configure(state='normal')
            page_resources.qc_output_box.delete(0, tkinter.END)
            page_resources.qc_output_box.insert(0, qc_output_path)
            page_resources.qc_output_box.configure(state='readonly')
            if qc_dir_path != '' and qc_output_path != '':
                page_resources.qc_compile_button.configure(state='normal')
            else:
                page_resources.qc_compile_button.configure(state='disabled')


def edit_script():
    for script_path in script_file_path_list:
        try:
            os.rename(script_path, '%s.bak' % script_path)
        except OSError:
            if messagebox.askquestion('确认', '检测到.bak备份文件！\n若继续则会删除该备份文件！\n是否继续？') == 'yes':
                os.remove('%s.bak' % script_path)
                os.rename(script_path, '%s.bak' % script_path)
            else:
                return
        with open('%s.bak' % script_path, 'r', -1, 'utf-8') as old_file, open(script_path, 'w', -1, 'utf-8') as new_file:
            for file_row in old_file:
                for entities_item in entities_dict.items():
                    if entities_item[0] in file_row:
                        file_row = file_row.replace(entities_item[0], entities_item[1])
                new_file.write(file_row)


def update_flags():
    if move_checkbutton_flag.get():
        page_first.move_box.configure(state='normal')
        page_first.move_button.configure(state='normal')
    else:
        page_first.move_box.configure(state='disabled')
        page_first.move_button.configure(state='disabled')
    if script_checkbutton_flag.get():
        page_first.script_select_button.configure(state='normal')
        script_string_var.set('(已选择%s个脚本文件)' % len(script_file_path_list))
    else:
        page_first.script_select_button.configure(state='disabled')
        script_string_var.set('')
    if msg_checkbutton_flag.get():
        page_rescue.msg_button.configure(state='normal')
    else:
        page_rescue.msg_button.configure(state='disabled')


def do_obfuscate():
    if vmf_path == '':
        messagebox.showerror('错误', '请选择文件！')
        return
    if move_checkbutton_flag.get() and not check_coordinate():
        messagebox.showerror('错误', '不合法的地图坐标！')
        return
    if messagebox.askquestion('确认', '确认要混淆vmf文件吗？\n将会覆盖源文件并创建.bak备份文件！') == 'yes':
        file_path = vmf_path.replace('\\', '/')
        analyze_file(open(file_path, 'r', -1, 'utf-8'))
        try:
            os.rename(file_path, '%s.bak' % file_path)
        except OSError:
            if messagebox.askquestion('确认', '检测到.bak备份文件！\n若继续则会删除该备份文件！\n是否继续？') == 'yes':
                os.remove('%s.bak' % file_path)
                os.rename(file_path, '%s.bak' % file_path)
            else:
                return
        with open('%s.bak' % file_path, 'r', -1, 'utf-8') as old_file, open(file_path, 'w', -1, 'utf-8') as new_file:
            replace_string(old_file, new_file, file_path)


def analyze_file(file):
    if move_checkbutton_flag.get():
        move_entities()
    for file_row in file:
        if '*' in file_row:
            blacklist_list.append(file_row.split('*')[0].split('\"')[-1].split('\x1b')[-1])
        if re.findall('\"targetname\" \".*?\"', file_row):
            file_row = file_row.split("\" \"")[1][:-2]
            if utils.is_startswith_in_list(file_row, blacklist_list):
                entities_dict[file_row] = utils.generate_random_string()


def replace_string(old_file, new_file, file_path):
    flag = False
    for old_file_row in old_file:
        if re.search("\"[A-Za-z0-9]+\" \"", old_file_row):
            criteria = re.search("\"[A-Za-z0-9]+\" \"", old_file_row).group()[1:-3]
            if criteria in replace_criteria:
                for entities_item in entities_dict.items():
                    old_file_row = old_file_row.replace('\"' + criteria + '\" \"' + entities_item[0] + '\"', '\"' + criteria + '\" \"' + entities_item[1] + '\"')
        if re.search("[A-Za-z0-9]+\x1b", old_file_row):
            for entities_item in entities_dict.items():
                old_file_row = old_file_row.replace(entities_item[0] + '\x1b', entities_item[1] + '\x1b')
        if flag is False and re.match('\t\"id\" \"[0-9]*\"', old_file_row):
            entity_id = old_file_row.split('\" \"')[1].replace('\"', '').replace('\n', '')
            if entity_id in move_entities_dict.keys():
                flag = True
            else:
                continue
        if flag is True and re.match('\t\"origin\" \".*?\"', old_file_row):
            old_file_row = '\t\"origin\" \"%s\"\n' % move_coordinate
            flag = False
        new_file.write(old_file_row)
    if log_checkbutton_flag.get():
        with open('%s.log' % file_path, 'w', -1, 'utf-8') as log_file:
            for entities_item in entities_dict.items():
                log_file.write('%s -> %s\n' % (entities_item[0], entities_item[1]))
            for entities_item in list(set(blacklist_list)):
                log_file.write('%s\n' % entities_item)
            log_file.write('!%s' % time.strftime('%Y-%m-%d %H:%M:%S'))
    messagebox.showinfo('提示', 'vmf已混淆完成！\n.bak备份文件已创建！')


def update_rescue_box():
    global update_rescue_stage_flag
    stage_number = rescue_text['stage_number']
    page_rescue.text_box.configure(state='normal')
    page_rescue.text_box.delete('1.0', '100000.end')
    if msg_checkbutton_flag.get():
        page_rescue.text_box.insert('insert', 'Msg(\"%s\");\n\n' % rescue_text['msg'])
    page_rescue.text_box.insert('insert', 'PANIC <- 0\nTANK <- 1\nDELAY <- 2\nSCRIPTED <- 3\nCLEAROUT <- 4\nSETUP <- 5\nESCAPE <- 7\nRESULTS <- 8\nNONE <- 9\n\nDirectorOptions <-\n{\n')
    if stage_number.isnumeric() and int(stage_number) > 0 and update_rescue_stage_flag:
        page_rescue.text_box.insert('insert', '\tA_CustomFinale_StageCount = %s\n\n' % stage_number)
        for index in range(1, int(stage_number)+1):
            page_rescue.text_box.insert('insert', '\tA_CustomFinale%s = %s\n' % (index, rescue_value_dict[index].split('\x1b')[0]))
            page_rescue.text_box.insert('insert', '\tA_CustomFinaleValue%s = %s\n\n' % (index, rescue_value_dict[index].split('\x1b')[1]))
    if prohibit_bosses_checkbutton_flag.get():
        page_rescue.text_box.insert('insert', '\tProhibitBosses = true\n')
    page_rescue.text_box.insert('insert', '}\n')
    page_rescue.text_box.configure(state='disabled')


def open_text_window(title_text, size, text, button, dict_type):
    child_window = tkinter.Toplevel(window)
    child_window.title(title_text)
    child_window.geometry(size)
    child_window.resizable(False, False)
    child_window.focus_force()
    window.attributes('-disabled', True)
    button.configure(state='disabled')
    ttk.Button(child_window, text='保存', command=lambda: destroy_window(dict_type), width=10).pack(side='bottom', pady=5)
    child_window.text = tkinter.Label(child_window, text=text, font=('DengXian', 12))
    child_window.text.place(relx=0.02, rely=0.1)
    child_window.text_box = ttk.Entry(child_window, width=70, font=('DengXian', 12))
    child_window.text_box.pack(side='bottom')

    def destroy_window(name):
        rescue_text[name] = child_window.text_box.get()
        child_window.destroy()

    button.wait_window(child_window)
    window.attributes('-disabled', False)
    button.configure(state='normal')
    window.focus_force()


def open_stage_window():
    global update_rescue_stage_flag
    if int(rescue_text['stage_number']) >= 16:
        return
    rescue_combobox_list.clear()
    rescue_entry_list.clear()
    rescue_value_dict.clear()
    update_rescue_stage_flag = False
    stage_window = tkinter.Toplevel(window)
    stage_window.title('救援阶段详细设置')
    stage_window.geometry('450x%s' % utils.get_window_y_size(rescue_text['stage_number']))
    stage_window.resizable(False, False)
    stage_window.focus_force()
    window.attributes('-disabled', True)
    page_rescue.stage_button.configure(state='disabled')
    ttk.Button(stage_window, text='保存', command=lambda: destroy_window(), width=10).grid(columnspan=3, column=0, row=int(rescue_text['stage_number']) + 1, padx=5, pady=5)
    for index in range(1, int(rescue_text['stage_number']) + 1):
        tkinter.Label(stage_window, text='阶段 %s: ' % str(index).zfill(2), font=('DengXian', 12)).grid(column=0, row=index-1, padx=5, pady=5, sticky='w')
        combobox = ttk.Combobox(stage_window, width=12, state='readonly', textvariable=tkinter.StringVar())
        combobox['values'] = rescue_type_list
        combobox.current(0)
        combobox.grid(column=1, row=index-1, padx=5, pady=5)
        entry = ttk.Entry(stage_window, width=31, font=('DengXian', 12))
        entry.grid(column=2, row=index-1, padx=5, pady=5)
        rescue_combobox_list[index] = combobox
        rescue_entry_list[index] = entry

    def anti_closing():
        pass

    def destroy_window():
        global update_rescue_stage_flag
        for _index in range(1, int(rescue_text['stage_number']) + 1):
            if utils.is_text_valid(rescue_combobox_list[_index].get(), rescue_entry_list[_index].get()):
                if rescue_combobox_list[_index].get() == 'SCRIPTED':
                    rescue_value_dict[_index] = rescue_combobox_list[_index].get() + '\x1b' + utils.standardized_scripted(rescue_entry_list[_index].get())
                else:
                    rescue_value_dict[_index] = rescue_combobox_list[_index].get() + '\x1b' + rescue_entry_list[_index].get()
            else:
                messagebox.showerror('错误', '不合法的内容！')
                stage_window.focus_force()
                return
        stage_window.destroy()
        window.after(10, update_rescue_box)
        update_rescue_stage_flag = True

    stage_window.protocol('WM_DELETE_WINDOW', anti_closing)
    page_rescue.stage_button.wait_window(stage_window)
    window.attributes('-disabled', False)
    page_rescue.stage_button.configure(state='normal')
    window.focus_force()


def auto_refresh_rescue_window():
    global update_rescue_stage_flag
    rescue_text['stage_number'] = page_rescue.stage_box.get()
    if rescue_text['stage_number'].isnumeric() and 0 < int(rescue_text['stage_number']) < 16:
        page_rescue.stage_button.configure(state='normal')
    else:
        page_rescue.stage_button.configure(state='disable')
    window.after(100, auto_refresh_rescue_window)


def walk_through_qc_files(raw_path, mdl_path):
    gameinfo_path = mdl_path.removesuffix('bin/studiomdl.exe') + 'left4dead2/'
    for dir_path, dir_names, file_names in os.walk(raw_path):
        for file_name in file_names:
            if file_name.endswith('.qc'):
                _thread.start_new_thread(os.system, ('""%s" -game "%s" -nop4 "%s/%s""' % (mdl_path, gameinfo_path, dir_path, file_name),))


page_first.option_frame = tkinter.LabelFrame(page_first, text='选项', font=('DengXian', 10))
page_first.option_frame.place(relx=0.01, rely=0.01, relwidth=0.48, relheight=0.48)
page_first.move_checkbutton = ttk.Checkbutton(page_first.option_frame, text='将指定点实体移动到指定位置:', command=lambda: update_flags(), variable=move_checkbutton_flag)
page_first.move_checkbutton.grid(column=0, row=0, padx=5, pady=5, sticky='w')
page_first.move_box = ttk.Entry(page_first.option_frame, width=28, state='readonly', font=('Calibri', 10))
page_first.move_box.grid(column=1, row=0, padx=5, pady=5)
page_first.move_button = ttk.Button(page_first.option_frame, text='指定实体类型', command=lambda: choose_move_entity_type(), width=15)
page_first.move_button.grid(column=2, row=0, padx=5)
page_first.script_checkbutton = ttk.Checkbutton(page_first.option_frame, text='同时对指定脚本文件进行混淆:', command=lambda: update_flags(), variable=script_checkbutton_flag)
page_first.script_checkbutton.grid(column=0, row=1, padx=5, pady=5, sticky='w')
page_first.text_third = ttk.Label(page_first.option_frame, textvariable=script_string_var)
page_first.text_third.grid(column=1, row=1, padx=5, pady=5, sticky='w')
page_first.script_select_button = ttk.Button(page_first.option_frame, text='选择脚本文件', command=lambda: choose_script_file(), width=15, state='disabled')
page_first.script_select_button.grid(column=2, row=1, padx=5, pady=5)
page_first.wildcard_checkbutton = ttk.Checkbutton(page_first.option_frame, text='启用通配符黑名单', variable=wildcard_checkbutton_flag)
page_first.wildcard_checkbutton.grid(column=0, row=2, padx=5, pady=5, sticky='w')
page_first.wildcard_checkbutton.invoke()
page_first.log_checkbutton = ttk.Checkbutton(page_first.option_frame, text='保存混淆字典', variable=log_checkbutton_flag)
page_first.log_checkbutton.grid(column=0, row=3, padx=5, pady=5, sticky='w')
page_first.log_checkbutton.invoke()
page_first.execute_button = ttk.Button(page_first, text='混淆', command=lambda: do_obfuscate(), width=9)
page_first.execute_button.place(relx=0.8, rely=0.83)
page_first.test_button = ttk.Button(page_first, text='测试', command=lambda: edit_script(), width=9)
page_first.test_button.place(relx=0.6, rely=0.83)
page_first.text_second = tkinter.Label(page_first, text='仅用于求生之路2的vmf文件！', font=('DengXian', 12), fg='red')
page_first.text_second.place(relx=0.05, rely=0.835)

page_resources.qc_frame = tkinter.LabelFrame(page_resources, text='qc批量编译', font=('DengXian', 10))
page_resources.qc_frame.place(relx=0.005, rely=0.005, relwidth=0.49, relheight=0.24)
ttk.Label(page_resources.qc_frame, text='选择文件夹：').grid(column=0, row=0, padx=5, pady=6, sticky='w')
page_resources.qc_box = ttk.Entry(page_resources.qc_frame, width=62, state='readonly')
page_resources.qc_box.grid(column=1, row=0, padx=5, pady=6)
ttk.Button(page_resources.qc_frame, text='浏览', command=lambda: select_file(5, window), width=9).grid(column=2, row=0, padx=5, pady=6)
ttk.Label(page_resources.qc_frame, text='选择输出位置：').grid(column=0, row=1, padx=5, pady=6, sticky='w')
page_resources.qc_output_box = ttk.Entry(page_resources.qc_frame, width=62, state='readonly')
page_resources.qc_output_box.grid(column=1, row=1, padx=5, pady=6)
ttk.Button(page_resources.qc_frame, text='浏览', command=lambda: select_file(6, window), width=9).grid(column=2, row=1, padx=5, pady=6)
page_resources.qc_nop4_checkbutton = ttk.Checkbutton(page_resources.qc_frame, text='-nop4', command=lambda: update_flags(), variable=qc_nop4_checkbutton_flag)
page_resources.qc_nop4_checkbutton.grid(column=0, row=2, padx=5, pady=5, sticky='w')
page_resources.qc_compile_button = ttk.Button(page_resources.qc_frame, text='编译', command=lambda: walk_through_qc_files(qc_dir_path, game_path.removesuffix('left4dead2.exe') + 'bin/studiomdl.exe'), width=9, state='disabled')
page_resources.qc_compile_button.grid(column=2, row=3, padx=5, pady=6)

page_rescue.option_necessary_frame = tkinter.LabelFrame(page_rescue, text='必选设置', font=('DengXian', 10))
page_rescue.option_necessary_frame.place(relx=0.005, rely=0.005, relwidth=0.24, relheight=0.09)
ttk.Label(page_rescue.option_necessary_frame, text='救援阶段数:').grid(column=0, row=0, padx=5, pady=5, sticky='w')
page_rescue.stage_box = ttk.Entry(page_rescue.option_necessary_frame, width=6)
page_rescue.stage_box.grid(column=1, row=0, padx=5, pady=5, sticky='w')
page_rescue.stage_button = ttk.Button(page_rescue.option_necessary_frame, text='详细设置', command=lambda: open_stage_window(), width=10, state='disabled')
page_rescue.stage_button.grid(column=2, row=0, padx=5, pady=5, sticky='w')
ttk.Button(page_rescue.option_necessary_frame, text='?', command=lambda: messagebox.showinfo('提示', '救援阶段数：救援持续的总波数\n\nPANIC：进入该阶段后刷新尸潮的波数\n\nTANK：进入该阶段后生成Tank的个数\n\nDELAY：进入下一阶段之前等待的秒数\n\nSCRIPTED：进入该阶段时执行的尸潮脚本名字\n\n脚本应直接位于scripts\\vscript文件夹下且不带.nut后缀名'), width=3).grid(column=3, row=0, padx=5, pady=5, sticky='w')
page_rescue.option_additional_frame = tkinter.LabelFrame(page_rescue, text='额外设置', font=('DengXian', 10))
page_rescue.option_additional_frame.place(relx=0.255, rely=0.005, relwidth=0.24, relheight=0.88)
page_rescue.msg_checkbutton = ttk.Checkbutton(page_rescue.option_additional_frame, text='', command=lambda: update_flags(), variable=msg_checkbutton_flag)
page_rescue.msg_checkbutton.grid(column=0, row=0, padx=5, pady=5, sticky='w')
page_rescue.msg_button = ttk.Button(page_rescue.option_additional_frame, text='自定义消息设置', command=lambda: open_text_window('自定义消息设置', '600x100', '请输入自定义消息内容：', page_rescue.msg_button, 'msg'), width=15)
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
ttk.Button(page_options.option_frame, text='浏览', command=lambda: select_file(0, window), width=9).grid(column=2, row=0, padx=5, pady=6)
ttk.Label(page_options.option_frame, text='混淆字典路径：').grid(column=0, row=1, padx=5, pady=6, sticky='w')
page_options.dict_box = ttk.Entry(page_options.option_frame, width=165, state='readonly')
page_options.dict_box.grid(column=1, row=1, padx=5, pady=6)
ttk.Button(page_options.option_frame, text='浏览', command=lambda: select_file(1, window), width=9).grid(column=2, row=1, padx=5, pady=6)
ttk.Label(page_options.option_frame, text='游戏本体路径：').grid(column=0, row=2, padx=5, pady=6, sticky='w')
page_options.game_box = ttk.Entry(page_options.option_frame, width=165, state='readonly')
page_options.game_box.grid(column=1, row=2, padx=5, pady=6)
ttk.Button(page_options.option_frame, text='浏览', command=lambda: select_file(2, window), width=9).grid(column=2, row=2, padx=5, pady=6)
ttk.Label(page_options.option_frame, text='救援脚本路径：').grid(column=0, row=3, padx=5, pady=6, sticky='w')
page_options.rescue_box = ttk.Entry(page_options.option_frame, width=165, state='readonly')
page_options.rescue_box.grid(column=1, row=3, padx=5, pady=6)
ttk.Button(page_options.option_frame, text='浏览', command=lambda: select_file(4, window), width=9).grid(column=2, row=3, padx=5, pady=6)

page_update.update_frame = tkinter.LabelFrame(page_update, text='当前版本：%s' % __version__, font=('DengXian', 10))
page_update.update_frame.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.98)
ttk.Button(page_update.update_frame, text='检查更新', command=lambda: manually_update(), width=9).grid(column=0, row=1, padx=5, pady=5)
page_update.update_frame.version_box = ttk.Entry(page_update.update_frame, width=94, state='readonly')
page_update.update_frame.version_box.grid(column=1, row=1, pady=5)
ttk.Button(page_update.update_frame, text='手动更新', state='disabled', command=lambda: manually_update(), width=9).grid(column=2, row=1, padx=5, pady=5)

notebook.add(page_first, text='Targetname混淆')
notebook.add(page_second, text='贴图')
notebook.add(page_third, text='脚本')
notebook.add(page_resources, text='资源提取器')
notebook.add(page_rescue, text='自定义救援')
notebook.add(page_options, text='路径设置')
notebook.add(page_update, text='版本更新')
notebook.pack(padx=10, pady=5, fill='both', expand=True)


with open(os.getenv('APPDATA') + '\\Director\\director.ini', 'a+') as director_settings:
    director_settings.seek(0)
    for row in director_settings:
        if row.startswith('move_coordinate ='):
            move_coordinate = row.split(' = ')[1].replace('\n', '')
            page_first.move_box.configure(state='normal')
            page_first.move_box.insert(0, move_coordinate)
            page_first.move_box.configure(state='readonly')
        if row.startswith('move_checkbutton_flag ='):
            if int(row.split(' = ')[1]) == 1:
                page_first.move_checkbutton.invoke()
        if row.startswith('script_checkbutton_flag ='):
            if int(row.split(' = ')[1]) == 1:
                page_first.script_checkbutton.invoke()
        if row.startswith('log_checkbutton_flag ='):
            if int(row.split(' = ')[1]) == 0:
                page_first.log_checkbutton.invoke()
        if row.startswith('wildcard_checkbutton_flag ='):
            if int(row.split(' = ')[1]) == 0:
                page_first.wildcard_checkbutton.invoke()
        if row.startswith('msg_checkbutton_flag ='):
            if int(row.split(' = ')[1]) == 1:
                page_rescue.msg_checkbutton.invoke()
        if row.startswith('prohibit_bosses_checkbutton_flag ='):
            if int(row.split(' = ')[1]) == 1:
                page_rescue.prohibit_bosses_checkbutton.invoke()
        if row.startswith('vmf_path ='):
            vmf_path = row.split(' = ')[1].replace('\n', '')
            page_options.vmf_box.configure(state='normal')
            page_options.vmf_box.insert(0, vmf_path)
            page_options.vmf_box.configure(state='readonly')
        if row.startswith('dict_path ='):
            dict_path = row.split(' = ')[1].replace('\n', '')
            page_options.dict_box.configure(state='normal')
            page_options.dict_box.insert(0, dict_path)
            page_options.dict_box.configure(state='readonly')
        if row.startswith('game_path ='):
            game_path = row.split(' = ')[1].replace('\n', '')
            page_options.game_box.configure(state='normal')
            page_options.game_box.insert(0, game_path)
            page_options.game_box.configure(state='readonly')
        if row.startswith('rescue_path ='):
            rescue_path = row.split(' = ')[1].replace('\n', '')
            page_options.rescue_box.configure(state='normal')
            page_options.rescue_box.insert(0, rescue_path)
            page_options.rescue_box.configure(state='readonly')
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


atexit.register(save_settings_before_exit)
window.after(100, auto_refresh_rescue_window)
window.mainloop()