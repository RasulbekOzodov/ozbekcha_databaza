#!/usr/bin/env python3
"""
Test misollar - PostgreSQL stilida
"""

from uzdb_final import Executor
import shutil
import os
import sys

# Windows uchun UTF-8 encoding o'rnatish
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def test_setup():
    """Test uchun database tayyorlash"""
    if os.path.exists("test_db"):
        shutil.rmtree("test_db")
    return Executor("test_db")

def print_result(title, result):
    """Natijalarni chiroyli chiqarish"""
    print(f"\n{'='*60}")
    print(f"📊 {title}")
    print('='*60)
    if isinstance(result, list):
        if result:
            cols = list(result[0].keys())
            widths = {c: max(len(c), max(len(str(r.get(c,''))) for r in result)) for c in cols}
            line = '+' + '+'.join('-'*(widths[c]+2) for c in cols) + '+'
            print(line)
            print('|' + '|'.join(f" {c:<{widths[c]}} " for c in cols) + '|')
            print(line)
            for r in result:
                print('|' + '|'.join(f" {str(r.get(c,'')):<{widths[c]}} " for c in cols) + '|')
            print(line)
            print(f"✅ {len(result)} qator topildi")
        else:
            print("(Bo'sh natija)")
    else:
        print(f"✅ {result}")

def test_1_create_tables(db):
    """1️⃣ Jadvallar yaratish (CREATE TABLE)"""
    print("\n" + "🔷"*30)
    print("TEST 1: JADVALLAR YARATISH")
    print("🔷"*30)

    # Foydalanuvchilar jadvali
    sql = """
    JADVAL_YARAT foydalanuvchilar (
        id BUTUN_SON ASOSIY_KALIT,
        ism MATN BOSH_EMAS,
        familiya MATN,
        yosh BUTUN_SON,
        email MATN
    )
    """
    print(f"\n📝 SQL: {sql.strip()}")
    result = db.bajar(sql)
    print(f"   {result}")

    # Buyurtmalar jadvali
    sql = """
    JADVAL_YARAT buyurtmalar (
        id BUTUN_SON ASOSIY_KALIT,
        foydalanuvchi_id BUTUN_SON,
        mahsulot MATN,
        narx HAQIQIY,
        sana MATN
    )
    """
    print(f"\n📝 SQL: {sql.strip()}")
    result = db.bajar(sql)
    print(f"   {result}")

    # Mahsulotlar jadvali
    sql = """
    JADVAL_YARAT mahsulotlar (
        id BUTUN_SON ASOSIY_KALIT,
        nom MATN,
        kategoriya MATN,
        narx HAQIQIY,
        soni BUTUN_SON
    )
    """
    print(f"\n📝 SQL: {sql.strip()}")
    result = db.bajar(sql)
    print(f"   {result}")

