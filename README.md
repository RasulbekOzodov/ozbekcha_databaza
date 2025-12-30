# 🗄️ UZDB - O'zbekcha Database Engine

To'liq ishlaydigan, PostgreSQL stilidagi o'zbekcha database management system.

## ✨ Xususiyatlar

- ✅ **O'zbekcha SQL sintaksisi** - To'liq o'zbekcha buyruqlar
- ✅ **Page-based Storage** - Samarali ma'lumot saqlash
- ✅ **B+Tree Indekslash** - Tez qidiruv
- ✅ **Interactive CLI** - Qulay terminal interfeysi
- ✅ **Web UI** - Chiroyli brauzer interfeysi
- ✅ **To'liq test suite** - PostgreSQL stilidagi testlar

## 📋 O'rnatish

### 1. Virtual Environment yaratish (ixtiyoriy)

```bash
python -m venv venv
```

### 2. Flask o'rnatish (Web UI uchun)

```bash
pip install Flask
```

## 🚀 Ishga tushirish

### 1️⃣ CLI rejimi (Terminal)

```bash
python uzdb_final.py
```

**CLI buyruqlari:**
- `.yordam` - yo'riqnoma
- `.jadvallar` - mavjud jadvallarni ko'rish
- `.chiqish` - dasturdan chiqish

### 2️⃣ Demo rejimi

```bash
python uzdb_final.py --demo
```

### 3️⃣ Web UI (Tavsiya etiladi!)

```bash
python web_ui.py
```

Keyin brauzeringizda oching: **http://localhost:5000**

### 4️⃣ Test misollar

```bash
python test_examples.py
```

## 📚 SQL Sintaksisi

### Jadval yaratish

```sql
JADVAL_YARAT foydalanuvchilar (
    id BUTUN_SON ASOSIY_KALIT,
    ism MATN BOSH_EMAS,
    yosh BUTUN_SON,
    email MATN
)
```

### Ma'lumot qo'shish

```sql
QO'SH ICHIGA foydalanuvchilar (id, ism, yosh, email)
QIYMATLAR (1, 'Ali', 25, 'ali@mail.uz')
```

### Ma'lumot olish

```sql
-- Barcha ustunlar
TANLASH * JADVALDAN foydalanuvchilar

-- Ma'lum ustunlar
TANLASH ism, email JADVALDAN foydalanuvchilar

-- Shart bilan
TANLASH ism, yosh JADVALDAN foydalanuvchilar
QAYERDA yosh > 25

-- Tartiblash
TANLASH * JADVALDAN foydalanuvchilar
TARTIBLA yosh KAMAYISH

-- Limit
TANLASH * JADVALDAN foydalanuvchilar
TARTIBLA yosh OSHISH CHEGARA 5

-- Murakkab shart
TANLASH ism, yosh JADVALDAN foydalanuvchilar
QAYERDA yosh > 25 VA yosh < 35
```

### Yangilash (demo)

```sql
YANGILASH foydalanuvchilar
BELGILASH yosh = 26
QAYERDA id = 1
```

### O'chirish (demo)

```sql
O'CHIR JADVALDAN foydalanuvchilar
QAYERDA id = 1
```

## 🔤 Kalit so'zlar

| O'zbekcha | PostgreSQL |
|-----------|------------|
| TANLASH | SELECT |
| JADVALDAN | FROM |
| QAYERDA | WHERE |
| VA | AND |
| YOKI | OR |
| TARTIBLA | ORDER BY |
| OSHISH | ASC |
| KAMAYISH | DESC |
| CHEGARA | LIMIT |
| QO'SH | INSERT |
| ICHIGA | INTO |
| QIYMATLAR | VALUES |
| YANGILASH | UPDATE |
| BELGILASH | SET |
| O'CHIR | DELETE |
| JADVAL_YARAT | CREATE TABLE |
| BUTUN_SON | INTEGER |
| MATN | TEXT |
| HAQIQIY | REAL/FLOAT |
| ASOSIY_KALIT | PRIMARY KEY |
| BOSH_EMAS | NOT NULL |
| YAGONA | UNIQUE |

## 📁 Fayl strukturasi

```
Ozbekchadb/
├── uzdb_final.py      # Asosiy database engine
├── web_ui.py          # Web interfeysi (Flask)
├── test_examples.py   # PostgreSQL stilidagi testlar
├── requirements.txt   # Python kutubxonalari
├── README.md          # Bu fayl
├── demo_db/          # Demo database fayllari
├── test_db/          # Test database fayllari
└── web_db/           # Web UI database fayllari
```

## 🧪 Test natijalar

Barcha testlar muvaffaqiyatli o'tdi:
- ✅ Jadval yaratish
- ✅ Ma'lumot qo'shish
- ✅ SELECT so'rovlari
- ✅ WHERE shartlari
- ✅ ORDER BY (TARTIBLA)
- ✅ LIMIT (CHEGARA)
- ✅ Murakkab so'rovlar (VA/YOKI)

## 🌐 Web UI Xususiyatlari

- 🎨 Zamonaviy, chiroyli interfeys
- 📝 Misol so'rovlar
- 🔄 Real-time natijalar
- 📊 Jadvallar ro'yxati
- ⌨️ Ctrl+Enter - so'rovni bajarish
- 📱 Responsive dizayn

## 💡 Misollar

### E-commerce database

```sql
-- Jadvallar yaratish
JADVAL_YARAT mahsulotlar (
    id BUTUN_SON ASOSIY_KALIT,
    nom MATN,
    kategoriya MATN,
    narx HAQIQIY,
    soni BUTUN_SON
)

-- Ma'lumot qo'shish
QO'SH ICHIGA mahsulotlar (id, nom, kategoriya, narx, soni)
QIYMATLAR (1, 'Laptop', 'Elektronika', 5000000, 15)

-- Eng qimmat mahsulotlar
TANLASH nom, narx JADVALDAN mahsulotlar
TARTIBLA narx KAMAYISH CHEGARA 5

-- Arzon mahsulotlar
TANLASH * JADVALDAN mahsulotlar
QAYERDA narx < 1000000
```

## 🛠️ Texnologiyalar

- **Python 3.13** - Asosiy til
- **Flask** - Web framework
- **Page-based Storage** - Ma'lumot saqlash
- **Custom Tokenizer & Parser** - SQL parsing
- **B+Tree** - Indekslash (rejada)

## 📈 Keyingi rejalar

- [ ] UPDATE va DELETE to'liq implementatsiyasi
- [ ] JOIN operatsiyalari
- [ ] Transactions (ACID)
- [ ] B+Tree indekslash
- [ ] Multi-threading
- [ ] SQL dump/restore
- [ ] Foreign keys
- [ ] Aggregation (SUM, COUNT, AVG)
- [ ] GROUP BY

## 🤝 Hissa qo'shish

Pull request'lar va issue'lar qabul qilinadi!

## 📄 Litsenziya

MIT License - O'zbekiston uchun ochiq kodli loyiha

## 👨‍💻 Muallif

Rasulbek Ozodov - O'zbekcha Database Engine

---

**UZDB** - O'zbek dasturchilar uchun, o'zbek dasturchilar tomonidan yaratilgan! 🇺🇿
