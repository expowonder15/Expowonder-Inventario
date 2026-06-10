import os
import sqlite3
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)
DB_PATH = "inventario.db"

CATALOGO = [{"codigo": "", "nombre": "Rose Alive", "categoria": "Rosa"}, {"codigo": "", "nombre": "Rose Blue Berry", "categoria": "Rosa"}, {"codigo": "FL-003", "nombre": "Rose Bi Color", "categoria": "Rosa"}, {"codigo": "FL-004", "nombre": "Rose Blush", "categoria": "Rosa"}, {"codigo": "FL-005", "nombre": "Rose Brighton", "categoria": "Rosa"}, {"codigo": "", "nombre": "Rose Blessing", "categoria": "Rosa"}, {"codigo": "", "nombre": "Rose Café Del Mar", "categoria": "Rosa"}, {"codigo": "FL-006", "nombre": "Rose Cherry Brandy", "categoria": "Rosa"}, {"codigo": "FL-007", "nombre": "Rose Cool Water", "categoria": "Rosa"}, {"codigo": "", "nombre": "Rose Deep Silver", "categoria": "Rosa"}, {"codigo": "FL-008", "nombre": "Rose Deep Purple", "categoria": "Rosa"}, {"codigo": "FL-009", "nombre": "Rose Engagement", "categoria": "Rosa"}, {"codigo": "FL-010", "nombre": "Rose Forever Young", "categoria": "Rosa"}, {"codigo": "FL-011", "nombre": "Rose Freedom", "categoria": "Rosa"}, {"codigo": "", "nombre": "Rose Friendship", "categoria": "Rosa"}, {"codigo": "FL-012", "nombre": "Rose Garota", "categoria": "Rosa"}, {"codigo": "", "nombre": "Rose Gold Fish", "categoria": "Rosa"}, {"codigo": "FL-013", "nombre": "Rose Gold Star", "categoria": "Rosa"}, {"codigo": "FL-014", "nombre": "Rose Green", "categoria": "Rosa"}, {"codigo": "", "nombre": "Rose Hearts", "categoria": "Rosa"}, {"codigo": "FL-015", "nombre": "Rose Hermosa", "categoria": "Rosa"}, {"codigo": "FL-016", "nombre": "Rose High And Arena", "categoria": "Rosa"}, {"codigo": "FL-017", "nombre": "Rose High And Bonita", "categoria": "Rosa"}, {"codigo": "FL-018", "nombre": "Rose High And Blooming", "categoria": "Rosa"}, {"codigo": "FL-019", "nombre": "Rose High And Magic", "categoria": "Rosa"}, {"codigo": "", "nombre": "Rose Hilux", "categoria": "Rosa"}, {"codigo": "FL-020", "nombre": "Rose Hot Pink", "categoria": "Rosa"}, {"codigo": "FL-021", "nombre": "Rose Hot Princess", "categoria": "Rosa"}, {"codigo": "FL-022", "nombre": "Rose Ivory", "categoria": "Rosa"}, {"codigo": "FL-023", "nombre": "Rose Lavender", "categoria": "Rosa"}, {"codigo": "", "nombre": "Rose Light Orlando", "categoria": "Rosa"}, {"codigo": "FL-024", "nombre": "Rose Light Pink", "categoria": "Rosa"}, {"codigo": "FL-025", "nombre": "Rose Lola", "categoria": "Rosa"}, {"codigo": "FL-026", "nombre": "Rose Luciano", "categoria": "Rosa"}, {"codigo": "FL-027", "nombre": "Rose Minion Yellow", "categoria": "Rosa"}, {"codigo": "FL-028", "nombre": "Rose Mondial", "categoria": "Rosa"}, {"codigo": "FL-029", "nombre": "Rose Movistar", "categoria": "Rosa"}, {"codigo": "", "nombre": "Rose New Face", "categoria": "Rosa"}, {"codigo": "FL-030", "nombre": "Rose New Flash", "categoria": "Rosa"}, {"codigo": "FL-031", "nombre": "Rose Orange", "categoria": "Rosa"}, {"codigo": "FL-032", "nombre": "Rose Orlando", "categoria": "Rosa"}, {"codigo": "FL-033", "nombre": "Rose Peach", "categoria": "Rosa"}, {"codigo": "FL-034", "nombre": "Rose Pink", "categoria": "Rosa"}, {"codigo": "", "nombre": "Rose Pink Floyd", "categoria": "Rosa"}, {"codigo": "FL-035", "nombre": "Rose Pink Mondial", "categoria": "Rosa"}, {"codigo": "FL-036", "nombre": "Rose Playa Blanca", "categoria": "Rosa"}, {"codigo": "FL-037", "nombre": "Rose Pleasure", "categoria": "Rosa"}, {"codigo": "FL-038", "nombre": "Rose Polar Star", "categoria": "Rosa"}, {"codigo": "", "nombre": "Rose Princess Crown", "categoria": "Rosa"}, {"codigo": "FL-039", "nombre": "Rose Proud", "categoria": "Rosa"}, {"codigo": "FL-040", "nombre": "Rose Purple", "categoria": "Rosa"}, {"codigo": "", "nombre": "Rose Queens Crown", "categoria": "Rosa"}, {"codigo": "FL-041", "nombre": "Rose Ragazza", "categoria": "Rosa"}, {"codigo": "FL-042", "nombre": "Rose Red", "categoria": "Rosa"}, {"codigo": "", "nombre": "Rose Shimmer", "categoria": "Rosa"}, {"codigo": "FL-043", "nombre": "Rose Silantoy", "categoria": "Rosa"}, {"codigo": "FL-044", "nombre": "Rose Skyline", "categoria": "Rosa"}, {"codigo": "FL-045", "nombre": "Rose Soulmate", "categoria": "Rosa"}, {"codigo": "FL-046", "nombre": "Rose Stardust", "categoria": "Rosa"}, {"codigo": "FL-047", "nombre": "Rose Sugar Doll", "categoria": "Rosa"}, {"codigo": "", "nombre": "Rose Sweet Unique", "categoria": "Rosa"}, {"codigo": "FL-048", "nombre": "Rose Sweetness", "categoria": "Rosa"}, {"codigo": "FL-049", "nombre": "Rose Tabata", "categoria": "Rosa"}, {"codigo": "FL-050", "nombre": "Rose Tiffany", "categoria": "Rosa"}, {"codigo": "", "nombre": "Rose V.P Pink", "categoria": "Rosa"}, {"codigo": "FL-051", "nombre": "Rose Vendela", "categoria": "Rosa"}, {"codigo": "FL-052", "nombre": "Rose White", "categoria": "Rosa"}, {"codigo": "FL-053", "nombre": "Rose Yellow", "categoria": "Rosa"}, {"codigo": "SP-001", "nombre": "Rose Spray Red", "categoria": "Rose Spray"}, {"codigo": "SP-002", "nombre": "Rose Spray Hot Pink", "categoria": "Rose Spray"}, {"codigo": "SP-003", "nombre": "Rose Spray Pink", "categoria": "Rose Spray"}, {"codigo": "SP-004", "nombre": "Rose Spray White", "categoria": "Rose Spray"}, {"codigo": "SP-005", "nombre": "Rose Spray Yellow", "categoria": "Rose Spray"}, {"codigo": "AL-001", "nombre": "Alstroemeria Assorted", "categoria": "Alstroemeria"}, {"codigo": "AL-002", "nombre": "Alstroemeria Bi Color", "categoria": "Alstroemeria"}, {"codigo": "AL-003", "nombre": "Alstroemeria Creme", "categoria": "Alstroemeria"}, {"codigo": "AL-004", "nombre": "Alstroemeria Hot Pink", "categoria": "Alstroemeria"}, {"codigo": "AL-005", "nombre": "Alstroemeria Lavender", "categoria": "Alstroemeria"}, {"codigo": "AL-006", "nombre": "Alstroemeria Orange", "categoria": "Alstroemeria"}, {"codigo": "AL-007", "nombre": "Alstroemeria Pink", "categoria": "Alstroemeria"}, {"codigo": "AL-008", "nombre": "Alstroemeria Purple", "categoria": "Alstroemeria"}, {"codigo": "AL-009", "nombre": "Alstroemeria Red", "categoria": "Alstroemeria"}, {"codigo": "AL-010", "nombre": "Alstroemeria White", "categoria": "Alstroemeria"}, {"codigo": "AL-011", "nombre": "Alstroemeria Yellow", "categoria": "Alstroemeria"}, {"codigo": "FC-001", "nombre": "Asiatic Lily Red", "categoria": "Lirio"}, {"codigo": "FC-002", "nombre": "Asiatic Lily Orange", "categoria": "Lirio"}, {"codigo": "FC-003", "nombre": "Asiatic Lily Pink", "categoria": "Lirio"}, {"codigo": "FC-004", "nombre": "Asiatic Lily White", "categoria": "Lirio"}, {"codigo": "FC-005", "nombre": "Asiatic Lily Yellow", "categoria": "Lirio"}, {"codigo": "", "nombre": "Oriental Lily Red", "categoria": "Lirio"}, {"codigo": "", "nombre": "Oriental Lily Orange", "categoria": "Lirio"}, {"codigo": "", "nombre": "Oriental Lily Pink", "categoria": "Lirio"}, {"codigo": "", "nombre": "Oriental Lily White", "categoria": "Lirio"}, {"codigo": "", "nombre": "Oriental Lily Yellow", "categoria": "Lirio"}, {"codigo": "FC-006", "nombre": "Calla Lily Pink", "categoria": "Calla"}, {"codigo": "FC-007", "nombre": "Calla Lily White", "categoria": "Calla"}, {"codigo": "", "nombre": "Button White", "categoria": "pompon"}, {"codigo": "", "nombre": "Button Yellow", "categoria": "pompon"}, {"codigo": "", "nombre": "Button Pink", "categoria": "pompon"}, {"codigo": "", "nombre": "Button Hot Pink", "categoria": "pompon"}, {"codigo": "", "nombre": "Button Lavender", "categoria": "pompon"}, {"codigo": "", "nombre": "Button Orange", "categoria": "pompon"}, {"codigo": "", "nombre": "Button Purple", "categoria": "pompon"}, {"codigo": "", "nombre": "Button Novelty Light Bronze", "categoria": "pompon"}, {"codigo": "", "nombre": "Button Dark Bronze", "categoria": "pompon"}, {"codigo": "", "nombre": "Button Red", "categoria": "pompon"}, {"codigo": "", "nombre": "Button  Green", "categoria": "pompon"}, {"codigo": "", "nombre": "Novelty White", "categoria": "pompon"}, {"codigo": "", "nombre": "Novelty Yellow", "categoria": "pompon"}, {"codigo": "", "nombre": "Novelty Pink", "categoria": "pompon"}, {"codigo": "", "nombre": "Novelty Hot Pink", "categoria": "pompon"}, {"codigo": "", "nombre": "Novelty Lavender", "categoria": "pompon"}, {"codigo": "", "nombre": "Novelty Orange", "categoria": "pompon"}, {"codigo": "", "nombre": "Novelty Purple", "categoria": "pompon"}, {"codigo": "", "nombre": "Novelty Light Bronze", "categoria": "pompon"}, {"codigo": "", "nombre": "Novelty Dark Bronze", "categoria": "pompon"}, {"codigo": "", "nombre": "Novelty Red", "categoria": "pompon"}, {"codigo": "", "nombre": "Novelty Green", "categoria": "pompon"}, {"codigo": "", "nombre": "Cushion White", "categoria": "pompon"}, {"codigo": "", "nombre": "Cushion Yellow", "categoria": "pompon"}, {"codigo": "", "nombre": "Cushion Pink", "categoria": "pompon"}, {"codigo": "", "nombre": "Cushion Hot Pink", "categoria": "pompon"}, {"codigo": "", "nombre": "Cushion Lavender", "categoria": "pompon"}, {"codigo": "", "nombre": "Cushion Orange", "categoria": "pompon"}, {"codigo": "", "nombre": "Cushion Purple", "categoria": "pompon"}, {"codigo": "", "nombre": "Cushion Light Bronze", "categoria": "pompon"}, {"codigo": "", "nombre": "Cushion Dark Bronze", "categoria": "pompon"}, {"codigo": "", "nombre": "Cushion Red", "categoria": "pompon"}, {"codigo": "", "nombre": "Cushion Green", "categoria": "pompon"}, {"codigo": "  DAISY", "nombre": "Daisy White", "categoria": "pompon"}, {"codigo": "", "nombre": "Daisy Yellow", "categoria": "pompon"}, {"codigo": "", "nombre": "Daisy Pink", "categoria": "pompon"}, {"codigo": "", "nombre": "Daisy Hot Pink", "categoria": "pompon"}, {"codigo": "", "nombre": "Daisy Lavender", "categoria": "pompon"}, {"codigo": "", "nombre": "Daisy Orange", "categoria": "pompon"}, {"codigo": "", "nombre": "Daisy Purple", "categoria": "pompon"}, {"codigo": "", "nombre": "Daisy Light Bronze", "categoria": "pompon"}, {"codigo": "", "nombre": "Daisy Dark Bronze", "categoria": "pompon"}, {"codigo": "", "nombre": "Daisy Red", "categoria": "pompon"}, {"codigo": "", "nombre": "Purple Green", "categoria": "pompon"}, {"codigo": "", "nombre": "Purple Micro Poms", "categoria": "pompon"}, {"codigo": "", "nombre": "Pink Micro Poms", "categoria": "pompon"}, {"codigo": "", "nombre": "Viking Yellow", "categoria": "pompon"}, {"codigo": "FC-008", "nombre": "Orinoco Dsy", "categoria": "pompon"}, {"codigo": "FC-009", "nombre": "Gerbera Pink", "categoria": "Gerbera"}, {"codigo": "FC-010", "nombre": "Gerbera Red", "categoria": "Gerbera"}, {"codigo": "FC-011", "nombre": "Gerbera White", "categoria": "Gerbera"}, {"codigo": "", "nombre": "Gerbera Purple", "categoria": "Gerbera"}, {"codigo": "", "nombre": "Gerbera Green", "categoria": "Gerbera"}, {"codigo": "", "nombre": "Gerbera Dark Pink", "categoria": "Gerbera"}, {"codigo": "", "nombre": "Gerbera Orange", "categoria": "Gerbera"}, {"codigo": "", "nombre": "Gerbera Burgundy", "categoria": "Gerbera"}, {"codigo": "", "nombre": "Gerbera Hot Pink", "categoria": "Gerbera"}, {"codigo": "FC-012", "nombre": "Gerbera Yellow", "categoria": "Gerbera"}, {"codigo": "FC-013", "nombre": "Hydrangea Blue", "categoria": "Hydrangea"}, {"codigo": "FC-014", "nombre": "Hydrangea Pink", "categoria": "Hydrangea"}, {"codigo": "", "nombre": "Hydrangea Green", "categoria": "Hydrangea"}, {"codigo": "", "nombre": "Hydrangea White", "categoria": "Hydrangea"}, {"codigo": "FC-015", "nombre": "Mini Hydrangea  Green", "categoria": "Mini-Hydrangea"}, {"codigo": "", "nombre": "Hypericum Pink", "categoria": "Hypericum"}, {"codigo": "", "nombre": "Hypericum Green", "categoria": "Hypericum"}, {"codigo": "FC-016", "nombre": "Hypericum Orange", "categoria": "Hypericum"}, {"codigo": "FC-017", "nombre": "Hypericum Red", "categoria": "Hypericum"}, {"codigo": "", "nombre": "Kangaroo Orange", "categoria": "Kangaroo"}, {"codigo": "", "nombre": "Kangaroo Yellow", "categoria": "Kangaroo"}, {"codigo": "", "nombre": "Kangaroo Green", "categoria": "Kangaroo"}, {"codigo": "FC-018", "nombre": "Kangaroo Red", "categoria": "Kangaroo"}, {"codigo": "FC-019", "nombre": "Limonium Purple", "categoria": "Limonium"}, {"codigo": "FC-020", "nombre": "Limonium White", "categoria": "Limonium"}, {"codigo": "", "nombre": "Limonium Lavender", "categoria": "Limonium"}, {"codigo": "", "nombre": "Limonium Peach", "categoria": "Limonium"}, {"codigo": "", "nombre": "Limonium Pink", "categoria": "Limonium"}, {"codigo": "FC-021", "nombre": "Limonium Yellow", "categoria": "Limonium"}, {"codigo": "FC-022", "nombre": "Matsumoto Red", "categoria": "Matsumoto"}, {"codigo": "", "nombre": "Matsumoto Blue", "categoria": "Matsumoto"}, {"codigo": "", "nombre": "Matsumoto Pink", "categoria": "Matsumoto"}, {"codigo": "", "nombre": "Matsumoto Purple", "categoria": "Matsumoto"}, {"codigo": "", "nombre": "Matsumoto Hot Pink", "categoria": "Matsumoto"}, {"codigo": "FC-023", "nombre": "Matsumoto White", "categoria": "Matsumoto"}, {"codigo": "FC-024", "nombre": "Ranunculus Pink", "categoria": "Ranunculus"}, {"codigo": "FC-025", "nombre": "Ranunculus White", "categoria": "Ranunculus"}, {"codigo": "FC-026", "nombre": "Ranunculus Yellow", "categoria": "Ranunculus"}, {"codigo": "FC-027", "nombre": "Snapdragon Orange", "categoria": "Snapdragon"}, {"codigo": "FC-028", "nombre": "Snapdragon Pink", "categoria": "Snapdragon"}, {"codigo": "", "nombre": "Snapdragon Yellow", "categoria": "Snapdragon"}, {"codigo": "", "nombre": "Snapdragon Purple", "categoria": "Snapdragon"}, {"codigo": "FC-029", "nombre": "Snapdragon White", "categoria": "Snapdragon"}, {"codigo": "", "nombre": "Spider Mums White", "categoria": "Spider Mums"}, {"codigo": "", "nombre": "Spider Mums Yellow", "categoria": "Spider Mums"}, {"codigo": "", "nombre": "Spider Mums Light Bronze", "categoria": "Spider Mums"}, {"codigo": "", "nombre": "Spider Mums Dark Bronze", "categoria": "Spider Mums"}, {"codigo": "", "nombre": "Spider Mums Green", "categoria": "Spider Mums"}, {"codigo": "", "nombre": "Spider Mums Lavanda", "categoria": "Spider Mums"}, {"codigo": "FC-030", "nombre": "Spider Mums Purple", "categoria": "Spider Mums"}, {"codigo": "", "nombre": "Statice Pink", "categoria": "Statice"}, {"codigo": "FC-031", "nombre": "Statice Purple", "categoria": "Statice"}, {"codigo": "FC-032", "nombre": "Statice White", "categoria": "Statice"}, {"codigo": "VD-001", "nombre": "Ave De Paraiso", "categoria": "Verde"}, {"codigo": "VD-002", "nombre": "Baby Blue", "categoria": "Verde"}, {"codigo": "VD-003", "nombre": "Bear Grass", "categoria": "Verde"}, {"codigo": "VD-004", "nombre": "Bells Of Ireland", "categoria": "Verde"}, {"codigo": "VD-005", "nombre": "Brillantina", "categoria": "Verde"}, {"codigo": "VD-006", "nombre": "Cocculus", "categoria": "Verde"}, {"codigo": "VD-007", "nombre": "Craspedia Yellow", "categoria": "Verde"}, {"codigo": "VD-008", "nombre": "Eryngium", "categoria": "Verde"}, {"codigo": "VD-009", "nombre": "Euc Cinerea", "categoria": "Eucalyptus"}, {"codigo": "VD-010", "nombre": "Euc Gunni", "categoria": "Eucalyptus"}, {"codigo": "VD-011", "nombre": "Euc Parvifolia", "categoria": "Eucalyptus"}, {"codigo": "VD-012", "nombre": "Euc Silver Dollar", "categoria": "Eucalyptus"}, {"codigo": "VD-013", "nombre": "Eucalyptus", "categoria": "Eucalyptus"}, {"codigo": "VD-014", "nombre": "Green Pino", "categoria": "Verde"}, {"codigo": "VD-015", "nombre": "Gypso", "categoria": "Gypso"}, {"codigo": "VD-016", "nombre": "Kale", "categoria": "Verde"}, {"codigo": "VD-017", "nombre": "Leather Leaf", "categoria": "Verde"}, {"codigo": "VD-018", "nombre": "Leucadendron Red", "categoria": "Verde"}, {"codigo": "VD-019", "nombre": "Ligustrum", "categoria": "Verde"}, {"codigo": "VD-020", "nombre": "Lily Grass", "categoria": "Verde"}, {"codigo": "VD-021", "nombre": "Pilea", "categoria": "Verde"}, {"codigo": "VD-022", "nombre": "Pittosporum", "categoria": "Verde"}, {"codigo": "VD-023", "nombre": "Ruscus", "categoria": "Verde"}, {"codigo": "VD-024", "nombre": "Solidago", "categoria": "Verde"}, {"codigo": "VD-025", "nombre": "Star Of Bethlehem", "categoria": "Verde"}, {"codigo": "VD-026", "nombre": "Sunflower", "categoria": "Verde"}, {"codigo": "VD-027", "nombre": "Traqueleo", "categoria": "Verde"}, {"codigo": "VD-028", "nombre": "Trefern", "categoria": "Verde"}, {"codigo": "VD-029", "nombre": "Variegated Pittosporum", "categoria": "Verde"}, {"codigo": "VD-030", "nombre": "Viburnum", "categoria": "Verde"}, {"codigo": "", "nombre": "Single Red Roses", "categoria": "Verde"}, {"codigo": "", "nombre": "Single Red Roses Fillers", "categoria": "Verde"}, {"codigo": "", "nombre": "Single Asst Roses", "categoria": "Verde"}, {"codigo": "", "nombre": "Single Asst Roses Fillers", "categoria": "Verde"}, {"codigo": "", "nombre": "Carnations White", "categoria": "Carnations"}, {"codigo": "", "nombre": "Carnations Yellow", "categoria": "Carnations"}, {"codigo": "", "nombre": "Carnations Pink", "categoria": "Carnations"}, {"codigo": "", "nombre": "Carnations Hot Pink", "categoria": "Carnations"}, {"codigo": "", "nombre": "Carnations Lavender", "categoria": "Carnations"}, {"codigo": "", "nombre": "Carnations Orange", "categoria": "Carnations"}, {"codigo": "", "nombre": "Carnations Purple", "categoria": "Carnations"}, {"codigo": "", "nombre": "Carnations Light Bronze", "categoria": "Carnations"}, {"codigo": "", "nombre": "Carnations Dark Bronze", "categoria": "Carnations"}, {"codigo": "", "nombre": "Carnations Red", "categoria": "Carnations"}, {"codigo": "", "nombre": "Carnations Green", "categoria": "Carnations"}, {"codigo": "", "nombre": "Carnations Peach", "categoria": "Carnations"}, {"codigo": "", "nombre": "Mini Carnations White", "categoria": "Mini Carnations"}, {"codigo": "", "nombre": "Mini Carnations Yellow", "categoria": "Mini Carnations"}, {"codigo": "", "nombre": "Mini Carnations Pink", "categoria": "Mini Carnations"}, {"codigo": "", "nombre": "Mini Carnations Hot Pink", "categoria": "Mini Carnations"}, {"codigo": "", "nombre": "Mini Carnations Lavender", "categoria": "Mini Carnations"}, {"codigo": "", "nombre": "Mini Carnations Orange", "categoria": "Mini Carnations"}, {"codigo": "", "nombre": "Mini Carnations Purple", "categoria": "Mini Carnations"}, {"codigo": "", "nombre": "Mini Carnations Light Bronze", "categoria": "Mini Carnations"}, {"codigo": "", "nombre": "Mini Carnations Dark Bronze", "categoria": "Mini Carnations"}, {"codigo": "", "nombre": "Mini Carnations Red", "categoria": "Mini Carnations"}, {"codigo": "", "nombre": "Mini Carnations Green", "categoria": "Mini Carnations"}, {"codigo": "", "nombre": "Mini Carnations Peach", "categoria": "Mini Carnations"}, {"codigo": "", "nombre": "Dianthus White", "categoria": "Dianthus"}, {"codigo": "", "nombre": "Dianthus Yellow", "categoria": "Dianthus"}, {"codigo": "", "nombre": "Dianthus Pink", "categoria": "Dianthus"}, {"codigo": "", "nombre": "Dianthus Hot Pink", "categoria": "Dianthus"}, {"codigo": "", "nombre": "Dianthus Lavender", "categoria": "Dianthus"}, {"codigo": "", "nombre": "Dianthus Orange", "categoria": "Dianthus"}, {"codigo": "", "nombre": "Dianthus Purple", "categoria": "Dianthus"}, {"codigo": "", "nombre": "Dianthus Light Bronze", "categoria": "Dianthus"}, {"codigo": "", "nombre": "Dianthus Dark Bronze", "categoria": "Dianthus"}, {"codigo": "", "nombre": "Dianthus Red", "categoria": "Dianthus"}, {"codigo": "", "nombre": "Dianthus Green", "categoria": "Dianthus"}, {"codigo": "", "nombre": "Dianthus Peach", "categoria": "Dianthus"}, {"codigo": "", "nombre": "Green Ball", "categoria": "Verde"}, {"codigo": "", "nombre": "Mini Calla White", "categoria": "Mini Calla"}, {"codigo": "", "nombre": "Mini Calla Pink", "categoria": "Mini Calla"}, {"codigo": "", "nombre": "Mini Calla Lavender", "categoria": "Mini Calla"}, {"codigo": "", "nombre": "Mini Calla Orange", "categoria": "Mini Calla"}, {"codigo": "", "nombre": "Mini Calla Hot Pink", "categoria": "Mini Calla"}, {"codigo": "", "nombre": "Mini Calla Peach", "categoria": "Mini Calla"}, {"codigo": "", "nombre": "Mini calla Yellow", "categoria": "Mini Calla"}, {"codigo": "", "nombre": "Mini Calla Purple", "categoria": "Mini Calla"}, {"codigo": "", "nombre": "Mini Calla Red", "categoria": "Mini Calla"}, {"codigo": "", "nombre": "Mini Calla Green", "categoria": "Mini Calla"}, {"codigo": "", "nombre": "Stock White", "categoria": "Stock"}, {"codigo": "", "nombre": "Stock Yellow", "categoria": "Stock"}, {"codigo": "", "nombre": "Stock Pink", "categoria": "Stock"}, {"codigo": "", "nombre": "Stock Hot Pink", "categoria": "Stock"}, {"codigo": "", "nombre": "Stock Lavender", "categoria": "Stock"}, {"codigo": "", "nombre": "Stock Orange", "categoria": "Stock"}, {"codigo": "", "nombre": "Stock Purple", "categoria": "Stock"}, {"codigo": "", "nombre": "Stock Light Bronze", "categoria": "Stock"}, {"codigo": "", "nombre": "Stock Dark Bronze", "categoria": "Stock"}, {"codigo": "", "nombre": "Stock Red", "categoria": "Stock"}, {"codigo": "", "nombre": "Stock Green", "categoria": "Stock"}, {"codigo": "", "nombre": "Stock Peach", "categoria": "Stock"}, {"codigo": "", "nombre": "Aster White", "categoria": "Aster"}, {"codigo": "", "nombre": "Aster Purple", "categoria": "Aster"}, {"codigo": "", "nombre": "Aster Pink", "categoria": "Aster"}, {"codigo": "", "nombre": "Palma Robelina", "categoria": "verde"}, {"codigo": "", "nombre": "Liatris Purple", "categoria": "Liatris"}, {"codigo": "", "nombre": "Liatris White", "categoria": "Liatris"}]

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS flores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE NOT NULL,
            categoria TEXT,
            stock_ramos INTEGER DEFAULT 0,
            stock_tallos INTEGER DEFAULT 0,
            alerta_minimo INTEGER DEFAULT 50,
            activo INTEGER DEFAULT 1
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS movimientos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            flor_nombre TEXT NOT NULL,
            tipo TEXT NOT NULL,
            cantidad_ramos INTEGER DEFAULT 0,
            cantidad_tallos INTEGER DEFAULT 0,
            origen TEXT,
            proveedor TEXT,
            fecha_remision TEXT,
            usuario TEXT DEFAULT "sistema",
            notas TEXT
        )
    """)
    for p in CATALOGO:
        c.execute("INSERT OR IGNORE INTO flores (nombre, categoria) VALUES (?, ?)",
                  (p["nombre"], p["categoria"]))
    conn.commit()
    conn.close()

HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
<title>Expowonder Inventario</title>
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; background: #f0f7f4; color: #222; }
.header { background: #1D9E75; color: white; padding: 14px 20px; position: sticky; top: 0; z-index: 100; }
.header h1 { font-size: 18px; font-weight: 600; }
.header p { font-size: 12px; opacity: 0.85; margin-top: 1px; }
.tabs { display: flex; background: white; border-bottom: 1px solid #eee; position: sticky; top: 56px; z-index: 99; }
.tab { flex: 1; padding: 12px 4px; font-size: 12px; font-weight: 500; text-align: center; cursor: pointer; color: #888; border-bottom: 3px solid transparent; }
.tab.active { color: #1D9E75; border-bottom-color: #1D9E75; }
.container { padding: 14px; max-width: 500px; margin: 0 auto; }
.card { background: white; border-radius: 12px; padding: 14px; margin-bottom: 12px; box-shadow: 0 1px 4px rgba(0,0,0,0.07); }
.card h2 { font-size: 14px; font-weight: 600; color: #1D9E75; margin-bottom: 10px; }
label { font-size: 12px; color: #666; display: block; margin-bottom: 3px; margin-top: 10px; }
input, select, textarea { width: 100%; padding: 10px 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 15px; background: #fafafa; }
input:focus, select:focus { outline: none; border-color: #1D9E75; background: white; }
.btn { width: 100%; padding: 13px; background: #1D9E75; color: white; border: none; border-radius: 10px; font-size: 15px; font-weight: 600; margin-top: 12px; cursor: pointer; }
.btn:active { background: #0F6E56; }
.btn-gray { background: #555; }
.btn-red { background: #C0392B; }
.btn-sm { padding: 8px 14px; font-size: 13px; margin-top: 0; width: auto; border-radius: 8px; }
.msg { padding: 12px; border-radius: 8px; font-size: 14px; margin-top: 10px; text-align: center; font-weight: 500; }
.msg.ok { background: #E0F5EC; color: #0F6E56; }
.msg.err { background: #FCEBEB; color: #A32D2D; }
.search-box { position: relative; }
.search-results { display: none; position: absolute; top: 100%; left: 0; right: 0; background: white; border: 1px solid #ddd; border-radius: 8px; max-height: 200px; overflow-y: auto; z-index: 200; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
.search-item { padding: 10px 12px; cursor: pointer; border-bottom: 1px solid #f0f0f0; font-size: 14px; }
.search-item:hover { background: #f0f7f4; }
.search-item small { color: #888; font-size: 11px; display: block; }
.flor-tag { display: flex; align-items: center; justify-content: space-between; background: #E0F5EC; border-radius: 8px; padding: 8px 12px; margin-top: 6px; }
.flor-tag span { font-size: 13px; color: #0F6E56; font-weight: 500; }
.flor-tag button { background: none; border: none; font-size: 18px; color: #888; cursor: pointer; padding: 0 4px; }
.carrito { background: #f9f9f9; border-radius: 10px; padding: 10px; margin-top: 10px; }
.carrito-titulo { font-size: 12px; font-weight: 600; color: #555; margin-bottom: 8px; }
.carrito-item { display: flex; align-items: center; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid #eee; font-size: 13px; }
.carrito-item:last-child { border-bottom: none; }
.carrito-item button { background: none; border: none; color: #C0392B; cursor: pointer; font-size: 16px; }
.row2 { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.badge-ok { color: #0F6E56; font-weight: 600; }
.badge-bajo { color: #A32D2D; font-weight: 600; }
.alerta-box { background: #FFF3E0; border-radius: 12px; padding: 12px; margin-bottom: 12px; }
.alerta-box h3 { font-size: 13px; color: #854F0B; margin-bottom: 6px; }
.alerta-item { font-size: 12px; color: #633806; padding: 4px 0; border-bottom: 1px solid #FFE0A0; }
.alerta-item:last-child { border-bottom: none; }
.tipo-selector { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 8px; }
.tipo-btn { padding: 10px; border: 2px solid #ddd; border-radius: 10px; text-align: center; cursor: pointer; font-size: 13px; font-weight: 500; color: #555; background: white; }
.tipo-btn.active { border-color: #1D9E75; color: #1D9E75; background: #E0F5EC; }
.tipo-btn.active.red { border-color: #C0392B; color: #C0392B; background: #FCEBEB; }
.section { display: none; }
.section.active { display: block; }
table { width: 100%; border-collapse: collapse; font-size: 12px; }
th { background: #E0F5EC; padding: 7px 6px; text-align: left; font-size: 11px; font-weight: 600; }
td { padding: 7px 6px; border-bottom: 1px solid #f0f0f0; }
.nueva-link { font-size: 12px; color: #1D9E75; margin-top: 6px; cursor: pointer; text-decoration: underline; display: inline-block; }
.nueva-form { display: none; margin-top: 8px; padding: 10px; background: #f9f9f9; border-radius: 8px; }
</style>
</head>
<body>
<div class="header">
  <h1>&#127800; Expowonder ERP</h1>
  <p>Control de inventario</p>
</div>
<div class="tabs">
  <div class="tab active" onclick="showTab('entrada', this)">&#128230; Entrada</div>
  <div class="tab" onclick="showTab('baja', this)">&#128683; Baja / Cambio</div>
  <div class="tab" onclick="showTab('stock', this)">&#128200; Stock</div>
</div>

<div class="container">
  <div id="alertas-box"></div>

  <!-- ===== ENTRADA ===== -->
  <div class="section active" id="tab-entrada">
    <div class="card">
      <h2>Registrar entrada de flores</h2>

      <label>Proveedor</label>
      <input type="text" id="e-proveedor" placeholder="Nombre del proveedor">

      <label>Fecha de remisión</label>
      <input type="date" id="e-fecha-remision">

      <label>Tu nombre</label>
      <input type="text" id="e-usuario" placeholder="Ej: Maria">

      <div style="margin-top:14px;border-top:1px solid #eee;padding-top:12px">
        <div class="card" style="background:#f9f9f9;box-shadow:none;padding:12px">
          <h2 style="font-size:13px">Agregar flor al listado</h2>
          <label>Buscar flor</label>
          <div class="search-box">
            <input type="text" id="e-buscar" placeholder="Escribe para buscar..." oninput="filtrar('e-buscar','e-lista')" autocomplete="off" onfocus="filtrar('e-buscar','e-lista')" onblur="setTimeout(()=>document.getElementById('e-lista').style.display='none',200)">
            <div class="search-results" id="e-lista"></div>
          </div>
          <div id="e-flor-tag" style="display:none" class="flor-tag">
            <span id="e-flor-nombre"></span>
            <button onclick="limpiarFlor('e')">✕</button>
          </div>
          <div class="row2">
            <div>
              <label>Ramos completos</label>
              <input type="number" id="e-ramos" min="0" value="0">
            </div>
            <div>
              <label>Tallos sueltos</label>
              <input type="number" id="e-tallos" min="0" value="0">
            </div>
          </div>
          <button class="btn btn-gray btn-sm" style="margin-top:10px;width:100%" onclick="agregarAlCarrito()">+ Agregar al listado</button>
        </div>

        <div class="carrito" id="carrito-box" style="display:none">
          <div class="carrito-titulo">&#128230; Flores a registrar:</div>
          <div id="carrito-items"></div>
        </div>

        <span class="nueva-link" onclick="toggleNueva('nueva-form-e')">+ Flor nueva que no está en la lista</span>
        <div class="nueva-form" id="nueva-form-e">
          <label>Nombre</label>
          <input type="text" id="e-nueva-nombre" placeholder="Ej: Rose Sunset">
          <label>Categoría</label>
          <input type="text" id="e-nueva-cat" placeholder="Ej: Rosa">
          <button class="btn btn-gray" style="padding:8px;font-size:13px;margin-top:8px" onclick="agregarNueva('e')">Guardar flor nueva</button>
        </div>
      </div>

      <button class="btn" onclick="registrarEntrada()">&#10003; Registrar todas las entradas</button>
      <div id="e-msg"></div>
    </div>
  </div>

  <!-- ===== BAJA / CAMBIO ===== -->
  <div class="section" id="tab-baja">
    <div class="card">
      <h2>Baja por daño o Cambio en despacho</h2>

      <label>Tipo de movimiento</label>
      <div class="tipo-selector">
        <div class="tipo-btn active red" id="tipo-dano" onclick="setTipo('dano')">&#128683; Baja por daño</div>
        <div class="tipo-btn" id="tipo-cambio" onclick="setTipo('cambio')">&#8646; Cambio en despacho</div>
      </div>

      <label>Proveedor</label>
      <input type="text" id="b-proveedor" placeholder="Nombre del proveedor">

      <label>Fecha</label>
      <input type="date" id="b-fecha">

      <label>Tu nombre</label>
      <input type="text" id="b-usuario" placeholder="Ej: Maria">

      <!-- BAJA POR DAÑO -->
      <div id="seccion-dano">
        <label>Flor dañada</label>
        <div class="search-box">
          <input type="text" id="b-buscar" placeholder="Buscar flor..." oninput="filtrar('b-buscar','b-lista')" autocomplete="off" onblur="setTimeout(()=>document.getElementById('b-lista').style.display='none',200)">
          <div class="search-results" id="b-lista"></div>
        </div>
        <div id="b-flor-tag" style="display:none" class="flor-tag" style="background:#FCEBEB">
          <span id="b-flor-nombre" style="color:#C0392B"></span>
          <button onclick="limpiarFlor('b')">✕</button>
        </div>
        <div class="row2">
          <div>
            <label>Ramos a dar de baja</label>
            <input type="number" id="b-ramos" min="0" value="0">
          </div>
          <div>
            <label>Tallos sueltos</label>
            <input type="number" id="b-tallos" min="0" value="0">
          </div>
        </div>
        <label>Notas (opcional)</label>
        <input type="text" id="b-notas" placeholder="Ej: llegaron marchitas">
      </div>

      <!-- CAMBIO EN DESPACHO -->
      <div id="seccion-cambio" style="display:none">
        <div style="background:#FFF3E0;border-radius:8px;padding:10px;margin-top:10px;font-size:12px;color:#854F0B">
          &#9888;&#65039; El sistema devolverá la flor original al inventario y descontará la flor enviada.
        </div>

        <label>Flor ORIGINAL (la que pedía la orden — se devuelve)</label>
        <div class="search-box">
          <input type="text" id="c-buscar-orig" placeholder="Buscar flor original..." oninput="filtrar('c-buscar-orig','c-lista-orig')" autocomplete="off" onblur="setTimeout(()=>document.getElementById('c-lista-orig').style.display='none',200)">
          <div class="search-results" id="c-lista-orig"></div>
        </div>
        <div id="c-flor-orig-tag" style="display:none" class="flor-tag">
          <span id="c-flor-orig-nombre"></span>
          <button onclick="limpiarFlorCambio('orig')">✕</button>
        </div>

        <label>Flor ENVIADA (la que se mandó realmente — se descuenta)</label>
        <div class="search-box">
          <input type="text" id="c-buscar-env" placeholder="Buscar flor enviada..." oninput="filtrar('c-buscar-env','c-lista-env')" autocomplete="off" onblur="setTimeout(()=>document.getElementById('c-lista-env').style.display='none',200)">
          <div class="search-results" id="c-lista-env"></div>
        </div>
        <div id="c-flor-env-tag" style="display:none" class="flor-tag" style="background:#FCEBEB">
          <span id="c-flor-env-nombre" style="color:#C0392B"></span>
          <button onclick="limpiarFlorCambio('env')">✕</button>
        </div>

        <div class="row2" style="margin-top:10px">
          <div>
            <label>Ramos</label>
            <input type="number" id="c-ramos" min="0" value="0">
          </div>
          <div>
            <label>Tallos sueltos</label>
            <input type="number" id="c-tallos" min="0" value="0">
          </div>
        </div>
        <label>Notas (opcional)</label>
        <input type="text" id="c-notas" placeholder="Ej: cliente aceptó el cambio">
      </div>

      <button class="btn btn-red" onclick="registrarBaja()">Registrar</button>
      <div id="b-msg"></div>
    </div>
  </div>

  <!-- ===== HISTORIAL ===== -->
  <div class="section" id="tab-historial">
    <div class="card">
      <h2>Historial de movimientos</h2>
      <p style="font-size:12px;color:#888;margin-bottom:10px">Toca un registro para eliminarlo si hubo un error.</p>
      <div id="historial-list">Cargando...</div>
    </div>
  </div>

  <!-- ===== STOCK ===== -->
  <div class="section" id="tab-stock">
    <div class="card">
      <h2>Stock actual</h2>
      <input type="text" id="s-buscar" placeholder="Filtrar por nombre..." oninput="filtrarStock()" style="margin-bottom:10px">
      <div id="stock-list">Cargando...</div>
    </div>
  </div>
</div>

<script>
let CATALOGO = [];
let carrito = [];
let tipoActual = "dano";
let florSeleccionada = { e: "", b: "" };
let florCambio = { orig: "", env: "" };
let stockData = [];

async function init() {
  const res = await fetch("/catalogo");
  CATALOGO = await res.json();
  // Setear fecha de hoy por defecto
  const hoy = new Date().toISOString().split("T")[0];
  document.getElementById("e-fecha-remision").value = hoy;
  document.getElementById("b-fecha").value = hoy;
  cargarStock();
  cargarAlertas();
}

function showTab(tab, el) {
  document.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
  document.querySelectorAll(".section").forEach(s => s.classList.remove("active"));
  document.getElementById("tab-" + tab).classList.add("active");
  el.classList.add("active");
  if (tab === "stock") cargarStock();
  if (tab === "historial") cargarHistorial();
}

function filtrar(inputId, listaId) {
  const q = document.getElementById(inputId).value.trim().toLowerCase();
  const lista = document.getElementById(listaId);
  if (q.length < 1) { lista.style.display = "none"; return; }
  const matches = CATALOGO.filter(p =>
    p.nombre.toLowerCase().includes(q) || p.categoria.toLowerCase().includes(q)
  ).slice(0, 12);
  if (!matches.length) { lista.style.display = "none"; return; }
  lista.innerHTML = "";
  matches.forEach(p => {
    const div = document.createElement("div");
    div.className = "search-item";
    div.innerHTML = `${p.nombre}<small>${p.categoria}</small>`;
    div.onmousedown = () => elegirFlor(inputId, listaId, p.nombre);
    lista.appendChild(div);
  });
  lista.style.display = "block";
}

function elegirFlor(inputId, listaId, nombre) {
  document.getElementById(inputId).value = "";
  document.getElementById(listaId).style.display = "none";
  if (inputId === "e-buscar") {
    florSeleccionada.e = nombre;
    document.getElementById("e-flor-nombre").textContent = "✓ " + nombre;
    document.getElementById("e-flor-tag").style.display = "flex";
  } else if (inputId === "b-buscar") {
    florSeleccionada.b = nombre;
    document.getElementById("b-flor-nombre").textContent = "✓ " + nombre;
    document.getElementById("b-flor-tag").style.display = "flex";
  } else if (inputId === "c-buscar-orig") {
    florCambio.orig = nombre;
    document.getElementById("c-flor-orig-nombre").textContent = "↩ " + nombre;
    document.getElementById("c-flor-orig-tag").style.display = "flex";
  } else if (inputId === "c-buscar-env") {
    florCambio.env = nombre;
    document.getElementById("c-flor-env-nombre").textContent = "↗ " + nombre;
    document.getElementById("c-flor-env-tag").style.display = "flex";
  }
}

function limpiarFlor(prefix) {
  florSeleccionada[prefix] = "";
  document.getElementById(prefix + "-flor-tag").style.display = "none";
  document.getElementById(prefix + "-buscar").value = "";
}

function limpiarFlorCambio(tipo) {
  florCambio[tipo] = "";
  document.getElementById("c-flor-" + tipo + "-tag").style.display = "none";
  document.getElementById("c-buscar-" + tipo).value = "";
}

function setTipo(tipo) {
  tipoActual = tipo;
  document.getElementById("tipo-dano").classList.toggle("active", tipo === "dano");
  document.getElementById("tipo-dano").classList.toggle("red", tipo === "dano");
  document.getElementById("tipo-cambio").classList.toggle("active", tipo === "cambio");
  document.getElementById("seccion-dano").style.display = tipo === "dano" ? "block" : "none";
  document.getElementById("seccion-cambio").style.display = tipo === "cambio" ? "block" : "none";
}

// ===== CARRITO =====
function agregarAlCarrito() {
  const flor = florSeleccionada.e;
  const ramos = parseInt(document.getElementById("e-ramos").value) || 0;
  const tallos = parseInt(document.getElementById("e-tallos").value) || 0;
  if (!flor) { showMsg("e-msg", "Selecciona una flor", "err"); return; }
  if (ramos <= 0 && tallos <= 0) { showMsg("e-msg", "Ingresa ramos o tallos", "err"); return; }
  carrito.push({ flor, ramos, tallos });
  renderCarrito();
  limpiarFlor("e");
  document.getElementById("e-ramos").value = "0";
  document.getElementById("e-tallos").value = "0";
}

function renderCarrito() {
  const box = document.getElementById("carrito-box");
  const items = document.getElementById("carrito-items");
  if (!carrito.length) { box.style.display = "none"; return; }
  box.style.display = "block";
  items.innerHTML = carrito.map((item, i) =>
    `<div class="carrito-item">
      <span>${item.flor}<br><small style="color:#888">${item.ramos} ramos · ${item.tallos} tallos</small></span>
      <button onclick="quitarDelCarrito(${i})">✕</button>
    </div>`
  ).join("");
}

function quitarDelCarrito(i) {
  carrito.splice(i, 1);
  renderCarrito();
}

async function registrarEntrada() {
  if (!carrito.length) { showMsg("e-msg", "Agrega al menos una flor al listado", "err"); return; }
  const proveedor = document.getElementById("e-proveedor").value.trim();
  const fecha_remision = document.getElementById("e-fecha-remision").value;
  const usuario = document.getElementById("e-usuario").value.trim() || "finca";
  if (!proveedor) { showMsg("e-msg", "Escribe el nombre del proveedor", "err"); return; }

  const res = await fetch("/entrada", {
    method: "POST", headers: {"Content-Type":"application/json"},
    body: JSON.stringify({ items: carrito, proveedor, fecha_remision, usuario })
  });
  const data = await res.json();
  if (data.ok) {
    showMsg("e-msg", "✓ " + carrito.length + " flores registradas correctamente", "ok");
    carrito = [];
    renderCarrito();
    document.getElementById("e-proveedor").value = "";
    cargarAlertas();
  } else {
    showMsg("e-msg", "Error: " + data.error, "err");
  }
}

async function registrarBaja() {
  const proveedor = document.getElementById("b-proveedor").value.trim();
  const fecha = document.getElementById("b-fecha").value;
  const usuario = document.getElementById("b-usuario").value.trim() || "finca";

  if (tipoActual === "dano") {
    const flor = florSeleccionada.b;
    const ramos = parseInt(document.getElementById("b-ramos").value) || 0;
    const tallos = parseInt(document.getElementById("b-tallos").value) || 0;
    const notas = document.getElementById("b-notas").value.trim();
    if (!flor) { showMsg("b-msg", "Selecciona la flor dañada", "err"); return; }
    if (ramos <= 0 && tallos <= 0) { showMsg("b-msg", "Ingresa cantidad", "err"); return; }
    const res = await fetch("/baja", {
      method: "POST", headers: {"Content-Type":"application/json"},
      body: JSON.stringify({ tipo: "BAJA_DAÑO", flor, ramos, tallos, proveedor, fecha, usuario, notas })
    });
    const data = await res.json();
    if (data.ok) {
      showMsg("b-msg", "✓ Baja registrada: " + flor, "ok");
      limpiarFlor("b");
      document.getElementById("b-ramos").value = "0";
      document.getElementById("b-tallos").value = "0";
      document.getElementById("b-notas").value = "";
      cargarAlertas();
    } else {
      showMsg("b-msg", "Error: " + data.error, "err");
    }
  } else {
    const florOrig = florCambio.orig;
    const florEnv = florCambio.env;
    const ramos = parseInt(document.getElementById("c-ramos").value) || 0;
    const tallos = parseInt(document.getElementById("c-tallos").value) || 0;
    const notas = document.getElementById("c-notas").value.trim();
    if (!florOrig || !florEnv) { showMsg("b-msg", "Selecciona ambas flores", "err"); return; }
    if (ramos <= 0 && tallos <= 0) { showMsg("b-msg", "Ingresa cantidad", "err"); return; }
    const res = await fetch("/cambio", {
      method: "POST", headers: {"Content-Type":"application/json"},
      body: JSON.stringify({ flor_original: florOrig, flor_enviada: florEnv, ramos, tallos, proveedor, fecha, usuario, notas })
    });
    const data = await res.json();
    if (data.ok) {
      showMsg("b-msg", "✓ Cambio registrado correctamente", "ok");
      limpiarFlorCambio("orig");
      limpiarFlorCambio("env");
      document.getElementById("c-ramos").value = "0";
      document.getElementById("c-tallos").value = "0";
      document.getElementById("c-notas").value = "";
      cargarAlertas();
    } else {
      showMsg("b-msg", "Error: " + data.error, "err");
    }
  }
}

function showMsg(id, txt, tipo) {
  const m = document.getElementById(id);
  m.className = "msg " + tipo;
  m.textContent = txt;
  setTimeout(() => { m.textContent = ""; m.className = ""; }, 5000);
}

async function cargarStock() {
  const res = await fetch("/stock");
  stockData = await res.json();
  renderStock(stockData);
}

function filtrarStock() {
  const q = document.getElementById("s-buscar").value.toLowerCase();
  renderStock(stockData.filter(f => f.nombre.toLowerCase().includes(q) || f.categoria.toLowerCase().includes(q)));
}

function renderStock(data) {
  const div = document.getElementById("stock-list");
  if (!data.length) { div.textContent = "Sin datos"; return; }
  let html = '<table><tr><th>Flor</th><th>Ramos</th><th>Tallos</th><th>Estado</th></tr>';
  data.forEach(f => {
    const bajo = f.stock_ramos < f.alerta_minimo;
    html += `<tr>
      <td class="${bajo ? 'badge-bajo' : ''}">${f.nombre}</td>
      <td style="text-align:center" class="${bajo ? 'badge-bajo' : 'badge-ok'}">${f.stock_ramos}</td>
      <td style="text-align:center">${f.stock_tallos}</td>
      <td style="text-align:center">${bajo ? "⚠️" : "✓"}</td>
    </tr>`;
  });
  html += "</table>";
  div.innerHTML = html;
}

async function cargarAlertas() {
  const res = await fetch("/stock");
  const data = await res.json();
  const alertas = data.filter(f => f.stock_ramos < f.alerta_minimo && (f.stock_ramos > 0 || f.stock_tallos > 0));
  const box = document.getElementById("alertas-box");
  if (alertas.length) {
    let html = `<div class="alerta-box"><h3>&#9888;&#65039; ${alertas.length} flores bajo mínimo (50 ramos)</h3>`;
    alertas.forEach(a => {
      html += `<div class="alerta-item">${a.nombre} — ${a.stock_ramos} ramos</div>`;
    });
    html += "</div>";
    box.innerHTML = html;
  } else {
    box.innerHTML = "";
  }
}

function toggleNueva(id) {
  const f = document.getElementById(id);
  f.style.display = f.style.display === "none" ? "block" : "none";
}

async function agregarNueva(prefix) {
  const nombre = document.getElementById(prefix + "-nueva-nombre").value.trim();
  const cat = document.getElementById(prefix + "-nueva-cat").value.trim() || "Sin categoría";
  if (!nombre) return;
  const res = await fetch("/agregar_flor", {
    method: "POST", headers: {"Content-Type":"application/json"},
    body: JSON.stringify({nombre, categoria: cat})
  });
  const data = await res.json();
  if (data.ok) {
    CATALOGO.push({nombre, categoria: cat});
    document.getElementById(prefix + "-nueva-nombre").value = "";
    document.getElementById(prefix + "-nueva-cat").value = "";
    showMsg("e-msg", "Flor agregada: " + nombre, "ok");
  }
}

async function cargarHistorial() {
  const res = await fetch("/historial");
  const data = await res.json();
  const div = document.getElementById("historial-list");
  if (!data.length) { div.innerHTML = '<p style="color:#888;font-size:13px">Sin movimientos registrados.</p>'; return; }
  let html = '';
  data.forEach(m => {
    const color = m.tipo === "ENTRADA" ? "#E0F5EC" : "#FCEBEB";
    const icono = m.tipo === "ENTRADA" ? "&#128230;" : "&#128683;";
    html += `<div style="background:${color};border-radius:8px;padding:10px;margin-bottom:8px">
      <div style="display:flex;justify-content:space-between;align-items:flex-start">
        <div>
          <div style="font-size:13px;font-weight:600">${icono} ${m.flor_nombre}</div>
          <div style="font-size:11px;color:#666;margin-top:2px">${m.tipo} · ${m.ramos} ramos · ${m.tallos} tallos</div>
          <div style="font-size:11px;color:#888">${m.fecha} · ${m.usuario}${m.proveedor ? " · " + m.proveedor : ""}</div>
        </div>
        <button onclick="eliminarMovimiento(${m.id}, '${m.flor_nombre}')"
          style="background:#C0392B;color:white;border:none;border-radius:6px;padding:6px 10px;font-size:12px;cursor:pointer">
          Eliminar
        </button>
      </div>
    </div>`;
  });
  div.innerHTML = html;
}

async function eliminarMovimiento(id, nombre) {
  if (!confirm("¿Eliminar este registro de " + nombre + "?")) return;
  const res = await fetch("/eliminar_movimiento", {
    method: "POST", headers: {"Content-Type":"application/json"},
    body: JSON.stringify({id})
  });
  const data = await res.json();
  if (data.ok) {
    cargarHistorial();
    cargarAlertas();
  } else {
    alert("Error: " + data.error);
  }
}

init();
</script>
</body>
</html>
"""