def test_2_insert_data(db):
    """2️⃣ Ma'lumot qo'shish (INSERT)"""
    print("\n" + "🔷"*30)
    print("TEST 2: MA'LUMOT QO'SHISH")
    print("🔷"*30)

    # Foydalanuvchilar
    users = [
        (1, 'Ali', 'Valiyev', 25, 'ali@mail.uz'),
        (2, 'Malika', 'Karimova', 30, 'malika@mail.uz'),
        (3, 'Sardor', 'Toshmatov', 28, 'sardor@mail.uz'),
        (4, 'Nilufar', 'Rahimova', 22, 'nilufar@mail.uz'),
        (5, 'Jamshid', 'Ergashev', 35, 'jamshid@mail.uz'),
        (6, 'Dildora', 'Ahmadova', 27, 'dildora@mail.uz'),
        (7, 'Bobur', 'Usmonov', 31, 'bobur@mail.uz'),
        (8, 'Zarina', 'Hakimova', 24, 'zarina@mail.uz'),
    ]

    for id, ism, familiya, yosh, email in users:
        sql = f"QO'SH ICHIGA foydalanuvchilar (id, ism, familiya, yosh, email) QIYMATLAR ({id}, '{ism}', '{familiya}', {yosh}, '{email}')"
        result = db.bajar(sql)
        print(f"   {result}")

    # Mahsulotlar
    products = [
        (1, 'Laptop', 'Elektronika', 5000000, 15),
        (2, 'Telefon', 'Elektronika', 3000000, 25),
        (3, 'Stol', 'Mebel', 800000, 10),
        (4, 'Kitob', 'Oquv', 50000, 100),
        (5, 'Ruchka', 'Oquv', 5000, 500),
    ]

    for id, nom, kategoriya, narx, soni in products:
        sql = f"QO'SH ICHIGA mahsulotlar (id, nom, kategoriya, narx, soni) QIYMATLAR ({id}, '{nom}', '{kategoriya}', {narx}, {soni})"
        result = db.bajar(sql)
        print(f"   {result}")

    # Buyurtmalar
    orders = [
        (1, 1, 'Laptop', 5000000, '2024-01-15'),
        (2, 2, 'Telefon', 3000000, '2024-01-16'),
        (3, 3, 'Stol', 800000, '2024-01-17'),
        (4, 1, 'Kitob', 50000, '2024-01-18'),
        (5, 4, 'Ruchka', 5000, '2024-01-19'),
        (6, 2, 'Laptop', 5000000, '2024-01-20'),
    ]

    for id, uid, mahsulot, narx, sana in orders:
        sql = f"QO'SH ICHIGA buyurtmalar (id, foydalanuvchi_id, mahsulot, narx, sana) QIYMATLAR ({id}, {uid}, '{mahsulot}', {narx}, '{sana}')"
        result = db.bajar(sql)
        print(f"   {result}")

def test_3_select_queries(db):
    """3️⃣ SELECT so'rovlari"""
    print("\n" + "🔷"*30)
    print("TEST 3: SELECT SO'ROVLARI")
    print("🔷"*30)

    # Barcha foydalanuvchilar
    sql = "TANLASH * JADVALDAN foydalanuvchilar"
    print(f"\n📝 SQL: {sql}")
    result = db.bajar(sql)
    print_result("Barcha foydalanuvchilar", result)

    # Faqat ism va email
    sql = "TANLASH ism, email JADVALDAN foydalanuvchilar"
    print(f"\n📝 SQL: {sql}")
    result = db.bajar(sql)
    print_result("Ism va email", result)

    # Barcha mahsulotlar
    sql = "TANLASH * JADVALDAN mahsulotlar"
    print(f"\n📝 SQL: {sql}")
    result = db.bajar(sql)
    print_result("Barcha mahsulotlar", result)

def test_4_where_conditions(db):
    """4️⃣ WHERE shartlari"""
    print("\n" + "🔷"*30)
    print("TEST 4: WHERE SHARTLARI")
    print("🔷"*30)

    # Yoshi 25 dan katta
    sql = "TANLASH ism, familiya, yosh JADVALDAN foydalanuvchilar QAYERDA yosh > 25"
    print(f"\n📝 SQL: {sql}")
    result = db.bajar(sql)
    print_result("Yoshi 25 dan katta", result)

    # Yoshi 30 ga teng
    sql = "TANLASH ism, yosh JADVALDAN foydalanuvchilar QAYERDA yosh = 30"
    print(f"\n📝 SQL: {sql}")
    result = db.bajar(sql)
    print_result("Yoshi 30 ga teng", result)

    # Narxi 1000000 dan past mahsulotlar
    sql = "TANLASH nom, narx JADVALDAN mahsulotlar QAYERDA narx < 1000000"
    print(f"\n📝 SQL: {sql}")
    result = db.bajar(sql)
    print_result("Arzon mahsulotlar", result)

    # Elektronika kategoriyasi
    sql = "TANLASH nom, kategoriya, narx JADVALDAN mahsulotlar QAYERDA kategoriya = 'Elektronika'"
    print(f"\n📝 SQL: {sql}")
    result = db.bajar(sql)
    print_result("Elektronika mahsulotlari", result)

