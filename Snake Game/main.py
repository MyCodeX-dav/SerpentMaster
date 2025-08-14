import tkinter as tk
from tkinter import messagebox, ttk
import random
import time
import math
import json
import os

class UltimateSnakeGame:
    def __init__(self, master):
        self.master = master
        self.setup_main_window()
        self.setup_menu()
        self.setup_game()
        
    def setup_main_window(self):
        """تهيئة النافذة الرئيسية"""
        self.master.title("Snake Ultimate - النسخة الاحترافية")
        self.master.geometry("820x720")
        self.master.resizable(False, False)
        self.master.configure(bg='#0a0a1a')
        
        # محاولة تحميل الأيقونة (اختياري)
        try:
            self.master.iconbitmap('snake_icon.ico') if os.path.exists('snake_icon.ico') else None
        except:
            pass
        
        # إطار اللعبة
        self.game_frame = tk.Frame(self.master, bg='#0a0a1a')
        self.game_frame.pack(pady=10)
    
    def setup_menu(self):
        """إنشاء قائمة اللعبة"""
        self.menu_bar = tk.Menu(self.master)
        
        # قائمة الإعدادات
        settings_menu = tk.Menu(self.menu_bar, tearoff=0)
        settings_menu.add_command(label="إعدادات السرعة", command=self.open_speed_settings)
        settings_menu.add_command(label="تخصيص المظهر", command=self.open_skin_settings)
        settings_menu.add_command(label="إعدادات اللعبة", command=self.open_game_settings)
        settings_menu.add_separator()
        settings_menu.add_command(label="إعادة التشغيل", command=self.reset_game)
        self.menu_bar.add_cascade(label="الإعدادات", menu=settings_menu)
        
        # قائمة الأدوات
        tools_menu = tk.Menu(self.menu_bar, tearoff=0)
        tools_menu.add_command(label="أدوات خاصة", command=self.use_special_tool)
        tools_menu.add_command(label="تفعيل الغش", command=self.toggle_cheat_mode)
        self.menu_bar.add_cascade(label="الأدوات", menu=tools_menu)
        
        # قائمة المساعدة
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="تعليمات اللعب", command=self.show_help)
        help_menu.add_command(label="أسرار اللعبة", command=self.show_secrets)
        help_menu.add_command(label="حول اللعبة", command=self.show_about)
        self.menu_bar.add_cascade(label="مساعدة", menu=help_menu)
        
        self.master.config(menu=self.menu_bar)
    
    def setup_game(self):
        """تهيئة إعدادات اللعبة"""
        # حجم اللعبة
        self.canvas_width = 600
        self.canvas_height = 600
        self.grid_size = 20
        
        # إعدادات اللعبة
        self.game_speed = 120
        self.wall_pass = True
        self.ghost_mode = False
        self.cheat_mode = False
        self.special_tools = 3
        self.mystery_boxes = []
        self.secret_codes = {
            'invincible': False,
            'doublepoints': False,
            'fastsnake': False
        }
        
        # ألوان اللعبة
        self.snake_color = '#4CAF50'
        self.food_color = '#FF5252'
        self.special_food_color = '#FFD700'
        self.bg_color = '#000000'
        self.obstacle_color = '#555555'
        self.mystery_color = '#9C27B0'
        
        # واجهة اللعبة
        self.setup_ui()
        self.load_settings()
        self.reset_game()
        
        # أحداث لوحة المفاتيح
        self.master.bind("<KeyPress>", self.change_direction)
        self.master.bind("<F1>", lambda e: self.activate_cheat_code('invincible'))
        self.master.bind("<F2>", lambda e: self.activate_cheat_code('doublepoints'))
        self.master.bind("<F3>", lambda e: self.activate_cheat_code('fastsnake'))
        
    def setup_ui(self):
        """إنشاء واجهة المستخدم"""
        # لوحة المعلومات
        self.info_frame = tk.Frame(self.game_frame, bg='#0a0a1a')
        self.info_frame.pack(fill=tk.X, pady=(0, 10))
        
        # لوحة النقاط والمستوى
        left_frame = tk.Frame(self.info_frame, bg='#0a0a1a')
        left_frame.pack(side=tk.LEFT)
        
        self.score_label = tk.Label(
            left_frame, text="النقاط: 0", 
            font=('Arial', 12, 'bold'), fg='white', bg='#0a0a1a'
        )
        self.score_label.pack(anchor='w')
        
        self.level_label = tk.Label(
            left_frame, text="المستوى: 1", 
            font=('Arial', 12, 'bold'), fg='lightblue', bg='#0a0a1a'
        )
        self.level_label.pack(anchor='w')
        
        # لوحة الأدوات والإضافات
        center_frame = tk.Frame(self.info_frame, bg='#0a0a1a')
        center_frame.pack(side=tk.LEFT, padx=20)
        
        self.tools_label = tk.Label(
            center_frame, text="الأدوات: 3", 
            font=('Arial', 12, 'bold'), fg='#FF9800', bg='#0a0a1a'
        )
        self.tools_label.pack(anchor='w')
        
        self.cheat_label = tk.Label(
            center_frame, text="وضع الغش: غير مفعل", 
            font=('Arial', 10), fg='red', bg='#0a0a1a'
        )
        self.cheat_label.pack(anchor='w')
        
        # لوحة الوقت وأفضل نتيجة
        right_frame = tk.Frame(self.info_frame, bg='#0a0a1a')
        right_frame.pack(side=tk.RIGHT)
        
        self.time_label = tk.Label(
            right_frame, text="الوقت: 00:00", 
            font=('Arial', 12, 'bold'), fg='lightgreen', bg='#0a0a1a'
        )
        self.time_label.pack(anchor='e')
        
        self.highscore_label = tk.Label(
            right_frame, text="أفضل نتيجة: 0", 
            font=('Arial', 12, 'bold'), fg='gold', bg='#0a0a1a'
        )
        self.highscore_label.pack(anchor='e')
        
        # لوحة اللعبة
        self.canvas = tk.Canvas(
            self.game_frame, bg=self.bg_color, 
            width=self.canvas_width, height=self.canvas_height,
            highlightthickness=0, bd=0
        )
        self.canvas.pack()
        
        # شريط التقدم
        self.progress_bar = ttk.Progressbar(
            self.game_frame, orient='horizontal', 
            length=600, mode='determinate'
        )
        self.progress_bar.pack(pady=(10, 0))
        self.progress_bar['value'] = 0
        self.progress_bar['maximum'] = 100
        
        # تأثيرات خاصة
        self.effects = []
        self.power_ups = []
        self.obstacles = []
    
    def load_settings(self):
        """تحميل الإعدادات المحفوظة"""
        try:
            with open('snake_settings.json', 'r') as f:
                settings = json.load(f)
                self.highscore = settings.get('highscore', 0)
                self.wall_pass = settings.get('wall_pass', True)
                self.game_speed = settings.get('game_speed', 120)
                self.snake_color = settings.get('snake_color', '#4CAF50')
                self.food_color = settings.get('food_color', '#FF5252')
                self.special_food_color = settings.get('special_food_color', '#FFD700')
                self.bg_color = settings.get('bg_color', '#000000')
        except:
            self.highscore = 0
            self.wall_pass = True
            self.game_speed = 120
            self.snake_color = '#4CAF50'
            self.food_color = '#FF5252'
            self.special_food_color = '#FFD700'
            self.bg_color = '#000000'
    
    def save_settings(self):
        """حفظ الإعدادات الحالية"""
        settings = {
            'highscore': self.highscore,
            'wall_pass': self.wall_pass,
            'game_speed': self.game_speed,
            'snake_color': self.snake_color,
            'food_color': self.food_color,
            'special_food_color': self.special_food_color,
            'bg_color': self.bg_color
        }
        with open('snake_settings.json', 'w') as f:
            json.dump(settings, f)
    
    def reset_game(self):
        """إعادة تعيين اللعبة"""
        # حالة اللعبة
        self.snake = [(200, 200), (180, 200), (160, 200)]
        self.snake_direction = "Right"
        self.next_direction = "Right"
        self.food = self.create_food()
        self.special_food = None
        self.special_food_timer = 0
        self.score = 0
        self.level = 1
        self.game_active = True
        self.paused = False
        self.speed_boost = False
        self.speed_boost_end = 0
        self.last_food_time = time.time()
        self.start_time = time.time()
        self.obstacles = []
        self.power_ups = []
        self.mystery_boxes = []
        self.special_tools = 3
        self.ghost_mode = False
        
        # تحديث الواجهة
        self.update_score_display()
        self.canvas.config(bg=self.bg_color)
        self.draw_game()
        
        # بدء اللعبة
        if not hasattr(self, 'game_loop'):
            self.game_loop()
        else:
            self.master.after_cancel(self.game_loop)
            self.game_loop()
    
    def create_food(self):
        """إنشاء طعام جديد"""
        while True:
            x = random.randint(1, (self.canvas_width - self.grid_size) // self.grid_size) * self.grid_size
            y = random.randint(1, (self.canvas_height - self.grid_size) // self.grid_size) * self.grid_size
            food_pos = (x, y)
            
            if (food_pos not in self.snake and 
                food_pos not in self.obstacles and 
                food_pos not in [p[0] for p in self.power_ups] and
                food_pos not in [m[0] for m in self.mystery_boxes]):
                self.last_food_time = time.time()
                return food_pos
    
    def create_special_food(self):
        """إنشاء طعام خاص"""
        if (self.special_food is None and 
            random.random() < 0.15 and 
            len(self.snake) > 5):
            while True:
                x = random.randint(1, (self.canvas_width - self.grid_size) // self.grid_size) * self.grid_size
                y = random.randint(1, (self.canvas_height - self.grid_size) // self.grid_size) * self.grid_size
                food_pos = (x, y)
                
                if (food_pos not in self.snake and 
                    food_pos != self.food and 
                    food_pos not in self.obstacles and 
                    food_pos not in [p[0] for p in self.power_ups] and
                    food_pos not in [m[0] for m in self.mystery_boxes]):
                    self.special_food = food_pos
                    self.special_food_timer = time.time() + 8  # يختفي بعد 8 ثواني
                    break
    
    def create_obstacles(self):
        """إنشاء عوائق عشوائية"""
        if self.level > 2 and len(self.obstacles) < (self.level - 1) * 2:
            for _ in range(2):
                while True:
                    x = random.randint(1, (self.canvas_width - self.grid_size) // self.grid_size) * self.grid_size
                    y = random.randint(1, (self.canvas_height - self.grid_size) // self.grid_size) * self.grid_size
                    obstacle_pos = (x, y)
                    
                    if (obstacle_pos not in self.snake and 
                        obstacle_pos != self.food and 
                        (self.special_food is None or obstacle_pos != self.special_food) and
                        obstacle_pos not in [m[0] for m in self.mystery_boxes]):
                        self.obstacles.append(obstacle_pos)
                        break
    
    def create_power_up(self):
        """إنشاء قوة إضافية"""
        if (random.random() < 0.1 and 
            len(self.power_ups) < 1 and 
            self.level > 3):
            power_type = random.choice(['shield', 'slow', 'reverse', 'ghost', 'teleport'])
            while True:
                x = random.randint(1, (self.canvas_width - self.grid_size) // self.grid_size) * self.grid_size
                y = random.randint(1, (self.canvas_height - self.grid_size) // self.grid_size) * self.grid_size
                power_pos = (x, y)
                
                if (power_pos not in self.snake and 
                    power_pos != self.food and 
                    (self.special_food is None or power_pos != self.special_food) and 
                    power_pos not in self.obstacles and
                    power_pos not in [m[0] for m in self.mystery_boxes]):
                    self.power_ups.append((power_pos, power_type, time.time() + 15))
                    break
    
    def create_mystery_box(self):
        """إنشاء صندوق غامض"""
        if (random.random() < 0.05 and 
            len(self.mystery_boxes) < 1 and 
            self.level > 4):
            while True:
                x = random.randint(1, (self.canvas_width - self.grid_size) // self.grid_size) * self.grid_size
                y = random.randint(1, (self.canvas_height - self.grid_size) // self.grid_size) * self.grid_size
                box_pos = (x, y)
                
                if (box_pos not in self.snake and 
                    box_pos != self.food and 
                    (self.special_food is None or box_pos != self.special_food) and 
                    box_pos not in self.obstacles and
                    box_pos not in [p[0] for p in self.power_ups]):
                    self.mystery_boxes.append((box_pos, time.time() + 20))  # يختفي بعد 20 ثانية
                    break
    
    def change_direction(self, event):
        """تغيير اتجاه الثعبان"""
        if not self.game_active:
            if event.keysym == "space":
                self.reset_game()
            return
            
        if event.keysym == "p":
            self.paused = not self.paused
            if not self.paused:
                self.game_loop()
            else:
                self.draw_pause_message()
            return
        
        key = event.keysym
        if key in ["Up", "Down", "Left", "Right", "w", "s", "a", "d"]:
            # تحويل WASD إلى اتجاهات
            if key == "w": key = "Up"
            elif key == "s": key = "Down"
            elif key == "a": key = "Left"
            elif key == "d": key = "Right"
            
            # منع الحركة العكسية المباشرة
            if (key == "Up" and self.snake_direction != "Down") or \
               (key == "Down" and self.snake_direction != "Up") or \
               (key == "Left" and self.snake_direction != "Right") or \
               (key == "Right" and self.snake_direction != "Left"):
                self.next_direction = key
    
    def game_loop(self):
        """الحلقة الرئيسية للعبة"""
        if not self.game_active or self.paused:
            return
            
        # تحديث الوقت
        self.update_time()
        
        # تحديث الاتجاه
        self.snake_direction = self.next_direction
        
        # حساب الموضع الجديد للرأس
        head_x, head_y = self.snake[0]
        
        if self.snake_direction == "Up":
            new_head = (head_x, head_y - self.grid_size)
        elif self.snake_direction == "Down":
            new_head = (head_x, head_y + self.grid_size)
        elif self.snake_direction == "Left":
            new_head = (head_x - self.grid_size, head_y)
        elif self.snake_direction == "Right":
            new_head = (head_x + self.grid_size, head_y)
        
        # التحقق من المرور عبر الجدران إذا كان مفعلاً
        if self.wall_pass:
            if new_head[0] < 0:
                new_head = (self.canvas_width - self.grid_size, new_head[1])
            elif new_head[0] >= self.canvas_width:
                new_head = (0, new_head[1])
            elif new_head[1] < 0:
                new_head = (new_head[0], self.canvas_height - self.grid_size)
            elif new_head[1] >= self.canvas_height:
                new_head = (new_head[0], 0)
        
        # التحقق من الاصطدام بالجدران إذا كان المرور معطلاً
        if not self.wall_pass and (
            new_head[0] < 0 or new_head[0] >= self.canvas_width or
            new_head[1] < 0 or new_head[1] >= self.canvas_height
        ):
            if not self.ghost_mode and not self.secret_codes['invincible']:
                self.game_over()
            return
        
        # التحقق من الاصطدام بالنفس
        if new_head in self.snake and not self.ghost_mode and not self.secret_codes['invincible']:
            self.game_over()
            return
        
        # التحقق من الاصطدام بالعوائق
        if new_head in self.obstacles and not self.ghost_mode and not self.secret_codes['invincible']:
            self.game_over()
            return
        
        # إضافة الرأس الجديدة
        self.snake.insert(0, new_head)
        
        # التحقق من أكل الطعام العادي
        if new_head == self.food:
            points = 2 if self.secret_codes['doublepoints'] else 1
            self.score += points
            self.update_level()
            self.food = self.create_food()
            self.create_special_food()
            self.create_obstacles()
            self.create_power_up()
            self.create_mystery_box()
            self.add_effect('grow', new_head)
        
        # التحقق من أكل الطعام الخاص
        elif self.special_food and new_head == self.special_food:
            points = 6 if self.secret_codes['doublepoints'] else 3
            self.score += points
            self.update_level()
            self.special_food = None
            self.speed_boost = True
            self.speed_boost_end = time.time() + 5
            self.add_effect('star', new_head)
        
        # التحقق من أكل القوى الإضافية
        elif any(new_head == p[0] for p in self.power_ups):
            for power_up in self.power_ups:
                if new_head == power_up[0]:
                    self.apply_power_up(power_up[1])
                    self.add_effect('power', new_head)
                    self.power_ups.remove(power_up)
                    break
        
        # التحقق من أكل الصناديق الغامضة
        elif any(new_head == m[0] for m in self.mystery_boxes):
            for box in self.mystery_boxes:
                if new_head == box[0]:
                    self.open_mystery_box(box[0])
                    self.mystery_boxes.remove(box)
                    break
        
        else:
            # إذا لم يأكل أي شيء، إزالة الذيل
            self.snake.pop()
        
        # التحقق من انتهاء مدة الطعام الخاص
        if self.special_food and time.time() > self.special_food_timer:
            self.special_food = None
        
        # التحقق من انتهاء مدة القوى الإضافية
        self.check_power_ups_expiry()
        
        # التحقق من انتهاء مدة الصناديق الغامضة
        self.check_mystery_boxes_expiry()
        
        # التحقق من انتهاء مدة زيادة السرعة
        if self.speed_boost and time.time() > self.speed_boost_end:
            self.speed_boost = False
        
        # تحديث واجهة المستخدم
        self.update_score_display()
        self.draw_game()
        
        # حساب سرعة اللعبة
        current_speed = max(50, self.game_speed - (self.level * 5))
        if self.speed_boost or self.secret_codes['fastsnake']:
            current_speed = max(30, current_speed // 2)
        
        # الاستمرار في اللعبة
        self.master.after(current_speed, self.game_loop)
    
    def apply_power_up(self, power_type):
        """تطبيق تأثير القوة الإضافية"""
        if power_type == 'shield':
            self.shield_active = True
            self.shield_end = time.time() + 10
            self.add_effect('shield', self.snake[0])
        elif power_type == 'slow':
            self.slow_active = True
            self.slow_end = time.time() + 8
        elif power_type == 'reverse':
            self.reverse_active = True
            self.reverse_end = time.time() + 6
            self.snake.reverse()
            self.next_direction = self.get_opposite_direction(self.snake_direction)
        elif power_type == 'ghost':
            self.ghost_mode = True
            self.ghost_end = time.time() + 12
        elif power_type == 'teleport':
            self.teleport_snake()
    
    def teleport_snake(self):
        """نقل الثعبان إلى مكان عشوائي"""
        # احتفظ بالرأس فقط
        head = self.snake[0]
        self.snake = [head]
        
        # أنشئ موقعاً جديداً للرأس
        while True:
            x = random.randint(1, (self.canvas_width - self.grid_size) // self.grid_size) * self.grid_size
            y = random.randint(1, (self.canvas_height - self.grid_size) // self.grid_size) * self.grid_size
            new_head = (x, y)
            
            if (new_head not in self.obstacles and 
                new_head != self.food and 
                (self.special_food is None or new_head != self.special_food) and
                new_head not in [p[0] for p in self.power_ups] and
                new_head not in [m[0] for m in self.mystery_boxes]):
                self.snake[0] = new_head
                self.add_effect('teleport', new_head)
                break
    
    def open_mystery_box(self, position):
        """فتح الصندوق الغامض"""
        rewards = [
            ('score', 10),
            ('tools', 1),
            ('speed', 5),
            ('shrink', -3),
            ('surprise', 0)
        ]
        
        reward_type, value = random.choice(rewards)
        
        if reward_type == 'score':
            self.score += value
            self.add_effect('score_up', position)
        elif reward_type == 'tools':
            self.special_tools += value
            self.add_effect('tool_add', position)
        elif reward_type == 'speed':
            self.speed_boost = True
            self.speed_boost_end = time.time() + value
            self.add_effect('speed_boost', position)
        elif reward_type == 'shrink':
            # تقليل طول الثعبان (لكن ليس أقل من 3)
            new_length = max(3, len(self.snake) + value)
            self.snake = self.snake[:new_length]
            self.add_effect('shrink', position)
        elif reward_type == 'surprise':
            # مفاجأة عشوائية
            surprise = random.choice(['flash', 'rainbow', 'invert'])
            if surprise == 'flash':
                self.add_effect('flash', position)
                old_bg = self.bg_color
                self.bg_color = '#FFFFFF'
                self.canvas.config(bg=self.bg_color)
                self.master.after(200, lambda: self.restore_bg_color(old_bg))
            elif surprise == 'rainbow':
                self.add_effect('rainbow', position)
                self.rainbow_snake = True
                self.rainbow_end = time.time() + 10
            elif surprise == 'invert':
                self.add_effect('invert', position)
                self.invert_colors()
                self.master.after(5000, self.restore_colors)
    
    def restore_bg_color(self, color):
        """استعادة لون الخلفية"""
        self.bg_color = color
        self.canvas.config(bg=self.bg_color)
    
    def invert_colors(self):
        """عكس ألوان اللعبة"""
        self.snake_color, self.food_color = self.food_color, self.snake_color
        self.bg_color = '#FFFFFF'
        self.canvas.config(bg=self.bg_color)
    
    def restore_colors(self):
        """استعادة الألوان الأصلية"""
        self.snake_color = '#4CAF50'
        self.food_color = '#FF5252'
        self.bg_color = '#000000'
        self.canvas.config(bg=self.bg_color)
    
    def check_power_ups_expiry(self):
        """التحقق من انتهاء مدة القوى الإضافية"""
        current_time = time.time()
        if hasattr(self, 'shield_end') and current_time > self.shield_end:
            self.shield_active = False
        if hasattr(self, 'slow_end') and current_time > self.slow_end:
            self.slow_active = False
        if hasattr(self, 'reverse_end') and current_time > self.reverse_end:
            self.reverse_active = False
            self.snake.reverse()
        if hasattr(self, 'ghost_end') and current_time > self.ghost_end:
            self.ghost_mode = False
        if hasattr(self, 'rainbow_end') and current_time > self.rainbow_end:
            self.rainbow_snake = False
        
        # إزالة القوى الإضافية المنتهية
        self.power_ups = [p for p in self.power_ups if p[2] > current_time]
    
    def check_mystery_boxes_expiry(self):
        """التحقق من انتهاء مدة الصناديق الغامضة"""
        current_time = time.time()
        self.mystery_boxes = [m for m in self.mystery_boxes if m[1] > current_time]
    
    def get_opposite_direction(self, direction):
        """الحصول على الاتجاه المعاكس"""
        opposites = {
            'Up': 'Down',
            'Down': 'Up',
            'Left': 'Right',
            'Right': 'Left'
        }
        return opposites.get(direction, direction)
    
    def update_level(self):
        """تحديث مستوى اللعبة"""
        new_level = self.score // 5 + 1
        if new_level > self.level:
            self.level = new_level
            self.add_effect('level_up', (300, 300))
    
    def update_time(self):
        """تحديث وقت اللعبة"""
        elapsed = int(time.time() - self.start_time)
        minutes = elapsed // 60
        seconds = elapsed % 60
        self.time_label.config(text=f"الوقت: {minutes:02d}:{seconds:02d}")
    
    def update_score_display(self):
        """تحديث عرض النتائج"""
        self.score_label.config(text=f"النقاط: {self.score}")
        self.highscore_label.config(text=f"أفضل نتيجة: {max(self.score, self.highscore)}")
        self.level_label.config(text=f"المستوى: {self.level}")
        self.tools_label.config(text=f"الأدوات: {self.special_tools}")
        
        if self.cheat_mode:
            self.cheat_label.config(text="وضع الغش: مفعل", fg='green')
        else:
            self.cheat_label.config(text="وضع الغش: غير مفعل", fg='red')
        
        # تحديث شريط التقدم
        progress = (self.score % 5) * 20
        self.progress_bar['value'] = progress
    
    def draw_game(self):
        """رسم جميع عناصر اللعبة"""
        self.canvas.delete("all")
        
        # رسم الشبكة (خلفية)
        self.draw_grid()
        
        # رسم العوائق
        for obstacle in self.obstacles:
            x, y = obstacle
            self.canvas.create_rectangle(
                x, y, x + self.grid_size, y + self.grid_size,
                fill=self.obstacle_color, outline='#333333', width=2
            )
        
        # رسم القوى الإضافية
        for power_up in self.power_ups:
            x, y, power_type, _ = power_up
            color = {
                'shield': '#00BCD4',
                'slow': '#9C27B0',
                'reverse': '#FF9800',
                'ghost': '#607D8B',
                'teleport': '#673AB7'
            }.get(power_type, '#FFFFFF')
            
            self.canvas.create_rectangle(
                x, y, x + self.grid_size, y + self.grid_size,
                fill=color, outline='#333333', width=2
            )
            self.canvas.create_text(
                x + self.grid_size//2, y + self.grid_size//2,
                text=power_type[0].upper(), fill='white', font=('Arial', 10, 'bold')
            )
        
        # رسم الصناديق الغامضة
        for box in self.mystery_boxes:
            x, y = box[0]
            self.canvas.create_rectangle(
                x, y, x + self.grid_size, y + self.grid_size,
                fill=self.mystery_color, outline='#7B1FA2', width=2
            )
            self.canvas.create_text(
                x + self.grid_size//2, y + self.grid_size//2,
                text="?", fill='white', font=('Arial', 12, 'bold')
            )
        
        # رسم الثعبان
        for i, segment in enumerate(self.snake):
            x, y = segment
            if i == 0:  # رأس الثعبان
                if hasattr(self, 'rainbow_snake') and self.rainbow_snake:
                    color = self.get_rainbow_color(i)
                else:
                    color = '#00E676'
                
                self.canvas.create_rectangle(
                    x, y, x + self.grid_size, y + self.grid_size,
                    fill=color, outline='#00C853', width=2
                )
                
                # رسم العيون
                eye_size = 4
                if self.snake_direction == "Right":
                    self.canvas.create_oval(
                        x + 13, y + 5, x + 13 + eye_size, y + 5 + eye_size,
                        fill="black"
                    )
                    self.canvas.create_oval(
                        x + 13, y + 11, x + 13 + eye_size, y + 11 + eye_size,
                        fill="black"
                    )
                elif self.snake_direction == "Left":
                    self.canvas.create_oval(
                        x + 3, y + 5, x + 3 + eye_size, y + 5 + eye_size,
                        fill="black"
                    )
                    self.canvas.create_oval(
                        x + 3, y + 11, x + 3 + eye_size, y + 11 + eye_size,
                        fill="black"
                    )
                elif self.snake_direction == "Up":
                    self.canvas.create_oval(
                        x + 5, y + 3, x + 5 + eye_size, y + 3 + eye_size,
                        fill="black"
                    )
                    self.canvas.create_oval(
                        x + 11, y + 3, x + 11 + eye_size, y + 3 + eye_size,
                        fill="black"
                    )
                elif self.snake_direction == "Down":
                    self.canvas.create_oval(
                        x + 5, y + 13, x + 5 + eye_size, y + 13 + eye_size,
                        fill="black"
                    )
                    self.canvas.create_oval(
                        x + 11, y + 13, x + 11 + eye_size, y + 13 + eye_size,
                        fill="black"
                    )
                
                # تأثير الدرع إذا كان نشطاً
                if hasattr(self, 'shield_active') and self.shield_active:
                    self.canvas.create_oval(
                        x - 3, y - 3, x + self.grid_size + 3, y + self.grid_size + 3,
                        outline="#00BCD4", width=2, dash=(3, 3)
                    )
            else:  # جسم الثعبان
                if hasattr(self, 'rainbow_snake') and self.rainbow_snake:
                    color = self.get_rainbow_color(i)
                else:
                    color = '#4CAF50' if i % 2 == 0 else '#8BC34A'
                
                self.canvas.create_rectangle(
                    x, y, x + self.grid_size, y + self.grid_size,
                    fill=color, outline='#2E7D32', width=1
                )
        
        # رسم الطعام العادي
        food_x, food_y = self.food
        self.canvas.create_oval(
            food_x + 2, food_y + 2, food_x + self.grid_size - 2, food_y + self.grid_size - 2,
            fill=self.food_color, outline='#D32F2F', width=2
        )
        
        # رسم الطعام الخاص إذا كان موجوداً
        if self.special_food:
            sf_x, sf_y = self.special_food
            self.canvas.create_oval(
                sf_x + 2, sf_y + 2, sf_x + self.grid_size - 2, sf_y + self.grid_size - 2,
                fill=self.special_food_color, outline='#FFA500', width=2
            )
            # تأثير متوهج
            self.canvas.create_oval(
                sf_x - 3, sf_y - 3, sf_x + self.grid_size + 3, sf_y + self.grid_size + 3,
                outline=self.special_food_color, width=1, dash=(3, 3)
            )
        
        # رسم التأثيرات الخاصة
        self.draw_effects()
        
        # عرض رسالة الإيقاف المؤقت إذا كانت اللعبة متوقفة
        if self.paused:
            self.draw_pause_message()
    
    def get_rainbow_color(self, index):
        """الحصول على لون قوس قزح حسب المؤشر"""
        colors = [
            '#FF0000', '#FF7F00', '#FFFF00', 
            '#00FF00', '#0000FF', '#4B0082', '#9400D3'
        ]
        return colors[index % len(colors)]
    
    def draw_grid(self):
        """رسم شبكة خلفية"""
        for i in range(0, self.canvas_width, self.grid_size):
            self.canvas.create_line(
                i, 0, i, self.canvas_height, 
                fill='#111111', width=1, dash=(2, 2)
            )
        for i in range(0, self.canvas_height, self.grid_size):
            self.canvas.create_line(
                0, i, self.canvas_width, i, 
                fill='#111111', width=1, dash=(2, 2)
            )
    
    def add_effect(self, effect_type, position):
        """إضافة تأثير خاص"""
        self.effects.append({
            'type': effect_type,
            'position': position,
            'size': 5,
            'alpha': 1.0,
            'created': time.time()
        })
    
    def draw_effects(self):
        """رسم التأثيرات الخاصة"""
        current_time = time.time()
        effects_to_keep = []
        
        for effect in self.effects:
            elapsed = current_time - effect['created']
            if elapsed > 1.0:  # تأثيرات لمدة ثانية واحدة
                continue
            
            effects_to_keep.append(effect)
            x, y = effect['position']
            size = effect['size'] + (elapsed * 20)
            alpha = 1.0 - elapsed
            
            if effect['type'] == 'grow':
                self.canvas.create_oval(
                    x - size//2, y - size//2, 
                    x + self.grid_size + size//2, y + self.grid_size + size//2,
                    outline='#00E676', width=2
                )
            elif effect['type'] == 'star':
                self.draw_star(
                    x + self.grid_size//2, y + self.grid_size//2,
                    size, '#FFD700'
                )
            elif effect['type'] == 'power':
                self.canvas.create_oval(
                    x - size//2, y - size//2, 
                    x + self.grid_size + size//2, y + self.grid_size + size//2,
                    outline='#00BCD4', width=2
                )
            elif effect['type'] == 'level_up':
                self.canvas.create_text(
                    x, y, text=f"المستوى {self.level}!", 
                    fill='#FF9800', 
                    font=('Arial', 24, 'bold')
                )
            elif effect['type'] == 'score_up':
                self.canvas.create_text(
                    x, y, text="+10 نقاط!", 
                    fill='#4CAF50', 
                    font=('Arial', 16, 'bold')
                )
            elif effect['type'] == 'tool_add':
                self.canvas.create_text(
                    x, y, text="أداة إضافية!", 
                    fill='#FF9800', 
                    font=('Arial', 16, 'bold')
                )
            elif effect['type'] == 'speed_boost':
                self.canvas.create_text(
                    x, y, text="سرعة مضاعفة!", 
                    fill='#2196F3', 
                    font=('Arial', 16, 'bold')
                )
            elif effect['type'] == 'shrink':
                self.canvas.create_text(
                    x, y, text="تقليص الحجم!", 
                    fill='#F44336', 
                    font=('Arial', 16, 'bold')
                )
            elif effect['type'] == 'flash':
                self.canvas.create_rectangle(
                    x - size//2, y - size//2, 
                    x + self.grid_size + size//2, y + self.grid_size + size//2,
                    fill='#FFFFFF', outline=''
                )
            elif effect['type'] == 'rainbow':
                self.draw_rainbow_effect(x, y, size)
            elif effect['type'] == 'invert':
                self.canvas.create_rectangle(
                    x - size//2, y - size//2, 
                    x + self.grid_size + size//2, y + self.grid_size + size//2,
                    fill='#000000', outline=''
                )
            elif effect['type'] == 'teleport':
                self.canvas.create_text(
                    x, y, text="انتقال!", 
                    fill='#673AB7', 
                    font=('Arial', 16, 'bold')
                )
            elif effect['type'] == 'shield':
                self.canvas.create_text(
                    x, y, text="درع واقي!", 
                    fill='#00BCD4', 
                    font=('Arial', 16, 'bold')
                )
        
        self.effects = effects_to_keep
    
    def draw_star(self, x, y, size, color):
        """رسم نجمة للتأثيرات"""
        points = []
        for i in range(5):
            angle = math.radians(90 + i * 72)
            outer_x = x + math.cos(angle) * size
            outer_y = y - math.sin(angle) * size
            points.extend([outer_x, outer_y])
            
            inner_angle = angle + math.radians(36)
            inner_x = x + math.cos(inner_angle) * size * 0.4
            inner_y = y - math.sin(inner_angle) * size * 0.4
            points.extend([inner_x, inner_y])
        
        self.canvas.create_polygon(points, outline=color, fill='', width=2)
    
    def draw_rainbow_effect(self, x, y, size):
        """رسم تأثير قوس قزح"""
        colors = ['#FF0000', '#FF7F00', '#FFFF00', '#00FF00', '#0000FF', '#4B0082', '#9400D3']
        for i, color in enumerate(colors):
            self.canvas.create_oval(
                x - size//2 + i*2, y - size//2 + i*2, 
                x + self.grid_size + size//2 - i*2, y + self.grid_size + size//2 - i*2,
                outline=color, width=2
            )
    
    def draw_pause_message(self):
        """رسم رسالة الإيقاف المؤقت"""
        self.canvas.create_rectangle(
            150, 250, 450, 350, fill="#000000", outline="#FFFFFF", width=2
        )
        self.canvas.create_text(
            300, 280, text="الإيقاف المؤقت", 
            fill="white", font=('Arial', 24, 'bold')
        )
        self.canvas.create_text(
            300, 320, text="اضغط P للمتابعة", 
            fill="white", font=('Arial', 14)
        )
    
    def game_over(self):
        """إنهاء اللعبة"""
        self.game_active = False
        
        if self.score > self.highscore:
            self.highscore = self.score
            self.save_settings()
        
        # تأثير انفجار للثعبان
        for segment in self.snake:
            self.add_effect('explosion', segment)
        
        # رسم رسالة نهاية اللعبة
        self.canvas.create_rectangle(
            100, 200, 500, 400, fill="#000000", outline="#FF0000", width=3
        )
        self.canvas.create_text(
            300, 250, text="انتهت اللعبة!", 
            fill="#FF5252", font=('Arial', 32, 'bold')
        )
        self.canvas.create_text(
            300, 300, text=f"النقاط النهائية: {self.score}", 
            fill="white", font=('Arial', 20)
        )
        self.canvas.create_text(
            300, 350, text="اضغط زر المسافة للعب مرة أخرى", 
            fill="#4CAF50", font=('Arial', 14)
        )
    
    def use_special_tool(self):
        """استخدام أداة خاصة"""
        if self.special_tools > 0 and self.game_active and not self.paused:
            tools = [
                ('إزالة العوائق', self.remove_obstacles),
                ('تخطي المستوى', self.skip_level),
                ('شفاء الثعبان', self.heal_snake),
                ('تجديد الأدوات', self.refill_tools)
            ]
            
            tool_name, tool_func = random.choice(tools)
            tool_func()
            self.special_tools -= 1
            self.update_score_display()
            messagebox.showinfo("أداة خاصة", f"تم استخدام الأداة: {tool_name}")
        else:
            messagebox.showwarning("تحذير", "لا تمتلك أدوات كافية أو اللعبة غير نشطة")
    
    def remove_obstacles(self):
        """إزالة جميع العوائق"""
        self.obstacles = []
        self.add_effect('clear', (300, 300))
    
    def skip_level(self):
        """تخطي المستوى الحالي"""
        self.score += (5 - (self.score % 5))
        self.update_level()
    
    def heal_snake(self):
        """شفاء الثعبان (إزالة أي تأثيرات سلبية)"""
        if hasattr(self, 'reverse_active'):
            self.reverse_active = False
        self.add_effect('heal', self.snake[0])
    
    def refill_tools(self):
        """تجديد الأدوات"""
        self.special_tools += 2
        self.add_effect('refill', (300, 300))
    
    def toggle_cheat_mode(self):
        """تفعيل/تعطيل وضع الغش"""
        self.cheat_mode = not self.cheat_mode
        self.update_score_display()
        if self.cheat_mode:
            messagebox.showinfo("وضع الغش", "تم تفعيل وضع الغش!\n\nاستخدم:\nF1 للعدم القابل للهزيمة\nF2 لنقاط مضاعفة\nF3 لثعبان سريع")
        else:
            # إيقاف جميع أكواد الغش عند تعطيل وضع الغش
            for code in self.secret_codes:
                self.secret_codes[code] = False
    
    def activate_cheat_code(self, code):
        """تفعيل كود غش"""
        if self.cheat_mode:
            self.secret_codes[code] = not self.secret_codes[code]
            status = "مفعل" if self.secret_codes[code] else "معطل"
            messagebox.showinfo("كود غش", f"كود {code} {status}")
            self.update_score_display()
    
    def open_speed_settings(self):
        """فتح نافذة إعدادات السرعة"""
        settings_win = tk.Toplevel(self.master)
        settings_win.title("إعدادات السرعة")
        settings_win.geometry("300x200")
        settings_win.resizable(False, False)
        
        tk.Label(settings_win, text="اختر سرعة اللعبة:", font=('Arial', 14)).pack(pady=10)
        
        speeds = [("بطيئة", 180), ("عادية", 120), ("سريعة", 80), ("سريعة جداً", 50)]
        selected_speed = tk.IntVar(value=self.game_speed)
        
        for text, speed in speeds:
            tk.Radiobutton(
                settings_win, text=text, variable=selected_speed, 
                value=speed, font=('Arial', 12)
            ).pack(anchor='w', padx=50)
        
        def apply_speed():
            self.game_speed = selected_speed.get()
            self.save_settings()
            settings_win.destroy()
        
        tk.Button(
            settings_win, text="تطبيق", command=apply_speed,
            font=('Arial', 12), bg='#4CAF50', fg='white'
        ).pack(pady=10)
    
    def open_skin_settings(self):
        """فتح نافذة إعدادات المظهر"""
        skin_win = tk.Toplevel(self.master)
        skin_win.title("إعدادات المظهر")
        skin_win.geometry("400x350")
        skin_win.resizable(False, False)
        
        # إعدادات الألوان
        tk.Label(skin_win, text="إعدادات الألوان:", font=('Arial', 14, 'underline')).pack(pady=5)
        
        colors_frame = tk.Frame(skin_win)
        colors_frame.pack(pady=5)
        
        # لون الثعبان
        tk.Label(colors_frame, text="لون الثعبان:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        snake_color_btn = tk.Button(
            colors_frame, bg=self.snake_color, width=3, 
            command=lambda: self.choose_color('snake_color', snake_color_btn)
        )
        snake_color_btn.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        
        # لون الطعام
        tk.Label(colors_frame, text="لون الطعام:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        food_color_btn = tk.Button(
            colors_frame, bg=self.food_color, width=3, 
            command=lambda: self.choose_color('food_color', food_color_btn)
        )
        food_color_btn.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        
        # لون الطعام الخاص
        tk.Label(colors_frame, text="لون الطعام الخاص:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        special_food_color_btn = tk.Button(
            colors_frame, bg=self.special_food_color, width=3, 
            command=lambda: self.choose_color('special_food_color', special_food_color_btn)
        )
        special_food_color_btn.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        
        # لون الخلفية
        tk.Label(colors_frame, text="لون الخلفية:").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        bg_color_btn = tk.Button(
            colors_frame, bg=self.bg_color, width=3, 
            command=lambda: self.choose_color('bg_color', bg_color_btn)
        )
        bg_color_btn.grid(row=3, column=1, padx=5, pady=5, sticky='w')
        
        # لون العوائق
        tk.Label(colors_frame, text="لون العوائق:").grid(row=4, column=0, padx=5, pady=5, sticky='e')
        obstacle_color_btn = tk.Button(
            colors_frame, bg=self.obstacle_color, width=3, 
            command=lambda: self.choose_color('obstacle_color', obstacle_color_btn)
        )
        obstacle_color_btn.grid(row=4, column=1, padx=5, pady=5, sticky='w')
        
        def apply_settings():
            self.save_settings()
            self.canvas.config(bg=self.bg_color)
            skin_win.destroy()
        
        tk.Button(
            skin_win, text="تطبيق الإعدادات", command=apply_settings,
            font=('Arial', 12), bg='#2196F3', fg='white'
        ).pack(pady=10)
    
    def open_game_settings(self):
        """فتح نافذة إعدادات اللعبة"""
        settings_win = tk.Toplevel(self.master)
        settings_win.title("إعدادات اللعبة")
        settings_win.geometry("300x200")
        settings_win.resizable(False, False)
        
        tk.Label(settings_win, text="إعدادات اللعبة:", font=('Arial', 14)).pack(pady=10)
        
        wall_pass_var = tk.BooleanVar(value=self.wall_pass)
        tk.Checkbutton(
            settings_win, text="المرور عبر الجدران", 
            variable=wall_pass_var, font=('Arial', 12)
        ).pack(anchor='w', padx=20)
        
        ghost_var = tk.BooleanVar(value=self.ghost_mode)
        tk.Checkbutton(
            settings_win, text="وضع الشبح (لا تصادم)", 
            variable=ghost_var, font=('Arial', 12)
        ).pack(anchor='w', padx=20)
        
        cheat_var = tk.BooleanVar(value=self.cheat_mode)
        tk.Checkbutton(
            settings_win, text="تفعيل وضع الغش", 
            variable=cheat_var, font=('Arial', 12)
        ).pack(anchor='w', padx=20)
        
        def apply_settings():
            self.wall_pass = wall_pass_var.get()
            self.ghost_mode = ghost_var.get()
            self.cheat_mode = cheat_var.get()
            self.update_score_display()
            settings_win.destroy()
        
        tk.Button(
            settings_win, text="تطبيق", command=apply_settings,
            font=('Arial', 12), bg='#4CAF50', fg='white'
        ).pack(pady=10)
    
    def choose_color(self, color_type, button):
        """اختيار لون جديد"""
        from tkinter import colorchooser
        color = colorchooser.askcolor(title=f"اختر لون {color_type}")[1]
        if color:
            setattr(self, color_type, color)
            button.config(bg=color)
    
    def show_help(self):
        """عرض تعليمات اللعب"""
        help_text = """
        تعليمات لعبة الثعبان الاحترافية:
        
        التحكم:
        - استخدم مفاتيح الأسهم (↑ ↓ ← →) أو WASD للتحكم
        - اضغط P للإيقاف المؤقت
        - اضغط المسافة لإعادة التشغيل بعد الخسارة
        
        الميزات:
        - الطعام الأحمر: نقطة واحدة (أو نقطتان بوضع الغش)
        - الطعام الذهبي: 3 نقاط (أو 6 بوضع الغش)
        - العوائق: تظهر من المستوى 3 فما فوق
        
        القوى الإضافية:
        - الدرع (أزرق): حماية من الاصطدامات لمدة 10 ثواني
        - التباطؤ (بنفسجي): يبطئ اللعبة لمدة 8 ثواني
        - عكس الاتجاه (برتقالي): يعكس اتجاه الحركة لمدة 6 ثواني
        - وضع الشبح (رمادي): يمكنك المرور عبر الجدران لمدة 12 ثانية
        - الانتقال (بنفسجي غامق): ينقل الثعبان لمكان عشوائي
        
        الصناديق الغامضة:
        - تحتوي على مفاجآت عشوائية (جيدة أو سيئة)
        
        الأدوات الخاصة:
        - يمكنك استخدامها من قائمة الأدوات
        - كل أداة لها تأثير فريد
        
        أكواد الغش (في وضع الغش فقط):
        - F1: عدم القابل للهزيمة
        - F2: نقاط مضاعفة
        - F3: ثعبان سريع
        """
        messagebox.showinfo("تعليمات اللعب", help_text.strip())
    
    def show_secrets(self):
        """عرض أسرار اللعبة"""
        secrets_text = """
        أسرار وخدع اللعبة:
        
        1. كل 5 نقاط تنتقل لمستوى أعلى
        2. في المستويات الأعلى تظهر عوائق أكثر
        3. الصناديق الغامضة قد تحتوي على:
           - نقاط إضافية
           - أدوات إضافية
           - زيادة سرعة
           - تقليص حجم الثعبان
           - مفاجآت عشوائية
        
        4. يمكنك تفعيل وضع الغش من قائمة الأدوات
        5. عند تفعيل وضع الغش، استخدم:
           - F1 للعدم القابل للهزيمة
           - F2 لنقاط مضاعفة
           - F3 لثعبان سريع
        
        6. الأدوات الخاصة تعطيك قدرات مؤقتة:
           - إزالة جميع العوائق
           - تخطي المستوى الحالي
           - شفاء الثعبان
           - الحصول على أدوات إضافية
        
        7. حاول جمع أكبر عدد ممكن من النقاط لتحطيم رقمك القياسي!
        """
        messagebox.showinfo("أسرار اللعبة", secrets_text.strip())
    
    def show_about(self):
        """عرض معلومات عن اللعبة"""
        about_text = """
        Snake Ultimate - النسخة الاحترافية
        
        إصدار: 3.0
        تاريخ: 2023
        مطور بواسطة: DeepSeek Chat
        
        لعبة الثعبان الكلاسيكية مع ميزات متقدمة:
        - نظام مستويات متطور
        - قوى إضافية متنوعة
        - صناديق غامضة
        - أدوات خاصة
        - وضع غش مع أكواد سرية
        - تأثيرات بصرية مذهلة
        - إعدادات قابلة للتخصيص بالكامل
        - واجهة مستخدم محسنة
        
        تم تطوير اللعبة باستخدام Python و Tkinter
        """
        messagebox.showinfo("حول اللعبة", about_text.strip())

# تشغيل اللعبة
if __name__ == "__main__":
    root = tk.Tk()
    try:
        game = UltimateSnakeGame(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("خطأ", f"حدث خطأ: {str(e)}")