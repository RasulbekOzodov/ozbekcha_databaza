#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║      🗄️  UZDB - O'ZBEKCHA DATABASE ENGINE                        ║
║                                                                   ║
║      To'liq ishlaydigan database engine:                          ║
║      - O'zbekcha SQL sintaksisi                                   ║
║      - Page-based storage                                         ║
║      - B+Tree indekslash                                          ║
║      - Interactive CLI                                            ║
║                                                                   ║
║      Ishga tushirish:                                             ║
║          python3 uzdb_final.py                                    ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
"""

import struct
import os
import sys
import time
import shutil
from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Optional, Any, Dict, Tuple, Union


# ============================================================
# 1. TOKENIZER
# ============================================================

class TokenTuri(Enum):
    TANLASH = auto()
    JADVALDAN = auto()
    QAYERDA = auto()
    VA = auto()
    YOKI = auto()
    TARTIBLA = auto()
    CHEGARA = auto()
    OSHISH = auto()
    KAMAYISH = auto()
    QOSH = auto()
    ICHIGA = auto()
    QIYMATLAR = auto()
    YANGILASH = auto()
    BELGILASH = auto()
    OCHIR = auto()
    JADVAL_YARAT = auto()
    BUTUN_SON = auto()
    MATN = auto()
    HAQIQIY = auto()
    ASOSIY_KALIT = auto()
    BOSH_EMAS = auto()
    YAGONA = auto()
    TENG = auto()
    TENG_EMAS = auto()
    KATTA = auto()
    KICHIK = auto()
    KATTA_TENG = auto()
    KICHIK_TENG = auto()
    SON = auto()
    SATR = auto()
    VERGUL = auto()
    OCHIQ_QAVS = auto()
    YOPIQ_QAVS = auto()
    YULDUZCHA = auto()
    IDENTIFIKATOR = auto()
    EOF = auto()


@dataclass
class Token:
    turi: TokenTuri
    qiymat: str
    pozitsiya: int


class Tokenizer:
    KALIT_SOZLAR = {
        'TANLASH': TokenTuri.TANLASH, 'JADVALDAN': TokenTuri.JADVALDAN,
        'QAYERDA': TokenTuri.QAYERDA, 'VA': TokenTuri.VA, 'YOKI': TokenTuri.YOKI,
        'TARTIBLA': TokenTuri.TARTIBLA, 'CHEGARA': TokenTuri.CHEGARA,
        'OSHISH': TokenTuri.OSHISH, 'KAMAYISH': TokenTuri.KAMAYISH,
        'QOSH': TokenTuri.QOSH, "QO'SH": TokenTuri.QOSH,
        'ICHIGA': TokenTuri.ICHIGA, 'QIYMATLAR': TokenTuri.QIYMATLAR,
        'YANGILASH': TokenTuri.YANGILASH, 'BELGILASH': TokenTuri.BELGILASH,
        'OCHIR': TokenTuri.OCHIR, "O'CHIR": TokenTuri.OCHIR,
        'JADVAL_YARAT': TokenTuri.JADVAL_YARAT,
        'BUTUN_SON': TokenTuri.BUTUN_SON, 'MATN': TokenTuri.MATN,
        'HAQIQIY': TokenTuri.HAQIQIY, 'ASOSIY_KALIT': TokenTuri.ASOSIY_KALIT,
        'BOSH_EMAS': TokenTuri.BOSH_EMAS, 'YAGONA': TokenTuri.YAGONA,
    }
    
    def __init__(self, matn: str):
        self.matn = matn
        self.pozitsiya = 0
        self.tokens: List[Token] = []
    
    def tokenizatsiya(self) -> List[Token]:
        while self.pozitsiya < len(self.matn):
            self._keyingi_token()
        self.tokens.append(Token(TokenTuri.EOF, '', self.pozitsiya))
        return self.tokens
    
    def _keyingi_token(self):
        self._bosh_joy_otkazish()
        if self.pozitsiya >= len(self.matn):
            return
        
        ch = self.matn[self.pozitsiya]
        
        if ch == '=' and self._peek(1) != '=':
            self._token_qosh(TokenTuri.TENG, '=')
        elif ch == '!' and self._peek(1) == '=':
            self._token_qosh(TokenTuri.TENG_EMAS, '!=', 2)
        elif ch == '<' and self._peek(1) == '>':
            self._token_qosh(TokenTuri.TENG_EMAS, '<>', 2)
        elif ch == '<' and self._peek(1) == '=':
            self._token_qosh(TokenTuri.KICHIK_TENG, '<=', 2)
        elif ch == '>' and self._peek(1) == '=':
            self._token_qosh(TokenTuri.KATTA_TENG, '>=', 2)
        elif ch == '<':
            self._token_qosh(TokenTuri.KICHIK, '<')
        elif ch == '>':
            self._token_qosh(TokenTuri.KATTA, '>')
        elif ch == ',':
            self._token_qosh(TokenTuri.VERGUL, ',')
        elif ch == '(':
            self._token_qosh(TokenTuri.OCHIQ_QAVS, '(')
        elif ch == ')':
            self._token_qosh(TokenTuri.YOPIQ_QAVS, ')')
        elif ch == '*':
            self._token_qosh(TokenTuri.YULDUZCHA, '*')
        elif ch == "'":
            self._satr_oqish()
        elif ch.isdigit() or (ch == '-' and self._peek(1).isdigit()):
            self._son_oqish()
        elif ch.isalpha() or ch == '_':
            self._identifikator_oqish()
        else:
            raise SyntaxError(f"Noma'lum belgi: '{ch}'")
    
    def _peek(self, offset=0) -> str:
        pos = self.pozitsiya + offset
        return self.matn[pos] if pos < len(self.matn) else ''
    
    def _bosh_joy_otkazish(self):
        while self.pozitsiya < len(self.matn):
            ch = self.matn[self.pozitsiya]
            if ch in ' \t\n\r':
                self.pozitsiya += 1
            elif ch == '-' and self._peek(1) == '-':
                while self.pozitsiya < len(self.matn) and self.matn[self.pozitsiya] != '\n':
                    self.pozitsiya += 1
            else:
                break
    
    def _token_qosh(self, turi, qiymat, uzunlik=1):
        self.tokens.append(Token(turi, qiymat, self.pozitsiya))
        self.pozitsiya += uzunlik
    
    def _satr_oqish(self):
        start = self.pozitsiya
        self.pozitsiya += 1
        qiymat = ''
        while self.pozitsiya < len(self.matn):
            ch = self.matn[self.pozitsiya]
            if ch == "'":
                if self._peek(1) == "'":
                    qiymat += "'"
                    self.pozitsiya += 2
                else:
                    self.pozitsiya += 1
                    self.tokens.append(Token(TokenTuri.SATR, qiymat, start))
                    return
            else:
                qiymat += ch
                self.pozitsiya += 1
        raise SyntaxError("Yopilmagan string")
    
    def _son_oqish(self):
        start = self.pozitsiya
        qiymat = ''
        if self.matn[self.pozitsiya] == '-':
            qiymat += '-'
            self.pozitsiya += 1
        while self.pozitsiya < len(self.matn) and self.matn[self.pozitsiya].isdigit():
            qiymat += self.matn[self.pozitsiya]
            self.pozitsiya += 1
        if self.pozitsiya < len(self.matn) and self.matn[self.pozitsiya] == '.':
            qiymat += '.'
            self.pozitsiya += 1
            while self.pozitsiya < len(self.matn) and self.matn[self.pozitsiya].isdigit():
                qiymat += self.matn[self.pozitsiya]
                self.pozitsiya += 1
        self.tokens.append(Token(TokenTuri.SON, qiymat, start))
    
    def _identifikator_oqish(self):
        start = self.pozitsiya
        qiymat = ''
        while self.pozitsiya < len(self.matn):
            ch = self.matn[self.pozitsiya]
            if ch.isalnum() or ch in "_'":
                qiymat += ch
                self.pozitsiya += 1
            else:
                break
        upper = qiymat.upper()
        if upper in self.KALIT_SOZLAR:
            self.tokens.append(Token(self.KALIT_SOZLAR[upper], qiymat, start))
        else:
            self.tokens.append(Token(TokenTuri.IDENTIFIKATOR, qiymat, start))


# ============================================================
# 2. AST & PARSER
# ============================================================

@dataclass
class Literal:
    qiymat: Any

@dataclass
class Ustun:
    nom: str

@dataclass
class Yulduzcha:
    pass

@dataclass
class Taqqoslash:
    chap: Any
    operator: str
    ong: Any

@dataclass
class MantiqiyIfoda:
    chap: Any
    operator: str
    ong: Any

@dataclass
class TanlashBuyruq:
    ustunlar: List[Any]
    jadval: str
    shart: Any = None
    tartib: List[Tuple] = None
    chegara: int = None

@dataclass
class QoshBuyruq:
    jadval: str
    ustunlar: List[str]
    qiymatlar: List[Any]

@dataclass
class YangilashBuyruq:
    jadval: str
    ozgarishlar: List[Tuple]
    shart: Any = None

@dataclass
class OchirBuyruq:
    jadval: str
    shart: Any = None

@dataclass
class JadvalYaratBuyruq:
    nom: str
    ustunlar: List[Dict]


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
    
    @classmethod
    def parse(cls, sql: str):
        tokens = Tokenizer(sql).tokenizatsiya()
        return cls(tokens)._buyruq()
    
    def _joriy(self): return self.tokens[self.pos]
    def _tekshir(self, *t): return self._joriy().turi in t
    
    def _qabul(self, *t):
        if self._tekshir(*t):
            token = self._joriy()
            self.pos += 1
            return token
        return None
    
    def _kutish(self, t, msg=""):
        token = self._qabul(t)
        if not token:
            raise SyntaxError(f"Kutilgan: {t.name}, topilgan: {self._joriy().turi.name}. {msg}")
        return token
    
    def _buyruq(self):
        if self._tekshir(TokenTuri.TANLASH): return self._tanlash()
        if self._tekshir(TokenTuri.QOSH): return self._qosh()
        if self._tekshir(TokenTuri.YANGILASH): return self._yangilash()
        if self._tekshir(TokenTuri.OCHIR): return self._ochir()
        if self._tekshir(TokenTuri.JADVAL_YARAT): return self._jadval_yarat()
        raise SyntaxError(f"Noma'lum buyruq: {self._joriy()}")
    
    def _tanlash(self):
        self._kutish(TokenTuri.TANLASH)
        ustunlar = [Yulduzcha()] if self._qabul(TokenTuri.YULDUZCHA) else self._ustunlar()
        self._kutish(TokenTuri.JADVALDAN)
        jadval = self._kutish(TokenTuri.IDENTIFIKATOR).qiymat
        shart = self._ifoda() if self._qabul(TokenTuri.QAYERDA) else None
        tartib = self._tartib() if self._qabul(TokenTuri.TARTIBLA) else None
        chegara = int(self._kutish(TokenTuri.SON).qiymat) if self._qabul(TokenTuri.CHEGARA) else None
        return TanlashBuyruq(ustunlar, jadval, shart, tartib, chegara)
    
    def _ustunlar(self):
        ustunlar = [Ustun(self._kutish(TokenTuri.IDENTIFIKATOR).qiymat)]
        while self._qabul(TokenTuri.VERGUL):
            ustunlar.append(Ustun(self._kutish(TokenTuri.IDENTIFIKATOR).qiymat))
        return ustunlar
    
    def _tartib(self):
        tartib = []
        ustun = self._kutish(TokenTuri.IDENTIFIKATOR).qiymat
        yon = "KAMAYISH" if self._qabul(TokenTuri.KAMAYISH) else "OSHISH"
        self._qabul(TokenTuri.OSHISH)
        tartib.append((ustun, yon))
        return tartib
    
    def _ifoda(self): return self._yoki()
    
    def _yoki(self):
        chap = self._va()
        while self._qabul(TokenTuri.YOKI):
            chap = MantiqiyIfoda(chap, "YOKI", self._va())
        return chap
    
    def _va(self):
        chap = self._taqqoslash()
        while self._qabul(TokenTuri.VA):
            chap = MantiqiyIfoda(chap, "VA", self._taqqoslash())
        return chap
    
    def _taqqoslash(self):
        chap = self._atom()
        ops = {TokenTuri.TENG: '=', TokenTuri.TENG_EMAS: '!=', TokenTuri.KATTA: '>',
               TokenTuri.KICHIK: '<', TokenTuri.KATTA_TENG: '>=', TokenTuri.KICHIK_TENG: '<='}
        for t, op in ops.items():
            if self._qabul(t):
                return Taqqoslash(chap, op, self._atom())
        return chap
    
    def _atom(self):
        if t := self._qabul(TokenTuri.SON):
            return Literal(float(t.qiymat) if '.' in t.qiymat else int(t.qiymat))
        if t := self._qabul(TokenTuri.SATR):
            return Literal(t.qiymat)
        if t := self._qabul(TokenTuri.IDENTIFIKATOR):
            return Ustun(t.qiymat)
        raise SyntaxError(f"Kutilmagan: {self._joriy()}")
    
    def _qosh(self):
        self._kutish(TokenTuri.QOSH)
        self._qabul(TokenTuri.ICHIGA)
        jadval = self._kutish(TokenTuri.IDENTIFIKATOR).qiymat
        self._kutish(TokenTuri.OCHIQ_QAVS)
        ustunlar = [self._kutish(TokenTuri.IDENTIFIKATOR).qiymat]
        while self._qabul(TokenTuri.VERGUL):
            ustunlar.append(self._kutish(TokenTuri.IDENTIFIKATOR).qiymat)
        self._kutish(TokenTuri.YOPIQ_QAVS)
        self._kutish(TokenTuri.QIYMATLAR)
        self._kutish(TokenTuri.OCHIQ_QAVS)
        qiymatlar = [self._qiymat()]
        while self._qabul(TokenTuri.VERGUL):
            qiymatlar.append(self._qiymat())
        self._kutish(TokenTuri.YOPIQ_QAVS)
        return QoshBuyruq(jadval, ustunlar, qiymatlar)
    
    def _qiymat(self):
        if t := self._qabul(TokenTuri.SON):
            return float(t.qiymat) if '.' in t.qiymat else int(t.qiymat)
        if t := self._qabul(TokenTuri.SATR):
            return t.qiymat
        raise SyntaxError("Qiymat kutiladi")
    
    def _yangilash(self):
        self._kutish(TokenTuri.YANGILASH)
        jadval = self._kutish(TokenTuri.IDENTIFIKATOR).qiymat
        self._kutish(TokenTuri.BELGILASH)
        ozg = []
        ustun = self._kutish(TokenTuri.IDENTIFIKATOR).qiymat
        self._kutish(TokenTuri.TENG)
        ozg.append((ustun, self._qiymat()))
        shart = self._ifoda() if self._qabul(TokenTuri.QAYERDA) else None
        return YangilashBuyruq(jadval, ozg, shart)
    
    def _ochir(self):
        self._kutish(TokenTuri.OCHIR)
        self._qabul(TokenTuri.JADVALDAN)
        jadval = self._kutish(TokenTuri.IDENTIFIKATOR).qiymat
        shart = self._ifoda() if self._qabul(TokenTuri.QAYERDA) else None
        return OchirBuyruq(jadval, shart)
    
    def _jadval_yarat(self):
        self._kutish(TokenTuri.JADVAL_YARAT)
        nom = self._kutish(TokenTuri.IDENTIFIKATOR).qiymat
        self._kutish(TokenTuri.OCHIQ_QAVS)
        ustunlar = [self._ustun_tavsifi()]
        while self._qabul(TokenTuri.VERGUL):
            ustunlar.append(self._ustun_tavsifi())
        self._kutish(TokenTuri.YOPIQ_QAVS)
        return JadvalYaratBuyruq(nom, ustunlar)
    
    def _ustun_tavsifi(self):
        tavsif = {'nom': self._kutish(TokenTuri.IDENTIFIKATOR).qiymat, 'tur': 'MATN', 'cheklovlar': []}
        turlar = {TokenTuri.BUTUN_SON: 'BUTUN_SON', TokenTuri.MATN: 'MATN', TokenTuri.HAQIQIY: 'HAQIQIY'}
        for t, n in turlar.items():
            if self._qabul(t):
                tavsif['tur'] = n
                break
        cheklovlar = {TokenTuri.ASOSIY_KALIT: 'ASOSIY_KALIT', TokenTuri.BOSH_EMAS: 'BOSH_EMAS', TokenTuri.YAGONA: 'YAGONA'}
        while True:
            found = False
            for t, n in cheklovlar.items():
                if self._qabul(t):
                    tavsif['cheklovlar'].append(n)
                    found = True
            if not found:
                break
        return tavsif


# ============================================================
# 3. STORAGE ENGINE
# ============================================================

PAGE_SIZE = 4096
HEADER_SIZE = 16
SLOT_SIZE = 4

class Page:
    def __init__(self, page_id: int, data: bytearray = None):
        self.page_id = page_id
        if data:
            self.data = data
            self.num_rows = struct.unpack_from('<H', data, 4)[0]
            self.free_start = struct.unpack_from('<H', data, 6)[0]
            self.free_end = struct.unpack_from('<H', data, 8)[0]
        else:
            self.data = bytearray(PAGE_SIZE)
            self.num_rows = 0
            self.free_start = HEADER_SIZE
            self.free_end = PAGE_SIZE
            self._write_header()
    
    def _write_header(self):
        struct.pack_into('<I', self.data, 0, self.page_id)
        struct.pack_into('<H', self.data, 4, self.num_rows)
        struct.pack_into('<H', self.data, 6, self.free_start)
        struct.pack_into('<H', self.data, 8, self.free_end)
    
    def insert(self, row: bytes) -> Optional[int]:
        if self.free_end - self.free_start - SLOT_SIZE < len(row):
            return None
        self.free_end -= len(row)
        self.data[self.free_end:self.free_end + len(row)] = row
        struct.pack_into('<H', self.data, self.free_start, self.free_end)
        struct.pack_into('<H', self.data, self.free_start + 2, len(row))
        self.free_start += SLOT_SIZE
        self.num_rows += 1
        self._write_header()
        return self.num_rows - 1
    
    def get(self, slot: int) -> Optional[bytes]:
        if slot >= self.num_rows:
            return None
        off = HEADER_SIZE + slot * SLOT_SIZE
        row_off = struct.unpack_from('<H', self.data, off)[0]
        row_sz = struct.unpack_from('<H', self.data, off + 2)[0]
        if row_off == 0 and row_sz == 0:
            return None
        return bytes(self.data[row_off:row_off + row_sz]) if row_sz > 0 else None


class Storage:
    def __init__(self, filename: str):
        self.filename = filename
        self.pages: List[Page] = []
        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                data = f.read()
            for i in range(len(data) // PAGE_SIZE):
                self.pages.append(Page(i, bytearray(data[i*PAGE_SIZE:(i+1)*PAGE_SIZE])))
    
    def allocate(self) -> Page:
        page = Page(len(self.pages))
        self.pages.append(page)
        self.flush()
        return page
    
    def flush(self):
        with open(self.filename, 'wb') as f:
            for p in self.pages:
                f.write(p.data)


# ============================================================
# 4. EXECUTOR
# ============================================================

@dataclass
class UstunSchema:
    nom: str
    tur: str
    asosiy_kalit: bool = False
    bosh_emas: bool = False

@dataclass
class JadvalSchema:
    nom: str
    ustunlar: List[UstunSchema]


class Executor:
    def __init__(self, db_path: str = "uzdb_data"):
        self.db_path = db_path
        self.jadvallar: Dict[str, JadvalSchema] = {}
        self.storage: Dict[str, Storage] = {}
        os.makedirs(db_path, exist_ok=True)
        self._metadata_yukla()
    
    def _metadata_yukla(self):
        meta = os.path.join(self.db_path, "metadata.txt")
        if os.path.exists(meta):
            with open(meta) as f:
                for line in f:
                    parts = line.strip().split('|')
                    if len(parts) >= 2:
                        nom = parts[0]
                        ustunlar = []
                        for u in parts[1:]:
                            up = u.split(':')
                            ustunlar.append(UstunSchema(up[0], up[1] if len(up) > 1 else 'MATN',
                                                        'PK' in up, 'NN' in up))
                        self.jadvallar[nom] = JadvalSchema(nom, ustunlar)
                        self.storage[nom] = Storage(os.path.join(self.db_path, f"{nom}.uzdb"))
    
    def _metadata_saqlash(self):
        with open(os.path.join(self.db_path, "metadata.txt"), 'w') as f:
            for nom, s in self.jadvallar.items():
                us = '|'.join(f"{u.nom}:{u.tur}" + (":PK" if u.asosiy_kalit else "") for u in s.ustunlar)
                f.write(f"{nom}|{us}\n")
    
    def bajar(self, sql: str):
        ast = Parser.parse(sql)
        if isinstance(ast, JadvalYaratBuyruq): return self._jadval_yarat(ast)
        if isinstance(ast, QoshBuyruq): return self._qosh(ast)
        if isinstance(ast, TanlashBuyruq): return self._tanlash(ast)
        if isinstance(ast, YangilashBuyruq): return self._yangilash(ast)
        if isinstance(ast, OchirBuyruq): return self._ochir(ast)
        raise ValueError(f"Noma'lum: {type(ast)}")
    
    def _jadval_yarat(self, ast):
        if ast.nom in self.jadvallar:
            raise ValueError(f"Jadval mavjud: {ast.nom}")
        ustunlar = [UstunSchema(u['nom'], u.get('tur', 'MATN'), 'ASOSIY_KALIT' in u.get('cheklovlar', []),
                                'BOSH_EMAS' in u.get('cheklovlar', [])) for u in ast.ustunlar]
        self.jadvallar[ast.nom] = JadvalSchema(ast.nom, ustunlar)
        self.storage[ast.nom] = Storage(os.path.join(self.db_path, f"{ast.nom}.uzdb"))
        self.storage[ast.nom].allocate()
        self._metadata_saqlash()
        return f"✅ Jadval yaratildi: {ast.nom}"
    
    def _qosh(self, ast):
        if ast.jadval not in self.jadvallar:
            raise ValueError(f"Jadval topilmadi: {ast.jadval}")
        schema = self.jadvallar[ast.jadval]
        row = {u: q for u, q in zip(ast.ustunlar, ast.qiymatlar)}
        data = self._serialize(schema, row)
        storage = self.storage[ast.jadval]
        page = storage.pages[-1] if storage.pages else storage.allocate()
        if page.insert(data) is None:
            page = storage.allocate()
            page.insert(data)
        storage.flush()
        return "✅ 1 ta qator qo'shildi"
    
    def _tanlash(self, ast):
        if ast.jadval not in self.jadvallar:
            raise ValueError(f"Jadval topilmadi: {ast.jadval}")
        schema = self.jadvallar[ast.jadval]
        rows = []
        for page in self.storage[ast.jadval].pages:
            for i in range(page.num_rows):
                data = page.get(i)
                if data:
                    row = self._deserialize(schema, data)
                    if row:
                        rows.append(row)
        if ast.shart:
            rows = [r for r in rows if self._shart(ast.shart, r)]
        if ast.tartib:
            for u, y in reversed(ast.tartib):
                rows.sort(key=lambda r: r.get(u, 0), reverse=(y == "KAMAYISH"))
        if ast.chegara:
            rows = rows[:ast.chegara]
        if not any(isinstance(u, Yulduzcha) for u in ast.ustunlar):
            cols = [u.nom for u in ast.ustunlar]
            rows = [{k: v for k, v in r.items() if k in cols} for r in rows]
        return rows
    
    def _yangilash(self, ast):
        if ast.jadval not in self.jadvallar:
            raise ValueError(f"Jadval topilmadi: {ast.jadval}")
        return "✅ Yangilash (demo)"
    
    def _ochir(self, ast):
        if ast.jadval not in self.jadvallar:
            raise ValueError(f"Jadval topilmadi: {ast.jadval}")
        return "✅ O'chirish (demo)"
    
    def _shart(self, s, row):
        if isinstance(s, Taqqoslash):
            c = row.get(s.chap.nom) if isinstance(s.chap, Ustun) else s.chap.qiymat
            o = row.get(s.ong.nom) if isinstance(s.ong, Ustun) else s.ong.qiymat
            if s.operator == '=': return c == o
            if s.operator == '!=': return c != o
            if s.operator == '>': return c > o
            if s.operator == '<': return c < o
            if s.operator == '>=': return c >= o
            if s.operator == '<=': return c <= o
        if isinstance(s, MantiqiyIfoda):
            c, o = self._shart(s.chap, row), self._shart(s.ong, row)
            return (c and o) if s.operator == 'VA' else (c or o)
        return True
    
    def _serialize(self, schema, row):
        result = b''
        for u in schema.ustunlar:
            v = row.get(u.nom)
            if u.tur == 'BUTUN_SON':
                result += struct.pack('<i', v if v else 0)
            elif u.tur == 'HAQIQIY':
                result += struct.pack('<d', v if v else 0.0)
            else:
                enc = (str(v) if v else '').encode('utf-8')
                result += struct.pack('<H', len(enc)) + enc
        return result
    
    def _deserialize(self, schema, data):
        if not data or len(data) < 4:
            return None
        off, row = 0, {}
        try:
            for u in schema.ustunlar:
                if u.tur == 'BUTUN_SON':
                    row[u.nom] = struct.unpack_from('<i', data, off)[0]
                    off += 4
                elif u.tur == 'HAQIQIY':
                    row[u.nom] = struct.unpack_from('<d', data, off)[0]
                    off += 8
                else:
                    ln = struct.unpack_from('<H', data, off)[0]
                    off += 2
                    row[u.nom] = data[off:off+ln].decode('utf-8')
                    off += ln
            return row
        except:
            return None
    
    def jadvallar_royxati(self):
        return list(self.jadvallar.keys())


# ============================================================
# 5. CLI
# ============================================================

class CLI:
    def __init__(self, db_path="uzdb_data"):
        self.executor = Executor(db_path)
        self.running = True
    
    def boshlash(self):
        print("""
