import pandas as pd
import subprocess
import os
from datetime import datetime

# -----------------------------------------------------
# 1. إعدادات الملف (المؤكدة)
# -----------------------------------------------------
# المسار الكامل والمؤكد لملف Excel
EXCEL_FILE_PATH = r'C:\Users\user\Desktop\منظومة التدريب الجديدة\منظومة التدريب .xlsm'

# اسم الشيت التي تحتوي على بيانات البحث
SHEET_NAME = 'TR-Date'

# ملف CSV الذي سيقرأه موقع الويب
CSV_FILE_PATH = 'data.csv'       

# -----------------------------------------------------
# 2. وظيفة التحديث والرفع
# -----------------------------------------------------
def update_and_push_data():
    repo_path = os.getcwd() 
    csv_output_path = os.path.join(repo_path, CSV_FILE_PATH)

    # التحقق من وجود ملف Excel
    if not os.path.exists(EXCEL_FILE_PATH):
        print("❌ خطأ: ملف Excel غير موجود في المسار المحدد. يرجى التأكد من اسم الملف والمسار.")
        return

    # -----------------------------------------------------
    # وظيفة مساعدة لتشغيل أوامر Git وعرض النتيجة بشكل واضح
    # -----------------------------------------------------
    def run_git_command(command, error_msg):
        # تشغيل الأمر مع التقاط الإخراج والأخطاء
        result = subprocess.run(command, capture_output=True, text=True, cwd=repo_path)
        
        if result.returncode != 0:
            # إذا فشل الأمر (return code غير صفر)
            print(f"❌ خطأ في أمر Git: {error_msg}")
            print(f"Git Stderr (رسالة الخطأ):\n{result.stderr}")
            # نرفع استثناء لإيقاف السكريبت وإظهار المشكلة
            raise subprocess.CalledProcessError(result.returncode, command, output=result.stdout, stderr=result.stderr)
        
        # طباعة الإخراج القياسي لأوامر Pull/Push
        if result.stdout.strip():
            print(f"Git Output:\n{result.stdout.strip()}")
        
        return result.stdout

    try:
        # القراءة من شيت Excel المحددة
        print(f"🔄 قراءة البيانات من الملف: {EXCEL_FILE_PATH}, شيت: {SHEET_NAME}...")
        df = pd.read_excel(EXCEL_FILE_PATH, sheet_name=SHEET_NAME)
        
        # حفظ البيانات كملف CSV في مجلد المستودع المحلي
        df.to_csv(csv_output_path, index=False, encoding='utf-8')
        
        print(f"✅ تم تحديث ملف {CSV_FILE_PATH} محلياً. يحتوي على {len(df)} صفاً.")

        # 3. تنفيذ أوامر Git (ستظهر رسائل واضحة الآن)
        
        print("\n--- بدء عملية الرفع (Git) ---")
        
        # سحب أحدث التغييرات قبل الرفع (لحل أي تعارض محتمل)
        print("-> سحب التغييرات الأخيرة...")
        run_git_command(['git', 'pull', 'origin', 'main'], "فشل سحب التغييرات.")
        
        # إضافة الملف المحدّث للمتابعة
        print("-> إضافة الملف للتثبيت (Commit)...")
        run_git_command(['git', 'add', CSV_FILE_PATH], "فشل إضافة الملف.")
        
        # عمل Commit برسالة واضحة
        commit_message = f"AUTO: Update data via automation - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        print("-> إنشاء تثبيت (Commit)...")
        run_git_command(['git', 'commit', '-m', commit_message], "فشل إنشاء التثبيت.")
        
        # رفع التغييرات إلى GitHub
        print("-> رفع التغييرات إلى GitHub...")
        run_git_command(['git', 'push', 'origin', 'main'], "فشل الرفع (Push).")
        
        print("\n--------------------------------------------------")
        print("🚀 تم الرفع بنجاح إلى GitHub!")
        print("سيتم تحديث موقعك خلال دقيقة واحدة.")
        print("--------------------------------------------------")

    except subprocess.CalledProcessError:
        # يتم التقاط هذا من دالة run_git_command وطباعة الخطأ بالداخل
        print("\n⚠️ فشل الرفع. تم طباعة رسالة الخطأ أعلاه. يرجى التحقق من صلاحياتك.")
    except Exception as e:
        print(f"\n❌ فشل عملية الأتمتة: {e}")
        if "Permission denied" in str(e) or "Access is denied" in str(e):
             print("\n⚠️ تنبيه: فشل القراءة، عادة ما يحدث هذا لأن ملف Excel مفتوح حالياً. يرجى إغلاقه والمحاولة مرة أخرى.")


if __name__ == "__main__":
    update_and_push_data()