@app.route("/")
def index():
    return HTML

@app.route("/catalogo")
def catalogo():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT nombre, categoria FROM flores WHERE activo=1 ORDER BY categoria, nombre")
    rows = c.fetchall()
    conn.close()
    if rows:
        return jsonify([{"nombre": r[0], "categoria": r[1]} for r in rows])
    return jsonify(CATALOGO)

@app.route("/entrada", methods=["POST"])
def entrada():
    data = request.json
    items = data.get("items", [])
    proveedor = data.get("proveedor", "")
    fecha_remision = data.get("fecha_remision", "")
    usuario = data.get("usuario", "finca")
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        for item in items:
            flor = item.get("flor", "").strip()
            ramos = int(item.get("ramos", 0))
            tallos = int(item.get("tallos", 0))
            if not flor: continue
            c.execute("SELECT id FROM flores WHERE LOWER(nombre)=LOWER(?)", (flor,))
            if not c.fetchone():
                c.execute("INSERT INTO flores (nombre, categoria) VALUES (?, ?)", (flor, "Sin categoría"))
            c.execute("UPDATE flores SET stock_ramos=stock_ramos+?, stock_tallos=stock_tallos+? WHERE LOWER(nombre)=LOWER(?)",
                      (ramos, tallos, flor))
            c.execute("INSERT INTO movimientos (fecha, flor_nombre, tipo, cantidad_ramos, cantidad_tallos, origen, proveedor, fecha_remision, usuario) VALUES (?,?,?,?,?,?,?,?,?)",
                      (datetime.now().strftime("%Y-%m-%d %H:%M"), flor, "ENTRADA", ramos, tallos, "REMISION", proveedor, fecha_remision, usuario))
        conn.commit()
        conn.close()
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})

