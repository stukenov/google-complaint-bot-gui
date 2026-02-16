import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import time
import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager


class GoogleComplaintBot:
    def __init__(self, root):
        self.root = root
        self.root.title("Google Complaint Bot")
        self.root.geometry("800x600")
        
        self.driver = None
        self.is_running = False
        
        self.setup_ui()
        
    def create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Загрузить запросы...", command=self.load_queries)
        file_menu.add_command(label="Сохранить запросы...", command=self.save_queries)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Справка", menu=help_menu)
        help_menu.add_command(label="О программе", command=self.show_about)
        
    def load_queries(self):
        """Load queries from file"""
        try:
            filename = filedialog.askopenfilename(
                title="Загрузить запросы",
                filetypes=[("JSON файлы", "*.json"), ("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
            )
            if filename:
                if filename.endswith('.json'):
                    with open(filename, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        queries = data.get('queries', [])
                        self.queries_text.delete("1.0", tk.END)
                        self.queries_text.insert("1.0", '\n'.join(queries))
                else:
                    with open(filename, 'r', encoding='utf-8') as f:
                        content = f.read()
                        self.queries_text.delete("1.0", tk.END)
                        self.queries_text.insert("1.0", content)
                self.log_message(f"Загружено запросов из файла: {filename}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {str(e)}")
            
    def save_queries(self):
        """Save queries to file"""
        try:
            queries = self.queries_text.get("1.0", tk.END).strip().split('\n')
            queries = [q.strip() for q in queries if q.strip()]
            
            if not queries:
                messagebox.showwarning("Предупреждение", "Нет запросов для сохранения")
                return
                
            filename = filedialog.asksaveasfilename(
                title="Сохранить запросы",
                defaultextension=".json",
                filetypes=[("JSON файлы", "*.json"), ("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
            )
            if filename:
                if filename.endswith('.json'):
                    data = {
                        'queries': queries,
                        'created': time.strftime("%Y-%m-%d %H:%M:%S")
                    }
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                else:
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write('\n'.join(queries))
                self.log_message(f"Запросы сохранены в файл: {filename}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {str(e)}")
            
    def show_about(self):
        """Show about dialog"""
        about_text = """Google Complaint Bot v1.0
        
Приложение для автоматизации подачи жалоб в Google.

⚠️ Важно: Используйте ответственно и в соответствии с условиями использования Google.

Разработано с использованием:
- Python + tkinter (GUI)
- Selenium WebDriver (автоматизация браузера)
- ChromeDriver (управление Chrome)

© 2024"""
        messagebox.showinfo("О программе", about_text)
        
    def setup_ui(self):
        # Create menu
        self.create_menu()
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Search queries input
        ttk.Label(main_frame, text="Поисковые запросы (по одному на строку):").grid(
            row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 5)
        )
        
        self.queries_text = scrolledtext.ScrolledText(main_frame, height=8, width=60)
        self.queries_text.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Settings frame
        settings_frame = ttk.LabelFrame(main_frame, text="Настройки", padding="5")
        settings_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        settings_frame.columnconfigure(1, weight=1)
        
        # Delay setting
        ttk.Label(settings_frame, text="Задержка между действиями (сек):").grid(
            row=0, column=0, sticky=tk.W, padx=(0, 5)
        )
        self.delay_var = tk.StringVar(value="2")
        delay_entry = ttk.Entry(settings_frame, textvariable=self.delay_var, width=10)
        delay_entry.grid(row=0, column=1, sticky=tk.W)
        
        # Headless mode
        self.headless_var = tk.BooleanVar(value=False)
        headless_check = ttk.Checkbutton(
            settings_frame, 
            text="Скрытый режим браузера", 
            variable=self.headless_var
        )
        headless_check.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(5, 0))
        
        # Control buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=3, column=0, columnspan=2, pady=(0, 10))
        
        self.start_button = ttk.Button(
            buttons_frame, 
            text="Запустить", 
            command=self.start_complaints
        )
        self.start_button.grid(row=0, column=0, padx=(0, 5))
        
        self.stop_button = ttk.Button(
            buttons_frame, 
            text="Остановить", 
            command=self.stop_complaints,
            state=tk.DISABLED
        )
        self.stop_button.grid(row=0, column=1)
        
        # Log output
        ttk.Label(main_frame, text="Лог выполнения:").grid(
            row=4, column=0, columnspan=2, sticky=tk.W, pady=(10, 5)
        )
        
        self.log_text = scrolledtext.ScrolledText(main_frame, height=15, width=60)
        self.log_text.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
    def log_message(self, message):
        """Add message to log with timestamp"""
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update()
        
    def start_complaints(self):
        """Start the complaint process in a separate thread"""
        queries = self.queries_text.get("1.0", tk.END).strip().split('\n')
        queries = [q.strip() for q in queries if q.strip()]
        
        if not queries:
            messagebox.showwarning("Предупреждение", "Введите хотя бы один поисковый запрос")
            return
            
        self.is_running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.progress.start()
        self.log_text.delete("1.0", tk.END)
        
        # Start in separate thread to keep GUI responsive
        thread = threading.Thread(target=self.run_complaints, args=(queries,))
        thread.daemon = True
        thread.start()
        
    def stop_complaints(self):
        """Stop the complaint process"""
        self.is_running = False
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.progress.stop()
        self.log_message("Процесс остановлен пользователем")
        
    def setup_driver(self):
        """Setup Chrome WebDriver"""
        try:
            self.log_message("Инициализация браузера...")
            chrome_options = Options()
            if self.headless_var.get():
                chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Automatically download and setup ChromeDriver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.log_message("Браузер успешно инициализирован")
            return True
        except Exception as e:
            self.log_message(f"Ошибка инициализации браузера: {str(e)}")
            return False
            
    def run_complaints(self, queries):
        """Main complaint processing function"""
        try:
            if not self.setup_driver():
                return
                
            delay = float(self.delay_var.get())
            
            for i, query in enumerate(queries):
                if not self.is_running:
                    break
                    
                self.log_message(f"Обрабатываем запрос {i+1}/{len(queries)}: {query}")
                
                try:
                    self.process_single_query(query, delay)
                except Exception as e:
                    self.log_message(f"Ошибка при обработке запроса '{query}': {str(e)}")
                    
                if self.is_running and i < len(queries) - 1:
                    self.log_message(f"Пауза {delay} секунд перед следующим запросом...")
                    time.sleep(delay)
                    
        except Exception as e:
            self.log_message(f"Критическая ошибка: {str(e)}")
        finally:
            if self.driver:
                self.driver.quit()
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.progress.stop()
            self.log_message("Процесс завершен")
            
    def process_single_query(self, query, delay):
        """Process a single search query and submit complaint"""
        try:
            # Navigate to Google
            self.log_message("Открываем Google...")
            self.driver.get("https://www.google.com")
            time.sleep(delay)
            
            # Accept cookies if present
            try:
                accept_button = WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Принять все') or contains(text(), 'Accept all')]"))
                )
                accept_button.click()
                time.sleep(1)
            except TimeoutException:
                pass
            
            # Find search box and enter query
            self.log_message(f"Вводим запрос: {query}")
            search_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "q"))
            )
            search_box.clear()
            search_box.send_keys(query)
            
            # Wait for suggestions to appear
            time.sleep(delay)
            
            # Look for complaint button
            self.log_message("Ищем кнопку жалобы...")
            self.find_and_click_complaint_button(delay)
            
        except TimeoutException:
            self.log_message("Таймаут при загрузке страницы")
        except Exception as e:
            self.log_message(f"Ошибка при обработке запроса: {str(e)}")
            
    def find_and_click_complaint_button(self, delay):
        """Find and click the complaint button"""
        try:
            # This is a simplified version - actual implementation would need
            # to handle Google's specific UI elements
            self.log_message("Поиск элементов жалобы...")
            
            # Look for "Report inappropriate predictions" or similar text
            complaint_selectors = [
                "//span[contains(text(), 'неприемлемые подсказки')]",
                "//span[contains(text(), 'inappropriate predictions')]",
                "//button[contains(@aria-label, 'report')]",
                "//div[contains(text(), 'Пожаловаться')]"
            ]
            
            complaint_button = None
            for selector in complaint_selectors:
                try:
                    complaint_button = self.driver.find_element(By.XPATH, selector)
                    if complaint_button.is_displayed():
                        break
                except NoSuchElementException:
                    continue
                    
            if complaint_button:
                self.log_message("Нажимаем на кнопку жалобы...")
                complaint_button.click()
                time.sleep(delay)
                
                # Handle complaint form
                self.handle_complaint_form(delay)
            else:
                self.log_message("Кнопка жалобы не найдена")
                
        except Exception as e:
            self.log_message(f"Ошибка при поиске кнопки жалобы: {str(e)}")
            
    def handle_complaint_form(self, delay):
        """Handle the complaint form submission"""
        try:
            self.log_message("Заполняем форму жалобы...")
            
            # Wait for form to load
            time.sleep(delay)
            
            # Look for "Harassment and bullying" option
            harassment_selectors = [
                "//span[contains(text(), 'Оскорбление и унижение')]",
                "//span[contains(text(), 'Harassment')]",
                "//label[contains(text(), 'унижение')]"
            ]
            
            for selector in harassment_selectors:
                try:
                    option = self.driver.find_element(By.XPATH, selector)
                    if option.is_displayed():
                        option.click()
                        self.log_message("Выбрали тип жалобы: Оскорбление и унижение")
                        break
                except NoSuchElementException:
                    continue
                    
            time.sleep(delay)
            
            # Find and fill comment field
            comment_selectors = [
                "//textarea",
                "//input[@type='text']",
                "//div[@contenteditable='true']"
            ]
            
            complaint_text = ("Данный запрос является искусственно сформированным для того, "
                            "чтобы исказить информацию о человеке и запятнать его репутацию. "
                            "Прошу срочно удалить данный запрос")
            
            for selector in comment_selectors:
                try:
                    comment_field = self.driver.find_element(By.XPATH, selector)
                    if comment_field.is_displayed():
                        comment_field.clear()
                        comment_field.send_keys(complaint_text)
                        self.log_message("Заполнили текст жалобы")
                        break
                except NoSuchElementException:
                    continue
                    
            time.sleep(delay)
            
            # Find and click submit button
            submit_selectors = [
                "//button[contains(text(), 'Отправить')]",
                "//button[contains(text(), 'Submit')]",
                "//input[@type='submit']",
                "//button[@type='submit']"
            ]
            
            for selector in submit_selectors:
                try:
                    submit_button = self.driver.find_element(By.XPATH, selector)
                    if submit_button.is_displayed() and submit_button.is_enabled():
                        submit_button.click()
                        self.log_message("Жалоба отправлена!")
                        return
                except NoSuchElementException:
                    continue
                    
            self.log_message("Кнопка отправки не найдена")
            
        except Exception as e:
            self.log_message(f"Ошибка при заполнении формы: {str(e)}")


def main():
    root = tk.Tk()
    app = GoogleComplaintBot(root)
    root.mainloop()


if __name__ == "__main__":
    main()
