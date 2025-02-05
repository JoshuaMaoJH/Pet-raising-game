import random
import time
from typing import List, Optional
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os


class Pet:
    def __init__(self, name: str, species: str):
        self.name = name
        self.species = species
        self.hunger = 50
        self.happiness = 50
        self.energy = 100
        self.health = 100
        self.is_sleeping = False
        self.last_feed_time = time.time()
        self.level = 1
        self.experience = 0

    def feed(self, food_type: str):
        """喂食宠物"""
        foods = {
            "regular_food": {"hunger": 30, "health": 5, "exp": 10},
            "premium_food": {"hunger": 50, "health": 10, "exp": 20},
            "treats": {"hunger": 10, "health": 2, "exp": 5},
            "fresh_meat": {"hunger": 40, "health": 15, "exp": 25},
            "fish": {"hunger": 35, "health": 12, "exp": 22},
            "vegetables": {"hunger": 25, "health": 8, "exp": 15},
            "fruits": {"hunger": 20, "health": 10, "exp": 18},
            "special_meal": {"hunger": 60, "health": 20, "exp": 30}
        }

        if food_type in foods:
            food = foods[food_type]
            self.hunger = max(0, min(100, self.hunger - food["hunger"]))
            self.health = min(100, self.health + food["health"])
            self.happiness += 10
            self.gain_experience(food["exp"])
            self.last_feed_time = time.time()
            return f"{self.name}吃了{food_type},看起来很满意! (获得{food['exp']}经验)"
        return f"{self.name}对这个食物不感兴趣..."

    def gain_experience(self, exp: int):
        """获得经验值"""
        self.experience += exp
        while self.experience >= 100:
            self.level_up()
            self.experience -= 100

    def level_up(self):
        """升级"""
        self.level = min(100,self.level+1)
        self.health = min(100, self.health + 20)
        self.happiness = min(100, self.happiness + 20)
        return f"{self.name}升级了! 现在是{self.level}级"

    def play(self, game_type: str):
        """和宠物玩耍"""
        if self.energy < 20:
            return f"{self.name}太累了,需要休息..."

        games = {
            "fetch": {"energy": -20, "happiness": 30, "exp": 15},
            "chase": {"energy": -30, "happiness": 40, "exp": 20},
            "cuddle": {"energy": -10, "happiness": 20, "exp": 10}
        }

        if game_type in games:
            game = games[game_type]
            self.energy = max(0, self.energy + game["energy"])
            self.happiness = min(100, self.happiness + game["happiness"])
            self.hunger += 10
            self.gain_experience(game["exp"])
            return f"{self.name}玩得很开心! (获得{game['exp']}经验)"
        return "这个游戏好像不太适合..."

    def sleep(self):
        """让宠物睡觉"""
        if not self.is_sleeping:
            self.is_sleeping = True
            self.energy = min(100, self.energy + 50)
            self.health += 10
            self.gain_experience(5)
            return f"{self.name}睡着了,好好休息吧..."
        return f"{self.name}已经在睡觉了..."

    def wake_up(self):
        """唤醒宠物"""
        if self.is_sleeping:
            self.is_sleeping = False
            return f"{self.name}醒来了,精神焕发!"
        return f"{self.name}已经醒着呢..."

    def save_pet(self, save_dir="pet_saves"):
        """保存宠物数据到文件"""
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        pet_data = {
            "name": self.name,
            "species": self.species,
            "hunger": self.hunger,
            "happiness": self.happiness,
            "energy": self.energy,
            "health": self.health,
            "is_sleeping": self.is_sleeping,
            "level": self.level,
            "experience": self.experience
        }

        file_path = os.path.join(save_dir, f"{self.name}.json")
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(pet_data, f, ensure_ascii=False, indent=4)

        return f"宠物 {self.name} 已保存到 {file_path}"

    def check_status(self) -> str:
        """检查宠物状态"""
        return f"""
{self.name}的状态:
品种: {self.species}
等级: {self.level}
经验值: {self.experience}/100
饥饿度: {self.hunger}/100
心情: {self.happiness}/100
体力: {self.energy}/100
健康: {self.health}/100
状态: {'睡眠中' if self.is_sleeping else '清醒'}
"""

    def calculate_value(self) -> int:
        """计算宠物价值"""
        base_value = 500
        level_bonus = self.level * 200
        stats_bonus = (self.health + self.happiness) * 5
        return base_value + level_bonus + stats_bonus