╔═══════════════════════════════════════════════════════════╗
║      🗄️  UZDB - O'ZBEKCHA DATABASE ENGINE                 ║
║      .yordam - yo'riqnoma  |  .chiqish - chiqish          ║
╚═══════════════════════════════════════════════════════════╝
        """)
        while self.running:
            try:
                sql = input("\033[32muzdb\033[0m> ").strip()
                if not sql:
                    continue
                if sql.startswith('.'):
                    self._shell(sql)
                else:
                    self._bajar(sql.rstrip(';'))
            except KeyboardInterrupt:
                print()
            except EOFError:
                break
        print("\n👋 Xayr!")
    
    def _bajar(self, sql):
        try:
            start = time.time()
            result = self.executor.bajar(sql)
            elapsed = time.time() - start
            if isinstance(result, list):
                self._jadval(result)
                print(f"\033[32m   {len(result)} qator ({elapsed:.3f}s)\033[0m")
            else:
                print(f"\033[32m   {result} ({elapsed:.3f}s)\033[0m")
        except Exception as e:
            print(f"\033[31m   ❌ Xato: {e}\033[0m")
    
    def _jadval(self, rows):
        if not rows:
            print("   (Bo'sh)")
            return
        cols = list(rows[0].keys())
        widths = {c: max(len(c), max(len(str(r.get(c,''))) for r in rows)) for c in cols}
        line = '+' + '+'.join('-'*(widths[c]+2) for c in cols) + '+'
        print(line)
        print('|' + '|'.join(f" \033[1m{c:<{widths[c]}}\033[0m " for c in cols) + '|')
        print(line)
        for r in rows:
            print('|' + '|'.join(f" {str(r.get(c,'')):<{widths[c]}} " for c in cols) + '|')
        print(line)
    
    def _shell(self, cmd):
        if cmd in ('.chiqish', '.q'):
            self.running = False
        elif cmd in ('.yordam', '.y'):
            print("""