@app.route("/baja", methods=["POST"])
def baja():
    data = request.json
    flor = data.get("flor", "").strip()
    ramos = int(data.get("ramos", 0))
    tallos = int(data.get("tallos", 0))
    proveedor = data.get("proveedor", "")
    fecha = data.get("fecha", "")
    usuario = data.get("usuario", "finca")
    notas = data.get("notas", "")
    tipo = data.get("tipo", "BAJA_DAÑO")
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("UPDATE flores SET stock_ramos=stock_ramos-?, stock_tallos=stock_tallos-? WHERE LOWER(nombre)=LOWER(?)",
                  (ramos, tallos, flor))
        c.execute("INSERT INTO movimientos (fecha, flor_nombre, tipo, cantidad_ramos, cantidad_tallos, origen, proveedor, fecha_remision, usuario, notas) VALUES (?,?,?,?,?,?,?,?,?,?)",
                  (datetime.now().strftime("%Y-%m-%d %H:%M"), flor, tipo, ramos, tallos, "BAJA", proveedor, fecha, usuario, notas))
        conn.commit()
        conn.close()
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})

@app.route("/cambio", methods=["POST"])
def cambio():
    data = request.json
    flor_orig = data.get("flor_original", "").strip()
    flor_env = data.get("flor_enviada", "").strip()
    ramos = int(data.get("ramos", 0))
    tallos = int(data.get("tallos", 0))
    proveedor = data.get("proveedor", "")
    fecha = data.get("fecha", "")
    usuario = data.get("usuario", "finca")
    notas = data.get("notas", "")
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        # Devolver flor original al inventario
        c.execute("UPDATE flores SET stock_ramos=stock_ramos+?, stock_tallos=stock_tallos+? WHERE LOWER(nombre)=LOWER(?)",
                  (ramos, tallos, flor_orig))
        c.execute("INSERT INTO movimientos (fecha, flor_nombre, tipo, cantidad_ramos, cantidad_tallos, origen, proveedor, fecha_remision, usuario, notas) VALUES (?,?,?,?,?,?,?,?,?,?)",
                  (datetime.now().strftime("%Y-%m-%d %H:%M"), flor_orig, "CAMBIO_DEVOLUCION", ramos, tallos, "CAMBIO", proveedor, fecha, usuario, f"Cambio por: {flor_env}. {notas}"))
        # Descontar flor enviada
        c.execute("UPDATE flores SET stock_ramos=stock_ramos-?, stock_tallos=stock_tallos-? WHERE LOWER(nombre)=LOWER(?)",
                  (ramos, tallos, flor_env))
        c.execute("INSERT INTO movimientos (fecha, flor_nombre, tipo, cantidad_ramos, cantidad_tallos, origen, proveedor, fecha_remision, usuario, notas) VALUES (?,?,?,?,?,?,?,?,?,?)",
                  (datetime.now().strftime("%Y-%m-%d %H:%M"), flor_env, "CAMBIO_SALIDA", ramos, tallos, "CAMBIO", proveedor, fecha, usuario, f"Sustituyó a: {flor_orig}. {notas}"))
        conn.commit()
        conn.close()
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})

