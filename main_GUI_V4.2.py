import random  # 用于随机数生成
import time    # 用于时间戳
import json    # 用于存档数据序列化
import os      # 用于文件和目录操作
from datetime import datetime, timedelta
from typing import List, Optional, Dict, TypedDict, Tuple  # 用于类型提示
from enum import Enum, auto  # 用于枚举类型
from dataclasses import dataclass  # 用于数据类
import tkinter as tk
from tkinter import ttk, messagebox


class Pet:
    """增强的宠物类,包含更多属性和功能"""

    # 定义宠物品种的基础属性
    SPECIES_BASE_STATS = {
        "猫咪": {
            "health": 100,
            "strength": 70,
            "agility": 90,
            "intelligence": 85,
            "growth_rate": 1.2
        },
        "小狗": {
            "health": 120,
            "strength": 85,
            "agility": 80,
            "intelligence": 75,
            "growth_rate": 1.1
        },
        "兔子": {
            "health": 80,
            "strength": 50,
            "agility": 95,
            "intelligence": 70,
            "growth_rate": 1.0
        },
        "仓鼠": {
            "health": 60,
            "strength": 40,
            "agility": 85,
            "intelligence": 65,
            "growth_rate": 0.9
        }
    }

    def __init__(self, name: str, species: str):
        """初始化宠物"""
        self.name = name
        self.species = species
        self.level = 1
        self.experience = 0

        # 基础属性
        base_stats = self.SPECIES_BASE_STATS[species]
        self.health = base_stats["health"]
        self.strength = base_stats["strength"]
        self.agility = base_stats["agility"]
        self.intelligence = base_stats["intelligence"]
        self.growth_rate = base_stats["growth_rate"]

        # 状态属性
        self.hunger = 50
        self.happiness = 50
        self.energy = 100
        self.mood = "正常"
        self.is_sleeping = False

        # 技能相关
        self.skills: List[str] = []
        self.skill_exp: Dict[str, int] = {}

        # 记录数据
        self.birth_time = time.time()
        self.last_feed_time = time.time()
        self.last_interaction_time = time.time()
        self.total_training_time = 0

        # 成就数据
        self.won_contests = 0
        self.total_training_sessions = 0
        self.friends: List[str] = []

    def feed(self, food_type: str) -> str:
        """喂食系统"""
        foods = {
            "regular_food": {"hunger": 30, "health": 5, "exp": 10},
            "premium_food": {"hunger": 50, "health": 10, "exp": 20},
            "treats": {"hunger": 10, "health": 0, "exp": 5, "happiness": 15},
            "fresh_meat": {"hunger": 40, "health": 15, "exp": 25},
            "fish": {"hunger": 35, "health": 12, "exp": 22},
            "vegetables": {"hunger": 25, "health": 8, "exp": 15},
            "fruits": {"hunger": 20, "health": 10, "exp": 18},
            "special_meal": {"hunger": 60, "health": 20, "exp": 30}
        }

        if food_type not in foods:
            return f"{self.name}对这个食物不感兴趣..."

        food = foods[food_type]

        # 计算食物效果
        hunger_reduction = food["hunger"] * self.growth_rate
        exp_gain = food["exp"]
        happiness_gain = food.get("happiness", 5)

        # 更新状态
        self.hunger = max(0, min(100, self.hunger - hunger_reduction))
        self.health = min(100, self.health + food["health"])
        self.happiness = min(100, self.happiness + happiness_gain)
        self.gain_experience(exp_gain)

        # 更新时间和心情
        self.last_feed_time = time.time()
        self.update_mood()

        return f"{self.name}吃了{food_type},看起来很满意! (获得{exp_gain}经验)"

    def gain_experience(self, exp: int) -> None:
        """获得经验值"""
        self.experience += exp
        while self.experience >= self.get_exp_needed():
            self.level_up()

    def get_exp_needed(self) -> int:
        """计算升级所需经验"""
        return int(100 * (1 + (self.level - 1) * 0.5))

    def level_up(self) -> str:
        """升级"""
        if self.level >= 100:
            return f"{self.name}已达到最高等级!"

        self.level += 1
        self.experience = 0

        # 属性提升
        growth = self.growth_rate
        self.health += 5 * growth
        self.strength += 3 * growth
        self.agility += 3 * growth
        self.intelligence += 3 * growth

        # 解锁新技能
        if self.level in [5, 10, 15, 20, 30]:
            new_skill = self.unlock_skill()
            return f"{self.name}升到{self.level}级了！学会了新技能: {new_skill}!"

        return f"{self.name}升到{self.level}级了！"

    def unlock_skill(self) -> str:
        """解锁新技能"""
        species_skills = {
            "猫咪": ["灵巧跳跃", "夜视能力", "优雅姿态", "捕猎技巧", "九命"],
            "小狗": ["忠诚守护", "寻物技能", "游泳技巧", "救援能力", "领袖气质"],
            "兔子": ["快速跳跃", "挖掘技能", "隐藏技巧", "萝卜探测", "群体治愈"],
            "仓鼠": ["储物技能", "迷宫记忆", "平衡行走", "食物探索", "团队协作"]
        }

        available_skills = [s for s in species_skills[self.species] if s not in self.skills]
        if available_skills:
            new_skill = random.choice(available_skills)
            self.skills.append(new_skill)
            self.skill_exp[new_skill] = 0
            return new_skill
        return "没有新技能可以学习"

    def train_skill(self, skill_name: str) -> str:
        """训练特定技能"""
        if skill_name not in self.skills:
            return f"{self.name}还没有学会这个技能"

        if self.energy < 20:
            return f"{self.name}太累了,需要休息"

        # 训练消耗和收益
        self.energy -= 20
        exp_gain = random.randint(10, 20)
        self.skill_exp[skill_name] += exp_gain
        self.total_training_time += 1
        self.total_training_sessions += 1

        return f"{self.name}训练了{skill_name},熟练度提升{exp_gain}点"

    def update_mood(self) -> None:
        """更新心情状态"""
        current_time = time.time()
        hours_since_feed = (current_time - self.last_feed_time) / 3600
        hours_since_interaction = (current_time - self.last_interaction_time) / 3600

        if self.hunger > 80:
            self.mood = "饥饿"
        elif self.energy < 20:
            self.mood = "疲惫"
        elif hours_since_interaction > 24:
            self.mood = "孤独"
        elif self.happiness < 30:
            self.mood = "沮丧"
        elif self.happiness > 80:
            self.mood = "兴奋"
        else:
            self.mood = "正常"

    def check_status(self) -> str:
        """检查宠物状态"""
        skills_str = "、".join(self.skills) if self.skills else "暂无"
        skill_levels = "\\n".join(
            [f"{skill}: 熟练度 {exp}" for skill, exp in self.skill_exp.items()]) if self.skill_exp else "暂无"

        return f"""
{self.name}的状态:
品种: {self.species}
等级: {self.level} ({self.experience}/{self.get_exp_needed()})
属性:
  生命: {self.health}
  力量: {self.strength}
  敏捷: {self.agility}
  智力: {self.intelligence}
基础状态:
  饥饿度: {self.hunger}/100
  心情: {self.happiness}/100
  体力: {self.energy}/100
  状态: {'睡眠中' if self.is_sleeping else '清醒'}
  当前心情: {self.mood}
已学技能: {skills_str}
技能熟练度:
{skill_levels}
训练总次数: {self.total_training_sessions}
比赛获胜: {self.won_contests}次
年龄: {int((time.time() - self.birth_time) / 86400)}天
"""

    def get_status(self) -> dict:
        """获取宠物完整状态"""
        return {
            "name": self.name,
            "species": self.species,
            "level": self.level,
            "experience": self.experience,
            "exp_needed": self.get_exp_needed(),
            "health": self.health,
            "strength": self.strength,
            "agility": self.agility,
            "intelligence": self.intelligence,
            "hunger": self.hunger,
            "happiness": self.happiness,
            "energy": self.energy,
            "mood": self.mood,
            "is_sleeping": self.is_sleeping,
            "skills": self.skills,
            "skill_levels": self.skill_exp,
            "age_days": int((time.time() - self.birth_time) / 86400),
            "total_training": self.total_training_sessions,
            "contests_won": self.won_contests
        }

    def sleep(self) -> str:
        """睡眠"""
        if self.is_sleeping:
            return f"{self.name}已经在睡觉了"

        self.is_sleeping = True
        self.energy = min(100, self.energy + 50)
        self.health = min(100, self.health + 10)
        return f"{self.name}睡着了,开始恢复体力"

    def wake_up(self) -> str:
        """唤醒"""
        if not self.is_sleeping:
            return f"{self.name}已经醒着呢"

        self.is_sleeping = False
        return f"{self.name}醒来了,精神焕发!"

    def save_pet(self, save_dir="pet_saves"):
        """保存宠物数据到文件"""
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        pet_data = {
            "name": self.name,
            "species": self.species,
            "level": self.level,
            "experience": self.experience,
            "health": self.health,
            "strength": self.strength,
            "agility": self.agility,
            "intelligence": self.intelligence,
            "hunger": self.hunger,
            "happiness": self.happiness,
            "energy": self.energy,
            "mood": self.mood,
            "is_sleeping": self.is_sleeping,
            "skills": self.skills,
            "skill_exp": self.skill_exp,
            "birth_time": self.birth_time,
            "last_feed_time": self.last_feed_time,
            "last_interaction_time": self.last_interaction_time,
            "total_training_time": self.total_training_time,
            "total_training_sessions": self.total_training_sessions,
            "won_contests": self.won_contests,
            "friends": self.friends
        }

        file_path = os.path.join(save_dir, f"{self.name}.json")
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(pet_data, f, ensure_ascii=False, indent=4)

        return f"宠物 {self.name} 已保存到 {file_path}"

    def calculate_value(self) -> int:
        """计算宠物价值"""
        # 基础价值
        base_value = 1000

        # 等级加成
        level_bonus = self.level * 200

        # 属性加成
        stats_bonus = (self.health + self.strength + self.agility + self.intelligence) * 10

        # 技能加成
        skill_bonus = len(self.skills) * 500
        skill_exp_bonus = sum(self.skill_exp.values()) * 2

        # 成就加成
        achievement_bonus = (self.won_contests * 300 +
                             self.total_training_sessions * 50)

        # 品种成长率加成
        growth_bonus = int(1000 * self.growth_rate)

        total_value = (base_value + level_bonus + stats_bonus +
                       skill_bonus + skill_exp_bonus +
                       achievement_bonus + growth_bonus)

        return total_value

    def play(self, game_type: str) -> str:
        """玩耍活动"""
        if self.energy < 20:
            return f"{self.name}太累了,需要休息"

        games = {
            "fetch": {"energy": -20, "happiness": 30, "exp": 15},
            "chase": {"energy": -30, "happiness": 40, "exp": 20},
            "hide_seek": {"energy": -25, "happiness": 35, "exp": 18},
            "training": {"energy": -35, "happiness": 25, "exp": 25}
        }

        if game_type not in games:
            return "没有这种游戏..."

        game = games[game_type]
        self.energy = max(0, self.energy + game["energy"])
        self.happiness = min(100, self.happiness + game["happiness"])
        self.gain_experience(game["exp"])
        self.last_interaction_time = time.time()

        return f"{self.name}玩得很开心! (获得{game['exp']}经验)"