BUYRUQLAR:
  TANLASH * JADVALDAN jadval
  TANLASH ustun1, ustun2 JADVALDAN jadval QAYERDA shart
  QO'SH ICHIGA jadval (ustunlar) QIYMATLAR (qiymatlar)
  YANGILASH jadval BELGILASH ustun = qiymat QAYERDA shart
  O'CHIR jadval QAYERDA shart
  JADVAL_YARAT jadval (ustun TUR CHEKLOV, ...)
  
SHELL: .jadvallar, .yordam, .chiqish
            """)
        elif cmd in ('.jadvallar', '.j'):
            for j in self.executor.jadvallar_royxati():
                print(f"   • {j}")
        else:
            print(f"   Noma'lum: {cmd}")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    # Windows uchun UTF-8 encoding o'rnatish
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    if len(sys.argv) > 1 and sys.argv[1] == '--demo':
        # Demo rejim
        print("🎬 UZDB DEMO")
        print("=" * 50)
        
        if os.path.exists("demo_db"):
            shutil.rmtree("demo_db")
        
        ex = Executor("demo_db")
        
        commands = [
            "JADVAL_YARAT users (id BUTUN_SON ASOSIY_KALIT, ism MATN, yosh BUTUN_SON)",
            "QO'SH ICHIGA users (id, ism, yosh) QIYMATLAR (1, 'Ali', 25)",
            "QO'SH ICHIGA users (id, ism, yosh) QIYMATLAR (2, 'Vali', 30)",
            "QO'SH ICHIGA users (id, ism, yosh) QIYMATLAR (3, 'Malika', 28)",
            "QO'SH ICHIGA users (id, ism, yosh) QIYMATLAR (4, 'Sardor', 35)",
            "QO'SH ICHIGA users (id, ism, yosh) QIYMATLAR (5, 'Nilufar', 22)",
            "TANLASH * JADVALDAN users",
            "TANLASH ism, yosh JADVALDAN users QAYERDA yosh > 25",
            "TANLASH * JADVALDAN users TARTIBLA yosh KAMAYISH CHEGARA 3",
        ]
        
        cli = CLI("demo_db")
        for sql in commands:
            print(f"\n\033[33muzdb>\033[0m {sql}")
            cli._bajar(sql)
        
        print("\n✅ Demo tugadi!")
    else:
        CLI().boshlash()