def test_5_order_by(db):
    """5️⃣ ORDER BY (TARTIBLA)"""
    print("\n" + "🔷"*30)
    print("TEST 5: TARTIBLA (ORDER BY)")
    print("🔷"*30)

    # Yoshiga ko'ra o'sish tartibida
    sql = "TANLASH ism, yosh JADVALDAN foydalanuvchilar TARTIBLA yosh OSHISH"
    print(f"\n📝 SQL: {sql}")
    result = db.bajar(sql)
    print_result("Yosh bo'yicha o'sish", result)

    # Yoshiga ko'ra kamayish tartibida
    sql = "TANLASH ism, yosh JADVALDAN foydalanuvchilar TARTIBLA yosh KAMAYISH"
    print(f"\n📝 SQL: {sql}")
    result = db.bajar(sql)
    print_result("Yosh bo'yicha kamayish", result)

    # Narx bo'yicha kamayish
    sql = "TANLASH nom, narx JADVALDAN mahsulotlar TARTIBLA narx KAMAYISH"
    print(f"\n📝 SQL: {sql}")
    result = db.bajar(sql)
    print_result("Qimmat mahsulotlar birinchi", result)

def test_6_limit(db):
    """6️⃣ LIMIT (CHEGARA)"""
    print("\n" + "🔷"*30)
    print("TEST 6: CHEGARA (LIMIT)")
    print("🔷"*30)

    # Eng yosh 3 ta foydalanuvchi
    sql = "TANLASH ism, yosh JADVALDAN foydalanuvchilar TARTIBLA yosh OSHISH CHEGARA 3"
    print(f"\n📝 SQL: {sql}")
    result = db.bajar(sql)
    print_result("Eng yosh 3 ta foydalanuvchi", result)

    # Eng qimmat 2 ta mahsulot
    sql = "TANLASH nom, narx JADVALDAN mahsulotlar TARTIBLA narx KAMAYISH CHEGARA 2"
    print(f"\n📝 SQL: {sql}")
    result = db.bajar(sql)
    print_result("Eng qimmat mahsulotlar", result)

    # Oxirgi 3 ta buyurtma
    sql = "TANLASH mahsulot, narx, sana JADVALDAN buyurtmalar TARTIBLA id KAMAYISH CHEGARA 3"
    print(f"\n📝 SQL: {sql}")
    result = db.bajar(sql)
    print_result("Oxirgi buyurtmalar", result)

def test_7_complex_queries(db):
    """7️⃣ Murakkab so'rovlar"""
    print("\n" + "🔷"*30)
    print("TEST 7: MURAKKAB SO'ROVLAR")
    print("🔷"*30)

    # 25 va 30 oralig'idagi foydalanuvchilar
    sql = "TANLASH ism, yosh JADVALDAN foydalanuvchilar QAYERDA yosh > 24 VA yosh < 31"
    print(f"\n📝 SQL: {sql}")
    result = db.bajar(sql)
    print_result("25-30 yosh oralig'idagi foydalanuvchilar", result)

    # Arzon va ko'p mahsulotlar
    sql = "TANLASH nom, narx, soni JADVALDAN mahsulotlar QAYERDA narx < 1000000 VA soni > 50"
    print(f"\n📝 SQL: {sql}")
    result = db.bajar(sql)
    print_result("Arzon va ko'p mavjud mahsulotlar", result)

def run_all_tests():
    """Barcha testlarni ishga tushirish"""
    print("""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║      🧪 UZDB TEST SUITE - PostgreSQL Stilida                  ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
    """)

    db = test_setup()

    try:
        test_1_create_tables(db)
        test_2_insert_data(db)
        test_3_select_queries(db)
        test_4_where_conditions(db)
        test_5_order_by(db)
        test_6_limit(db)
        test_7_complex_queries(db)

        print("\n" + "="*60)
        print("✅ BARCHA TESTLAR MUVAFFAQIYATLI O'TDI!")
        print("="*60)
        print(f"\n📁 Database joylashuvi: test_db/")
        print(f"📊 Jadvallar: {', '.join(db.jadvallar_royxati())}")

    except Exception as e:
        print(f"\n❌ XATO: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_all_tests()
