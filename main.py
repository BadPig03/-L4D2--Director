import random
import re
import os
import tkinter
import time
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox


class App:
    def __init__(self, master):
        replace_criteria = ['targetname', 'parentname', 'target', 'PSName', 'SourceEntityName', 'DestinationGroup', 'TemplateName', 'RenameNPC', 'panelname', 'LightningStart', 'LightningEnd', 'filtername', 'ignoredEntity', 'lightingorigin',
                            'LaserTarget', 'directionentityname', 'targetentityname', 'MainSoundscapeName', 'position0', 'position1', 'position2', 'position3', 'position4', 'position5', 'position6', 'position7', 'master', 'ApplyEntity',
                            'referencename', 'm_SourceEntityName', 'cpoint1', 'cpoint2', 'cpoint3', 'cpoint4', 'cpoint5', 'cpoint6', 'cpoint7', 'cpoint8', 'cpoint9', 'cpoint10', 'cpoint11', 'cpoint12', 'cpoint13', 'cpoint14', 'cpoint15',
                            'cpoint16', 'cpoint17', 'cpoint18', 'cpoint19', 'cpoint20', 'cpoint21', 'cpoint22', 'cpoint23', 'cpoint24', 'cpoint25', 'cpoint26', 'cpoint27', 'cpoint28', 'cpoint29', 'cpoint30', 'cpoint31', 'cpoint32',
                            'cpoint33',
                            'cpoint34', 'cpoint35', 'cpoint36', 'cpoint37', 'cpoint38', 'cpoint39', 'cpoint40', 'cpoint41', 'cpoint42', 'cpoint43', 'cpoint44', 'cpoint45', 'cpoint46', 'cpoint47', 'cpoint48', 'cpoint49', 'cpoint50',
                            'cpoint51',
                            'cpoint52', 'cpoint53', 'cpoint54', 'cpoint55', 'cpoint56', 'cpoint57', 'cpoint58', 'cpoint59', 'cpoint60', 'cpoint61', 'cpoint62', 'cpoint63', 'globalname', 'slavename', 'NextKey', 'moveto', 'PropName',
                            'Branch01',
                            'Branch02', 'Branch03', 'Branch04', 'Branch05', 'Branch06', 'Branch07', 'Branch08', 'Branch09', 'Branch10', 'Branch11', 'Branch12', 'Branch13', 'Branch14', 'Branch15', 'Branch16', 'IgnoredName01',
                            'IgnoredName02',
                            'IgnoredName03', 'IgnoredName04', 'IgnoredName05', 'IgnoredName06', 'IgnoredName07', 'IgnoredName08', 'IgnoredName09', 'IgnoredName10', 'IgnoredName11', 'IgnoredName12', 'IgnoredName13', 'IgnoredName14',
                            'IgnoredName15',
                            'IgnoredName16', 'attach1', 'attach2', 'SpeakerName', 'ListenFilter', 'source', 'lookatname', 'Filter01', 'Filter02', 'Filter03', 'Filter04', 'Filter05', 'Filter06', 'Filter07', 'Filter08', 'Filter09',
                            'Filter10',
                            'EntityTemplate', 'Template01', 'Template02', 'Template03', 'Template04', 'Template05', 'Template06', 'Template07', 'Template08', 'Template09', 'Template10', 'Template11', 'Template12', 'Template13',
                            'Template14',
                            'Template15', 'Template16', 'DamageTarget', 'constraintsystem', 'newtarget', 'damagefilter', 'InitialOwner', 'altpath', 'PointCamera', 'MeasureTarget', 'MeasureReference', 'Target', 'TargetReference',
                            'enemyfilter',
                            'squadname', 'cameraname', 'spawnpositionname', 'scene0', 'scene1', 'scene2', 'scene3', 'scene4', 'scene5', 'scene6', 'scene7', 'scene8', 'scene9', 'scene10', 'scene11', 'scene12', 'scene13', 'scene14',
                            'scene15',
                            'target1', 'target2', 'target3', 'target4', 'target5', 'target6', 'target7', 'target8', 'target_entity', 'hint_target', 'nozzle', 'RockTargetName', 'model', 'ColorCorrectionName', 'FogName', 'PostProcessName',
                            'glow',
                            'train', 'toptrack', 'bottomtrack', 'landmark', 'measuretarget', 'soundscape', 'TonemapName']
        move_criteria = ['env_dof_controller', 'game_gib_manager', 'game_ragdoll_manager', 'env_texturetoggle', 'env_screeneffect', 'env_screenoverlay', 'env_zoom', 'sound_mix_layer', 'ambient_music', 'env_fade',
                         'env_player_surface_trigger',
                         'env_tonemap_controller', 'env_tonemap_controller_infected', 'env_tonemap_controller_ghost', 'vgui_screen', 'vgui_slideshow_display', 'env_hudhint', 'env_message', 'postprocess_controller', 'env_fog_controller',
                         'env_wind', 'game_weapon_manager', 'game_end', 'game_player_equip', 'game_player_team', 'game_score', 'game_text', 'info_no_dynamic_shadow', 'point_bonusmaps_accessor', 'point_broadcastclientcommand',
                         'point_servercommand', 'point_clientcommand', 'env_effectscript', 'env_particlescript', 'color_correction', 'shadow_control', 'light_directional', 'light_environment', 'logic_auto', 'point_posecontroller',
                         'logic_compare', 'logic_branch', 'logic_branch_listener', 'logic_case', 'logic_multicompare', 'logic_relay', 'logic_timer', 'hammer_updateignorelist', 'logic_collision_pair', 'math_remap', 'math_colorblend',
                         'math_counter', 'logic_navigation', 'logic_autosave', 'logic_active_autosave', 'point_template', 'filter_multi', 'filter_activator_name', 'filter_activator_model', 'filter_activator_context',
                         'filter_activator_class',
                         'filter_activator_mass_greater', 'filter_damage_type', 'point_angularvelocitysensor', 'point_velocitysensor', 'phys_constraintsystem', 'phys_keepupright', 'tanktrain_ai', 'phys_convert', 'ai_speechfilter',
                         'water_lod_control', 'info_camera_link', 'env_credits', 'material_modify_control', 'logic_playerproxy', 'env_particle_performance_monitor', 'point_gamestats_counter', 'logic_scene_list_manager',
                         'logic_choreographed_scene', 'func_timescale', 'logic_script', 'player_weaponstrip', 'logic_director_query', 'info_director', 'game_scavenge_progress_display', 'filter_activator_team',
                         'filter_activator_infected_class',
                         'filter_melee_damage', 'filter_health', 'info_map_parameters', 'info_map_parameters_versus', 'info_gamemode', 'env_detail_controller', 'env_outtro_stats', 'logic_game_event', 'logic_versus_random', 'env_global',
                         'point_surroundtest', 'player_speedmod', 'target_changegravity']
        flags = [tkinter.IntVar(), tkinter.IntVar(), tkinter.IntVar()]
        entities_dict = {}
        move_entities_dict = {}
        blacklist_dict = []
        script_file_path = []
        script_string = tkinter.StringVar()
        script_string.set('')
        selected_file_path = ''
        move_coordinates = ''

        self.notebook = ttk.Notebook(master)
        self.page_first = tkinter.Frame(master)
        self.page_second = tkinter.Frame(master)
        self.page_third = tkinter.Frame(master)
        self.page_options = tkinter.Frame(master)

        self.style = ttk.Style()
        self.style.theme_settings('xpnative', settings={
            'TLabel': {'configure': {'font': ('DengXian', 12)}},
            'TCheckbutton': {'configure': {'font': ('DengXian', 12)}},
            'TButton': {'configure': {'font': ('DengXian', 12)}},
            'TEntry': {'configure': {'font': ('Calibri', 10)}},
            'TNotebook': {'configure': {'background': 'white', 'font': ('DengXian', 12)}},
            'TNotebook.Tab': {'configure': {'font': ('DengXian', 12), 'width': 8}}})
        self.style.theme_use('xpnative')

        self.page_first.option_frame = tkinter.LabelFrame(self.page_first, text='设置', font=('DengXian', 10))
        self.page_first.option_frame.place(relx=0.06, rely=0.25, relwidth=0.88, relheight=0.5)

        self.page_first.execute_button = ttk.Button(self.page_first, text='混淆', command=lambda: do_obfuscate(), width=9)
        self.page_first.execute_button.place(relx=0.8, rely=0.83)

        self.page_first.test_button = ttk.Button(self.page_first, text='测试', command=lambda: edit_script(), width=9)
        self.page_first.test_button.place(relx=0.6, rely=0.83)

        self.page_first.text_second = tkinter.Label(self.page_first, text='仅用于求生之路2的vmf文件！', font=('DengXian', 12), fg='red')
        self.page_first.text_second.place(relx=0.05, rely=0.835)

        self.page_first.move_checkbutton = ttk.Checkbutton(self.page_first.option_frame, text='将部分实体移动到                                的位置', command=lambda: update_flags(), variable=flags[0])
        self.page_first.move_checkbutton.place(relx=0.02, rely=0.05)

        self.page_first.coordinate_box = ttk.Entry(self.page_first.option_frame, width=20, state='readonly')
        self.page_first.coordinate_box.place(relx=0.366, rely=0.053)

        self.page_first.script_checkbutton = ttk.Checkbutton(self.page_first.option_frame, text='一并处理脚本文件', command=lambda: update_flags(), variable=flags[1])
        self.page_first.script_checkbutton.place(relx=0.02, rely=0.4)

        self.page_first.text_third = ttk.Label(self.page_first.option_frame, textvariable=script_string)
        self.page_first.text_third.place(relx=0.37, rely=0.4)

        self.page_first.script_select_button = ttk.Button(self.page_first.option_frame, text='选择文件', command=lambda: select_script_file(), width=9, state='disabled')
        self.page_first.script_select_button.place(relx=0.78, rely=0.38)

        self.page_first.log_checkbutton = ttk.Checkbutton(self.page_first.option_frame, text='保存混淆字典', variable=flags[2])
        self.page_first.log_checkbutton.place(relx=0.02, rely=0.75)
        self.page_first.log_checkbutton.invoke()

        self.page_options.option_frame = tkinter.LabelFrame(self.page_options, text='设置', font=('DengXian', 10))
        self.page_options.option_frame.place(relx=0.06, rely=0.25, relwidth=0.88, relheight=0.5)

        self.page_options.text_first = ttk.Label(self.page_options, text='vmf路径：')
        self.page_options.text_first.place(relx=0.055, rely=0.105)

        self.page_options.file_box = ttk.Entry(self.page_options, width=48, state='readonly')
        self.page_options.file_box.place(relx=0.196, rely=0.1)

        self.page_options.file_select_button = ttk.Button(self.page_options, text='浏览', command=lambda: select_file(), width=9)
        self.page_options.file_select_button.place(relx=0.8, rely=0.09)

        self.notebook.add(self.page_first, text='点实体')
        self.notebook.add(self.page_second, text='  贴图')
        self.notebook.add(self.page_third, text='  脚本')
        self.notebook.add(self.page_options, text='路径设置')
        self.notebook.pack(padx=10, pady=5, fill='both', expand=True)

        def edit_script():
            for file_path in script_file_path:
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
            nonlocal script_string
            if flags[0].get():
                self.page_first.coordinate_box.config(state='normal')
            else:
                self.page_first.coordinate_box.config(state='readonly')
            if flags[1].get():
                self.page_first.script_select_button.config(state='normal')
                script_string.set('(已选择%s个脚本文件)' % len(script_file_path))
            else:
                self.page_first.script_select_button.config(state='disabled')
                script_string.set('')

        def move_entities():
            nonlocal selected_file_path
            flag = False
            entity_id = 0
            with open(selected_file_path, 'r', -1, 'utf-8') as file:
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
            if flags[0].get():
                nonlocal move_coordinates
                temp_coordinates = self.page_first.coordinate_box.get()
                if re.fullmatch('^(-?[0-9]+)(.[0-9]+)?([^0-9]+)(-?[0-9]+)(.[0-9]+)?([^0-9]+)(-?[0-9]+)(.[0-9]+)?$', temp_coordinates):
                    move_coordinates = re.sub('[^0-9.-]+', ' ', temp_coordinates)
                    return True
                else:
                    return False

        def do_obfuscate():
            nonlocal selected_file_path
            if selected_file_path == '':
                messagebox.showerror('错误', '请选择文件！')
                return
            if flags[0].get() and not check_coordinate():
                messagebox.showerror('错误', '不合法的地图坐标！')
                return
            if messagebox.askquestion('确认', '确认要混淆vmf文件吗？\n将会覆盖源文件并创建.bak备份文件！') == 'yes':
                edit_file()

        def select_file():
            nonlocal selected_file_path
            selected_file_path = tkinter.filedialog.askopenfilename(filetypes=[('Valve Map Format', '*.vmf')])
            self.page_options.file_box.configure(state='normal')
            self.page_options.file_box.delete(0, 100000)
            self.page_options.file_box.insert(0, selected_file_path)
            self.page_options.file_box.configure(state='readonly')

        def select_script_file():
            nonlocal script_file_path
            script_file_path = tkinter.filedialog.askopenfilenames(filetypes=[('NUT File', '*.nut')])
            script_string.set('(已选择%s个脚本文件)' % len(script_file_path))

        def edit_file():
            nonlocal selected_file_path
            file_path = selected_file_path.replace('\\', '/')
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
            for blacklist_item in blacklist_dict:
                if row.startswith(blacklist_item):
                    return False
            return True

        def parse(file):
            if flags[0].get():
                move_entities()
            for row in file:
                if '*' in row:
                    blacklist_dict.append(row.split('*')[0].split('\"')[-1].split('')[-1])
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
                    row = '\t\"origin\" \"%s\"\n' % move_coordinates
                    flag = False
                new_file.write(row)
            if flags[2].get():
                with open('%s.log' % file_path, 'w', -1, 'utf-8') as log_file:
                    for item in entities_dict.items():
                        log_file.write('%s -> %s\n' % (item[0], item[1]))
                    for item in list(set(blacklist_dict)):
                        log_file.write('%s\n' % item)
                    log_file.write('!%s' % time.strftime('%Y-%m-%d %H:%M:%S'))
            messagebox.showinfo('提示', 'vmf已混淆完成！\n.bak备份文件已创建！')


if __name__ == '__main__':
    window = tkinter.Tk()
    window.title('求生之路2 vmf混淆器 by ty')
    window.geometry('800x600')
    window.resizable(False, False)
    window.configure(bg='white')
    window.iconphoto(True, tkinter.PhotoImage(file='icon.png'))

    App(window)
    # messagebox.showinfo('提示', 'vmf混淆器的作用：\n1.将所有实体的targetname重命名为无意义字符串\n2.IO里对应的targetname也会随之更改\n3.(可选)将对位置无要求的点实体移动到指定位置\n4.(可选)将指定脚本文件里的targetname也一并混淆\n5.(可选)保存一个targetname被混淆前后的日志文件')

    window.mainloop()
