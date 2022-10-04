import atexit
import random
import re
import os
import tkinter
import time
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

if __name__ != '__main__':
    exit(0)

window = tkinter.Tk()
window.title('Director by ty')
window.geometry('800x600')
window.resizable(False, False)
window.configure(bg='white')
window.iconphoto(True, tkinter.PhotoImage(file='icon_small.png'))

# messagebox.showinfo('提示', 'vmf混淆器的作用：\n1.将所有实体的targetname重命名为无意义字符串\n2.IO里对应的targetname也会随之更改\n3.(可选)将对位置无要求的点实体移动到指定位置\n4.(可选)将指定脚本文件里的targetname也一并混淆\n5.(可选)保存一个targetname被混淆前后的日志文件')

replace_criteria = ['targetname', 'parentname', 'target', 'PSName', 'SourceEntityName', 'DestinationGroup', 'TemplateName', 'RenameNPC', 'panelname', 'LightningStart', 'LightningEnd', 'filtername', 'ignoredEntity', 'lightingorigin',
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
                    'FogName', 'PostProcessName', 'glow', 'train', 'toptrack', 'bottomtrack', 'landmark', 'measuretarget', 'soundscape', 'TonemapName']
move_criteria = ['env_dof_controller', 'game_gib_manager', 'game_ragdoll_manager', 'env_texturetoggle', 'env_screeneffect', 'env_screenoverlay', 'env_zoom', 'sound_mix_layer', 'ambient_music', 'env_fade', 'env_player_surface_trigger',
                 'env_tonemap_controller', 'env_tonemap_controller_infected', 'env_tonemap_controller_ghost', 'vgui_screen', 'vgui_slideshow_display', 'env_hudhint', 'env_message', 'postprocess_controller', 'env_fog_controller',
                 'env_wind', 'game_weapon_manager', 'game_end', 'game_player_equip', 'game_player_team', 'game_score', 'game_text', 'info_no_dynamic_shadow', 'point_bonusmaps_accessor', 'point_broadcastclientcommand',
                 'point_servercommand', 'point_clientcommand', 'env_effectscript', 'env_particlescript', 'color_correction', 'shadow_control', 'light_directional', 'light_environment', 'logic_auto', 'point_posecontroller',
                 'logic_compare', 'logic_branch', 'logic_branch_listener', 'logic_case', 'logic_multicompare', 'logic_relay', 'logic_timer', 'hammer_updateignorelist', 'logic_collision_pair', 'math_remap', 'math_colorblend',
                 'math_counter', 'logic_navigation', 'logic_autosave', 'logic_active_autosave', 'point_template', 'filter_multi', 'filter_activator_name', 'filter_activator_model', 'filter_activator_context', 'filter_activator_class',
                 'filter_activator_mass_greater', 'filter_damage_type', 'point_angularvelocitysensor', 'point_velocitysensor', 'phys_constraintsystem', 'phys_keepupright', 'tanktrain_ai', 'phys_convert', 'ai_speechfilter',
                 'water_lod_control', 'info_camera_link', 'env_credits', 'material_modify_control', 'logic_playerproxy', 'env_particle_performance_monitor', 'point_gamestats_counter', 'logic_scene_list_manager',
                 'logic_choreographed_scene', 'func_timescale', 'logic_script', 'player_weaponstrip', 'logic_director_query', 'info_director', 'game_scavenge_progress_display', 'filter_activator_team', 'filter_activator_infected_class',
                 'filter_melee_damage', 'filter_health', 'info_map_parameters', 'info_map_parameters_versus', 'info_gamemode', 'env_detail_controller', 'env_outtro_stats', 'logic_game_event', 'logic_versus_random', 'env_global',
                 'point_surroundtest', 'player_speedmod', 'target_changegravity']
move_checkbutton_flag = tkinter.IntVar()
script_checkbutton_flag = tkinter.IntVar()
log_checkbutton_flag = tkinter.IntVar()

entities_dict = {}
move_entities_dict = {}

blacklist_list = []
script_file_path_list = []

script_string_var = tkinter.StringVar()
script_string_var.set('')
move_coordinate = ''
vmf_path = ''
dict_path = ''
game_path = ''