class PetGame:
    def __init__(self):
        self.pets = []
        self.money = 1000
        self.food_inventory = {
            "regular_food": 5,
            "premium_food": 2,
            "treats": 3,
            "fresh_meat": 0,
            "fish": 0,
            "vegetables": 0,
            "fruits": 0,
            "special_meal": 0
        }
        self.food_prices = {
            "regular_food": 50,
            "premium_food": 100,
            "treats": 30,
            "fresh_meat": 80,
            "fish": 70,
            "vegetables": 40,
            "fruits": 45,
            "special_meal": 150
        }
        # 添加已售出宠物列表
        self.sold_pets = []
        # 添加比赛记录
        self.contest_record = {}

    def add_pet(self, name: str, species: str):
        """添加新宠物"""
        new_pet = Pet(name, species)
        self.pets.append(new_pet)
        return f"欢迎{name}加入家族!"

    def find_pet(self, name: str) -> Optional[Pet]:
        """查找特定宠物"""
        for pet in self.pets:
            if pet.name == name:
                return pet
        return None

    def buy_food(self, food_type: str, quantity: int):
        """购买食物"""
        if food_type not in self.food_prices:
            return "没有这种食物..."

        total_cost = self.food_prices[food_type] * quantity
        if self.money >= total_cost:
            self.money -= total_cost
            self.food_inventory[food_type] += quantity
            return f"购买了{quantity}份{food_type},剩余金额:{self.money}"
        return "钱不够..."

    def add_record(self, contest_type: str, result: str):
        """添加比赛记录"""
        if contest_type not in self.contest_record:
            self.contest_record[contest_type] = []
        self.contest_record[contest_type].append(result)

    def sell_pet(self, name: str) -> str:
        """出售宠物"""
        pet = self.find_pet(name)
        if pet:
            value = pet.calculate_value()
            self.money += value
            self.pets.remove(pet)
            self.sold_pets.append(pet)  # 添加到已售出列表
            return f"你出售了{pet.name},获得{value}金币! 当前金币:{self.money}"
        return "找不到这个宠物..."

    def check_inventory(self) -> str:
        """查看库存"""
        inventory_str = "\n当前库存:"
        for food, amount in self.food_inventory.items():
            inventory_str += f"\n{food}: {amount}份 (价格:{self.food_prices[food]}金币/份)"
        inventory_str += f"\n金币: {self.money}"
        return inventory_str

    def save_game(self, filename="game_save.json"):
        """保存游戏状态"""
        save_data = {
            "money": self.money,
            "food_inventory": self.food_inventory,
            "pets": [],
            "sold_pets": [],
            "contest_record": {}
        }

        # 保存当前宠物数据
        for pet in self.pets:
            pet_data = {
                "name": pet.name,
                "species": pet.species,
                "hunger": pet.hunger,
                "happiness": pet.happiness,
                "energy": pet.energy,
                "health": pet.health,
                "is_sleeping": pet.is_sleeping,
                "level": pet.level,
                "experience": pet.experience
            }
            save_data["pets"].append(pet_data)

        # 保存已售出宠物数据
        for pet in self.sold_pets:
            pet_data = {
                "name": pet.name,
                "species": pet.species,
                "hunger": pet.hunger,
                "happiness": pet.happiness,
                "energy": pet.energy,
                "health": pet.health,
                "is_sleeping": pet.is_sleeping,
                "level": pet.level,
                "experience": pet.experience,
                "sell_value": pet.calculate_value()
            }
            save_data["sold_pets"].append(pet_data)

        for contest_type, record in self.contest_record.items():
            save_data["contest_record"][contest_type] = record

        # 保存到文件
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, ensure_ascii=False, indent=4)

        return "游戏已保存"

    def load_game(self, filename="game_save.json"):
        """加载游戏状态"""
        if not os.path.exists(filename):
            return "没有找到存档文件"

        try:
            with open(filename, 'r', encoding='utf-8') as f:
                save_data = json.load(f)

            # 恢复游戏状态
            self.money = save_data["money"]
            self.food_inventory = save_data["food_inventory"]

            # 恢复宠物
            self.pets = []
            for pet_data in save_data["pets"]:
                pet = Pet(pet_data["name"], pet_data["species"])
                pet.hunger = pet_data["hunger"]
                pet.happiness = pet_data["happiness"]
                pet.energy = pet_data["energy"]
                pet.health = pet_data["health"]
                pet.is_sleeping = pet_data["is_sleeping"]
                pet.level = pet_data["level"]
                pet.experience = pet_data["experience"]
                self.pets.append(pet)

            # 恢复已售出宠物
            self.sold_pets = []
            for pet_data in save_data["sold_pets"]:
                pet = Pet(pet_data["name"], pet_data["species"])
                pet.hunger = pet_data["hunger"]
                pet.happiness = pet_data["happiness"]
                pet.energy = pet_data["energy"]
                pet.health = pet_data["health"]
                pet.is_sleeping = pet_data["is_sleeping"]
                pet.level = pet_data["level"]
                pet.experience = pet_data["experience"]
                self.sold_pets.append(pet)

            self.contest_record = save_data["contest_record"]

            return "游戏已加载"
        except Exception as e:
            return f"加载游戏失败: {str(e)}"

    def buy_back_pet(self, name: str) -> str:
        """回购已售出的宠物"""
        for pet in self.sold_pets:
            if pet.name == name:
                value = pet.calculate_value()
                if self.money >= value:
                    self.money -= value
                    self.sold_pets.remove(pet)
                    self.pets.append(pet)
                    return f"你回购了{pet.name},花费{value}金币! 当前金币:{self.money}"
                else:
                    return "金币不足,无法回购..."
        return "找不到这个宠物..."


