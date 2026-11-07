#!/usr/bin/env python3
"""Build isolated QGIS layouts from validated original-grid statistics.

Rendering interpolation is optional and never used for analysis. Original
QGIS project and original exports are not modified. Run with QT_QPA_PLATFORM=offscreen.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
os.environ.setdefault('QT_QPA_PLATFORM','offscreen')
from qgis.core import (
    QgsApplication,QgsProject,QgsRasterLayer,QgsVectorLayer,QgsPrintLayout,
    QgsLayoutItemMap,QgsLayoutItemLabel,QgsLayoutItemShape,QgsLayoutItemScaleBar,
    QgsLayoutPoint,QgsLayoutSize,QgsLayoutExporter,QgsCoordinateReferenceSystem,
    QgsLayoutItemPage,QgsLayoutMeasurement,
    QgsCoordinateTransform,QgsRectangle,QgsColorRampShader,QgsRasterShader,
    QgsSingleBandPseudoColorRenderer,QgsBilinearRasterResampler,QgsLineSymbol,
    QgsMarkerSymbol,QgsTextFormat,QgsTextBufferSettings,QgsPalLayerSettings,
    QgsVectorLayerSimpleLabeling,Qgis,QgsFillSymbol,QgsLayoutItemMapGrid)
from qgis.PyQt.QtGui import QColor,QFont
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'maxent'))
from izgara import read_grid,write_grid

ROOT=Path(__file__).resolve().parents[1]
ANALYSIS=ROOT/'maxent/cikti/duyarlilik_analizi_v1'
SUIT=[(0,'#313695'),(.2,'#4575b4'),(.4,'#abd9e9'),(.6,'#ffffbf'),(.8,'#fdae61'),(1,'#a50026')]
CHANGE=[(-.25,'#b2182b'),(-.05,'#ef8a62'),(.05,'#f7f7f7'),(.25,'#99d594'),(1,'#1b7837')]


def label(layout,ident,text,x,y,w,h,size=9,color='#23334a',bold=False):
    item=QgsLayoutItemLabel(layout);item.setId(ident);item.setText(text)
    item.setFont(QFont('DejaVu Sans',size,QFont.Weight.Bold if bold else QFont.Weight.Normal))
    item.setFontColor(QColor(color));item.setMargin(0)
    layout.addLayoutItem(item);item.attemptMove(QgsLayoutPoint(x,y));item.attemptResize(QgsLayoutSize(w,h))
    return item


def swatch(layout,ident,color,text,y):
    box=QgsLayoutItemShape(layout);box.setId(ident)
    box.setShapeType(QgsLayoutItemShape.Shape.Rectangle)
    box.setSymbol(QgsFillSymbol.createSimple({'color':color,'outline_color':'#ccd4dc','outline_width':'.1'}))
    layout.addLayoutItem(box);box.attemptMove(QgsLayoutPoint(212,y));box.attemptResize(QgsLayoutSize(5,3))
    label(layout,ident+'_label',text,220,y-1,64,7,8)


def raster(project,path,name,items,continuous=False,smooth=False):
    layer=QgsRasterLayer(str(path),name,'gdal')
    if not layer.isValid():raise RuntimeError(f'Invalid raster: {path}')
    if not layer.crs().isValid():layer.setCrs(QgsCoordinateReferenceSystem('EPSG:4326'))
    ramp=QgsColorRampShader();ramp.setColorRampType(
        QgsColorRampShader.Type.Interpolated if continuous else QgsColorRampShader.Type.Discrete)
    ramp.setColorRampItemList([QgsColorRampShader.ColorRampItem(v,QColor(c)) for v,c in items])
    shader=QgsRasterShader();shader.setRasterShaderFunction(ramp)
    layer.setRenderer(QgsSingleBandPseudoColorRenderer(layer.dataProvider(),1,shader))
    if smooth:
        layer.resampleFilter().setZoomedInResampler(QgsBilinearRasterResampler())
        layer.resampleFilter().setZoomedOutResampler(QgsBilinearRasterResampler())
    project.addMapLayer(layer)
    return layer


def vectors(project):
    gpkg=ROOT/'harita/qgis_katmanlari.gpkg'
    coast=QgsVectorLayer(f'{gpkg}|layername=kiyi_cizgi','Kıyı çizgisi (SCAR ADD v7.11)','ogr')
    points=QgsVectorLayer(f'{gpkg}|layername=noktalar','GBIF bulunuşları (67 nokta)','ogr')
    stations=QgsVectorLayer(f'{gpkg}|layername=istasyonlar','Referans konumlar','ogr')
    for l in [coast,points,stations]:
        if not l.isValid():raise RuntimeError('Invalid vector layer')
        project.addMapLayer(l)
    coast.renderer().setSymbol(QgsLineSymbol.createSimple({'line_color':'#334155','line_width':'.18'}))
    points.renderer().setSymbol(QgsMarkerSymbol.createSimple({'name':'circle','color':'#ffffff',
        'outline_color':'#152d46','outline_width':'.25','size':'1.6'}))
    stations.renderer().setSymbol(QgsMarkerSymbol.createSimple({'name':'triangle','color':'#132a45',
        'outline_color':'white','outline_width':'.2','size':'2.4'}))
    settings=QgsPalLayerSettings()
    settings.fieldName="CASE WHEN ad LIKE 'Horseshoe%' THEN 'Horseshoe' WHEN ad LIKE 'Rothera%' THEN 'Rothera' ELSE 'San Martín' END"
    settings.isExpression=True
    fmt=QgsTextFormat();fmt.setFont(QFont('DejaVu Sans'));fmt.setSize(7);fmt.setColor(QColor('#132a45'))
    buffer=QgsTextBufferSettings();buffer.setEnabled(True);buffer.setSize(.6);buffer.setColor(QColor('white'))
    fmt.setBuffer(buffer);settings.setFormat(fmt)
    stations.setLabeling(QgsVectorLayerSimpleLabeling(settings));stations.setLabelsEnabled(True)
    return [stations,points,coast]


def build(project,kind,output,metrics,smooth):
    real=metrics['scenario']['kind']=='cmip6_delta_projection'
    config={
        'gunumuz':('Günümüz çevresel uygunluğu','2000-2025 ERA5 referansı | Genel bulunuş modeli','gunumuz.asc',SUIT,True),
        'duyarlilik':('Varsayımsal çevre değişimi','Eski 2050 denemesinin düzeltilmiş sunumu | Gerçek CMIP6 projeksiyonu değildir','duyarlilik.asc',SUIT,True),
        'degisim':('Modellenen uygunluk değişimi','Varsayımsal deneme eksi günümüz | Habitat alanı kaybı değildir','uygunluk_farki.asc',CHANGE,False),
        'belirsizlik':('Projeksiyonun sınırları','Çevre aralığı dışına çıkma ve katlar arasında değişim yönü uyuşmazlığı','tanisal_sinif.asc',
            [(0,'#eef2f6'),(1,'#9467bd'),(2,'#e6ab02'),(3,'#33394c')],False)
    }
    if real:
        config['duyarlilik']=('2050 çevresel uygunluğu',
            'IPSL-CM6A-LR / r1i1p1f1 | SSP2-4.5 | 2041-2060 | Tek GCM, deneysel model aktarımı',
            'duyarlilik.asc',SUIT,True)
        config['degisim']=('2050 için uygunluk değişimi',
            'CMIP6 tek-model projeksiyonu eksi günümüz | Habitat alanı kaybı değildir',
            'uygunluk_farki.asc',CHANGE,False)
    title,subtitle,filename,palette,continuous=config[kind]
    grid,_=read_grid(ANALYSIS/'gunumuz.asc')
    source=ANALYSIS/filename
    if smooth and continuous:
        # Display-only warp: interpolate numeric scores before coloring. Never
        # feed this 1 km display grid into model fitting or change statistics.
        from osgeo import gdal
        gdal.UseExceptions()
        display=output/f'{kind}_yalniz_gosterim_1km.tif'
        ds=gdal.Warp(str(display),str(source),srcSRS='EPSG:4326',dstSRS='EPSG:3031',
                     xRes=1000,yRes=1000,resampleAlg='bilinear',srcNodata=-9999,
                     dstNodata=-9999,creationOptions=['COMPRESS=DEFLATE'])
        if ds is None:raise RuntimeError('Display-only interpolation failed')
        ds=None;source=display
    layer=raster(project,source,title,palette,continuous,smooth and continuous)
    overlays=vectors(project)
    layout=QgsPrintLayout(project);layout.initializeDefaults();layout.setName(kind)
    layout.pageCollection().pages()[0].setPageSize('A4',QgsLayoutItemPage.Orientation.Landscape)
    project.layoutManager().addLayout(layout)
    label(layout,'eyebrow','TÜBİTAK 2204-C  /  MARGUERITE KÖRFEZİ',12,7,273,6,8,'#51708d',True)
    label(layout,'title',title,12,15,273,12,20,'#152d46',True)
    label(layout,'subtitle',subtitle,12,29,273,8,8)
    map_item=QgsLayoutItemMap(layout);map_item.setId('main_map');layout.addLayoutItem(map_item)
    map_item.attemptMove(QgsLayoutPoint(16,43));map_item.attemptResize(QgsLayoutSize(183,141))
    crs=QgsCoordinateReferenceSystem('EPSG:3031');map_item.setCrs(crs)
    map_item.setLayers(overlays+[layer]);map_item.setKeepLayerSet(True)
    transform=QgsCoordinateTransform(QgsCoordinateReferenceSystem('EPSG:4326'),crs,project)
    extent=transform.transformBoundingBox(QgsRectangle(*grid.extent));extent.scale(1.025)
    map_item.zoomToExtent(extent);map_item.setFrameEnabled(True)
    map_item.setFrameStrokeColor(QColor('#9babb9'));map_item.setFrameStrokeWidth(QgsLayoutMeasurement(.2))
    graticule=map_item.grid();graticule.setEnabled(True)
    graticule.setCrs(QgsCoordinateReferenceSystem('EPSG:4326'))
    graticule.setIntervalX(2);graticule.setIntervalY(1)
    graticule.setLineSymbol(QgsLineSymbol.createSimple({'line_color':'120,140,160,100','line_width':'.1','line_style':'dash'}))
    graticule.setAnnotationEnabled(True);graticule.setAnnotationFormat(QgsLayoutItemMapGrid.AnnotationFormat.DecimalWithSuffix)
    graticule.setAnnotationFont(QFont('DejaVu Sans',7));graticule.setAnnotationPrecision(0)
    graticule.setAnnotationFrameDistance(1.2)
    for side in [QgsLayoutItemMapGrid.BorderSide.Top,QgsLayoutItemMapGrid.BorderSide.Right]:
        graticule.setAnnotationDisplay(QgsLayoutItemMapGrid.DisplayMode.HideAll,side)
    graticule.setAnnotationDisplay(QgsLayoutItemMapGrid.DisplayMode.LatitudeOnly,QgsLayoutItemMapGrid.BorderSide.Left)
    graticule.setAnnotationDisplay(QgsLayoutItemMapGrid.DisplayMode.LongitudeOnly,QgsLayoutItemMapGrid.BorderSide.Bottom)
    label(layout,'species','Adélie pengueni\nPygoscelis adeliae',212,42,72,15,10,'#152d46',True)
    label(layout,'legend_title','GÖSTERİM',212,62,72,7,8,'#51708d',True)
    if continuous:
        for i,(v,c) in enumerate(SUIT):swatch(layout,f'legend_{i}',c,f'{v:.1f}  uygunluk puanı',73+i*7)
        note='Cloglog ölçeği: 0-1\nYüksek puan, gözlenmiş koloni\nveya nüfus büyüklüğü değildir.'
        if real:note+='\nMekânsal doğrulama zayıf;\nsonuçlar keşif amaçlıdır.'
        label(layout,'model_note',note,212,119,74,30,8)
    elif kind=='degisim':
        for i,((v,c),text) in enumerate(zip(CHANGE,['< -0,25','-0,25 ile -0,05','-0,05 ile +0,05','+0,05 ile +0,25','> +0,25'])):
            swatch(layout,f'legend_{i}',c,text,73+i*7)
        s=metrics['by_difference_threshold']['0.05']
        label(layout,'change_stats',f"Hücre payları (eşik ±0,05):\nAzalma: %{s['azalma']['cell_percent']:.1f}\nKararlı: %{s['kararli']['cell_percent']:.1f}\nArtış: %{s['artis']['cell_percent']:.1f}\nPayda: {metrics['valid_cells']} model hücresi",212,114,74,30,8)
    else:
        for i,((v,c),text) in enumerate(zip(palette,['İki uyarı da yok','Ekstrapolasyon','Değişim yönü belirsiz','Her iki uyarı birlikte'])):
            swatch(layout,f'legend_{i}',c,text,73+i*8)
        label(layout,'uncertainty_stats',f"Ekstrapolasyon: {metrics['novel_any_fold_cells']} / {metrics['valid_cells']}\nYön uyuşmazlığı: {metrics['sign_disagreement_cells']} / {metrics['valid_cells']}\n10 eşlenik model katı\nİklim modeli ensemble'ı değildir.",212,113,74,27,8)
    label(layout,'observations','○ GBIF bulunuş kaydı\n▲ Referans konum\n— SCAR ADD kıyı çizgisi',212,151,74,20,8)
    label(layout,'grid_info','Kaynak ızgara: 0,25° (37 × 19)\nGösterim: EPSG:3031\n'+('Görsel bilinear enterpolasyon\nAnaliz özgün hücrelerden yapılır.' if smooth and continuous else 'Hücre/sınıf sınırları korunur.'),212,176,75,24,7)
    bar=QgsLayoutItemScaleBar(layout);bar.setId('scale');bar.setStyle('Single Box');bar.setLinkedMap(map_item)
    bar.applyDefaultSize();bar.setUnits(Qgis.DistanceUnit.Kilometers);bar.setUnitsPerSegment(50)
    bar.setNumberOfSegments(2);bar.setNumberOfSegmentsLeft(0);bar.setUnitLabel('km')
    bar.setFont(QFont('DejaVu Sans',7));layout.addLayoutItem(bar);bar.attemptMove(QgsLayoutPoint(19,187))
    foot='Kaynak: GBIF • ERA5 2000-2025 • SCAR ADD v7.11 • MaxEnt 3.4.4\n'
    if real:
        foot+='IPSL-CM6A-LR SSP2-4.5, 2041-2060: kaynaklı aylık delta yöntemi. Eski modelin mekânsal aktarımı zayıf; nihai biyolojik sonuç değildir.'
    elif kind=='gunumuz':
        foot+='Bölgesel çevresel uygunluk; koloni ölçeğinde tahmin değildir. Bağımsız mekânsal değerlendirme ve alan seçimi sınırlılıkları geçerlidir.'
    else:
        foot+='Değişim denemesi: SST +0,8°C; deniz buzu ×0,80; BIO18 ×1,15; kaya sabit. Bölgesel uygunluk; koloni ölçeğinde tahmin değildir.'
    label(layout,'footnote',foot,12,199,273,9,6)
    exporter=QgsLayoutExporter(layout)
    image_settings=QgsLayoutExporter.ImageExportSettings();image_settings.dpi=300
    pdf_settings=QgsLayoutExporter.PdfExportSettings();pdf_settings.dpi=300
    for suffix,func,settings in [('png',exporter.exportToImage,image_settings),('pdf',exporter.exportToPdf,pdf_settings)]:
        name='2050' if real and kind=='duyarlilik' else kind
        path=output/f'{name}_A4.{suffix}'
        result=func(str(path),settings)
        if result!=QgsLayoutExporter.ExportResult.Success:raise RuntimeError(f'Export failed: {path}: {result}')
    print('Exported',kind,flush=True)


def main(default_kinds=None):
    global ANALYSIS
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    parser.add_argument('--analysis-dir',type=Path,default=ANALYSIS)
    parser.add_argument('--smooth-display',action='store_true')
    parser.add_argument('--kinds',nargs='+',choices=['gunumuz','duyarlilik','degisim','belirsizlik'],
                        default=default_kinds or ['gunumuz','duyarlilik','degisim','belirsizlik'])
    args=parser.parse_args();ANALYSIS=args.analysis_dir.resolve()
    metrics=json.loads((ANALYSIS/'ozet.json').read_text())
    real=metrics['scenario']['kind']=='cmip6_delta_projection'
    if args.output is None:args.output=ROOT/('harita/cmip6_ipsl_2050_v1' if real else 'harita/duzeltilmis_v1')
    args.output.mkdir(parents=True,exist_ok=True)
    g,novel=read_grid(ANALYSIS/'ekstrapolasyon.asc');_,sign=read_grid(ANALYSIS/'isaret_belirsiz.asc')
    # Rendering is read-only with respect to analytical products/manifests.
    _,diagnostic=read_grid(ANALYSIS/'tanisal_sinif.asc')
    import numpy as np
    if not np.array_equal(diagnostic,novel+2*sign):raise ValueError('Diagnostic classes disagree')
    app=QgsApplication([],False);app.initQgis()
    original=ROOT/'harita/a1.qgz';before=hashlib.sha256(original.read_bytes()).hexdigest()
    for kind in args.kinds:
        project=QgsProject();build(project,kind,args.output,metrics,args.smooth_display)
        project.setFileName(str(args.output/f'{kind}.qgz'))
        if not project.write():raise RuntimeError('Could not save isolated QGIS project')
        project.clear()
    if hashlib.sha256(original.read_bytes()).hexdigest()!=before:raise RuntimeError('Original project changed')
    manifest={'original_project_sha256':before,'source_resolution_degrees':.25,
              'display_interpolation':'bilinear for continuous suitability only' if args.smooth_display else 'nearest',
              'statistics':str((ANALYSIS/'ozet.json').relative_to(ROOT)),
              'analytical_manifest_sha256':hashlib.sha256((ANALYSIS/'manifest.json').read_bytes()).hexdigest(),
              'vector_source_sha256':hashlib.sha256((ROOT/'harita/qgis_katmanlari.gpkg').read_bytes()).hexdigest(),
              'qgis_version':Qgis.QGIS_VERSION,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'output_files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(args.output.iterdir())
                              if p.is_file() and p.name!='manifest.json'}}
    (args.output/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    # Qt/QGIS objects must be destroyed before application shutdown.
    del project
    app.exitQgis()


if __name__=='__main__':
    from qgis.core import QgsLayoutItemPage,QgsLayoutMeasurement
    main()