notebook = ttk.Notebook(window)
page_first = tkinter.Frame(window)
page_second = tkinter.Frame(window)
page_third = tkinter.Frame(window)
page_options = tkinter.Frame(window)

style = ttk.Style(window)
style.theme_settings('xpnative', settings={
    'TLabel': {'configure': {'font': ('DengXian', 12)}},
    'TCheckbutton': {'configure': {'font': ('DengXian', 12)}},
    'TButton': {'configure': {'font': ('DengXian', 12)}},
    'TEntry': {'configure': {'font': ('Calibri', 10)}},
    'TNotebook': {'configure': {'background': 'white', 'font': ('DengXian', 12)}},
    'TNotebook.Tab': {'configure': {'font': ('DengXian', 12), 'width': 8}}})
style.theme_use('xpnative')

page_first.option_frame = tkinter.LabelFrame(page_first, text='设置', font=('DengXian', 10))
page_first.option_frame.place(relx=0.06, rely=0.25, relwidth=0.88, relheight=0.5)

page_first.execute_button = ttk.Button(page_first, text='混淆', command=lambda: do_obfuscate(), width=9)
page_first.execute_button.place(relx=0.8, rely=0.83)

page_first.test_button = ttk.Button(page_first, text='测试', command=lambda: edit_script(), width=9)
page_first.test_button.place(relx=0.6, rely=0.83)

page_first.text_second = tkinter.Label(page_first, text='仅用于求生之路2的vmf文件！', font=('DengXian', 12), fg='red')
page_first.text_second.place(relx=0.05, rely=0.835)

page_first.move_checkbutton = ttk.Checkbutton(page_first.option_frame, text='将部分实体移动到                                的位置', command=lambda: update_flags(), variable=move_checkbutton_flag)
page_first.move_checkbutton.place(relx=0.02, rely=0.05)

page_first.coordinate_box = ttk.Entry(page_first.option_frame, width=20, state='readonly')
page_first.coordinate_box.place(relx=0.366, rely=0.053)

page_first.script_checkbutton = ttk.Checkbutton(page_first.option_frame, text='一并处理脚本文件', command=lambda: update_flags(), variable=script_checkbutton_flag)
page_first.script_checkbutton.place(relx=0.02, rely=0.4)

page_first.text_third = ttk.Label(page_first.option_frame, textvariable=script_string_var)
page_first.text_third.place(relx=0.37, rely=0.4)

page_first.script_select_button = ttk.Button(page_first.option_frame, text='选择文件', command=lambda: select_script_file(), width=9, state='disabled')
page_first.script_select_button.place(relx=0.78, rely=0.38)

page_first.log_checkbutton = ttk.Checkbutton(page_first.option_frame, text='保存混淆字典', variable=log_checkbutton_flag)
page_first.log_checkbutton.place(relx=0.02, rely=0.75)
page_first.log_checkbutton.invoke()

page_options.option_frame = tkinter.LabelFrame(page_options, text='文件路径', font=('DengXian', 10))
page_options.option_frame.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.48)

page_options.vmf_text = ttk.Label(page_options.option_frame, text='vmf文件路径：')
page_options.vmf_text.place(relx=0.01, rely=0.05)
page_options.vmf_box = ttk.Entry(page_options.option_frame, width=89, state='readonly')
page_options.vmf_box.place(relx=0.155, rely=0.045)
page_options.vmf_select_button = ttk.Button(page_options.option_frame, text='浏览', command=lambda: select_file(0), width=9)
page_options.vmf_select_button.place(relx=0.88, rely=0.036)

page_options.dict_text = ttk.Label(page_options.option_frame, text='混淆字典路径：')
page_options.dict_text.place(relx=0.01, rely=0.2)
page_options.dict_box = ttk.Entry(page_options.option_frame, width=89, state='readonly')
page_options.dict_box.place(relx=0.155, rely=0.195)
page_options.dict_select_button = ttk.Button(page_options.option_frame, text='浏览', command=lambda: select_file(1), width=9)
page_options.dict_select_button.place(relx=0.88, rely=0.186)

