import time
import random
from instagrapi import Client


class InstagramBot:
    def __init__(self, username, password, proxy=None):
        """
        مقداردهی اولیه و ورود به حساب
        """
        self.client = Client()
        if proxy:
            self.client.set_proxy(proxy)
        self.client.login(username, password)
        self.messages_sent = 0
        self.start_time = time.time()

    def send_message(self, user_id, message):
        """
        ارسال پیام با تأخیر تصادفی برای رفتار طبیعی
        """
        delay = random.uniform(2, 5)  # تأخیر بین 2 تا 5 ثانیه
        time.sleep(delay)
        return self.client.direct_send(message, user_id)

    def limit_messages(self, max_messages_per_hour=50):
        """
        محدود کردن تعداد پیام‌های ارسالی در یک ساعت
        """
        elapsed_time = time.time() - self.start_time
        if elapsed_time > 3600:  # اگر یک ساعت گذشته باشد، شمارش مجدد
            self.start_time = time.time()
            self.messages_sent = 0

        if self.messages_sent < max_messages_per_hour:
            self.messages_sent += 1
            return True
        else:
            return False

    def monitor_message_seen(self, user_id):
        """
        بررسی دیده شدن پیام
        """
        while True:
            thread = self.client.direct_thread(user_id)
            last_message = thread.messages[0]

            if last_message.seen:  # اگر پیام دیده شد
                return True
            time.sleep(5)  # هر 5 ثانیه وضعیت پیام بررسی شود

    def delete_message(self, message_id):
        """
        حذف پیام
        """
        time.sleep(60)  # انتظار یک دقیقه قبل از حذف پیام
        self.client.direct_delete(message_id)
        print("پیام حذف شد.")

    def process_user(self, target_username, first_message, second_message):
        """
        فرآیند ارسال پیام و مدیریت دیده شدن
        """
        try:
            # دریافت user_id مخاطب
            user_id = self.client.user_id_from_username(target_username)

            # ارسال پیام اول
            if self.limit_messages():
                self.send_message(user_id, first_message)
                print(f"پیام اول به {target_username} ارسال شد.")
            else:
                print("محدودیت تعداد پیام‌ها رعایت شد. لطفاً بعداً تلاش کنید.")
                return

            # بررسی خوانده شدن پیام
            print("منتظر خوانده شدن پیام هستیم...")
            if self.monitor_message_seen(user_id):
                print(f"پیام توسط {target_username} خوانده شد.")

                # ارسال پیام دوم
                if self.limit_messages():
                    second_message_id = self.send_message(user_id, second_message)
                    print("پیام دوم ارسال شد.")
                else:
                    print("محدودیت تعداد پیام‌ها رعایت شد. لطفاً بعداً تلاش کنید.")
                    return

                # حذف پیام دوم
                self.delete_message(second_message_id)
        except Exception as e:
            print(f"خطایی رخ داد: {e}")


# پیکربندی ربات
USERNAME = "YOUR_USERNAME"  # نام کاربری اینستاگرام
PASSWORD = "YOUR_PASSWORD"  # رمز عبور اینستاگرام
PROXY = None  # در صورت نیاز به پروکسی، اطلاعات آن را وارد کنید

# اطلاعات پیام‌ها
TARGET_USERNAME = "TARGET_USERNAME"  # نام کاربری مخاطب
FIRST_MESSAGE = "پیام اول شما اینجا قرار دارد."  # پیام اول
SECOND_MESSAGE = "این پیام یک دقیقه بعد حذف می‌شود."  # پیام دوم

# اجرای ربات
if __name__ == "__main__":
    bot = InstagramBot(USERNAME, PASSWORD, PROXY)
    bot.process_user(TARGET_USERNAME, FIRST_MESSAGE, SECOND_MESSAGE)
