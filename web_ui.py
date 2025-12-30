#!/usr/bin/env python3
"""
UZDB Web UI - To'liq ishlash versiyasi
"""

from flask import Flask, request, jsonify
from uzdb_final import Executor
import sys

# Windows uchun UTF-8 encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

app = Flask(__name__)
db = Executor("web_db")

@app.route('/')
def index():
    return '''<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UZDB - O'zbekcha Database</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        .header {
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            text-align: center;
        }
        .header h1 { color: #667eea; font-size: 2.5em; margin-bottom: 10px; }
        .header p { color: #666; font-size: 1.1em; }
        .main-content {
            display: grid;
            grid-template-columns: 1fr 2fr;
            gap: 20px;
            margin-bottom: 20px;
        }
        .sidebar {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .sidebar h2 {
            color: #667eea;
            margin-bottom: 20px;
            font-size: 1.5em;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }
        .example-query {
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 12px;
            margin: 10px 0;
            cursor: pointer;
            border-radius: 5px;
            transition: all 0.3s;
        }
        .example-query:hover {
            background: #e9ecef;
            transform: translateX(5px);
        }
        .example-query code {
            display: block;
            color: #495057;
            font-size: 0.9em;
            margin-top: 5px;
        }
        .query-panel {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .query-panel h2 {
            color: #667eea;
            margin-bottom: 20px;
            font-size: 1.5em;
        }
        #sqlInput {
            width: 100%;
            min-height: 120px;
            padding: 15px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            resize: vertical;
            margin-bottom: 15px;
        }
        #sqlInput:focus { outline: none; border-color: #667eea; }
        .btn-group { display: flex; gap: 10px; margin-bottom: 20px; }
        button {
            padding: 12px 30px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            transition: all 0.3s;
            font-weight: 600;
        }
        .btn-execute {
            background: #667eea;
            color: white;
            flex: 1;
        }
        .btn-execute:hover {
            background: #5568d3;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        .btn-clear { background: #6c757d; color: white; }
        .btn-clear:hover { background: #5a6268; }
        .results {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            min-height: 300px;
        }
        .results h2 {
            color: #667eea;
            margin-bottom: 20px;
            font-size: 1.5em;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }
        th {
            background: #667eea;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
        }
        td {
            padding: 12px;
            border-bottom: 1px solid #ddd;
        }
        tr:hover { background: #f8f9fa; }
        .success {
            background: #d4edda;
            color: #155724;
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
            border-left: 4px solid #28a745;
        }
        .error {
            background: #f8d7da;
            color: #721c24;
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
            border-left: 4px solid #dc3545;
        }
        .info {
            background: #d1ecf1;
            color: #0c5460;
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
            border-left: 4px solid #17a2b8;
        }
        .table-list {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 15px;
        }
        .table-badge {
            background: #667eea;
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.9em;
            cursor: pointer;
            transition: all 0.3s;
        }
        .table-badge:hover {
            background: #5568d3;
            transform: scale(1.05);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🗄️ UZDB - O'zbekcha Database Engine</h1>
            <p>PostgreSQL stilidagi to'liq funksional database</p>
        </div>

        <div class="main-content">
            <div class="sidebar">
                <h2>📚 Misol So'rovlar</h2>

                <div class="example-query" onclick="setQuery('JADVAL_YARAT test (id BUTUN_SON ASOSIY_KALIT, ism MATN, yosh BUTUN_SON)')">
                    <strong>➕ Jadval yaratish</strong>
                    <code>JADVAL_YARAT test (...)</code>
                </div>

                <div class="example-query" onclick="setQuery('QO\\'SH ICHIGA test (id, ism, yosh) QIYMATLAR (1, \\'Ali\\', 25)')">
                    <strong>✏️ Ma'lumot qo'shish</strong>
                    <code>QO'SH ICHIGA test ...</code>
                </div>

                <div class="example-query" onclick="setQuery('TANLASH * JADVALDAN test')">
                    <strong>📋 Barcha ma'lumotlar</strong>
                    <code>TANLASH * JADVALDAN test</code>
                </div>

                <div class="example-query" onclick="setQuery('TANLASH * JADVALDAN test QAYERDA yosh > 25')">
                    <strong>🔍 Shart bilan tanlash</strong>
                    <code>... QAYERDA yosh > 25</code>
                </div>

                <div class="example-query" onclick="setQuery('TANLASH * JADVALDAN test TARTIBLA yosh KAMAYISH')">
                    <strong>📊 Tartiblash</strong>
                    <code>... TARTIBLA yosh KAMAYISH</code>
                </div>

                <h2 style="margin-top: 30px;">📊 Jadvallar</h2>
                <div class="table-list" id="tableList">
                    <div class="info">Hozircha jadvallar yo'q</div>
                </div>
            </div>

            <div class="query-panel">
                <h2>💻 SQL So'rov</h2>
                <textarea id="sqlInput" placeholder="O'zbekcha SQL so'rovingizni kiriting...

Misol:
JADVAL_YARAT foydalanuvchilar (
    id BUTUN_SON ASOSIY_KALIT,
    ism MATN,
    yosh BUTUN_SON
)"></textarea>

                <div class="btn-group">
                    <button class="btn-execute" onclick="runQuery()">▶️ Bajarish</button>
                    <button class="btn-clear" onclick="clearAll()">🗑️ Tozalash</button>
                </div>
            </div>
        </div>

        <div class="results" id="results">
            <h2>📈 Natijalar</h2>
            <div class="info">
                <strong>Xush kelibsiz!</strong> Yuqoridagi maydonga SQL so'rovingizni kiriting va "Bajarish" tugmasini bosing.
            </div>
        </div>
    </div>

    <script>
        function setQuery(query) {
            document.getElementById('sqlInput').value = query;
        }

        function clearAll() {
            document.getElementById('sqlInput').value = '';
            document.getElementById('results').innerHTML = '<h2>📈 Natijalar</h2><div class="info">So\\'rov tozalandi.</div>';
        }

        async function runQuery() {
            const sql = document.getElementById('sqlInput').value.trim();
            if (!sql) {
                alert('Iltimos, SQL so\\'rov kiriting!');
                return;
            }

            const resultsDiv = document.getElementById('results');
            resultsDiv.innerHTML = '<h2>📈 Natijalar</h2><p>Bajarilmoqda...</p>';

            try {
                const response = await fetch('/execute', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ sql: sql })
                });

                const data = await response.json();

                if (data.success) {
                    showResults(data.result, data.type);
                    loadTables();
                } else {
                    resultsDiv.innerHTML = '<h2>📈 Natijalar</h2><div class="error"><strong>❌ Xato:</strong> ' + data.error + '</div>';
                }
            } catch (error) {
                resultsDiv.innerHTML = '<h2>📈 Natijalar</h2><div class="error"><strong>❌ Server xatosi:</strong> ' + error.message + '</div>';
            }
        }

        function showResults(result, type) {
            const resultsDiv = document.getElementById('results');

            if (type === 'table') {
                if (result.length === 0) {
                    resultsDiv.innerHTML = '<h2>📈 Natijalar</h2><div class="info">Bo\\'sh natija</div>';
                    return;
                }

                const columns = Object.keys(result[0]);
                let html = '<h2>📈 Natijalar</h2><div class="success">✅ ' + result.length + ' ta qator topildi</div><table><thead><tr>';

                columns.forEach(col => {
                    html += '<th>' + col + '</th>';
                });
                html += '</tr></thead><tbody>';

                result.forEach(row => {
                    html += '<tr>';
                    columns.forEach(col => {
                        html += '<td>' + (row[col] || '') + '</td>';
                    });
                    html += '</tr>';
                });

                html += '</tbody></table>';
                resultsDiv.innerHTML = html;
            } else {
                resultsDiv.innerHTML = '<h2>📈 Natijalar</h2><div class="success">' + result + '</div>';
            }
        }

        async function loadTables() {
            try {
                const response = await fetch('/tables');
                const data = await response.json();

                const tableList = document.getElementById('tableList');
                if (data.tables.length === 0) {
                    tableList.innerHTML = '<div class="info">Hozircha jadvallar yo\\'q</div>';
                } else {
                    let html = '';
                    data.tables.forEach(table => {
                        html += '<div class="table-badge" onclick="setQuery(\\'TANLASH * JADVALDAN ' + table + '\\')">' + table + '</div>';
                    });
                    tableList.innerHTML = html;
                }
            } catch (error) {
                console.error('Jadvallar yuklanmadi:', error);
            }
        }

        // Sahifa yuklanganda
        window.addEventListener('DOMContentLoaded', function() {
            loadTables();

            // Ctrl+Enter bilan bajarish
            document.getElementById('sqlInput').addEventListener('keydown', function(e) {
                if (e.ctrlKey && e.key === 'Enter') {
                    runQuery();
                }
            });
        });
    </script>
</body>
</html>'''

@app.route('/execute', methods=['POST'])
def execute():
    try:
        data = request.get_json()
        sql = data.get('sql', '').strip()

        if not sql:
            return jsonify({'success': False, 'error': 'SQL so\'rov bo\'sh'})

        result = db.bajar(sql)

        if isinstance(result, list):
            return jsonify({'success': True, 'result': result, 'type': 'table'})
        else:
            return jsonify({'success': True, 'result': str(result), 'type': 'message'})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/tables')
def tables():
    try:
        table_list = db.jadvallar_royxati()
        return jsonify({'tables': table_list})
    except Exception as e:
        return jsonify({'tables': [], 'error': str(e)})

if __name__ == '__main__':
    print("""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║      🌐 UZDB WEB UI - Yangi versiya                           ║
║                                                               ║
║      Brauzeringizda oching:                                   ║
║      👉 http://localhost:5001                                 ║
║                                                               ║
║      To'xtatish: Ctrl+C                                       ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
    """)
    app.run(debug=True, host='0.0.0.0', port=5001)