class DailyTasks:
    """每日任务系统"""
    def __init__(self):
        self.tasks = {
            "遛宠物": {"completed": False, "reward": 50, "description": "免费活动：带宠物散步"},
            "清理": {"completed": False, "reward": 30, "description": "免费活动：打扫宠物窝"},
            "训练": {"completed": False, "reward": 40, "description": "基础训练（无需道具）"},
            "社交": {"completed": False, "reward": 35, "description": "与其他宠物互动"}
        }
        self.last_refresh = datetime.now()

    def refresh_tasks(self):
        """刷新每日任务"""
        now = datetime.now()
        if (now - self.last_refresh).days >= 1:
            for task in self.tasks.values():
                task["completed"] = False
            self.last_refresh = now

    def complete_task(self, task_name: str) -> tuple[bool, int]:
        """完成任务"""
        if task_name in self.tasks and not self.tasks[task_name]["completed"]:
            self.tasks[task_name]["completed"] = True
            return True, self.tasks[task_name]["reward"]
        return False, 0

class PetGame:
    def __init__(self):
        self.daily_tasks = DailyTasks()
        self.pets = []  # 当前宠物列表
        self.sold_pets = []  # 已售出宠物
        self.money = 1000

        # 商店系统
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

        # 商店物品
        self.items_inventory = {
            "toy_ball": 2,  # 玩具球
            "pet_bed": 1,  # 宠物床
            "training_book": 1,  # 训练手册
            "medicine": 3,  # 药品
            "grooming_kit": 1,  # 美容套装
            "vitamins": 2  # 营养剂
        }

        self.items_prices = {
            "toy_ball": 100,
            "pet_bed": 200,
            "training_book": 300,
            "medicine": 150,
            "grooming_kit": 250,
            "vitamins": 120
        }

        # 比赛记录
        self.contest_record = {}

        # 商店折扣活动
        self.current_discounts = {}

        # 每日任务
        self.daily_tasks = []
        self.task_rewards = {}

    def add_pet(self, name: str, species: str) -> str:
        """添加新宠物"""
        # 检查名称是否已存在
        if any(pet.name == name for pet in self.pets):
            return "这个名字已经被使用了!"

        if species not in Pet.SPECIES_BASE_STATS:
            return "不支持的宠物品种!"

        new_pet = Pet(name, species)
        self.pets.append(new_pet)
        return f"欢迎{name}加入家族!"

    def find_pet(self, name: str) -> Optional[Pet]:
        """查找特定宠物"""
        for pet in self.pets:
            if pet.name == name:
                return pet
        return None

    def buy_food(self, food_type: str, quantity: int) -> str:
        """购买食物"""
        if food_type not in self.food_prices:
            return "没有这种食物..."

        total_cost = self.food_prices[food_type] * quantity

        # 检查折扣
        if food_type in self.current_discounts:
            discount = self.current_discounts[food_type]
            total_cost = int(total_cost * (1 - discount))

        if self.money >= total_cost:
            self.money -= total_cost
            self.food_inventory[food_type] += quantity
            return f"购买了{quantity}份{food_type},花费{total_cost}金币,剩余金币:{self.money}"
        return "金币不足..."

    def buy_item(self, item_type: str, quantity: int) -> str:
        """购买物品"""
        if item_type not in self.items_prices:
            return "商店没有这件物品..."

        total_cost = self.items_prices[item_type] * quantity

        # 检查折扣
        if item_type in self.current_discounts:
            discount = self.current_discounts[item_type]
            total_cost = int(total_cost * (1 - discount))

        if self.money >= total_cost:
            self.money -= total_cost
            self.items_inventory[item_type] += quantity
            return f"购买了{quantity}个{item_type},花费{total_cost}金币,剩余金币:{self.money}"
        return "金币不足..."

    def sell_pet(self, name: str) -> str:
        """出售宠物"""
        pet = self.find_pet(name)
        if not pet:
            return "找不到这个宠物..."

        value = pet.calculate_value()
        self.money += value
        self.pets.remove(pet)
        self.sold_pets.append(pet)
        return f"你出售了{pet.name},获得{value}金币! 当前金币:{self.money}"

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
                return "金币不足,无法回购..."
        return "找不到这个宠物..."

    def use_item(self, item_type: str, pet_name: str) -> str:
        """使用物品"""
        if item_type not in self.items_inventory:
            return "没有这个物品..."

        if self.items_inventory[item_type] <= 0:
            return "物品数量不足..."

        pet = self.find_pet(pet_name)
        if not pet:
            return "找不到这个宠物..."

        # 物品效果
        effects = {
            "toy_ball": {"happiness": 20, "energy": -10},
            "pet_bed": {"energy": 90, "health": 10},
            "training_book": {"experience": 50},
            "medicine": {"health": 30},
            "grooming_kit": {"happiness": 30, "health": -10},
            "vitamins": {"health": 15, "energy": 15}
        }

        effect = effects[item_type]
        self.items_inventory[item_type] -= 1

        # 应用效果
        for stat, value in effect.items():
            if stat == "experience":
                pet.gain_experience(value)
            elif stat == "happiness":
                pet.happiness = min(100, pet.happiness + value)
            elif stat == "energy":
                pet.energy = min(100, pet.energy + value)
            elif stat == "health":
                pet.health = min(100, pet.health + value)

        return f"对{pet_name}使用了{item_type},状态得到改善!"

    def check_inventory(self) -> str:
        """查看库存"""
        inventory_str = "\n当前库存:"

        inventory_str += "\n食物:"
        for food, amount in self.food_inventory.items():
            price = self.food_prices[food]
            if food in self.current_discounts:
                price = int(price * (1 - self.current_discounts[food]))
            inventory_str += f"\n{food}: {amount}份 (价格:{price}金币/份)"

        inventory_str += "\n\n物品:"
        for item, amount in self.items_inventory.items():
            price = self.items_prices[item]
            if item in self.current_discounts:
                price = int(price * (1 - self.current_discounts[item]))
            inventory_str += f"\n{item}: {amount}个 (价格:{price}金币/个)"

        inventory_str += f"\n\n金币: {self.money}"
        return inventory_str

    def generate_daily_tasks(self):
        """生成每日任务"""
        self.daily_tasks = [
            {"type": "feeding", "target": 3, "reward": 100},
            {"type": "training", "target": 2, "reward": 150},
            {"type": "playing", "target": 2, "reward": 100},
            {"type": "contest", "target": 1, "reward": 200}
        ]
        self.task_rewards = {task["type"]: False for task in self.daily_tasks}

    def check_task_completion(self, task_type: str) -> Optional[int]:
        """检查任务完成情况并发放奖励"""
        if task_type in self.task_rewards and not self.task_rewards[task_type]:
            for task in self.daily_tasks:
                if task["type"] == task_type:
                    self.task_rewards[task_type] = True
                    self.money += task["reward"]
                    return task["reward"]
        return None

    def save_game(self, filename="game_save.json"):
        """保存游戏状态"""
        save_data = {
            "money": self.money,
            "food_inventory": self.food_inventory,
            "items_inventory": self.items_inventory,
            "pets": [],
            "sold_pets": [],
            "contest_record": self.contest_record,
            "current_discounts": self.current_discounts
        }

        # 保存当前宠物数据
        for pet in self.pets:
            pet_data = pet.get_status()
            save_data["pets"].append(pet_data)

        # 保存已售出宠物数据
        for pet in self.sold_pets:
            pet_data = pet.get_status()
            save_data["sold_pets"].append(pet_data)

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
            self.items_inventory = save_data["items_inventory"]
            self.current_discounts = save_data["current_discounts"]

            # 恢复宠物
            self.pets = []
            for pet_data in save_data["pets"]:
                pet = Pet(pet_data["name"], pet_data["species"])
                # 恢复宠物所有属性
                for key, value in pet_data.items():
                    if hasattr(pet, key):
                        setattr(pet, key, value)
                self.pets.append(pet)

            # 恢复已售出宠物
            self.sold_pets = []
            for pet_data in save_data["sold_pets"]:
                pet = Pet(pet_data["name"], pet_data["species"])
                for key, value in pet_data.items():
                    if hasattr(pet, key):
                        setattr(pet, key, value)
                self.sold_pets.append(pet)

            self.contest_record = save_data["contest_record"]

            return "游戏已加载"
        except Exception as e:
            return f"加载游戏失败: {str(e)}"


