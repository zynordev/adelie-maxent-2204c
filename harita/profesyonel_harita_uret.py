import os
import sys
from qgis.core import (
    QgsApplication,
    QgsProject,
    QgsRasterLayer,
    QgsVectorLayer,
    QgsColorRampShader,
    QgsRasterShader,
    QgsSingleBandPseudoColorRenderer,
    QgsColorRampShader,
    QgsLayoutExporter,
    QgsSimpleFillSymbolLayer,
    QgsSimpleLineSymbolLayer,
    QgsFillSymbol,
    QgsLineSymbol,
    QgsMarkerSymbol,
    QgsPalLabeling,
    QgsTextFormat,
    QgsTextBufferSettings,
    QgsVectorLayerSimpleLabeling
)
from qgis.PyQt.QtGui import QColor

# Headless QGIS Application
qgs = QgsApplication([], False)
qgs.initQgis()

project_path = "/home/halil/adelie-maxent-2204c/harita/a1.qgz"
project = QgsProject.instance()
if not project.read(project_path):
    print("HATA: Proje okunamadı!")
    sys.exit(1)

print("Proje başarıyla yüklendi:", project.fileName())

# 1. Katmanları bul
layers = project.mapLayers()
kiyi_layer = None
kiyi_cizgi_layer = None
noktalar_layer = None
istasyonlar_layer = None
raster_layer = None

for l_id, l in layers.items():
    name = l.name()
    if "kiyi_cizgi" in name:
        kiyi_cizgi_layer = l
    elif "kiyi" in name:
        kiyi_layer = l
    elif "noktalar" in name:
        noktalar_layer = l
    elif "istasyonlar" in name:
        istasyonlar_layer = l
    elif "uygunluk" in name:
        raster_layer = l

gpkg_path = "/home/halil/adelie-maxent-2204c/harita/qgis_katmanlari.gpkg"

# kiyi_cizgi ekli değilse ekle
if not kiyi_cizgi_layer:
    kiyi_cizgi_layer = QgsVectorLayer(f"{gpkg_path}|layername=kiyi_cizgi", "Kıyı Çizgisi (SCAR ADD)", "ogr")
    if kiyi_cizgi_layer.isValid():
        project.addMapLayer(kiyi_cizgi_layer)
        print("kiyi_cizgi katmanı eklendi.")

# 2. Raster Sembolojisi (5 Ayrık Sınıf ve Etiketler)
if raster_layer:
    raster_layer.setName("Habitat Uygunluk İndeksi (MaxEnt)")
    shader = QgsRasterShader()
    color_ramp = QgsColorRampShader()
    color_ramp.setColorRampType(QgsColorRampShader.Discrete)
    
    items = [
        QgsColorRampShader.ColorRampItem(0.20, QColor(43, 131, 186, 180), "0.00 – 0.20 : Çok Düşük (Uygun Değil / Açık Deniz)"),
        QgsColorRampShader.ColorRampItem(0.40, QColor(171, 221, 164, 210), "0.20 – 0.40 : Düşük Uygunluk"),
        QgsColorRampShader.ColorRampItem(0.60, QColor(255, 255, 191, 230), "0.40 – 0.60 : Orta Uygunluk"),
        QgsColorRampShader.ColorRampItem(0.80, QColor(253, 174, 97, 245), "0.60 – 0.80 : Yüksek Uygunluk (Beslenme Alanı)"),
        QgsColorRampShader.ColorRampItem(1.00, QColor(215, 25, 28, 255), "0.80 – 1.00 : Çok Yüksek Uygunluk (Aktif Koloni / Yuvalama)")
    ]
    color_ramp.setColorRampItemList(items)
    shader.setRasterShaderFunction(color_ramp)
    renderer = QgsSingleBandPseudoColorRenderer(raster_layer.dataProvider(), 1, shader)
    renderer.setClassificationMin(0.0)
    renderer.setClassificationMax(1.0)
    raster_layer.setRenderer(renderer)
    raster_layer.triggerRepaint()
    print("Raster sembolojisi Discrete 5 sınıf olarak ayarlandı.")

