import os
import sys
from qgis.core import (
    QgsLayoutItemLabel,
    QgsApplication,
    QgsProject,
    QgsRasterLayer,
    QgsVectorLayer,
    QgsColorRampShader,
    QgsRasterShader,
    QgsSingleBandPseudoColorRenderer,
    QgsLayoutExporter,
    QgsSimpleFillSymbolLayer,
    QgsSimpleLineSymbolLayer,
    QgsFillSymbol,
    QgsLineSymbol,
    QgsMarkerSymbol,
    QgsTextFormat,
    QgsTextBufferSettings,
    QgsPalLayerSettings,
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

# 2050 katmanı ve Değişim katmanı yolları
tif_2050 = "/home/halil/adelie-maxent-2204c/harita/uygunluk_2050_ssp245_3031.tif"
tif_fark = "/home/halil/adelie-maxent-2204c/harita/habitat_degisimi_2050_3031.tif"

layer_2050 = QgsRasterLayer(tif_2050, "Habitat Uygunluğu 2050 (SSP2-4.5)", "gdal")
layer_fark = QgsRasterLayer(tif_fark, "Habitat Değişimi (2050 vs Günümüz)", "gdal")

# 1. 2050 Katmanı Sembolojisi (5 Ayrık Sınıf)
if layer_2050.isValid():
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
    renderer_2050 = QgsSingleBandPseudoColorRenderer(layer_2050.dataProvider(), 1, shader)
    renderer_2050.setClassificationMin(0.0)
    renderer_2050.setClassificationMax(1.0)
    layer_2050.setRenderer(renderer_2050)
    project.addMapLayer(layer_2050)

# 2. Fark / Değişim Katmanı Sembolojisi (Kırmızı / Nötr / Yeşil)
if layer_fark.isValid():
    shader_f = QgsRasterShader()
    color_ramp_f = QgsColorRampShader()
    color_ramp_f.setColorRampType(QgsColorRampShader.Discrete)
    items_f = [
        QgsColorRampShader.ColorRampItem(-0.25, QColor(215, 25, 28, 240), "Şiddetli Habitat Kaybı (<-0.25)"),
        QgsColorRampShader.ColorRampItem(-0.05, QColor(253, 174, 97, 210), "Hafif Habitat Kaybı (-0.25 ile -0.05)"),
        QgsColorRampShader.ColorRampItem(0.05, QColor(241, 245, 249, 100), "Kararlı / Değişmeyen (±0.05)"),
        QgsColorRampShader.ColorRampItem(0.25, QColor(166, 217, 106, 220), "Hafif Habitat Artışı (+0.05 ile +0.25)"),
        QgsColorRampShader.ColorRampItem(1.00, QColor(26, 150, 65, 255), "Güçlü İklim Sığınağı / Refugia (>+0.25)")
    ]
    color_ramp_f.setColorRampItemList(items_f)
    shader_f.setRasterShaderFunction(color_ramp_f)
    renderer_fark = QgsSingleBandPseudoColorRenderer(layer_fark.dataProvider(), 1, shader_f)
    renderer_fark.setClassificationMin(-1.0)
    renderer_fark.setClassificationMax(1.0)
    layer_fark.setRenderer(renderer_fark)
    project.addMapLayer(layer_fark)

layout_manager = project.layoutManager()
layout = layout_manager.layoutByName("harita_A4")
if not layout and layout_manager.layouts():
    layout = layout_manager.layouts()[0]

exporter = QgsLayoutExporter(layout)

# 1. 2050 Haritasını Render Et (layer_2050 görünür, layer_fark gizli)
# Katman görünürlüklerini kontrol eden Map 1 öğesi
map_item = None
for item in layout.items():
    if item.type() == 65639: # Map
        map_item = item
        break

pdf_settings = QgsLayoutExporter.PdfExportSettings()
pdf_settings.dpi = 300
img_settings = QgsLayoutExporter.ImageExportSettings()
img_settings.dpi = 300

# Projedeki tüm rasterları bul
rasters = [l for l in project.mapLayers().values() if l.type() == l.RasterLayer]
vectors = [l for l in project.mapLayers().values() if l.type() == l.VectorLayer]

# A) 2050 HARİTASI
if map_item and layer_2050.isValid():
    # Sadece 2050 raster'ı ve vektörler
    map_item.setLayers([layer_2050] + vectors)
    for item in layout.items():
        if isinstance(item, QgsLayoutItemLabel):
            text = item.text()
            if "HABİTAT UYGUNLUK" in text:
                item.setText(text.replace("HABİTAT UYGUNLUK MODELİ", "2050 GELECEK HABİTAT PROJEKSİYONU (SSP2-4.5)"))
        if item.type() == 65642: # Legend
            item.setAutoUpdateModel(True)
            item.setAutoUpdateModel(False)
            item.updateLegend()
            
    out_2050_png = "/home/halil/adelie-maxent-2204c/harita_2050_A4.png"
    out_2050_pdf = "/home/halil/adelie-maxent-2204c/harita_2050_A4.pdf"
    exporter.exportToImage(out_2050_png, img_settings)
    exporter.exportToPdf(out_2050_pdf, pdf_settings)
    print("✔ harita_2050_A4 (300 DPI) üretildi.")

# B) FARK / DEĞİŞİM HARİTASI
if map_item and layer_fark.isValid():
    map_item.setLayers([layer_fark] + vectors)
    for item in layout.items():
        if isinstance(item, QgsLayoutItemLabel):
            text = item.text()
            item.setText("""ADÉLIE PENGUENİ (Pygoscelis adeliae)
İKLİM KRİZİ HABİTAT DEĞİŞİMİ (2050 vs GÜNÜMÜZ)
Bölge: Marguerite Körfezi, Antarktika Yarımadası
Senaryo: IPCC CMIP6 SSP2-4.5 (Orta Emisyon)

Değişim Analizi Bulguları:
• Habitat Kaybı / Daralma: %54.6 (384 hücre)
• Kararlı Alanlar: %26.5 (186 hücre)
• İklim Sığınağı (Refugia): %18.9 (133 hücre)

Projeksiyon: EPSG:3031 WGS 84 / Antarctic Polar Stereographic""")
        if item.type() == 65642: # Legend
            item.setAutoUpdateModel(True)
            item.setAutoUpdateModel(False)
            item.updateLegend()

    out_fark_png = "/home/halil/adelie-maxent-2204c/harita_degisim_A4.png"
    out_fark_pdf = "/home/halil/adelie-maxent-2204c/harita_degisim_A4.pdf"
    exporter.exportToImage(out_fark_png, img_settings)
    exporter.exportToPdf(out_fark_pdf, pdf_settings)
    print("✔ harita_degisim_A4 (300 DPI) üretildi.")

project.write()
qgs.exitQgis()
print("Tüm yüksek çözünürlüklü haritalar tamamlandı!")