class ContestType(Enum):
    """比赛类型枚举"""
    AGILITY = "敏捷竞速"
    STRENGTH = "力量比拼"
    INTELLIGENCE = "智力竞赛"
    TALENT = "才艺表演"
    BEAUTY = "美容大赛"


class ContestDifficulty(Enum):
    """比赛难度枚举"""
    EASY = ("新手赛", 1.0)
    NORMAL = ("普通赛", 1.5)
    HARD = ("精英赛", 2.0)
    MASTER = ("大师赛", 3.0)


class ContestReward(TypedDict):
    """比赛奖励类型定义"""
    money: int
    exp: int
    items: Dict[str, int]

class ContestSystem:
    """宠物比赛系统"""

    def __init__(self):
        self.available_contests: List[Dict] = []
        self.refresh_time = datetime.now()
        self.refresh_contests()

    def refresh_contests(self):
        """刷新可参加的比赛"""
        self.available_contests.clear()
        # 为每个难度创建一个比赛
        for difficulty in ContestDifficulty:
            contest_type = random.choice(list(ContestType))
            self.available_contests.append({
                'type': contest_type,
                'difficulty': difficulty,
                'rewards': self._generate_rewards(difficulty),
                'min_level': self._get_min_level(difficulty),
                'entry_fee': self._get_entry_fee(difficulty)
            })

    def _generate_rewards(self, difficulty: ContestDifficulty) -> ContestReward:
        """生成比赛奖励"""
        difficulty_multiplier = difficulty.value[1]
        return {
            'money': int(100 * difficulty_multiplier),
            'exp': int(50 * difficulty_multiplier),
            'items': self._generate_item_rewards(difficulty)
        }

    def _generate_item_rewards(self, difficulty: ContestDifficulty) -> Dict[str, int]:
        """生成物品奖励"""
        items = {}
        if random.random() < 0.3:
            items['premium_food'] = random.randint(1, int(3 * difficulty.value[1]))
        if random.random() < 0.2:
            items['special_meal'] = random.randint(1, int(2 * difficulty.value[1]))
        return items

    def _get_min_level(self, difficulty: ContestDifficulty) -> int:
        """获取参赛最低等级要求"""
        return {
            ContestDifficulty.EASY: 1,
            ContestDifficulty.NORMAL: 5,
            ContestDifficulty.HARD: 15,
            ContestDifficulty.MASTER: 30
        }[difficulty]

    def _get_entry_fee(self, difficulty: ContestDifficulty) -> int:
        """获取参赛费用"""
        return {
            ContestDifficulty.EASY: 50,
            ContestDifficulty.NORMAL: 100,
            ContestDifficulty.HARD: 200,
            ContestDifficulty.MASTER: 500
        }[difficulty]

    def enter_contest(self, pet: Pet, contest_index: int) -> Tuple[bool, str, Optional[ContestReward]]:
        """参加比赛"""
        if contest_index >= len(self.available_contests):
            return False, "无效的比赛索引", None

        contest = self.available_contests[contest_index]

        # 检查等级要求
        if pet.level < self._get_min_level(contest['difficulty']):
            return False, f"宠物等级不足，需要{self._get_min_level(contest['difficulty'])}级", None

        # 检查体力
        if pet.energy < 30:
            return False, "体力不足，需要休息", None

        # 计算比赛结果
        result = self._calculate_contest_result(pet, contest)

        # 消耗体力
        pet.energy -= 30

        if result:
            pet.won_contests += 1
            return True, "比赛胜利！", contest['rewards']
        else:
            return False, "比赛失败，再接再厉！", None

    def _calculate_contest_result(self, pet: Pet, contest: Dict) -> bool:
        """计算比赛结果"""
        # 基础胜率计算
        base_chance = self._calculate_base_chance(pet, contest)

        # 技能加成
        skill_bonus = self._calculate_skill_bonus(pet, contest['type'])

        # 最终胜率
        final_chance = min(0.95, base_chance + skill_bonus)

        return random.random() < final_chance

    def _calculate_base_chance(self, pet: Pet, contest: Dict) -> float:
        """计算基础胜率"""
        contest_type = contest['type']
        difficulty_multiplier = contest['difficulty'].value[1]

        # 根据比赛类型选择相关属性
        attribute_value = {
            ContestType.AGILITY: pet.agility,
            ContestType.STRENGTH: pet.strength,
            ContestType.INTELLIGENCE: pet.intelligence,
            ContestType.TALENT: (pet.intelligence + pet.agility) / 2,
            ContestType.BEAUTY: pet.happiness
        }[contest_type]

        # 基础胜率计算
        base_chance = 0.5 + (attribute_value / 200) - (0.1 * difficulty_multiplier)
        return max(0.1, min(0.9, base_chance))

    def _calculate_skill_bonus(self, pet: Pet, contest_type: ContestType) -> float:
        """计算技能加成"""
        relevant_skills = {
            ContestType.AGILITY: ["灵巧跳跃", "快速跳跃"],
            ContestType.STRENGTH: ["忠诚守护", "救援能力"],
            ContestType.INTELLIGENCE: ["夜视能力", "迷宫记忆"],
            ContestType.TALENT: ["优雅姿态", "团队协作"],
            ContestType.BEAUTY: ["优雅姿态", "九命"]
        }

        bonus = 0.0
        for skill in pet.skills:
            if skill in relevant_skills[contest_type]:
                skill_level = pet.skill_exp.get(skill, 0) / 1000  # 假设1000为最高熟练度
                bonus += 0.05 * skill_level

        return min(0.2, bonus)  # 最高20%技能加成