page_options.game_text = ttk.Label(page_options.option_frame, text='游戏本体路径：')
page_options.game_text.place(relx=0.01, rely=0.35)
page_options.game_box = ttk.Entry(page_options.option_frame, width=89, state='readonly')
page_options.game_box.place(relx=0.155, rely=0.345)
page_options.game_select_button = ttk.Button(page_options.option_frame, text='浏览', command=lambda: select_file(2), width=9)
page_options.game_select_button.place(relx=0.88, rely=0.336)

notebook.add(page_first, text='点实体')
notebook.add(page_second, text='  贴图')
notebook.add(page_third, text='  脚本')
notebook.add(page_options, text='路径设置')
notebook.pack(padx=10, pady=5, fill='both', expand=True)


def save_settings_before_exit():
    with open(os.path.abspath('director.ini'), 'w') as settings_log:
        settings_log.write('move_coordinate = %s\n' % move_coordinate)
        settings_log.write('move_checkbutton_flag = %s\n' % move_checkbutton_flag.get())
        settings_log.write('script_checkbutton_flag = %s\n' % script_checkbutton_flag.get())
        settings_log.write('log_checkbutton_flag = %s\n' % log_checkbutton_flag.get())
        settings_log.write('vmf_path = %s\n' % vmf_path)
        settings_log.write('dict_path = %s\n' % dict_path)
        settings_log.write('game_path = %s\n' % game_path)
        settings_log.write('script_file_path_list = ')
        settings_log.write(' \x1b '.join([path for path in script_file_path_list]))


def select_file(index):
    global vmf_path
    global dict_path
    global game_path
    match index:
        case 0:
            vmf_path = tkinter.filedialog.askopenfilename(filetypes=[('Valve Map Format', '*.vmf')])
            page_options.vmf_box.configure(state='normal')
            page_options.vmf_box.delete(0, 100000)
            page_options.vmf_box.insert(0, vmf_path)
            page_options.vmf_box.configure(state='readonly')
        case 1:
            dict_path = tkinter.filedialog.askopenfilename(filetypes=[('Director Dict File', '*.dict')])
            page_options.dict_box.configure(state='normal')
            page_options.dict_box.delete(0, 100000)
            page_options.dict_box.insert(0, dict_path)
            page_options.dict_box.configure(state='readonly')
        case 2:
            game_path = tkinter.filedialog.askopenfilename(filetypes=[('left4dead2.exe', 'left4dead2.exe')])
            page_options.game_box.configure(state='normal')
            page_options.game_box.delete(0, 100000)
            page_options.game_box.insert(0, game_path)
            page_options.game_box.configure(state='readonly')


def edit_script():
    for file_path in script_file_path_list:
        try:
            os.rename(file_path, '%s.bak' % file_path)
        except OSError:
            if messagebox.askquestion('确认', '检测到.bak备份文件！\n若继续则会删除该备份文件！\n是否继续？') == 'yes':
                os.remove('%s.bak' % file_path)
                os.rename(file_path, '%s.bak' % file_path)
            else:
                return
        with open('%s.bak' % file_path, 'r', -1, 'utf-8') as old_file, open(file_path, 'w', -1, 'utf-8') as new_file:
            for row in old_file:
                for item in entities_dict.items():
                    if item[0] in row:
                        row = row.replace(item[0], item[1])
                new_file.write(row)


def update_flags():
    if move_checkbutton_flag.get():
        page_first.coordinate_box.config(state='normal')
    else:
        page_first.coordinate_box.config(state='readonly')
    if script_checkbutton_flag.get():
        page_first.script_select_button.config(state='normal')
        script_string_var.set('(已选择%s个脚本文件)' % len(script_file_path_list))
    else:
        page_first.script_select_button.config(state='disabled')
        script_string_var.set('')