@app.route("/historial")
def historial():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""
            SELECT id, fecha, flor_nombre, tipo, cantidad_ramos, cantidad_tallos, usuario, proveedor
            FROM movimientos
            ORDER BY id DESC
            LIMIT 50
        """)
        rows = c.fetchall()
        conn.close()
        return jsonify([{
            "id": r[0], "fecha": r[1], "flor_nombre": r[2], "tipo": r[3],
            "ramos": r[4], "tallos": r[5], "usuario": r[6], "proveedor": r[7] or ""
        } for r in rows])
    except Exception as e:
        return jsonify([])

@app.route("/eliminar_movimiento", methods=["POST"])
def eliminar_movimiento():
    data = request.json
    mov_id = data.get("id")
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        # Obtener el movimiento para revertir el stock
        c.execute("SELECT flor_nombre, tipo, cantidad_ramos, cantidad_tallos FROM movimientos WHERE id=?", (mov_id,))
        mov = c.fetchone()
        if mov:
            flor, tipo, ramos, tallos = mov
            # Revertir el efecto en stock
            if tipo == "ENTRADA":
                c.execute("UPDATE flores SET stock_ramos=stock_ramos-?, stock_tallos=stock_tallos-? WHERE LOWER(nombre)=LOWER(?)",
                          (ramos, tallos, flor))
            elif tipo in ("BAJA_DAÑO", "CAMBIO_SALIDA"):
                c.execute("UPDATE flores SET stock_ramos=stock_ramos+?, stock_tallos=stock_tallos+? WHERE LOWER(nombre)=LOWER(?)",
                          (ramos, tallos, flor))
            elif tipo == "CAMBIO_DEVOLUCION":
                c.execute("UPDATE flores SET stock_ramos=stock_ramos-?, stock_tallos=stock_tallos-? WHERE LOWER(nombre)=LOWER(?)",
                          (ramos, tallos, flor))
            c.execute("DELETE FROM movimientos WHERE id=?", (mov_id,))
        conn.commit()
        conn.close()
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})

@app.route("/stock")
def stock():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT nombre, categoria, stock_ramos, stock_tallos, alerta_minimo FROM flores WHERE activo=1 ORDER BY categoria, nombre")
        rows = c.fetchall()
        conn.close()
        return jsonify([{"nombre": r[0], "categoria": r[1], "stock_ramos": r[2], "stock_tallos": r[3], "alerta_minimo": r[4]} for r in rows])
    except:
        return jsonify([])

@app.route("/agregar_flor", methods=["POST"])
def agregar_flor():
    data = request.json
    nombre = data.get("nombre", "").strip()
    categoria = data.get("categoria", "Sin categoría").strip()
    if not nombre:
        return jsonify({"ok": False})
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO flores (nombre, categoria) VALUES (?, ?)", (nombre, categoria))
        conn.commit()
        conn.close()
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})

# Inicializar siempre al arrancar (funciona con gunicorn)
init_db()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