class PetGameGUI:
    def __init__(self, root, game):
        self.root = root
        self.root.title("宠物养成游戏")
        self.root.geometry("1200x800")

        self.game = game
        self.current_pet = None

        # 创建主界面
        self.create_gui()

        self.start_display_updates()

        # 初始化每日任务
        self.game.generate_daily_tasks()

        # 启动定时任务
        self.start_timers()

    def start_timers(self):
        """启动定时任务"""

        def update_pets():
            # 定期更新所有宠物状态
            for pet in self.game.pets:
                pet.update_mood()
            # 如果有当前选中的宠物，更新其显示
            if self.current_pet:
                self.update_status()
            self.root.after(1000, update_pets)  # 每分钟更新一次

        update_pets()

    def create_gui(self):
        # 创建主框架
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 创建菜单
        self.create_menu()

        # 创建标签页控件
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 创建各个标签页
        self.create_main_tab()  # 主要信息标签页
        self.create_shop_tab()  # 商店标签页
        self.create_contest_tab()  # 比赛标签页
        self.create_task_tab()  # 任务标签页

    def create_menu(self):
        """创建菜单栏"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # 文件菜单
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="新建宠物", command=self.show_add_pet_dialog)
        file_menu.add_command(label="保存宠物", command=self.save_current_pet)
        file_menu.add_command(label="加载宠物", command=self.load_pet_dialog)
        file_menu.add_separator()
        file_menu.add_command(label="保存游戏", command=self.save_game)
        file_menu.add_command(label="加载游戏", command=self.load_game)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.root.quit)

        # 功能菜单
        function_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="功能", menu=function_menu)
        function_menu.add_command(label="宠物训练", command=self.show_training_dialog)
        function_menu.add_command(label="宠物社交", command=self.show_social_dialog)
        function_menu.add_command(label="宠物技能", command=self.show_skills_dialog)
        function_menu.add_command(label="成就查看", command=self.show_achievements_dialog)

    def perform_free_activity(self, activity_type: str) -> str:
        """执行免费活动"""
        if not self.current_pet:
            return "请先选择一个宠物！"

        activities = {
            "遛宠物": {
                "energy_cost": 10,
                "happiness_gain": 15,
                "exp_gain": 10,
                "coin_gain": 20
            },
            "清理": {
                "energy_cost": 5,
                "happiness_gain": 10,
                "exp_gain": 5,
                "coin_gain": 15
            },
            "基础训练": {
                "energy_cost": 15,
                "happiness_gain": 5,
                "exp_gain": 15,
                "coin_gain": 25
            }
        }

        if activity_type not in activities:
            return "无效的活动类型"

        activity = activities[activity_type]

        # 检查体力
        if self.current_pet.energy < activity["energy_cost"]:
            return f"{self.current_pet.name}太累了，需要休息"

        # 执行活动
        self.current_pet.energy -= activity["energy_cost"]
        self.current_pet.happiness = min(100, self.current_pet.happiness + activity["happiness_gain"])
        self.current_pet.gain_experience(activity["exp_gain"])
        self.game.money += activity["coin_gain"]

        # 尝试完成每日任务
        success, bonus = self.game.daily_tasks.complete_task(activity_type)
        if success:
            self.game.money += bonus
            return f"{self.current_pet.name}完成了{activity_type}！获得{activity['coin_gain']}金币和{bonus}金币的任务奖励！"

        return f"{self.current_pet.name}完成了{activity_type}！获得{activity['coin_gain']}金币！"

    def create_main_tab(self):
        """创建主要信息标签页"""
        main_tab = ttk.Frame(self.notebook)
        self.notebook.add(main_tab, text="主页")

        # 使用grid布局管理器
        # 列的权重设置
        main_tab.grid_columnconfigure(1, weight=1)
        main_tab.grid_columnconfigure(2, weight=1)

        # 左侧宠物列表
        pet_list_frame = ttk.LabelFrame(main_tab, text="我的宠物", padding="5")
        pet_list_frame.grid(row=0, column=0, rowspan=3, padx=5, pady=5, sticky="nsew")

        self.pet_listbox = tk.Listbox(pet_list_frame, width=20, height=15)
        self.pet_listbox.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.pet_listbox.bind('<<ListboxSelect>>', self.on_select_pet)

        # 添加宠物按钮
        add_pet_button = ttk.Button(pet_list_frame, text="添加新宠物",
                                    command=self.show_add_pet_dialog)
        add_pet_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        # 中间状态显示
        self.create_status_frame(main_tab)

        # 右侧操作区
        self.create_action_frame(main_tab)

        # 免费活动区域
        activities_frame = ttk.LabelFrame(main_tab, text="免费活动", padding="5")
        activities_frame.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="nsew")

        # 免费活动按钮
        walk_button = ttk.Button(activities_frame, text="遛宠物 (获得20金币)",
                                 command=lambda: self.perform_free_activity("遛宠物"))
        walk_button.grid(row=0, column=0, padx=5, pady=2, sticky="ew")

        clean_button = ttk.Button(activities_frame, text="清理 (获得15金币)",
                                  command=lambda: self.perform_free_activity("清理"))
        clean_button.grid(row=1, column=0, padx=5, pady=2, sticky="ew")

        train_button = ttk.Button(activities_frame, text="基础训练 (获得25金币)",
                                  command=lambda: self.perform_free_activity("基础训练"))
        train_button.grid(row=2, column=0, padx=5, pady=2, sticky="ew")

        # 每日任务状态显示
        self.daily_tasks_text = tk.Text(activities_frame, height=6, width=40)
        self.daily_tasks_text.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")

        # 底部消息日志
        self.create_message_log(main_tab)

        # 配置grid的行和列权重
        activities_frame.grid_columnconfigure(0, weight=1)
        for i in range(4):
            activities_frame.grid_rowconfigure(i, weight=1)

    def create_status_frame(self, parent):
        """创建状态显示框架"""
        self.status_frame = ttk.LabelFrame(parent, text="宠物状态", padding="5")
        self.status_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        # 状态标签和进度条的创建使用grid而不是pack
        self.status_labels = {}
        self.status_bars = {}

        status_items = [
            ("等级", "level"),
            ("经验", "experience"),
            ("生命", "health"),
            ("力量", "strength"),
            ("敏捷", "agility"),
            ("智力", "intelligence"),
            ("饥饿度", "hunger"),
            ("心情", "happiness"),
            ("体力", "energy")
        ]

        for i, (label, var_name) in enumerate(status_items):
            ttk.Label(self.status_frame, text=f"{label}:").grid(
                row=i, column=0, padx=5, pady=2, sticky="w")

            self.status_labels[var_name] = ttk.Label(self.status_frame, text="0")
            self.status_labels[var_name].grid(
                row=i, column=1, padx=5, pady=2, sticky="w")

            if var_name != "level":
                self.status_bars[var_name] = ttk.Progressbar(
                    self.status_frame, length=150, mode='determinate')
                self.status_bars[var_name].grid(
                    row=i, column=2, padx=5, pady=2, sticky="ew")

        # 心情状态
        self.mood_label = ttk.Label(self.status_frame, text="当前心情: 正常")
        self.mood_label.grid(row=len(status_items), column=0, columnspan=3,
                             padx=5, pady=5, sticky="w")

        # 技能列表
        skills_frame = ttk.LabelFrame(self.status_frame, text="已学技能")
        skills_frame.grid(row=len(status_items) + 1, column=0, columnspan=3,
                          padx=5, pady=5, sticky="nsew")

        self.skills_list = tk.Listbox(skills_frame, height=5)
        self.skills_list.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        # 配置grid权重
        skills_frame.grid_columnconfigure(0, weight=1)
        skills_frame.grid_rowconfigure(0, weight=1)

    def update_all_displays(self):
        """更新所有显示内容的统一函数"""
        try:
            # 1. 更新宠物状态
            if self.current_pet:
                self.current_pet.update_mood()
                self.update_status()  # 更新主界面的宠物状态显示

            # 2. 更新每日任务状态和显示
            if hasattr(self, 'daily_tasks_text'):
                if hasattr(self.game, 'daily_tasks'):
                    tasks = self.game.daily_tasks
                    if hasattr(tasks, 'refresh_tasks'):  # 检查是否是正确的DailyTasks实例
                        tasks.refresh_tasks()  # 检查是否需要刷新每日任务

                        self.daily_tasks_text.delete(1.0, tk.END)
                        self.daily_tasks_text.insert(tk.END, "每日任务状态：\n")

                        # 计算任务刷新倒计时
                        now = datetime.now()
                        next_refresh = datetime.combine(
                            tasks.last_refresh.date() + timedelta(days=1),
                            datetime.min.time()
                        )
                        time_until_refresh = next_refresh - now
                        hours = time_until_refresh.seconds // 3600
                        minutes = (time_until_refresh.seconds % 3600) // 60

                        self.daily_tasks_text.insert(tk.END,
                                                     f"距离任务刷新还有：{hours}小时{minutes}分钟\n\n")

                        # 显示所有任务状态
                        for task_name, task_info in tasks.tasks.items():
                            status = "已完成" if task_info["completed"] else \
                                f"未完成 (奖励{task_info['reward']}金币)"
                            self.daily_tasks_text.insert(tk.END,
                                                         f"{task_name}: {status}\n{task_info['description']}\n")

            # 3. 更新金币显示
            if hasattr(self, 'money_label'):
                self.money_label.config(text=f"当前金币: {self.game.money}")

            # 4. 更新商店显示
            if hasattr(self, 'update_shop_display'):
                self.update_shop_display()

            # 5. 如果在比赛标签页，更新比赛相关信息
            if hasattr(self, 'contest_pet_info'):
                self.update_contest_pet_info()

            # 6. 更新宠物列表
            if hasattr(self, 'update_pet_list'):
                self.update_pet_list()

            # 7. 设置下一次自动更新
            self.root.after(1000, self.update_all_displays)  # 每分钟更新一次

        except Exception as e:
            self.log_message(f"更新显示时发生错误: {str(e)}")

    def start_display_updates(self):
        """启动定时更新"""
        self.update_all_displays()  # 立即进行一次更新
        self.log_message("已启动自动更新显示")

    def create_action_frame(self, parent):
        """创建操作区框架"""
        action_frame = ttk.LabelFrame(parent, text="操作", padding="5")
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
        game_combo['values'] = ["fetch", "chase", "hide_seek", "training"]
        game_combo.pack(fill=tk.X, padx=5, pady=2)

        play_button = ttk.Button(play_frame, text="玩耍", command=self.play_with_pet)
        play_button.pack(fill=tk.X, padx=5, pady=2)

        # 道具使用区域
        item_frame = ttk.LabelFrame(action_frame, text="道具", padding="5")
        item_frame.pack(fill=tk.X, padx=5, pady=5)

        self.item_var = tk.StringVar()
        item_combo = ttk.Combobox(item_frame, textvariable=self.item_var)
        item_combo['values'] = list(self.game.items_inventory.keys())
        item_combo.pack(fill=tk.X, padx=5, pady=2)

        use_item_button = ttk.Button(item_frame, text="使用道具",
                                     command=self.use_item)
        use_item_button.pack(fill=tk.X, padx=5, pady=2)

        # 休息区域
        rest_frame = ttk.LabelFrame(action_frame, text="休息", padding="5")
        rest_frame.pack(fill=tk.X, padx=5, pady=5)

        sleep_button = ttk.Button(rest_frame, text="睡觉",
                                  command=self.sleep_pet)
        sleep_button.pack(fill=tk.X, padx=5, pady=2)

        wake_button = ttk.Button(rest_frame, text="唤醒",
                                 command=self.wake_pet)
        wake_button.pack(fill=tk.X, padx=5, pady=2)

    def create_free_activities_frame(self, parent):
        """创建免费活动框架"""
        activities_frame = ttk.LabelFrame(parent, text="免费活动", padding="5")
        activities_frame.pack(fill=tk.X, padx=5, pady=5)

        # 遛宠物按钮
        walk_button = ttk.Button(activities_frame, text="遛宠物 (获得20金币)",
                                 command=lambda: self.perform_free_activity("遛宠物"))
        walk_button.pack(fill=tk.X, padx=5, pady=2)

        # 清理按钮
        clean_button = ttk.Button(activities_frame, text="清理 (获得15金币)",
                                  command=lambda: self.perform_free_activity("清理"))
        clean_button.pack(fill=tk.X, padx=5, pady=2)

        # 基础训练按钮
        train_button = ttk.Button(activities_frame, text="基础训练 (获得25金币)",
                                  command=lambda: self.perform_free_activity("基础训练"))
        train_button.pack(fill=tk.X, padx=5, pady=2)

        # 显示每日任务状态
        self.daily_tasks_text = tk.Text(activities_frame, height=6, width=40)
        self.daily_tasks_text.pack(fill=tk.X, padx=5, pady=5)
        self.update_daily_tasks_display()

    def update_daily_tasks_display(self):
        """更新每日任务显示"""
        self.daily_tasks_text.delete(1.0, tk.END)
        self.daily_tasks_text.insert(tk.END, "每日任务状态：\n")
        for task_name, task_info in self.game.daily_tasks.tasks.items():
            status = "已完成" if task_info["completed"] else f"未完成 (奖励{task_info['reward']}金币)"
            self.daily_tasks_text.insert(tk.END, f"{task_name}: {status}\n")

    def create_shop_tab(self):
        """创建商店标签页"""
        shop_tab = ttk.Frame(self.notebook)
        self.notebook.add(shop_tab, text="商店")

        # 显示金币
        money_frame = ttk.Frame(shop_tab)
        money_frame.pack(fill=tk.X, padx=5, pady=5)
        self.money_label = ttk.Label(money_frame, text=f"当前金币: {self.game.money}")
        self.money_label.pack(side=tk.LEFT)

        # 创建商品列表
        shop_frame = ttk.Frame(shop_tab)
        shop_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 食物商店
        food_frame = ttk.LabelFrame(shop_frame, text="食物商店")
        food_frame.pack(fill=tk.X, padx=5, pady=5)
        self.create_shop_items(food_frame, self.game.food_inventory,
                               self.game.food_prices)

        # 道具商店
        items_frame = ttk.LabelFrame(shop_frame, text="道具商店")
        items_frame.pack(fill=tk.X, padx=5, pady=5)
        self.create_shop_items(items_frame, self.game.items_inventory,
                               self.game.items_prices)

    def create_contest_tab(self):
        """创建比赛标签页"""
        contest_tab = ttk.Frame(self.notebook)
        self.notebook.add(contest_tab, text="比赛")

        # 创建左右分栏
        left_frame = ttk.Frame(contest_tab)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        right_frame = ttk.Frame(contest_tab)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 比赛列表
        contests_frame = ttk.LabelFrame(left_frame, text="可参加的比赛")
        contests_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 使用Treeview来显示比赛列表
        columns = ("类型", "难度", "等级要求", "报名费", "奖励")
        self.contest_tree = ttk.Treeview(contests_frame, columns=columns, show="headings", height=10)

        # 设置列标题和宽度
        for col in columns:
            self.contest_tree.heading(col, text=col)
            self.contest_tree.column(col, width=100)

        self.contest_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 添加刷新按钮
        refresh_button = ttk.Button(contests_frame, text="刷新比赛列表",
                                    command=self.refresh_contest_list)
        refresh_button.pack(pady=5)

        # 参赛按钮
        enter_button = ttk.Button(contests_frame, text="参加比赛",
                                  command=self.enter_selected_contest)
        enter_button.pack(pady=5)

        # 比赛信息显示
        info_frame = ttk.LabelFrame(right_frame, text="比赛信息")
        info_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 宠物状态
        self.contest_pet_info = tk.Text(info_frame, height=6, width=40)
        self.contest_pet_info.pack(fill=tk.X, padx=5, pady=5)

        # 比赛记录
        record_frame = ttk.LabelFrame(right_frame, text="比赛记录")
        record_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.contest_record = tk.Text(record_frame, height=10)
        self.contest_record.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 初始化比赛系统
        if not hasattr(self.game, 'contest_system'):
            self.game.contest_system = ContestSystem()

        # 初始显示比赛列表
        self.refresh_contest_list()

    def refresh_contest_list(self):
        """刷新比赛列表"""
        # 清空现有列表
        for item in self.contest_tree.get_children():
            self.contest_tree.delete(item)

        # 刷新比赛
        self.game.contest_system.refresh_contests()

        # 添加新的比赛
        for contest in self.game.contest_system.available_contests:
            values = (
                contest['type'].value,
                contest['difficulty'].value[0],
                f"{self.game.contest_system._get_min_level(contest['difficulty'])}级",
                f"{contest['entry_fee']}金币",
                f"{contest['rewards']['money']}金币"
            )
            self.contest_tree.insert("", tk.END, values=values)

    def update_contest_pet_info(self):
        """更新比赛页面的宠物信息"""
        if not self.current_pet:
            self.contest_pet_info.delete(1.0, tk.END)
            self.contest_pet_info.insert(tk.END, "请先选择一个宠物")
            return

        info = f"""当前宠物：{self.current_pet.name}
    等级：{self.current_pet.level}
    体力：{self.current_pet.energy}/100
    获胜次数：{self.current_pet.won_contests}
    属性：力量 {self.current_pet.strength} | 敏捷 {self.current_pet.agility} | 智力 {self.current_pet.intelligence}
    """
        self.contest_pet_info.delete(1.0, tk.END)
        self.contest_pet_info.insert(tk.END, info)

    def enter_selected_contest(self):
        """参加选中的比赛"""
        if not self.current_pet:
            messagebox.showwarning("警告", "请先选择一个宠物！")
            return

        selection = self.contest_tree.selection()
        if not selection:
            messagebox.showwarning("警告", "请选择一个比赛！")
            return

        # 获取选中的比赛索引
        contest_index = self.contest_tree.index(selection[0])

        # 检查金币是否足够支付报名费
        contest = self.game.contest_system.available_contests[contest_index]
        if self.game.money < contest['entry_fee']:
            messagebox.showwarning("警告", "金币不足，无法支付报名费！")
            return

        # 扣除报名费
        self.game.money -= contest['entry_fee']

        # 参加比赛
        success, message, rewards = self.game.contest_system.enter_contest(
            self.current_pet, contest_index)

        # 记录比赛结果
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        record = f"[{timestamp}] {self.current_pet.name} 参加 {contest['type'].value}"
        record += f"（{contest['difficulty'].value[0]}）: {message}\n"

        if "不足" in message:
            self.game.money += contest['entry_fee']  # 退还报名费

        if success and rewards:
            # 发放奖励
            self.game.money += rewards['money']
            self.current_pet.gain_experience(rewards['exp'])

            # 更新记录
            record += f"获得奖励：{rewards['money']}金币, {rewards['exp']}经验"
            if rewards['items']:
                record += ", 物品："
                for item, count in rewards['items'].items():
                    if item in self.game.food_inventory:
                        self.game.food_inventory[item] = \
                            self.game.food_inventory[item] + count
                    elif item in self.game.items_inventory:
                        self.game.items_inventory[item] = \
                            self.game.items_inventory[item] + count
                    record += f"{item}x{count} "
            record += "\n"

        # 显示比赛结果
        self.contest_record.insert(tk.END, record)
        self.contest_record.see(tk.END)

        # 更新显示
        self.update_contest_pet_info()
        self.update_status()  # 更新主页面宠物状态
        self.money_label.config(text=f"当前金币: {self.game.money}")  # 更新金币显示

    def create_task_tab(self):
        """创建任务标签页"""
        task_tab = ttk.Frame(self.notebook)
        self.notebook.add(task_tab, text="任务")

        # 每日任务列表
        task_frame = ttk.LabelFrame(task_tab, text="每日任务")
        task_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.task_labels = {}
        for task in self.game.daily_tasks:
            frame = ttk.Frame(task_frame)
            frame.pack(fill=tk.X, padx=5, pady=2)

            label = ttk.Label(frame,
                              text=f"{task['type']}: 0/{task['target']} (奖励: {task['reward']}金币)")
            label.pack(side=tk.LEFT)

            self.task_labels[task['type']] = label

    def create_message_log(self, parent):
        """创建消息日志"""
        log_frame = ttk.LabelFrame(parent, text="消息日志", padding="5")
        log_frame.grid(row=1, column=1, columnspan=2, padx=5, pady=5,
                       sticky=(tk.W, tk.E, tk.N, tk.S))

        self.log_text = tk.Text(log_frame, width=50, height=10, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def create_shop_items(self, parent, inventory, prices):
        """创建商店物品列表"""
        for item, amount in inventory.items():
            frame = ttk.Frame(parent)
            frame.pack(fill=tk.X, padx=5, pady=2)

            # 商品名称和价格
            name_label = ttk.Label(frame, text=f"{item}")
            name_label.pack(side=tk.LEFT, padx=5)

            price_label = ttk.Label(frame, text=f"价格: {prices[item]}金币")
            price_label.pack(side=tk.LEFT, padx=5)

            # 库存显示
            stock_label = ttk.Label(frame, text=f"库存: {amount}")
            stock_label.pack(side=tk.LEFT, padx=5)

            # 购买数量输入
            quantity_var = tk.StringVar(value="1")
            quantity_entry = ttk.Entry(frame, textvariable=quantity_var, width=5)
            quantity_entry.pack(side=tk.LEFT, padx=5)

            # 购买按钮
            buy_button = ttk.Button(frame, text="购买",
                                    command=lambda i=item, q=quantity_var: self.buy_item(i, q))
            buy_button.pack(side=tk.LEFT, padx=5)

    def buy_item(self, item_type: str, quantity_var: tk.StringVar):
        """购买物品"""
        try:
            quantity = int(quantity_var.get())
            if quantity <= 0:
                messagebox.showwarning("警告", "请输入正确的数量！")
                return
        except ValueError:
            messagebox.showwarning("警告", "请输入正确的数量！")
            return

        if item_type in self.game.food_prices:
            result = self.game.buy_food(item_type, quantity)
        else:
            result = self.game.buy_item(item_type, quantity)

        self.log_message(result)
        self.update_shop_display()

    def use_item(self):
        """使用物品"""
        if not self.current_pet:
            messagebox.showwarning("警告", "请先选择一个宠物！")
            return

        item_type = self.item_var.get()
        if not item_type:
            messagebox.showwarning("警告", "请选择要使用的物品！")
            return

        result = self.game.use_item(item_type, self.current_pet.name)
        self.log_message(result)
        self.update_status()
        self.update_shop_display()

    def update_shop_display(self):
        """更新商店显示"""
        # 找到商店标签页
        for tab in self.notebook.winfo_children():
            if isinstance(tab, ttk.Frame):
                # 检查是否是商店标签页
                for widget in tab.winfo_children():
                    if isinstance(widget, ttk.Frame):
                        # 递归更新所有标签
                        self._update_stock_labels(widget)

                        # 更新金币显示
                        if hasattr(self, 'money_label'):
                            self.money_label.config(text=f"当前金币: {self.game.money}")

    def _update_stock_labels(self, widget):
        """递归更新所有库存标签"""
        # 检查当前widget是否是标签
        if isinstance(widget, ttk.Label):
            text = widget.cget('text')
            if text.startswith('库存:'):
                # 从标签文本中提取物品名称
                for item, amount in self.game.food_inventory.items():
                    if item in text:
                        widget.config(text=f"库存: {amount}")
                for item, amount in self.game.items_inventory.items():
                    if item in text:
                        widget.config(text=f"库存: {amount}")

        # 递归处理所有子widget
        children = []
        try:
            children = widget.winfo_children()
        except:
            pass

        for child in children:
            self._update_stock_labels(child)

    def on_select_pet(self, event):
        """选择宠物时的回调"""
        selection = self.pet_listbox.curselection()
        if selection:
            pet_name = self.pet_listbox.get(selection[0])
            self.current_pet = self.game.find_pet(pet_name)
            self.update_status()

    def update_status(self):
        """更新状态显示"""
        if not self.current_pet:
            return

        # 更新标签
        stats = [
            ("level", self.current_pet.level),
            ("experience", f"{self.current_pet.experience}/{self.current_pet.get_exp_needed()}"),
            ("health", self.current_pet.health),
            ("strength", self.current_pet.strength),
            ("agility", self.current_pet.agility),
            ("intelligence", self.current_pet.intelligence),
            ("hunger", self.current_pet.hunger),
            ("happiness", self.current_pet.happiness),
            ("energy", self.current_pet.energy)
        ]

        for stat, value in stats:
            if stat in self.status_labels:
                self.status_labels[stat].config(text=str(value))

        # 更新进度条
        for stat, progress in self.status_bars.items():
            if hasattr(self.current_pet, stat):
                value = getattr(self.current_pet, stat)
                if stat == "experience":
                    progress["value"] = (value / self.current_pet.get_exp_needed()) * 100
                else:
                    progress["value"] = value

        # 更新心情
        self.mood_label.config(text=f"当前心情: {self.current_pet.mood}")

        # 更新技能列表
        self.skills_list.delete(0, tk.END)
        for skill in self.current_pet.skills:
            exp = self.current_pet.skill_exp.get(skill, 0)
            self.skills_list.insert(tk.END, f"{skill} (熟练度: {exp})")

    def show_training_dialog(self):
        """显示训练对话框"""
        if not self.current_pet:
            messagebox.showwarning("警告", "请先选择一个宠物！")
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("宠物训练")
        dialog.geometry("400x300")

        # 显示可训练的技能
        for skill in self.current_pet.skills:
            frame = ttk.Frame(dialog)
            frame.pack(fill=tk.X, padx=5, pady=2)

            ttk.Label(frame, text=f"{skill}").pack(side=tk.LEFT, padx=5)
            exp = self.current_pet.skill_exp.get(skill, 0)
            ttk.Label(frame, text=f"熟练度: {exp}").pack(side=tk.LEFT, padx=5)

            train_button = ttk.Button(frame, text="训练",
                                      command=lambda s=skill: self.train_skill(s))
            train_button.pack(side=tk.LEFT, padx=5)

    def train_skill(self, skill):
        """训练技能"""
        result = self.current_pet.train_skill(skill)
        self.log_message(result)
        self.update_status()

    def show_social_dialog(self):
        """显示社交对话框"""
        if not self.current_pet:
            messagebox.showwarning("警告", "请先选择一个宠物！")
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("宠物社交")
        dialog.geometry("400x300")

        # 显示其他宠物列表
        other_pets = [pet for pet in self.game.pets
                      if pet.name != self.current_pet.name]

        for pet in other_pets:
            frame = ttk.Frame(dialog)
            frame.pack(fill=tk.X, padx=5, pady=2)

            ttk.Label(frame, text=f"{pet.name} ({pet.species})").pack(
                side=tk.LEFT, padx=5)

            interact_button = ttk.Button(frame, text="互动",
                                         command=lambda p=pet: self.interact_with_pet(p))
            interact_button.pack(side=tk.LEFT, padx=5)

    def interact_with_pet(self, other_pet):
        """宠物互动"""
        # 这里可以添加具体的互动逻辑
        self.current_pet.happiness += 10
        other_pet.happiness += 10

        if other_pet.name not in self.current_pet.friends:
            self.current_pet.friends.append(other_pet.name)
        if self.current_pet.name not in other_pet.friends:
            other_pet.friends.append(self.current_pet.name)

        self.log_message(f"{self.current_pet.name}和{other_pet.name}进行了愉快的互动！")
        self.update_status()

    def show_achievements_dialog(self):
        """显示成就对话框"""
        if not self.current_pet:
            messagebox.showwarning("警告", "请先选择一个宠物！")
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("宠物成就")
        dialog.geometry("400x300")

        # 显示基本成就
        ttk.Label(dialog, text=f"等级: {self.current_pet.level}").pack(padx=5, pady=2)
        ttk.Label(dialog, text=f"已学技能: {len(self.current_pet.skills)}个").pack(
            padx=5, pady=2)
        ttk.Label(dialog, text=f"训练次数: {self.current_pet.total_training_sessions}次"
                  ).pack(padx=5, pady=2)
        ttk.Label(dialog, text=f"比赛获胜: {self.current_pet.won_contests}次").pack(
            padx=5, pady=2)
        ttk.Label(dialog, text=f"朋友数量: {len(self.current_pet.friends)}个").pack(
            padx=5, pady=2)

    def log_message(self, message):
        """添加消息到日志"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

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

            # 重置当前选中的宠物
            self.current_pet = None

            # 更新界面
            self.notebook.destroy()
            self.notebook = ttk.Notebook(self.main_frame)
            self.notebook.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))

            # 重新创建所有标签页
            self.create_main_tab()  # 主要信息标签页
            self.create_shop_tab()  # 商店标签页
            self.create_contest_tab()  # 比赛标签页
            self.create_task_tab()  # 任务标签页

            # 更新宠物列表
            self.update_pet_list()

            # 如果有宠物，选中第一个
            if self.game.pets:
                self.pet_listbox.selection_set(0)
                self.current_pet = self.game.pets[0]
                self.update_status()

            messagebox.showinfo("提示", result)

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
            name = name_entry.get().strip()
            species = species_var.get()

            if not name:
                messagebox.showwarning("警告", "请输入宠物名称！")
                return

            if not species:
                messagebox.showwarning("警告", "请选择宠物品种！")
                return

            if any(pet.name == name for pet in self.game.pets):
                messagebox.showwarning("警告", "这个名字已经被使用了！")
                return

            result = self.game.add_pet(name, species)
            self.log_message(result)
            self.update_pet_list()
            dialog.destroy()

        ttk.Button(dialog, text="添加", command=add_pet).pack(padx=5, pady=20)

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
                for key, value in pet_data.items():
                    if hasattr(pet, key):
                        setattr(pet, key, value)

                # 添加到游戏中
                self.game.pets.append(pet)
                self.log_message(f"成功加载宠物 {pet_name}！")
                self.update_pet_list()
                dialog.destroy()

            except Exception as e:
                messagebox.showerror("错误", f"加载宠物失败: {str(e)}")

        # 加载按钮
        load_button = ttk.Button(dialog, text="加载", command=load_selected_pet)
        load_button.pack(padx=5, pady=5)

        # 取消按钮
        cancel_button = ttk.Button(dialog, text="取消", command=dialog.destroy)
        cancel_button.pack(padx=5, pady=5)

    def update_pet_list(self):
        """更新宠物列表"""
        self.pet_listbox.delete(0, tk.END)
        for pet in self.game.pets:
            self.pet_listbox.insert(tk.END, pet.name)

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

    def show_skills_dialog(self):
        """显示技能详情对话框"""
        if not self.current_pet:
            messagebox.showwarning("警告", "请先选择一个宠物！")
            return

        dialog = tk.Toplevel(self.root)
        dialog.title(f"{self.current_pet.name}的技能")
        dialog.geometry("400x500")

        # 创建技能列表
        skill_frame = ttk.Frame(dialog)
        skill_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 显示技能信息
        if not self.current_pet.skills:
            ttk.Label(skill_frame, text="还没有学会任何技能").pack(pady=10)
        else:
            for skill in self.current_pet.skills:
                # 为每个技能创建一个框架
                skill_box = ttk.LabelFrame(skill_frame, text=skill)
                skill_box.pack(fill=tk.X, padx=5, pady=5)

                # 显示技能熟练度
                exp = self.current_pet.skill_exp.get(skill, 0)
                ttk.Label(skill_box, text=f"熟练度: {exp}").pack(padx=5, pady=2)

                # 创建进度条显示熟练度
                progress = ttk.Progressbar(skill_box, length=200, mode='determinate')
                progress["value"] = min(100, exp / 10)  # 假设1000是最大熟练度
                progress.pack(padx=5, pady=2)

                # 训练按钮
                train_button = ttk.Button(
                    skill_box,
                    text="训练",
                    command=lambda s=skill: self.train_skill_from_dialog(s, dialog)
                )
                train_button.pack(padx=5, pady=5)

        # 显示下一个可能解锁的技能
        next_level = self.get_next_skill_level()
        if next_level:
            ttk.Label(dialog,
                      text=f"达到{next_level}级可以解锁新技能",
                      font=("黑体", 10)).pack(pady=10)

    def train_skill_from_dialog(self, skill: str, dialog: tk.Toplevel):
        """从技能对话框中训练技能"""
        result = self.current_pet.train_skill(skill)
        self.log_message(result)
        self.update_status()
        # 关闭旧对话框并打开新的，以更新显示
        dialog.destroy()
        self.show_skills_dialog()

    def get_next_skill_level(self) -> Optional[int]:
        """获取下一个技能解锁等级"""
        skill_levels = [5, 10, 15, 20, 30]
        for level in skill_levels:
            if self.current_pet.level < level:
                return level
        return None


def main():
    root = tk.Tk()
    game = PetGame()
    app = PetGameGUI(root, game)
    root.mainloop()

if __name__ == "__main__":
    main()