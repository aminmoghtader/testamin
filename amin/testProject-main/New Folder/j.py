import json
import glob

def merge_json_files(output_filename="final_data.json"):
    merged_data = []

    # دریافت لیست فایل‌های JSON موجود در مسیر فعلی
    json_files = glob.glob("*.json")

    for file in json_files:
        with open(file, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)

                if isinstance(data, list):  # اگر داده‌ها لیست باشند
                    merged_data.extend(data)
                elif isinstance(data, dict):  # اگر داده‌ها دیکشنری باشند
                    merged_data.append(data)
                else:
                    print(f"⚠️ فرمت فایل {file} پشتیبانی نمی‌شود.")

            except json.JSONDecodeError:
                print(f"❌ خطا در خواندن فایل {file}")

    # ذخیره داده‌های ترکیب‌شده در فایل جدید
    with open(output_filename, "w", encoding="utf-8") as output_file:
        json.dump(merged_data, output_file, indent=4, ensure_ascii=False)

    print(f"✅ داده‌های ترکیب‌شده در {output_filename} ذخیره شد.")

# اجرای تابع
merge_json_files()