def print_help():
    """打印帮助信息"""
    print("""
可用命令:
1. add <名字> <品种> - 添加新宠物
2. feed <宠物名> <食物类型> - 喂食宠物
   可用食物: regular_food, premium_food, treats, fresh_meat, fish, 
   vegetables, fruits, special_meal
3. play <宠物名> <游戏类型> - 和宠物玩耍(fetch/chase/cuddle)
4. sleep <宠物名> - 让宠物睡觉
5. wake <宠物名> - 叫醒宠物
6. status <宠物名> - 查看宠物状态
7. buy <食物类型> <数量> - 购买食物
8. sell <宠物名> - 出售宠物
9. inventory - 查看库存
10. help - 显示帮助信息
11. exit - 退出游戏
""")


class PetGameGUI:
    def __init__(self, root, game):
        self.root = root
        self.root.title("宠物养成游戏")
        self.root.geometry("1024x768")

        self.game = game
        self.current_pet = None

        # 创建主界面
        self.create_gui()

        # 创建消息日志
        self.messages = []

    def save_current_pet(self):
        """保存当前选中的宠物"""
        if not self.current_pet:
            messagebox.showwarning("警告", "请先选择一个宠物！")
            return

        try:
            result = self.current_pet.save_pet()
            self.log_message(result)
            messagebox.showinfo("成功", result)
        except Exception as e:
            messagebox.showerror("错误", f"保存宠物失败: {str(e)}")

    def load_pet_dialog(self):
        """显示加载宠物对话框"""
        # 如果没有已保存的宠物数据文件夹，创建它
        save_dir = "pet_saves"
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
            messagebox.showinfo("提示", "没有找到已保存的宠物！")
            return

        # 获取所有宠物存档文件
        pet_files = [f for f in os.listdir(save_dir) if f.endswith('.json')]
        if not pet_files:
            messagebox.showinfo("提示", "没有找到已保存的宠物！")
            return

        # 创建对话框
        dialog = tk.Toplevel(self.root)
        dialog.title("加载宠物")
        dialog.geometry("400x500")

        # 创建Treeview来显示宠物列表
        columns = ("名称", "品种", "等级", "状态")
        tree = ttk.Treeview(dialog, columns=columns, show="headings")

        # 设置列标题
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        # 加载并显示宠物信息
        for file in pet_files:
            try:
                with open(os.path.join(save_dir, file), 'r', encoding='utf-8') as f:
                    pet_data = json.load(f)
                    # 添加到显示列表
                    tree.insert("", "end", values=(
                        pet_data["name"],
                        pet_data["species"],
                        pet_data["level"],
                        "睡眠中" if pet_data["is_sleeping"] else "清醒"
                    ))
            except Exception as e:
                print(f"加载宠物文件 {file} 时出错: {str(e)}")

        tree.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

        def load_selected_pet():
            """加载选中的宠物"""
            selection = tree.selection()
            if not selection:
                messagebox.showwarning("警告", "请选择一个宠物！")
                return

            # 获取选中的宠物名称
            pet_name = tree.item(selection[0])["values"][0]
            file_name = f"{pet_name}.json"

            try:
                # 读取宠物数据
                with open(os.path.join(save_dir, file_name), 'r', encoding='utf-8') as f:
                    pet_data = json.load(f)

                # 创建新的宠物实例
                pet = Pet(pet_data["name"], pet_data["species"])
                pet.hunger = pet_data["hunger"]
                pet.happiness = pet_data["happiness"]
                pet.energy = pet_data["energy"]
                pet.health = pet_data["health"]
                pet.is_sleeping = pet_data["is_sleeping"]
                pet.level = pet_data["level"]
                pet.experience = pet_data["experience"]

                # 添加到游戏中
                self.game.pets.append(pet)
                self.log_message(f"成功加载宠物 {pet_name}！")
                self.update_pet_list()

                # 关闭对话框
                dialog.destroy()

            except Exception as e:
                messagebox.showerror("错误", f"加载宠物失败: {str(e)}")

        # 加载按钮
        load_button = ttk.Button(dialog, text="加载", command=load_selected_pet)
        load_button.pack(padx=5, pady=5)

        # 取消按钮
        cancel_button = ttk.Button(dialog, text="取消", command=dialog.destroy)
        cancel_button.pack(padx=5, pady=5)

    def create_gui(self):
        # 创建主框架
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 创建菜单
        self.create_menu()

        # 左侧宠物列表
        self.create_pet_list()

        # 中间状态显示
        self.create_status_frame()

        # 右侧操作区
        self.create_action_frame()

        # 底部消息日志
        self.create_message_log()

    def create_menu(self):
        """创建菜单栏"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # 文件菜单
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="新建宠物", command=self.reset_form)
        file_menu.add_command(label="保存宠物", command=self.save_current_pet)
        file_menu.add_command(label="加载宠物", command=self.load_pet_dialog)
        file_menu.add_separator()
        file_menu.add_command(label="保存游戏", command=self.save_game)
        file_menu.add_command(label="加载游戏", command=self.load_game)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.root.quit)

        # 商店菜单
        shop_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="商店", menu=shop_menu)
        shop_menu.add_command(label="购买食物", command=self.show_shop_dialog)
        shop_menu.add_command(label="宠物回购", command=self.show_buyback_dialog)

        contest_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="比赛", menu=contest_menu)
        contest_menu.add_command(label="参加比赛", command=self.show_contest_dialog)
        contest_menu.add_command(label="比赛记录", command=self.show_contest_record)

    def show_contest_record(self):
        """显示比赛记录"""
        dialog = tk.Toplevel(self.root)
        dialog.title("比赛记录")
        dialog.geometry("400x500")

        for contest_type, record in self.game.contest_record.items():
            ttk.Label(dialog, text=f"{contest_type}比赛记录:").pack(padx=5, pady=5)
            for result in record:
                ttk.Label(dialog, text=result).pack(padx=5, pady=2)

    def create_pet_list(self):
        # 宠物列表框架
        pet_list_frame = ttk.LabelFrame(self.main_frame, text="我的宠物", padding="5")
        pet_list_frame.grid(row=0, column=0, rowspan=2, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 宠物列表
        self.pet_listbox = tk.Listbox(pet_list_frame, width=20, height=15)
        self.pet_listbox.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
        self.pet_listbox.bind('<<ListboxSelect>>', self.on_select_pet)

        # 添加宠物按钮
        add_pet_button = ttk.Button(pet_list_frame, text="添加新宠物", command=self.show_add_pet_dialog)
        add_pet_button.pack(padx=5, pady=5, fill=tk.X)

    def create_status_frame(self):
        # 状态显示框架
        self.status_frame = ttk.LabelFrame(self.main_frame, text="宠物状态", padding="5")
        self.status_frame.grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 创建状态标签和进度条
        self.status_vars = {}
        self.status_bars = {}

        status_items = [
            ("等级", "level"),
            ("经验", "experience"),
            ("饥饿度", "hunger"),
            ("心情", "happiness"),
            ("体力", "energy"),
            ("健康", "health")
        ]

        for i, (label, var_name) in enumerate(status_items):
            # 标签
            ttk.Label(self.status_frame, text=label).grid(row=i, column=0, padx=5, pady=2, sticky=tk.W)

            # 变量
            self.status_vars[var_name] = tk.StringVar(value="0")
            ttk.Label(self.status_frame, textvariable=self.status_vars[var_name]).grid(
                row=i, column=1, padx=5, pady=2)

            # 进度条（除了等级外）
            if var_name != "level":
                progress = ttk.Progressbar(self.status_frame, length=200, mode='determinate')
                progress.grid(row=i, column=2, padx=5, pady=2)
                self.status_bars[var_name] = progress

    def create_action_frame(self):
        # 操作区框架
        action_frame = ttk.LabelFrame(self.main_frame, text="操作", padding="5")
        action_frame.grid(row=0, column=2, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 喂食区域
        feed_frame = ttk.LabelFrame(action_frame, text="喂食", padding="5")
        feed_frame.pack(fill=tk.X, padx=5, pady=5)

        self.food_var = tk.StringVar()
        food_combo = ttk.Combobox(feed_frame, textvariable=self.food_var)
        food_combo['values'] = list(self.game.food_inventory.keys())
        food_combo.pack(fill=tk.X, padx=5, pady=2)

        feed_button = ttk.Button(feed_frame, text="喂食", command=self.feed_pet)
        feed_button.pack(fill=tk.X, padx=5, pady=2)

        # 玩耍区域
        play_frame = ttk.LabelFrame(action_frame, text="玩耍", padding="5")
        play_frame.pack(fill=tk.X, padx=5, pady=5)

        self.game_var = tk.StringVar()
        game_combo = ttk.Combobox(play_frame, textvariable=self.game_var)
        game_combo['values'] = ["fetch", "chase", "cuddle"]
        game_combo.pack(fill=tk.X, padx=5, pady=2)

        play_button = ttk.Button(play_frame, text="玩耍", command=self.play_with_pet)
        play_button.pack(fill=tk.X, padx=5, pady=2)

        # 休息区域
        rest_frame = ttk.LabelFrame(action_frame, text="休息", padding="5")
        rest_frame.pack(fill=tk.X, padx=5, pady=5)

        sleep_button = ttk.Button(rest_frame, text="睡觉", command=self.sleep_pet)
        sleep_button.pack(fill=tk.X, padx=5, pady=2)

        wake_button = ttk.Button(rest_frame, text="唤醒", command=self.wake_pet)
        wake_button.pack(fill=tk.X, padx=5, pady=2)

        # 商店区域
        shop_frame = ttk.LabelFrame(action_frame, text="商店", padding="5")
        shop_frame.pack(fill=tk.X, padx=5, pady=5)

        shop_button = ttk.Button(shop_frame, text="购买食物", command=self.show_shop_dialog)
        shop_button.pack(fill=tk.X, padx=5, pady=2)

        sell_button = ttk.Button(shop_frame, text="出售宠物", command=self.sell_pet)
        sell_button.pack(fill=tk.X, padx=5, pady=2)

    def create_message_log(self):
        # 消息日志框架
        log_frame = ttk.LabelFrame(self.main_frame, text="消息日志", padding="5")
        log_frame.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 消息文本框
        self.log_text = tk.Text(log_frame, width=50, height=10, wrap=tk.WORD)
        self.log_text.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

    def log_message(self, message):
        """添加消息到日志"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def update_pet_list(self):
        """更新宠物列表"""
        self.pet_listbox.delete(0, tk.END)
        for pet in self.game.pets:
            self.pet_listbox.insert(tk.END, pet.name)

    def update_status(self):
        """更新状态显示"""
        if self.current_pet:
            self.status_vars["level"].set(str(self.current_pet.level))
            self.status_vars["experience"].set(f"{self.current_pet.experience}/100")
            self.status_vars["hunger"].set(str(self.current_pet.hunger))
            self.status_vars["happiness"].set(str(self.current_pet.happiness))
            self.status_vars["energy"].set(str(self.current_pet.energy))
            self.status_vars["health"].set(str(self.current_pet.health))

            # 更新进度条
            for var_name, bar in self.status_bars.items():
                if var_name == "experience":
                    bar["value"] = self.current_pet.experience
                else:
                    bar["value"] = getattr(self.current_pet, var_name)

    def on_select_pet(self, event):
        """选择宠物时的回调"""
        selection = self.pet_listbox.curselection()
        if selection:
            pet_name = self.pet_listbox.get(selection[0])
            self.current_pet = self.game.find_pet(pet_name)
            self.update_status()

    def show_contest_dialog(self):
        if not self.current_pet:
            messagebox.showwarning("警告", "请先选择一个宠物！")
            return

        if '狗' not in self.current_pet.species and '猫' not in self.current_pet.species:
            messagebox.showwarning("警告", "此宠物不适合参加比赛！")
            return

        if self.game.money < 100:
            messagebox.showwarning("警告", "金币不足！")
            return

        if self.current_pet.is_sleeping:
            messagebox.showwarning("警告", "宠物正在睡觉！")
            return

        self.game.money -= 100
        self.update_status()

        dialog = tk.Toplevel(self.root)
        dialog.title("比赛")
        dialog.geometry("400x500")

        # 选择比赛类型
        contest_var = tk.StringVar()
        contest_combo = ttk.Combobox(dialog, textvariable=contest_var)
        contest_combo['values'] = ["飞盘比赛", "跑步比赛", "护卫比赛", "追踪比赛"] if '狗' in self.current_pet.species else ['跳高比赛', '抓老鼠比赛', '表演比赛']
        contest_combo.pack(padx=5, pady=5)

        # 开始比赛按钮
        start_button = ttk.Button(dialog, text="开始比赛", command=lambda: self.start_contest(contest_var.get()))
        start_button.pack(padx=5, pady=5)

    def start_contest(self, contest_type):
        if self.current_pet.energy < 30:
            messagebox.showwarning("警告", "体力不足！")
            return

        else:
            # 转换到金币范围
            add_money = random.randint(50, 300)
            self.game.money += add_money
            self.current_pet.energy -= 30
            self.log_message(f"{self.current_pet.name}参加了比赛，获得了{add_money}金币！")
            self.update_status()
            self.game.add_record(contest_type, f"{self.current_pet.name}参加了比赛，获得了{add_money}金币！")

    def show_add_pet_dialog(self):
        """显示添加宠物对话框"""
        dialog = tk.Toplevel(self.root)
        dialog.title("添加新宠物")
        dialog.geometry("300x200")

        ttk.Label(dialog, text="宠物名称:").pack(padx=5, pady=5)
        name_entry = ttk.Entry(dialog)
        name_entry.pack(padx=5, pady=5)

        ttk.Label(dialog, text="宠物品种:").pack(padx=5, pady=5)
        species_var = tk.StringVar()
        species_combo = ttk.Combobox(dialog, textvariable=species_var)
        species_combo['values'] = ["猫咪", "小狗", "兔子", "仓鼠"]
        species_combo.pack(padx=5, pady=5)

        def add_pet():
            name = name_entry.get()
            species = species_var.get()
            if name and species:
                result = self.game.add_pet(name, species)
                self.log_message(result)
                self.update_pet_list()
                dialog.destroy()
            else:
                messagebox.showwarning("警告", "请填写完整信息！")

        ttk.Button(dialog, text="添加", command=add_pet).pack(padx=5, pady=20)

    def show_shop_dialog(self):
        """显示商店对话框"""
        dialog = tk.Toplevel(self.root)
        dialog.title("商店")
        dialog.geometry("400x500")

        # 显示当前金币
        money_label = ttk.Label(dialog, text=f"当前金币: {self.game.money}")
        money_label.pack(padx=5, pady=5)

        shop_frame = ttk.Frame(dialog)
        shop_frame.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

        # 添加商品
        row = 0
        quantity_vars = {}
        for food_type, price in self.game.food_prices.items():
            ttk.Label(shop_frame, text=food_type).grid(row=row, column=0, padx=5, pady=2)
            ttk.Label(shop_frame, text=f"价格: {price}").grid(row=row, column=1, padx=5, pady=2)

            quantity_vars[food_type] = tk.StringVar(value="0")
            ttk.Entry(shop_frame, textvariable=quantity_vars[food_type], width=5).grid(
                row=row, column=2, padx=5, pady=2)

            ttk.Label(shop_frame, text=f"库存: {self.game.food_inventory[food_type]}").grid(
                row=row, column=3, padx=5, pady=2)

            row += 1

        def buy_items():
            total_cost = 0
            items_to_buy = {}

            for food_type, var in quantity_vars.items():
                try:
                    quantity = int(var.get())
                    if quantity > 0:
                        items_to_buy[food_type] = quantity
                        total_cost += self.game.food_prices[food_type] * quantity
                except ValueError:
                    continue

            if not items_to_buy:
                messagebox.showwarning("警告", "请选择要购买的物品！")
                return

            if total_cost > self.game.money:
                messagebox.showwarning("警告", "金币不足！")
                return

            # 执行购买
            for food_type, quantity in items_to_buy.items():
                result = self.game.buy_food(food_type, quantity)
                self.log_message(result)

            money_label.config(text=f"当前金币: {self.game.money}")

            # 更新库存显示
            for widget in shop_frame.winfo_children():
                if isinstance(widget, ttk.Label) and "库存:" in widget.cget("text"):
                    food = widget.cget("text").split("库存:")[0].strip()
                    widget.config(text=f"库存: {self.game.food_inventory[food]}")

        # 购买按钮
        ttk.Button(dialog, text="购买", command=buy_items).pack(padx=5, pady=10)

    def show_buyback_dialog(self):
        """显示宠物回购对话框"""
        if not self.game.sold_pets:
            messagebox.showinfo("提示", "没有可回购的宠物！")
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("宠物回购")
        dialog.geometry("400x500")

        # 显示当前金币
        money_label = ttk.Label(dialog, text=f"当前金币: {self.game.money}")
        money_label.pack(padx=5, pady=5)

        # 创建已售出宠物列表
        list_frame = ttk.Frame(dialog)
        list_frame.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

        # 列表标题
        columns = ("名称", "品种", "等级", "价格")
        tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        # 添加宠物数据
        for pet in self.game.sold_pets:
            value = pet.calculate_value()
            tree.insert("", "end", values=(pet.name, pet.species, pet.level, value))

        tree.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

        def buy_back():
            selection = tree.selection()
            if not selection:
                messagebox.showwarning("警告", "请选择要回购的宠物！")
                return

            pet_name = tree.item(selection[0])["values"][0]
            result = self.game.buy_back_pet(pet_name)
            self.log_message(result)

            if "回购了" in result:
                self.update_pet_list()
                money_label.config(text=f"当前金币: {self.game.money}")
                # 从列表中移除
                tree.delete(selection[0])
                if not tree.get_children():
                    dialog.destroy()

            messagebox.showinfo("提示", result)

        # 回购按钮
        ttk.Button(dialog, text="回购", command=buy_back).pack(padx=5, pady=10)

    def feed_pet(self):
        """喂食宠物"""
        if not self.current_pet:
            messagebox.showwarning("警告", "请先选择一个宠物！")
            return

        food_type = self.food_var.get()
        if not food_type:
            messagebox.showwarning("警告", "请选择食物！")
            return

        if self.game.food_inventory[food_type] <= 0:
            messagebox.showwarning("警告", "食物不足，请购买更多！")
            return

        self.game.food_inventory[food_type] -= 1
        result = self.current_pet.feed(food_type)
        self.log_message(result)
        self.update_status()

    def play_with_pet(self):
        """和宠物玩耍"""
        if not self.current_pet:
            messagebox.showwarning("警告", "请先选择一个宠物！")
            return

        game_type = self.game_var.get()
        if not game_type:
            messagebox.showwarning("警告", "请选择游戏！")
            return

        result = self.current_pet.play(game_type)
        self.log_message(result)
        self.update_status()

    def sleep_pet(self):
        """让宠物睡觉"""
        if not self.current_pet:
            messagebox.showwarning("警告", "请先选择一个宠物！")
            return

        result = self.current_pet.sleep()
        self.log_message(result)
        self.update_status()

    def wake_pet(self):
        """唤醒宠物"""
        if not self.current_pet:
            messagebox.showwarning("警告", "请先选择一个宠物！")
            return

        result = self.current_pet.wake_up()
        self.log_message(result)
        self.update_status()

    def sell_pet(self):
        """出售宠物"""
        if not self.current_pet:
            messagebox.showwarning("警告", "请先选择一个宠物！")
            return

        if messagebox.askyesno("确认", f"确定要出售{self.current_pet.name}吗？"):
            result = self.game.sell_pet(self.current_pet.name)
            self.log_message(result)
            self.current_pet = None
            self.update_pet_list()
            self.update_status()

    def save_game(self):
        """保存游戏"""
        result = self.game.save_game()
        self.log_message(result)
        messagebox.showinfo("提示", result)

    def load_game(self):
        """加载游戏"""
        if messagebox.askyesno("确认", "加载游戏将覆盖当前进度，是否继续？"):
            result = self.game.load_game()
            self.log_message(result)
            self.update_pet_list()
            self.update_status()
            messagebox.showinfo("提示", result)

    def reset_form(self):
        """重置表单"""
        self.current_pet = None
        self.update_pet_list()
        self.update_status()


def main():
    root = tk.Tk()
    game = PetGame()
    app = PetGameGUI(root, game)
    root.mainloop()

if __name__ == "__main__":
    main()