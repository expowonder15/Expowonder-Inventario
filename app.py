import os
import sqlite3
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)
DB_PATH = "inventario.db"

CATALOGO = [{"nombre": "Rose Alive", "categoria": "Rosa"}, {"nombre": "Rose Blue Berry", "categoria": "Rosa"}, {"nombre": "Rose Bi Color", "categoria": "Rosa"}, {"nombre": "Rose Blush", "categoria": "Rosa"}, {"nombre": "Rose Brighton", "categoria": "Rosa"}, {"nombre": "Rose Blessing", "categoria": "Rosa"}, {"nombre": "Rose Café Del Mar", "categoria": "Rosa"}, {"nombre": "Rose Cherry Brandy", "categoria": "Rosa"}, {"nombre": "Rose Cool Water", "categoria": "Rosa"}, {"nombre": "Rose Deep Silver", "categoria": "Rosa"}, {"nombre": "Rose Deep Purple", "categoria": "Rosa"}, {"nombre": "Rose Engagement", "categoria": "Rosa"}, {"nombre": "Rose Forever Young", "categoria": "Rosa"}, {"nombre": "Rose Freedom", "categoria": "Rosa"}, {"nombre": "Rose Friendship", "categoria": "Rosa"}, {"nombre": "Rose Garota", "categoria": "Rosa"}, {"nombre": "Rose Gold Fish", "categoria": "Rosa"}, {"nombre": "Rose Gold Star", "categoria": "Rosa"}, {"nombre": "Rose Green", "categoria": "Rosa"}, {"nombre": "Rose Hearts", "categoria": "Rosa"}, {"nombre": "Rose Hermosa", "categoria": "Rosa"}, {"nombre": "Rose High And Arena", "categoria": "Rosa"}, {"nombre": "Rose High And Bonita", "categoria": "Rosa"}, {"nombre": "Rose High And Blooming", "categoria": "Rosa"}, {"nombre": "Rose High And Magic", "categoria": "Rosa"}, {"nombre": "Rose Hilux", "categoria": "Rosa"}, {"nombre": "Rose Hot Pink", "categoria": "Rosa"}, {"nombre": "Rose Hot Princess", "categoria": "Rosa"}, {"nombre": "Rose Ivory", "categoria": "Rosa"}, {"nombre": "Rose Lavender", "categoria": "Rosa"}, {"nombre": "Rose Light Orlando", "categoria": "Rosa"}, {"nombre": "Rose Light Pink", "categoria": "Rosa"}, {"nombre": "Rose Lola", "categoria": "Rosa"}, {"nombre": "Rose Luciano", "categoria": "Rosa"}, {"nombre": "Rose Minion Yellow", "categoria": "Rosa"}, {"nombre": "Rose Mondial", "categoria": "Rosa"}, {"nombre": "Rose Movistar", "categoria": "Rosa"}, {"nombre": "Rose New Face", "categoria": "Rosa"}, {"nombre": "Rose New Flash", "categoria": "Rosa"}, {"nombre": "Rose Orange", "categoria": "Rosa"}, {"nombre": "Rose Orlando", "categoria": "Rosa"}, {"nombre": "Rose Peach", "categoria": "Rosa"}, {"nombre": "Rose Pink", "categoria": "Rosa"}, {"nombre": "Rose Pink Floyd", "categoria": "Rosa"}, {"nombre": "Rose Pink Mondial", "categoria": "Rosa"}, {"nombre": "Rose Playa Blanca", "categoria": "Rosa"}, {"nombre": "Rose Pleasure", "categoria": "Rosa"}, {"nombre": "Rose Polar Star", "categoria": "Rosa"}, {"nombre": "Rose Princess Crown", "categoria": "Rosa"}, {"nombre": "Rose Proud", "categoria": "Rosa"}, {"nombre": "Rose Purple", "categoria": "Rosa"}, {"nombre": "Rose Queens Crown", "categoria": "Rosa"}, {"nombre": "Rose Ragazza", "categoria": "Rosa"}, {"nombre": "Rose Red", "categoria": "Rosa"}, {"nombre": "Rose Shimmer", "categoria": "Rosa"}, {"nombre": "Rose Silantoy", "categoria": "Rosa"}, {"nombre": "Rose Skyline", "categoria": "Rosa"}, {"nombre": "Rose Soulmate", "categoria": "Rosa"}, {"nombre": "Rose Stardust", "categoria": "Rosa"}, {"nombre": "Rose Sugar Doll", "categoria": "Rosa"}, {"nombre": "Rose Sweet Unique", "categoria": "Rosa"}, {"nombre": "Rose Sweetness", "categoria": "Rosa"}, {"nombre": "Rose Tabata", "categoria": "Rosa"}, {"nombre": "Rose Tiffany", "categoria": "Rosa"}, {"nombre": "Rose V.P Pink", "categoria": "Rosa"}, {"nombre": "Rose Vendela", "categoria": "Rosa"}, {"nombre": "Rose White", "categoria": "Rosa"}, {"nombre": "Rose Yellow", "categoria": "Rosa"}, {"nombre": "Rose Spray Red", "categoria": "Rose Spray"}, {"nombre": "Rose Spray Hot Pink", "categoria": "Rose Spray"}, {"nombre": "Rose Spray Pink", "categoria": "Rose Spray"}, {"nombre": "Rose Spray White", "categoria": "Rose Spray"}, {"nombre": "Rose Spray Yellow", "categoria": "Rose Spray"}, {"nombre": "Alstroemeria Assorted", "categoria": "Alstroemeria"}, {"nombre": "Alstroemeria Bi Color", "categoria": "Alstroemeria"}, {"nombre": "Alstroemeria Creme", "categoria": "Alstroemeria"}, {"nombre": "Alstroemeria Hot Pink", "categoria": "Alstroemeria"}, {"nombre": "Alstroemeria Lavender", "categoria": "Alstroemeria"}, {"nombre": "Alstroemeria Orange", "categoria": "Alstroemeria"}, {"nombre": "Alstroemeria Pink", "categoria": "Alstroemeria"}, {"nombre": "Alstroemeria Purple", "categoria": "Alstroemeria"}, {"nombre": "Alstroemeria Red", "categoria": "Alstroemeria"}, {"nombre": "Alstroemeria White", "categoria": "Alstroemeria"}, {"nombre": "Alstroemeria Yellow", "categoria": "Alstroemeria"}, {"nombre": "Asiatic Lily Red", "categoria": "Lirio"}, {"nombre": "Asiatic Lily Orange", "categoria": "Lirio"}, {"nombre": "Asiatic Lily Pink", "categoria": "Lirio"}, {"nombre": "Asiatic Lily White", "categoria": "Lirio"}, {"nombre": "Asiatic Lily Yellow", "categoria": "Lirio"}, {"nombre": "Oriental Lily Red", "categoria": "Lirio"}, {"nombre": "Oriental Lily Orange", "categoria": "Lirio"}, {"nombre": "Oriental Lily Pink", "categoria": "Lirio"}, {"nombre": "Oriental Lily White", "categoria": "Lirio"}, {"nombre": "Oriental Lily Yellow", "categoria": "Lirio"}, {"nombre": "Calla Lily Pink", "categoria": "Calla"}, {"nombre": "Calla Lily White", "categoria": "Calla"}, {"nombre": "Button White", "categoria": "pompon"}, {"nombre": "Button Yellow", "categoria": "pompon"}, {"nombre": "Button Pink", "categoria": "pompon"}, {"nombre": "Button Hot Pink", "categoria": "pompon"}, {"nombre": "Button Lavender", "categoria": "pompon"}, {"nombre": "Button Orange", "categoria": "pompon"}, {"nombre": "Button Purple", "categoria": "pompon"}, {"nombre": "Button Novelty Light Bronze", "categoria": "pompon"}, {"nombre": "Button Dark Bronze", "categoria": "pompon"}, {"nombre": "Button Red", "categoria": "pompon"}, {"nombre": "Button  Green", "categoria": "pompon"}, {"nombre": "Novelty White", "categoria": "pompon"}, {"nombre": "Novelty Yellow", "categoria": "pompon"}, {"nombre": "Novelty Pink", "categoria": "pompon"}, {"nombre": "Novelty Hot Pink", "categoria": "pompon"}, {"nombre": "Novelty Lavender", "categoria": "pompon"}, {"nombre": "Novelty Orange", "categoria": "pompon"}, {"nombre": "Novelty Purple", "categoria": "pompon"}, {"nombre": "Novelty Light Bronze", "categoria": "pompon"}, {"nombre": "Novelty Dark Bronze", "categoria": "pompon"}, {"nombre": "Novelty Red", "categoria": "pompon"}, {"nombre": "Novelty Green", "categoria": "pompon"}, {"nombre": "Cushion White", "categoria": "pompon"}, {"nombre": "Cushion Yellow", "categoria": "pompon"}, {"nombre": "Cushion Pink", "categoria": "pompon"}, {"nombre": "Cushion Hot Pink", "categoria": "pompon"}, {"nombre": "Cushion Lavender", "categoria": "pompon"}, {"nombre": "Cushion Orange", "categoria": "pompon"}, {"nombre": "Cushion Purple", "categoria": "pompon"}, {"nombre": "Cushion Light Bronze", "categoria": "pompon"}, {"nombre": "Cushion Dark Bronze", "categoria": "pompon"}, {"nombre": "Cushion Red", "categoria": "pompon"}, {"nombre": "Cushion Green", "categoria": "pompon"}, {"nombre": "Daisy White", "categoria": "pompon"}, {"nombre": "Daisy Yellow", "categoria": "pompon"}, {"nombre": "Daisy Pink", "categoria": "pompon"}, {"nombre": "Daisy Hot Pink", "categoria": "pompon"}, {"nombre": "Daisy Lavender", "categoria": "pompon"}, {"nombre": "Daisy Orange", "categoria": "pompon"}, {"nombre": "Daisy Purple", "categoria": "pompon"}, {"nombre": "Daisy Light Bronze", "categoria": "pompon"}, {"nombre": "Daisy Dark Bronze", "categoria": "pompon"}, {"nombre": "Daisy Red", "categoria": "pompon"}, {"nombre": "Purple Green", "categoria": "pompon"}, {"nombre": "Purple Micro Poms", "categoria": "pompon"}, {"nombre": "Pink Micro Poms", "categoria": "pompon"}, {"nombre": "Viking Yellow", "categoria": "pompon"}, {"nombre": "Orinoco Dsy", "categoria": "pompon"}, {"nombre": "Gerbera Pink", "categoria": "Gerbera"}, {"nombre": "Gerbera Red", "categoria": "Gerbera"}, {"nombre": "Gerbera White", "categoria": "Gerbera"}, {"nombre": "Gerbera Purple", "categoria": "Gerbera"}, {"nombre": "Gerbera Green", "categoria": "Gerbera"}, {"nombre": "Gerbera Dark Pink", "categoria": "Gerbera"}, {"nombre": "Gerbera Orange", "categoria": "Gerbera"}, {"nombre": "Gerbera Burgundy", "categoria": "Gerbera"}, {"nombre": "Gerbera Hot Pink", "categoria": "Gerbera"}, {"nombre": "Gerbera Yellow", "categoria": "Gerbera"}, {"nombre": "Hydrangea Blue", "categoria": "Hydrangea"}, {"nombre": "Hydrangea Pink", "categoria": "Hydrangea"}, {"nombre": "Hydrangea Green", "categoria": "Hydrangea"}, {"nombre": "Hydrangea White", "categoria": "Hydrangea"}, {"nombre": "Mini Hydrangea  Green", "categoria": "Mini-Hydrangea"}, {"nombre": "Hypericum Pink", "categoria": "Hypericum"}, {"nombre": "Hypericum Green", "categoria": "Hypericum"}, {"nombre": "Hypericum Orange", "categoria": "Hypericum"}, {"nombre": "Hypericum Red", "categoria": "Hypericum"}, {"nombre": "Kangaroo Orange", "categoria": "Kangaroo"}, {"nombre": "Kangaroo Yellow", "categoria": "Kangaroo"}, {"nombre": "Kangaroo Green", "categoria": "Kangaroo"}, {"nombre": "Kangaroo Red", "categoria": "Kangaroo"}, {"nombre": "Limonium Purple", "categoria": "Limonium"}, {"nombre": "Limonium White", "categoria": "Limonium"}, {"nombre": "Limonium Lavender", "categoria": "Limonium"}, {"nombre": "Limonium Peach", "categoria": "Limonium"}, {"nombre": "Limonium Pink", "categoria": "Limonium"}, {"nombre": "Limonium Yellow", "categoria": "Limonium"}, {"nombre": "Matsumoto Red", "categoria": "Matsumoto"}, {"nombre": "Matsumoto Blue", "categoria": "Matsumoto"}, {"nombre": "Matsumoto Pink", "categoria": "Matsumoto"}, {"nombre": "Matsumoto Purple", "categoria": "Matsumoto"}, {"nombre": "Matsumoto Hot Pink", "categoria": "Matsumoto"}, {"nombre": "Matsumoto White", "categoria": "Matsumoto"}, {"nombre": "Ranunculus Pink", "categoria": "Ranunculus"}, {"nombre": "Ranunculus White", "categoria": "Ranunculus"}, {"nombre": "Ranunculus Yellow", "categoria": "Ranunculus"}, {"nombre": "Snapdragon Orange", "categoria": "Snapdragon"}, {"nombre": "Snapdragon Pink", "categoria": "Snapdragon"}, {"nombre": "Snapdragon Yellow", "categoria": "Snapdragon"}, {"nombre": "Snapdragon Purple", "categoria": "Snapdragon"}, {"nombre": "Snapdragon White", "categoria": "Snapdragon"}, {"nombre": "Spider Mums White", "categoria": "Spider Mums"}, {"nombre": "Spider Mums Yellow", "categoria": "Spider Mums"}, {"nombre": "Spider Mums Light Bronze", "categoria": "Spider Mums"}, {"nombre": "Spider Mums Dark Bronze", "categoria": "Spider Mums"}, {"nombre": "Spider Mums Green", "categoria": "Spider Mums"}, {"nombre": "Spider Mums Lavanda", "categoria": "Spider Mums"}, {"nombre": "Spider Mums Purple", "categoria": "Spider Mums"}, {"nombre": "Statice Pink", "categoria": "Statice"}, {"nombre": "Statice Purple", "categoria": "Statice"}, {"nombre": "Statice White", "categoria": "Statice"}, {"nombre": "Ave De Paraiso", "categoria": "Verde"}, {"nombre": "Baby Blue", "categoria": "Verde"}, {"nombre": "Bear Grass", "categoria": "Verde"}, {"nombre": "Bells Of Ireland", "categoria": "Verde"}, {"nombre": "Brillantina", "categoria": "Verde"}, {"nombre": "Cocculus", "categoria": "Verde"}, {"nombre": "Craspedia Yellow", "categoria": "Verde"}, {"nombre": "Eryngium", "categoria": "Verde"}, {"nombre": "Euc Cinerea", "categoria": "Eucalyptus"}, {"nombre": "Euc Gunni", "categoria": "Eucalyptus"}, {"nombre": "Euc Parvifolia", "categoria": "Eucalyptus"}, {"nombre": "Euc Silver Dollar", "categoria": "Eucalyptus"}, {"nombre": "Eucalyptus", "categoria": "Eucalyptus"}, {"nombre": "Green Pino", "categoria": "Verde"}, {"nombre": "Gypso", "categoria": "Gypso"}, {"nombre": "Kale", "categoria": "Verde"}, {"nombre": "Leather Leaf", "categoria": "Verde"}, {"nombre": "Leucadendron Red", "categoria": "Verde"}, {"nombre": "Ligustrum", "categoria": "Verde"}, {"nombre": "Lily Grass", "categoria": "Verde"}, {"nombre": "Pilea", "categoria": "Verde"}, {"nombre": "Pittosporum", "categoria": "Verde"}, {"nombre": "Ruscus", "categoria": "Verde"}, {"nombre": "Solidago", "categoria": "Verde"}, {"nombre": "Star Of Bethlehem", "categoria": "Verde"}, {"nombre": "Sunflower", "categoria": "Verde"}, {"nombre": "Traqueleo", "categoria": "Verde"}, {"nombre": "Trefern", "categoria": "Verde"}, {"nombre": "Variegated Pittosporum", "categoria": "Verde"}, {"nombre": "Viburnum", "categoria": "Verde"}, {"nombre": "Single Red Roses", "categoria": "Verde"}, {"nombre": "Single Red Roses Fillers", "categoria": "Verde"}, {"nombre": "Single Asst Roses", "categoria": "Verde"}, {"nombre": "Single Asst Roses Fillers", "categoria": "Verde"}, {"nombre": "Carnations White", "categoria": "Carnations"}, {"nombre": "Carnations Yellow", "categoria": "Carnations"}, {"nombre": "Carnations Pink", "categoria": "Carnations"}, {"nombre": "Carnations Hot Pink", "categoria": "Carnations"}, {"nombre": "Carnations Lavender", "categoria": "Carnations"}, {"nombre": "Carnations Orange", "categoria": "Carnations"}, {"nombre": "Carnations Purple", "categoria": "Carnations"}, {"nombre": "Carnations Light Bronze", "categoria": "Carnations"}, {"nombre": "Carnations Dark Bronze", "categoria": "Carnations"}, {"nombre": "Carnations Red", "categoria": "Carnations"}, {"nombre": "Carnations Green", "categoria": "Carnations"}, {"nombre": "Carnations Peach", "categoria": "Carnations"}, {"nombre": "Mini Carnations White", "categoria": "Mini Carnations"}, {"nombre": "Mini Carnations Yellow", "categoria": "Mini Carnations"}, {"nombre": "Mini Carnations Pink", "categoria": "Mini Carnations"}, {"nombre": "Mini Carnations Hot Pink", "categoria": "Mini Carnations"}, {"nombre": "Mini Carnations Lavender", "categoria": "Mini Carnations"}, {"nombre": "Mini Carnations Orange", "categoria": "Mini Carnations"}, {"nombre": "Mini Carnations Purple", "categoria": "Mini Carnations"}, {"nombre": "Mini Carnations Light Bronze", "categoria": "Mini Carnations"}, {"nombre": "Mini Carnations Dark Bronze", "categoria": "Mini Carnations"}, {"nombre": "Mini Carnations Red", "categoria": "Mini Carnations"}, {"nombre": "Mini Carnations Green", "categoria": "Mini Carnations"}, {"nombre": "Mini Carnations Peach", "categoria": "Mini Carnations"}, {"nombre": "Dianthus White", "categoria": "Dianthus"}, {"nombre": "Dianthus Yellow", "categoria": "Dianthus"}, {"nombre": "Dianthus Pink", "categoria": "Dianthus"}, {"nombre": "Dianthus Hot Pink", "categoria": "Dianthus"}, {"nombre": "Dianthus Lavender", "categoria": "Dianthus"}, {"nombre": "Dianthus Orange", "categoria": "Dianthus"}, {"nombre": "Dianthus Purple", "categoria": "Dianthus"}, {"nombre": "Dianthus Light Bronze", "categoria": "Dianthus"}, {"nombre": "Dianthus Dark Bronze", "categoria": "Dianthus"}, {"nombre": "Dianthus Red", "categoria": "Dianthus"}, {"nombre": "Dianthus Green", "categoria": "Dianthus"}, {"nombre": "Dianthus Peach", "categoria": "Dianthus"}, {"nombre": "Green Ball", "categoria": "Verde"}, {"nombre": "Mini Calla White", "categoria": "Mini Calla"}, {"nombre": "Mini Calla Pink", "categoria": "Mini Calla"}, {"nombre": "Mini Calla Lavender", "categoria": "Mini Calla"}, {"nombre": "Mini Calla Orange", "categoria": "Mini Calla"}, {"nombre": "Mini Calla Hot Pink", "categoria": "Mini Calla"}, {"nombre": "Mini Calla Peach", "categoria": "Mini Calla"}, {"nombre": "Mini calla Yellow", "categoria": "Mini Calla"}, {"nombre": "Mini Calla Purple", "categoria": "Mini Calla"}, {"nombre": "Mini Calla Red", "categoria": "Mini Calla"}, {"nombre": "Mini Calla Green", "categoria": "Mini Calla"}, {"nombre": "Stock White", "categoria": "Stock"}, {"nombre": "Stock Yellow", "categoria": "Stock"}, {"nombre": "Stock Pink", "categoria": "Stock"}, {"nombre": "Stock Hot Pink", "categoria": "Stock"}, {"nombre": "Stock Lavender", "categoria": "Stock"}, {"nombre": "Stock Orange", "categoria": "Stock"}, {"nombre": "Stock Purple", "categoria": "Stock"}, {"nombre": "Stock Light Bronze", "categoria": "Stock"}, {"nombre": "Stock Dark Bronze", "categoria": "Stock"}, {"nombre": "Stock Red", "categoria": "Stock"}, {"nombre": "Stock Green", "categoria": "Stock"}, {"nombre": "Stock Peach", "categoria": "Stock"}, {"nombre": "Aster White", "categoria": "Aster"}, {"nombre": "Aster Purple", "categoria": "Aster"}, {"nombre": "Aster Pink", "categoria": "Aster"}, {"nombre": "Palma Robelina", "categoria": "verde"}, {"nombre": "Liatris Purple", "categoria": "Liatris"}, {"nombre": "Liatris White", "categoria": "Liatris"}]


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS flores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT UNIQUE NOT NULL,
        categoria TEXT,
        stock_ramos INTEGER DEFAULT 0,
        stock_tallos INTEGER DEFAULT 0,
        alerta_minimo INTEGER DEFAULT 50,
        activo INTEGER DEFAULT 1
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS movimientos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT NOT NULL,
        flor_nombre TEXT NOT NULL,
        tipo TEXT NOT NULL,
        cantidad_ramos INTEGER DEFAULT 0,
        cantidad_tallos INTEGER DEFAULT 0,
        origen TEXT,
        proveedor TEXT,
        fecha_remision TEXT,
        usuario TEXT DEFAULT 'sistema',
        notas TEXT
    )""")
    for p in CATALOGO:
        c.execute("INSERT OR IGNORE INTO flores (nombre, categoria) VALUES (?, ?)",
                  (p["nombre"], p["categoria"]))
    conn.commit()
    conn.close()

HTML = """<!DOCTYPE html>
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
.tabs { display: flex; background: white; border-bottom: 1px solid #eee; position: sticky; top: 54px; z-index: 99; overflow-x: auto; }
.tab { flex: 1; min-width: 70px; padding: 11px 4px; font-size: 11px; font-weight: 500; text-align: center; cursor: pointer; color: #888; border-bottom: 3px solid transparent; white-space: nowrap; }
.tab.active { color: #1D9E75; border-bottom-color: #1D9E75; }
.container { padding: 14px; max-width: 500px; margin: 0 auto; }
.card { background: white; border-radius: 12px; padding: 14px; margin-bottom: 12px; box-shadow: 0 1px 4px rgba(0,0,0,0.07); }
.card h2 { font-size: 14px; font-weight: 600; color: #1D9E75; margin-bottom: 10px; }
label { font-size: 12px; color: #666; display: block; margin-bottom: 3px; margin-top: 10px; }
input, select { width: 100%; padding: 10px 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 15px; background: #fafafa; }
input:focus { outline: none; border-color: #1D9E75; background: white; }
.btn { width: 100%; padding: 13px; background: #1D9E75; color: white; border: none; border-radius: 10px; font-size: 15px; font-weight: 600; margin-top: 12px; cursor: pointer; }
.btn:active { background: #0F6E56; }
.btn-gray { background: #555; }
.btn-red { background: #C0392B; }
.btn-sm { padding: 8px 14px; font-size: 13px; margin-top: 0; width: 100%; border-radius: 8px; }
.msg { padding: 12px; border-radius: 8px; font-size: 14px; margin-top: 10px; text-align: center; font-weight: 500; }
.msg.ok { background: #E0F5EC; color: #0F6E56; }
.msg.err { background: #FCEBEB; color: #A32D2D; }
.search-box { position: relative; }
.search-results { display: none; position: absolute; top: 100%; left: 0; right: 0; background: white; border: 1px solid #ddd; border-radius: 8px; max-height: 180px; overflow-y: auto; z-index: 300; box-shadow: 0 4px 12px rgba(0,0,0,0.12); }
.search-item { padding: 10px 12px; cursor: pointer; border-bottom: 1px solid #f0f0f0; font-size: 14px; }
.search-item:active { background: #f0f7f4; }
.search-item small { color: #888; font-size: 11px; display: block; }
.flor-tag { display: flex; align-items: center; justify-content: space-between; background: #E0F5EC; border-radius: 8px; padding: 8px 12px; margin-top: 6px; }
.flor-tag span { font-size: 13px; color: #0F6E56; font-weight: 500; }
.flor-tag button { background: none; border: none; font-size: 18px; color: #888; cursor: pointer; }
.carrito { background: #f5f5f5; border-radius: 10px; padding: 10px; margin-top: 10px; }
.carrito-titulo { font-size: 12px; font-weight: 600; color: #555; margin-bottom: 8px; }
.carrito-item { display: flex; align-items: center; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid #e0e0e0; font-size: 13px; }
.carrito-item:last-child { border-bottom: none; }
.carrito-item button { background: none; border: none; color: #C0392B; cursor: pointer; font-size: 16px; }
.row2 { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.alerta-box { background: #FFF3E0; border-radius: 12px; padding: 12px; margin-bottom: 12px; }
.alerta-box h3 { font-size: 13px; color: #854F0B; margin-bottom: 6px; }
.alerta-item { font-size: 12px; color: #633806; padding: 4px 0; border-bottom: 1px solid #FFE0A0; }
.alerta-item:last-child { border-bottom: none; }
.tipo-selector { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 8px; }
.tipo-btn { padding: 10px; border: 2px solid #ddd; border-radius: 10px; text-align: center; cursor: pointer; font-size: 13px; font-weight: 500; color: #555; background: white; }
.tipo-btn.activo-verde { border-color: #1D9E75; color: #1D9E75; background: #E0F5EC; }
.tipo-btn.activo-rojo { border-color: #C0392B; color: #C0392B; background: #FCEBEB; }
.section { display: none; }
.section.active { display: block; }
table { width: 100%; border-collapse: collapse; font-size: 12px; }
th { background: #E0F5EC; padding: 7px 5px; text-align: left; font-size: 11px; font-weight: 600; }
td { padding: 7px 5px; border-bottom: 1px solid #f0f0f0; vertical-align: middle; }
.badge-ok { color: #0F6E56; font-weight: 600; }
.badge-bajo { color: #A32D2D; font-weight: 600; }
.nueva-link { font-size: 12px; color: #1D9E75; margin-top: 8px; cursor: pointer; text-decoration: underline; display: inline-block; }
.nueva-form { display: none; margin-top: 8px; padding: 10px; background: #f9f9f9; border-radius: 8px; }
.mov-card { background: #f9f9f9; border-radius: 8px; padding: 10px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: flex-start; }
.mov-info { font-size: 13px; }
.mov-info strong { display: block; margin-bottom: 2px; }
.mov-info small { color: #888; font-size: 11px; }
.btn-eliminar { background: #C0392B; color: white; border: none; border-radius: 6px; padding: 6px 12px; font-size: 12px; cursor: pointer; white-space: nowrap; margin-left: 8px; }
.mov-entrada { border-left: 3px solid #1D9E75; }
.mov-salida { border-left: 3px solid #C0392B; }
.mov-cambio { border-left: 3px solid #F39C12; }
</style>
</head>
<body>
<div class="header">
  <h1>&#127800; Expowonder ERP</h1>
  <p>Control de inventario de flores</p>
</div>
<div class="tabs">
  <div class="tab active" onclick="showTab('entrada',this)">&#128230; Entrada</div>
  <div class="tab" onclick="showTab('baja',this)">&#128683; Baja/Cambio</div>
  <div class="tab" onclick="showTab('stock',this)">&#128200; Stock</div>
  <div class="tab" onclick="showTab('historial',this)">&#128221; Historial</div>
</div>

<div class="container">
  <div id="alertas-box"></div>

  <!-- ENTRADA -->
  <div class="section active" id="tab-entrada">
    <div class="card">
      <h2>&#128230; Registrar entrada de flores</h2>
      <label>Proveedor</label>
      <input type="text" id="e-proveedor" placeholder="Nombre del proveedor">
      <label>Fecha de remision</label>
      <input type="date" id="e-fecha">
      <label>Tu nombre</label>
      <input type="text" id="e-usuario" placeholder="Ej: Maria">
      <div style="margin-top:12px;border-top:1px solid #eee;padding-top:12px">
        <div style="background:#f9f9f9;border-radius:10px;padding:12px">
          <div style="font-size:13px;font-weight:600;color:#1D9E75;margin-bottom:8px">Agregar flor al listado</div>
          <label>Buscar flor</label>
          <div class="search-box">
            <input type="text" id="e-buscar" placeholder="Escribe para buscar..." oninput="filtrar('e-buscar','e-lista')" autocomplete="off" onblur="ocultarLista('e-lista')">
            <div class="search-results" id="e-lista"></div>
          </div>
          <div id="e-tag" class="flor-tag" style="display:none">
            <span id="e-tag-nombre"></span>
            <button onclick="limpiarTag('e')">&#10005;</button>
          </div>
          <div class="row2">
            <div><label>Ramos completos</label><input type="number" id="e-ramos" min="0" value="0"></div>
            <div><label>Tallos sueltos</label><input type="number" id="e-tallos" min="0" value="0"></div>
          </div>
          <button class="btn btn-gray btn-sm" style="margin-top:10px" onclick="agregarCarrito()">+ Agregar al listado</button>
        </div>
        <div id="carrito-box" class="carrito" style="display:none">
          <div class="carrito-titulo">&#128230; Flores a registrar:</div>
          <div id="carrito-items"></div>
        </div>
        <span class="nueva-link" onclick="toggle('nueva-e')">+ Agregar flor nueva que no esta en la lista</span>
        <div class="nueva-form" id="nueva-e">
          <label>Nombre</label><input type="text" id="e-nueva-nom" placeholder="Ej: Rose Sunset">
          <label>Categoria</label><input type="text" id="e-nueva-cat" placeholder="Ej: Rosa">
          <button class="btn btn-gray btn-sm" style="margin-top:8px" onclick="nuevaFlor('e')">Guardar flor nueva</button>
        </div>
      </div>
      <button class="btn" onclick="registrarEntrada()">&#10003; Registrar todas las entradas</button>
      <div id="e-msg"></div>
    </div>
  </div>

  <!-- BAJA / CAMBIO -->
  <div class="section" id="tab-baja">
    <div class="card">
      <h2>&#128683; Baja por dano o Cambio en despacho</h2>
      <label>Tipo</label>
      <div class="tipo-selector">
        <div class="tipo-btn activo-rojo" id="btn-dano" onclick="setTipo('dano')">&#128683; Baja por dano</div>
        <div class="tipo-btn" id="btn-cambio" onclick="setTipo('cambio')">&#8646; Cambio despacho</div>
      </div>
      <label>Proveedor</label><input type="text" id="b-proveedor" placeholder="Nombre del proveedor">
      <label>Fecha</label><input type="date" id="b-fecha">
      <label>Tu nombre</label><input type="text" id="b-usuario" placeholder="Ej: Maria">

      <div id="sec-dano">
        <label>Flor danada</label>
        <div class="search-box">
          <input type="text" id="b-buscar" placeholder="Buscar flor..." oninput="filtrar('b-buscar','b-lista')" autocomplete="off" onblur="ocultarLista('b-lista')">
          <div class="search-results" id="b-lista"></div>
        </div>
        <div id="b-tag" class="flor-tag" style="display:none;background:#FCEBEB">
          <span id="b-tag-nombre" style="color:#C0392B"></span>
          <button onclick="limpiarTag('b')">&#10005;</button>
        </div>
        <div class="row2">
          <div><label>Ramos a dar de baja</label><input type="number" id="b-ramos" min="0" value="0"></div>
          <div><label>Tallos sueltos</label><input type="number" id="b-tallos" min="0" value="0"></div>
        </div>
        <label>Notas (opcional)</label>
        <input type="text" id="b-notas" placeholder="Ej: llegaron marchitas">
      </div>

      <div id="sec-cambio" style="display:none">
        <div style="background:#FFF3E0;border-radius:8px;padding:10px;margin-top:10px;font-size:12px;color:#854F0B">
          &#9888; La flor original se devuelve al stock. La flor enviada se descuenta.
        </div>
        <label>Flor ORIGINAL (la que pedia la orden)</label>
        <div class="search-box">
          <input type="text" id="co-buscar" placeholder="Buscar flor original..." oninput="filtrar('co-buscar','co-lista')" autocomplete="off" onblur="ocultarLista('co-lista')">
          <div class="search-results" id="co-lista"></div>
        </div>
        <div id="co-tag" class="flor-tag" style="display:none">
          <span id="co-tag-nombre"></span>
          <button onclick="limpiarTagC('orig')">&#10005;</button>
        </div>
        <label>Flor ENVIADA (la que se mando realmente)</label>
        <div class="search-box">
          <input type="text" id="ce-buscar" placeholder="Buscar flor enviada..." oninput="filtrar('ce-buscar','ce-lista')" autocomplete="off" onblur="ocultarLista('ce-lista')">
          <div class="search-results" id="ce-lista"></div>
        </div>
        <div id="ce-tag" class="flor-tag" style="display:none;background:#FCEBEB">
          <span id="ce-tag-nombre" style="color:#C0392B"></span>
          <button onclick="limpiarTagC('env')">&#10005;</button>
        </div>
        <div class="row2" style="margin-top:10px">
          <div><label>Ramos</label><input type="number" id="c-ramos" min="0" value="0"></div>
          <div><label>Tallos sueltos</label><input type="number" id="c-tallos" min="0" value="0"></div>
        </div>
        <label>Notas (opcional)</label>
        <input type="text" id="c-notas" placeholder="Ej: cliente acepto el cambio">
      </div>

      <button class="btn btn-red" onclick="registrarBaja()">Registrar</button>
      <div id="b-msg"></div>
    </div>
  </div>

  <!-- STOCK -->
  <div class="section" id="tab-stock">
    <div class="card">
      <h2>&#128200; Stock actual</h2>
      <input type="text" id="s-filtro" placeholder="Filtrar por nombre..." oninput="filtrarStock()" style="margin-bottom:10px">
      <div id="stock-list">Cargando...</div>
    </div>
  </div>

  <!-- HISTORIAL -->
  <div class="section" id="tab-historial">
    <div class="card">
      <h2>&#128221; Historial de movimientos</h2>
      <p style="font-size:12px;color:#888;margin-bottom:12px">Ultimos 50 movimientos. Toca Eliminar para corregir un error — esto revierte el stock automaticamente.</p>
      <div id="historial-list">Cargando...</div>
    </div>
  </div>

</div>

<script>
let CATALOGO = [];
let carrito = [];
let tipoActual = "dano";
let florSel = { e:"", b:"" };
let florCambio = { orig:"", env:"" };
let stockData = [];

async function init() {
  const res = await fetch("/catalogo");
  CATALOGO = await res.json();
  const hoy = new Date().toISOString().split("T")[0];
  document.getElementById("e-fecha").value = hoy;
  document.getElementById("b-fecha").value = hoy;
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

function ocultarLista(id) {
  setTimeout(() => { const el = document.getElementById(id); if(el) el.style.display="none"; }, 200);
}

function filtrar(inputId, listaId) {
  const q = document.getElementById(inputId).value.trim().toLowerCase();
  const lista = document.getElementById(listaId);
  if (q.length < 1) { lista.style.display="none"; return; }
  const matches = CATALOGO.filter(p => p.nombre.toLowerCase().includes(q) || p.categoria.toLowerCase().includes(q)).slice(0,12);
  if (!matches.length) { lista.style.display="none"; return; }
  lista.innerHTML = "";
  matches.forEach(p => {
    const div = document.createElement("div");
    div.className = "search-item";
    div.innerHTML = p.nombre + "<small>" + p.categoria + "</small>";
    div.onmousedown = () => elegir(inputId, listaId, p.nombre);
    lista.appendChild(div);
  });
  lista.style.display = "block";
}

function elegir(inputId, listaId, nombre) {
  document.getElementById(inputId).value = "";
  document.getElementById(listaId).style.display = "none";
  if (inputId === "e-buscar") { florSel.e = nombre; mostrarTag("e", nombre); }
  else if (inputId === "b-buscar") { florSel.b = nombre; mostrarTag("b", nombre); }
  else if (inputId === "co-buscar") { florCambio.orig = nombre; mostrarTagC("orig", nombre); }
  else if (inputId === "ce-buscar") { florCambio.env = nombre; mostrarTagC("env", nombre); }
}

function mostrarTag(p, nombre) {
  document.getElementById(p+"-tag-nombre").textContent = "&#10003; " + nombre;
  document.getElementById(p+"-tag").style.display = "flex";
}
function limpiarTag(p) {
  florSel[p] = "";
  document.getElementById(p+"-tag").style.display = "none";
  document.getElementById(p+"-buscar").value = "";
}
function mostrarTagC(t, nombre) {
  const pre = t === "orig" ? "co" : "ce";
  document.getElementById(pre+"-tag-nombre").textContent = (t==="orig"?"&#8617; ":"&#8618; ") + nombre;
  document.getElementById(pre+"-tag").style.display = "flex";
}
function limpiarTagC(t) {
  florCambio[t] = "";
  const pre = t === "orig" ? "co" : "ce";
  document.getElementById(pre+"-tag").style.display = "none";
  document.getElementById(pre+"-buscar").value = "";
}

function setTipo(tipo) {
  tipoActual = tipo;
  document.getElementById("btn-dano").className = "tipo-btn" + (tipo==="dano" ? " activo-rojo" : "");
  document.getElementById("btn-cambio").className = "tipo-btn" + (tipo==="cambio" ? " activo-verde" : "");
  document.getElementById("sec-dano").style.display = tipo==="dano" ? "block" : "none";
  document.getElementById("sec-cambio").style.display = tipo==="cambio" ? "block" : "none";
}

function agregarCarrito() {
  const flor = florSel.e;
  const ramos = parseInt(document.getElementById("e-ramos").value) || 0;
  const tallos = parseInt(document.getElementById("e-tallos").value) || 0;
  if (!flor) { showMsg("e-msg","Selecciona una flor","err"); return; }
  if (ramos<=0 && tallos<=0) { showMsg("e-msg","Ingresa ramos o tallos","err"); return; }
  carrito.push({flor, ramos, tallos});
  renderCarrito();
  limpiarTag("e");
  document.getElementById("e-ramos").value="0";
  document.getElementById("e-tallos").value="0";
}

function renderCarrito() {
  const box = document.getElementById("carrito-box");
  const items = document.getElementById("carrito-items");
  if (!carrito.length) { box.style.display="none"; return; }
  box.style.display = "block";
  items.innerHTML = carrito.map((item,i) =>
    `<div class="carrito-item"><span>${item.flor}<br><small style="color:#888">${item.ramos} ramos · ${item.tallos} tallos</small></span><button onclick="quitarCarrito(${i})">&#10005;</button></div>`
  ).join("");
}

function quitarCarrito(i) { carrito.splice(i,1); renderCarrito(); }

async function registrarEntrada() {
  if (!carrito.length) { showMsg("e-msg","Agrega al menos una flor al listado","err"); return; }
  const proveedor = document.getElementById("e-proveedor").value.trim();
  const fecha = document.getElementById("e-fecha").value;
  const usuario = document.getElementById("e-usuario").value.trim() || "finca";
  if (!proveedor) { showMsg("e-msg","Escribe el nombre del proveedor","err"); return; }
  const res = await fetch("/entrada", {
    method:"POST", headers:{"Content-Type":"application/json"},
    body: JSON.stringify({items:carrito, proveedor, fecha_remision:fecha, usuario})
  });
  const data = await res.json();
  if (data.ok) {
    showMsg("e-msg","&#10003; " + carrito.length + " flores registradas correctamente","ok");
    carrito=[];
    renderCarrito();
    document.getElementById("e-proveedor").value="";
    cargarAlertas();
  } else {
    showMsg("e-msg","Error: "+data.error,"err");
  }
}

async function registrarBaja() {
  const proveedor = document.getElementById("b-proveedor").value.trim();
  const fecha = document.getElementById("b-fecha").value;
  const usuario = document.getElementById("b-usuario").value.trim() || "finca";
  if (tipoActual === "dano") {
    const flor = florSel.b;
    const ramos = parseInt(document.getElementById("b-ramos").value)||0;
    const tallos = parseInt(document.getElementById("b-tallos").value)||0;
    const notas = document.getElementById("b-notas").value.trim();
    if (!flor) { showMsg("b-msg","Selecciona la flor danada","err"); return; }
    if (ramos<=0 && tallos<=0) { showMsg("b-msg","Ingresa cantidad","err"); return; }
    const res = await fetch("/baja", {
      method:"POST", headers:{"Content-Type":"application/json"},
      body: JSON.stringify({tipo:"BAJA_DANO", flor, ramos, tallos, proveedor, fecha, usuario, notas})
    });
    const data = await res.json();
    if (data.ok) {
      showMsg("b-msg","&#10003; Baja registrada: "+flor,"ok");
      limpiarTag("b");
      document.getElementById("b-ramos").value="0";
      document.getElementById("b-tallos").value="0";
      document.getElementById("b-notas").value="";
      cargarAlertas();
    } else { showMsg("b-msg","Error: "+data.error,"err"); }
  } else {
    const florOrig = florCambio.orig;
    const florEnv = florCambio.env;
    const ramos = parseInt(document.getElementById("c-ramos").value)||0;
    const tallos = parseInt(document.getElementById("c-tallos").value)||0;
    const notas = document.getElementById("c-notas").value.trim();
    if (!florOrig || !florEnv) { showMsg("b-msg","Selecciona ambas flores","err"); return; }
    if (ramos<=0 && tallos<=0) { showMsg("b-msg","Ingresa cantidad","err"); return; }
    const res = await fetch("/cambio", {
      method:"POST", headers:{"Content-Type":"application/json"},
      body: JSON.stringify({flor_original:florOrig, flor_enviada:florEnv, ramos, tallos, proveedor, fecha, usuario, notas})
    });
    const data = await res.json();
    if (data.ok) {
      showMsg("b-msg","&#10003; Cambio registrado correctamente","ok");
      limpiarTagC("orig"); limpiarTagC("env");
      document.getElementById("c-ramos").value="0";
      document.getElementById("c-tallos").value="0";
      document.getElementById("c-notas").value="";
      cargarAlertas();
    } else { showMsg("b-msg","Error: "+data.error,"err"); }
  }
}

function showMsg(id, txt, tipo) {
  const m = document.getElementById(id);
  m.className = "msg " + tipo;
  m.innerHTML = txt;
  setTimeout(() => { m.textContent=""; m.className=""; }, 5000);
}

async function cargarStock() {
  const res = await fetch("/stock");
  stockData = await res.json();
  renderStock(stockData);
}

function filtrarStock() {
  const q = document.getElementById("s-filtro").value.toLowerCase();
  renderStock(stockData.filter(f => f.nombre.toLowerCase().includes(q) || f.categoria.toLowerCase().includes(q)));
}

function renderStock(data) {
  const div = document.getElementById("stock-list");
  if (!data.length) { div.textContent="Sin datos"; return; }
  let html = '<table><tr><th>Flor</th><th>Cat</th><th>Ramos</th><th>Tallos</th><th></th></tr>';
  data.forEach(f => {
    const bajo = f.stock_ramos < f.alerta_minimo;
    html += `<tr><td class="${bajo?'badge-bajo':''}">${f.nombre}</td><td style="color:#888;font-size:11px">${f.categoria}</td><td style="text-align:center" class="${bajo?'badge-bajo':'badge-ok'}">${f.stock_ramos}</td><td style="text-align:center">${f.stock_tallos}</td><td style="text-align:center">${bajo?"&#9888;":"&#10003;"}</td></tr>`;
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
    let html = `<div class="alerta-box"><h3>&#9888;&#65039; ${alertas.length} flores bajo minimo (50 ramos)</h3>`;
    alertas.forEach(a => { html += `<div class="alerta-item">${a.nombre} — ${a.stock_ramos} ramos</div>`; });
    html += "</div>";
    box.innerHTML = html;
  } else { box.innerHTML = ""; }
}

async function cargarHistorial() {
  const div = document.getElementById("historial-list");
  div.innerHTML = "<p style='color:#888;font-size:13px;text-align:center;padding:20px'>Cargando...</p>";
  try {
    const res = await fetch("/historial");
    const data = await res.json();
    if (!data.length) { div.innerHTML = "<p style='color:#888;font-size:13px;padding:10px'>Sin movimientos registrados.</p>"; return; }
    let html = "";
    data.forEach(m => {
      let clase = "mov-entrada";
      let icono = "&#128230;";
      if (m.tipo.includes("BAJA") || m.tipo.includes("SALIDA")) { clase="mov-salida"; icono="&#128683;"; }
      else if (m.tipo.includes("CAMBIO")) { clase="mov-cambio"; icono="&#8646;"; }
      html += `<div class="mov-card ${clase}">
        <div class="mov-info">
          <strong>${icono} ${m.flor_nombre}</strong>
          <small>${m.tipo} &middot; ${m.ramos} ramos &middot; ${m.tallos} tallos</small>
          <small>${m.fecha}${m.usuario ? " &middot; " + m.usuario : ""}${m.proveedor ? " &middot; " + m.proveedor : ""}</small>
        </div>
        <button class="btn-eliminar" onclick="eliminarMov(${m.id},'${m.flor_nombre.replace(/'/g,"\\'")}')">Eliminar</button>
      </div>`;
    });
    div.innerHTML = html;
  } catch(e) {
    div.innerHTML = "<p style='color:red;font-size:13px;padding:10px'>Error cargando historial.</p>";
  }
}

async function eliminarMov(id, nombre) {
  if (!confirm("Eliminar registro de " + nombre + "?\\nEsto revertira el stock automaticamente.")) return;
  const res = await fetch("/eliminar_movimiento", {
    method:"POST", headers:{"Content-Type":"application/json"},
    body: JSON.stringify({id})
  });
  const data = await res.json();
  if (data.ok) { cargarHistorial(); cargarAlertas(); }
  else { alert("Error: " + (data.error || "desconocido")); }
}

function toggle(id) {
  const el = document.getElementById(id);
  el.style.display = el.style.display === "none" ? "block" : "none";
}

async function nuevaFlor(prefix) {
  const nombre = document.getElementById(prefix+"-nueva-nom").value.trim();
  const cat = document.getElementById(prefix+"-nueva-cat").value.trim() || "Sin categoria";
  if (!nombre) return;
  const res = await fetch("/agregar_flor", {
    method:"POST", headers:{"Content-Type":"application/json"},
    body: JSON.stringify({nombre, categoria:cat})
  });
  const data = await res.json();
  if (data.ok) {
    CATALOGO.push({nombre, categoria:cat});
    document.getElementById(prefix+"-nueva-nom").value="";
    document.getElementById(prefix+"-nueva-cat").value="";
    showMsg("e-msg","Flor agregada: "+nombre,"ok");
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
                c.execute("INSERT INTO flores (nombre, categoria) VALUES (?, ?)", (flor, "Sin categoria"))
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
    tipo = data.get("tipo", "BAJA_DANO")
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
        c.execute("UPDATE flores SET stock_ramos=stock_ramos+?, stock_tallos=stock_tallos+? WHERE LOWER(nombre)=LOWER(?)",
                  (ramos, tallos, flor_orig))
        c.execute("INSERT INTO movimientos (fecha, flor_nombre, tipo, cantidad_ramos, cantidad_tallos, origen, proveedor, fecha_remision, usuario, notas) VALUES (?,?,?,?,?,?,?,?,?,?)",
                  (datetime.now().strftime("%Y-%m-%d %H:%M"), flor_orig, "CAMBIO_DEVOLUCION", ramos, tallos, "CAMBIO", proveedor, fecha, usuario, "Cambio por: "+flor_env+". "+notas))
        c.execute("UPDATE flores SET stock_ramos=stock_ramos-?, stock_tallos=stock_tallos-? WHERE LOWER(nombre)=LOWER(?)",
                  (ramos, tallos, flor_env))
        c.execute("INSERT INTO movimientos (fecha, flor_nombre, tipo, cantidad_ramos, cantidad_tallos, origen, proveedor, fecha_remision, usuario, notas) VALUES (?,?,?,?,?,?,?,?,?,?)",
                  (datetime.now().strftime("%Y-%m-%d %H:%M"), flor_env, "CAMBIO_SALIDA", ramos, tallos, "CAMBIO", proveedor, fecha, usuario, "Sustituyo a: "+flor_orig+". "+notas))
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
        c.execute("""SELECT id, fecha, flor_nombre, tipo, cantidad_ramos, cantidad_tallos, usuario, proveedor
                     FROM movimientos ORDER BY id DESC LIMIT 50""")
        rows = c.fetchall()
        conn.close()
        return jsonify([{"id":r[0],"fecha":r[1],"flor_nombre":r[2],"tipo":r[3],
                         "ramos":r[4],"tallos":r[5],"usuario":r[6],"proveedor":r[7] or ""} for r in rows])
    except Exception as e:
        return jsonify([])

@app.route("/eliminar_movimiento", methods=["POST"])
def eliminar_movimiento():
    data = request.json
    mov_id = data.get("id")
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT flor_nombre, tipo, cantidad_ramos, cantidad_tallos FROM movimientos WHERE id=?", (mov_id,))
        mov = c.fetchone()
        if mov:
            flor, tipo, ramos, tallos = mov
            if tipo == "ENTRADA":
                c.execute("UPDATE flores SET stock_ramos=stock_ramos-?, stock_tallos=stock_tallos-? WHERE LOWER(nombre)=LOWER(?)", (ramos, tallos, flor))
            elif tipo in ("BAJA_DANO","BAJA_DAÑO","CAMBIO_SALIDA"):
                c.execute("UPDATE flores SET stock_ramos=stock_ramos+?, stock_tallos=stock_tallos+? WHERE LOWER(nombre)=LOWER(?)", (ramos, tallos, flor))
            elif tipo == "CAMBIO_DEVOLUCION":
                c.execute("UPDATE flores SET stock_ramos=stock_ramos-?, stock_tallos=stock_tallos-? WHERE LOWER(nombre)=LOWER(?)", (ramos, tallos, flor))
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
        return jsonify([{"nombre":r[0],"categoria":r[1],"stock_ramos":r[2],"stock_tallos":r[3],"alerta_minimo":r[4]} for r in rows])
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

init_db()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