# 3. Kıyı (Poligon) Katmanı - Kenar çizgisini sıfırla (şeffaf)
if kiyi_layer:
    kiyi_layer.setName("Kara ve Buz Sahanlığı")
    symbol = QgsFillSymbol.createSimple({
        'color': '#f1f5f9',
        'outline_color': 'transparent',
        'outline_width': '0'
    })
    kiyi_layer.renderer().setSymbol(symbol)
    kiyi_layer.triggerRepaint()
    print("Kıyı poligon kenar çizgisi gizlendi (kesim çizgileri yok edildi).")

# 4. Kıyı Çizgisi Katmanı - Koyu antrasit ince kıyı hattı
if kiyi_cizgi_layer:
    kiyi_cizgi_layer.setName("Kıyı Çizgisi (SCAR ADD v7.11)")
    line_symbol = QgsLineSymbol.createSimple({
        'color': '#334155',
        'width': '0.26'
    })
    kiyi_cizgi_layer.renderer().setSymbol(line_symbol)
    kiyi_cizgi_layer.triggerRepaint()
    print("Kıyı çizgisi stili uygulandı.")

# 5. Noktalar Katmanı
if noktalar_layer:
    noktalar_layer.setName("Adélie Pengueni Gözlemleri (GBIF, N=67)")
    pt_sym = QgsMarkerSymbol.createSimple({
        'color': '#f59e0b',
        'outline_color': '#1e293b',
        'outline_width': '0.3',
        'size': '1.8'
    })
    noktalar_layer.renderer().setSymbol(pt_sym)
    noktalar_layer.triggerRepaint()

# 6. İstasyonlar Katmanı
if istasyonlar_layer:
    istasyonlar_layer.setName("Araştırma İstasyonları")
    ist_sym = QgsMarkerSymbol.createSimple({
        'name': 'triangle',
        'color': '#ef4444',
        'outline_color': '#7f1d1d',
        'outline_width': '0.4',
        'size': '3.2'
    })
    istasyonlar_layer.renderer().setSymbol(ist_sym)
    
    # Etiketler (name sütunu + beyaz tampon)
    text_format = QgsTextFormat()
    text_format.setSize(8)
    text_format.setColor(QColor("#0f172a"))
    buffer_settings = QgsTextBufferSettings()
    buffer_settings.setEnabled(True)
    buffer_settings.setSize(0.8)
    buffer_settings.setColor(QColor(255, 255, 255, 230))
    text_format.setBuffer(buffer_settings)
    
    from qgis.core import QgsPalLayerSettings
    settings = QgsPalLayerSettings()
    settings.fieldName = "name"
    settings.setFormat(text_format)
    istasyonlar_layer.setLabeling(QgsVectorLayerSimpleLabeling(settings))
    istasyonlar_layer.setLabelsEnabled(True)
    istasyonlar_layer.triggerRepaint()

# Projeyi kaydet
project.write()
print("Proje güncellendi ve kaydedildi.")

# 7. Baskı Düzenini (Layout) Export Et
layout_manager = project.layoutManager()
layout = layout_manager.layoutByName("harita_A4")
if not layout:
    layouts = layout_manager.layouts()
    if layouts:
        layout = layouts[0]

if layout:
    print(f"Layout '{layout.name()}' bulundu, render ediliyor...")
    
    # Lejantı güncelle
    for item in layout.items():
        if item.type() == 65642: # QgsLayoutItemLegend
            item.setAutoUpdateModel(True)
            item.setAutoUpdateModel(False)
            item.updateLegend()

    exporter = QgsLayoutExporter(layout)
    
    pdf_path = "/home/halil/adelie-maxent-2204c/harita_final_A4.pdf"
    png_path = "/home/halil/adelie-maxent-2204c/harita_final_A4.png"
    
    # PDF export
    pdf_settings = QgsLayoutExporter.PdfExportSettings()
    pdf_settings.dpi = 300
    res_pdf = exporter.exportToPdf(pdf_path, pdf_settings)
    print("PDF Export sonucu:", "Başarılı" if res_pdf == QgsLayoutExporter.Success else "Hata:", res_pdf)
    
    # Image export
    img_settings = QgsLayoutExporter.ImageExportSettings()
    img_settings.dpi = 300
    res_img = exporter.exportToImage(png_path, img_settings)
    print("PNG Export sonucu:", "Başarılı" if res_img == QgsLayoutExporter.Success else "Hata:", res_img)
else:
    print("Layout bulunamadı!")

qgs.exitQgis()
print("Tamamlandı.")