def move_entities():
    flag = False
    entity_id = 0
    with open(vmf_path, 'r', -1, 'utf-8') as file:
        for row in file:
            if flag is False and re.match('\t\"id\" \"[0-9]*\"', row):
                entity_id = row.split('\" \"')[1].replace('\"', '').replace('\n', '')
            if flag is False and re.match('\t\"classname\" \".*?\"', row):
                entity_classname = row.split('\" \"')[1].replace('\"', '').replace('\n', '')
                if entity_classname in move_criteria:
                    flag = True
                else:
                    continue
            if flag is True and re.match('\t\"origin\" \".*?\"', row):
                move_entities_dict[entity_id] = row.split('\" \"')[1].replace('\"', '').replace('\n', '')
                flag = False


def check_coordinate():
    global move_coordinate
    if move_checkbutton_flag.get():
        temp_coordinates = page_first.coordinate_box.get()
        if re.fullmatch('^(-?[0-9]+)(.[0-9]+)?([^0-9]+)(-?[0-9]+)(.[0-9]+)?([^0-9]+)(-?[0-9]+)(.[0-9]+)?$', temp_coordinates):
            move_coordinate = re.sub('[^0-9.-]+', ' ', temp_coordinates)
            return True
        else:
            return False


def do_obfuscate():
    if vmf_path == '':
        messagebox.showerror('错误', '请选择文件！')
        return
    if move_checkbutton_flag.get() and not check_coordinate():
        messagebox.showerror('错误', '不合法的地图坐标！')
        return
    if messagebox.askquestion('确认', '确认要混淆vmf文件吗？\n将会覆盖源文件并创建.bak备份文件！') == 'yes':
        edit_file()


def select_script_file():
    global script_file_path_list
    script_file_path_list = tkinter.filedialog.askopenfilenames(filetypes=[('NUT File', '*.nut')])
    script_string_var.set('(已选择%s个脚本文件)' % len(script_file_path_list))


def edit_file():
    file_path = vmf_path.replace('\\', '/')
    parse(open(file_path, 'r', -1, 'utf-8'))
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


def is_in_blacklist(row):
    for blacklist_item in blacklist_list:
        if row.startswith(blacklist_item):
            return False
    return True


def parse(file):
    if move_checkbutton_flag.get():
        move_entities()
    for row in file:
        if '*' in row:
            blacklist_list.append(row.split('*')[0].split('\"')[-1].split('')[-1])
        if re.findall('\"targetname\" \".*?\"', row):
            row = row.split("\" \"")[1][:-2]
            if is_in_blacklist(row):
                entities_dict[row] = random_string()


def random_string():
    letters = 'abcedfghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    numbers = '0123456789'
    special_character = '#$%_-.+='
    string = random.sample(letters + numbers + special_character, 16)
    return ''.join(string)


def replace_string(old_file, new_file, file_path):
    flag = False
    for row in old_file:
        if re.search("\"[A-Za-z0-9]+\" \"", row):
            criteria = re.search("\"[A-Za-z0-9]+\" \"", row).group()[1:-3]
            if criteria in replace_criteria:
                for item in entities_dict.items():
                    row = row.replace('\"' + criteria + '\" \"' + item[0] + '\"', '\"' + criteria + '\" \"' + item[1] + '\"')
        if re.search("[A-Za-z0-9]+", row):
            for item in entities_dict.items():
                row = row.replace(item[0] + '', item[1] + '')
        if flag is False and re.match('\t\"id\" \"[0-9]*\"', row):
            entity_id = row.split('\" \"')[1].replace('\"', '').replace('\n', '')
            if entity_id in move_entities_dict.keys():
                flag = True
            else:
                continue
        if flag is True and re.match('\t\"origin\" \".*?\"', row):
            row = '\t\"origin\" \"%s\"\n' % move_coordinate
            flag = False
        new_file.write(row)
    if log_checkbutton_flag.get():
        with open('%s.log' % file_path, 'w', -1, 'utf-8') as log_file:
            for item in entities_dict.items():
                log_file.write('%s -> %s\n' % (item[0], item[1]))
            for item in list(set(blacklist_list)):
                log_file.write('%s\n' % item)
            log_file.write('!%s' % time.strftime('%Y-%m-%d %H:%M:%S'))
    messagebox.showinfo('提示', 'vmf已混淆完成！\n.bak备份文件已创建！')


atexit.register(save_settings_before_exit)


window.mainloop()