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
            usuario TEXT DEFAULT "sistema"
        )
    """)
    # Cargar catalogo inicial
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
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Expowonder - Inventario</title>
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; background: #f0f7f4; }
.header { background: #1D9E75; color: white; padding: 16px 20px; }
.header h1 { font-size: 20px; font-weight: 600; }
.header p { font-size: 13px; opacity: 0.85; margin-top: 2px; }
.container { padding: 16px; max-width: 500px; margin: 0 auto; }
.card { background: white; border-radius: 12px; padding: 16px; margin-bottom: 14px; box-shadow: 0 1px 4px rgba(0,0,0,0.08); }
.card h2 { font-size: 15px; font-weight: 600; margin-bottom: 12px; color: #1D9E75; }
label { font-size: 13px; color: #555; display: block; margin-bottom: 4px; margin-top: 10px; }
input, select { width: 100%; padding: 10px 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 15px; background: #fafafa; }
input:focus, select:focus { outline: none; border-color: #1D9E75; background: white; }
.btn { width: 100%; padding: 14px; background: #1D9E75; color: white; border: none; border-radius: 10px; font-size: 16px; font-weight: 600; margin-top: 14px; cursor: pointer; }
.btn:active { background: #0F6E56; }
.btn-gray { background: #555; }
.msg { padding: 12px; border-radius: 8px; font-size: 14px; margin-top: 10px; text-align: center; }
.msg.ok { background: #E0F5EC; color: #0F6E56; }
.msg.err { background: #FCEBEB; color: #A32D2D; }
.nueva-link { font-size: 12px; color: #1D9E75; margin-top: 6px; cursor: pointer; text-decoration: underline; display: inline-block; }
.nueva-form { display: none; margin-top: 8px; padding: 10px; background: #f9f9f9; border-radius: 8px; }
.alertas { background: #FFF3E0; border-radius: 12px; padding: 14px; margin-bottom: 14px; }
.alertas h3 { font-size: 14px; color: #854F0B; margin-bottom: 8px; }
.alerta-item { font-size: 13px; color: #633806; padding: 5px 0; border-bottom: 1px solid #FFE0A0; }
.alerta-item:last-child { border-bottom: none; }
table { width: 100%; border-collapse: collapse; font-size: 13px; }
th { background: #E0F5EC; padding: 8px 6px; text-align: left; font-size: 12px; }
td { padding: 7px 6px; border-bottom: 1px solid #eee; }
.bajo { color: #A32D2D; font-weight: 600; }
.tabs { display: flex; gap: 8px; margin-bottom: 14px; }
.tab { flex: 1; padding: 10px; background: white; border: 2px solid #ddd; border-radius: 10px; font-size: 14px; font-weight: 500; cursor: pointer; text-align: center; color: #555; }
.tab.active { border-color: #1D9E75; color: #1D9E75; background: #E0F5EC; }
.section { display: none; }
.section.active { display: block; }
</style>
</head>
<body>
<div class="header">
  <h1>&#127800; Expowonder</h1>
  <p>Control de inventario de flores</p>
</div>
<div class="container">
  <div id="alertas-box"></div>
  <div class="tabs">
    <div class="tab active" onclick="showTab('entrada')">Entrada</div>
    <div class="tab" onclick="showTab('stock')">Stock</div>
  </div>

  <div class="section active" id="tab-entrada">
    <div class="card">
      <h2>Registrar entrada de flor</h2>
      <label>Flor</label>
      <select id="flor-select">
        <option value="">-- Selecciona una flor --</option>
      </select>
      <span class="nueva-link" onclick="toggleNueva()">+ Agregar flor nueva</span>
      <div class="nueva-form" id="nueva-form">
        <label>Nombre</label>
        <input type="text" id="nueva-nombre" placeholder="Ej: Rose Sunset">
        <label>Categoría</label>
        <input type="text" id="nueva-cat" placeholder="Ej: Rosa">
        <button class="btn btn-gray" style="margin-top:8px;font-size:14px;padding:10px" onclick="agregarNueva()">Guardar flor nueva</button>
      </div>
      <label>Ramos completos</label>
      <input type="number" id="ramos" min="0" value="0" placeholder="0">
      <label>Tallos sueltos</label>
      <input type="number" id="tallos" min="0" value="0" placeholder="0">
      <label>Tu nombre</label>
      <input type="text" id="usuario" placeholder="Ej: Maria">
      <button class="btn" onclick="registrar()">Registrar entrada</button>
      <div id="msg"></div>
    </div>
  </div>

  <div class="section" id="tab-stock">
    <div class="card">
      <h2>Stock actual</h2>
      <div id="stock-list">Cargando...</div>
    </div>
  </div>
</div>

<script>
let CATALOGO = [];

async function init() {
  const res = await fetch("/catalogo");
  CATALOGO = await res.json();
  llenarSelect(CATALOGO);
  cargarStock();
  cargarAlertas();
}

function llenarSelect(lista) {
  const sel = document.getElementById("flor-select");
  sel.innerHTML = '<option value="">-- Selecciona una flor --</option>';
  const cats = [...new Set(lista.map(p => p.categoria))].sort();
  cats.forEach(cat => {
    const group = document.createElement("optgroup");
    group.label = cat;
    lista.filter(p => p.categoria === cat).forEach(p => {
      const opt = document.createElement("option");
      opt.value = p.nombre;
      opt.textContent = p.nombre;
      group.appendChild(opt);
    });
    sel.appendChild(group);
  });
}

function showTab(tab) {
  document.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
  document.querySelectorAll(".section").forEach(s => s.classList.remove("active"));
  document.querySelector(`#tab-${tab}`).classList.add("active");
  event.target.classList.add("active");
  if (tab === "stock") cargarStock();
}

function toggleNueva() {
  const f = document.getElementById("nueva-form");
  f.style.display = f.style.display === "none" ? "block" : "none";
}

async function agregarNueva() {
  const nombre = document.getElementById("nueva-nombre").value.trim();
  const cat = document.getElementById("nueva-cat").value.trim() || "Sin categoría";
  if (!nombre) return;
  const res = await fetch("/agregar_flor", {
    method: "POST", headers: {"Content-Type":"application/json"},
    body: JSON.stringify({nombre, categoria: cat})
  });
  const data = await res.json();
  if (data.ok) {
    CATALOGO.push({nombre, categoria: cat});
    llenarSelect(CATALOGO);
    document.getElementById("nueva-nombre").value = "";
    document.getElementById("nueva-cat").value = "";
    document.getElementById("nueva-form").style.display = "none";
    showMsg("Flor agregada: " + nombre, "ok");
  }
}

async function registrar() {
  const flor = document.getElementById("flor-select").value;
  const ramos = parseInt(document.getElementById("ramos").value) || 0;
  const tallos = parseInt(document.getElementById("tallos").value) || 0;
  const usuario = document.getElementById("usuario").value.trim() || "finca";
  if (!flor) { showMsg("Selecciona una flor", "err"); return; }
  if (ramos <= 0 && tallos <= 0) { showMsg("Ingresa ramos o tallos", "err"); return; }
  const res = await fetch("/entrada", {
    method: "POST", headers: {"Content-Type":"application/json"},
    body: JSON.stringify({flor, ramos, tallos, usuario})
  });
  const data = await res.json();
  if (data.ok) {
    showMsg("Entrada registrada: " + flor, "ok");
    document.getElementById("ramos").value = "0";
    document.getElementById("tallos").value = "0";
    document.getElementById("flor-select").value = "";
    cargarAlertas();
  } else {
    showMsg("Error: " + data.error, "err");
  }
}

function showMsg(txt, tipo) {
  const m = document.getElementById("msg");
  m.className = "msg " + tipo;
  m.textContent = txt;
  setTimeout(() => m.textContent = "", 4000);
}

async function cargarStock() {
  const res = await fetch("/stock");
  const data = await res.json();
  const div = document.getElementById("stock-list");
  if (!data.length) { div.textContent = "Sin datos"; return; }
  let html = '<table><tr><th>Flor</th><th>Ramos</th><th>Tallos</th></tr>';
  data.forEach(f => {
    const bajo = f.stock_ramos < f.alerta_minimo;
    html += `<tr>
      <td class="${bajo ? 'bajo' : ''}">${f.nombre}</td>
      <td style="text-align:center" class="${bajo ? 'bajo' : ''}">${f.stock_ramos}</td>
      <td style="text-align:center">${f.stock_tallos}</td>
    </tr>`;
  });
  html += '</table>';
  div.innerHTML = html;
}

async function cargarAlertas() {
  const res = await fetch("/stock");
  const data = await res.json();
  const alertas = data.filter(f => f.stock_ramos < f.alerta_minimo && f.stock_ramos > 0);
  const box = document.getElementById("alertas-box");
  if (alertas.length) {
    let html = `<div class="alertas"><h3>&#9888;&#65039; ${alertas.length} flores bajo minimo</h3>`;
    alertas.forEach(a => {
      html += `<div class="alerta-item">${a.nombre} — ${a.stock_ramos} ramos</div>`;
    });
    html += '</div>';
    box.innerHTML = html;
  } else {
    box.innerHTML = '';
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
    flor = data.get("flor", "").strip()
    ramos = int(data.get("ramos", 0))
    tallos = int(data.get("tallos", 0))
    usuario = data.get("usuario", "finca")
    if not flor or (ramos <= 0 and tallos <= 0):
        return jsonify({"ok": False, "error": "Datos invalidos"})
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT id FROM flores WHERE LOWER(nombre)=LOWER(?)", (flor,))
        if not c.fetchone():
            c.execute("INSERT INTO flores (nombre, categoria) VALUES (?, ?)", (flor, "Sin categoria"))
        c.execute("UPDATE flores SET stock_ramos=stock_ramos+?, stock_tallos=stock_tallos+? WHERE LOWER(nombre)=LOWER(?)",
                  (ramos, tallos, flor))
        c.execute("INSERT INTO movimientos (fecha, flor_nombre, tipo, cantidad_ramos, cantidad_tallos, origen, usuario) VALUES (?,?,?,?,?,?,?)",
                  (datetime.now().strftime('%Y-%m-%d %H:%M'), flor, "ENTRADA", ramos, tallos, "REMISION", usuario))
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
    categoria = data.get("categoria", "Sin categoria").strip()
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

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
