import os
import sys
import subprocess
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Fontları kaydet
F = '/usr/share/fonts/TTF/'
pdfmetrics.registerFont(TTFont('Roboto', F + 'Roboto-Regular.ttf'))
pdfmetrics.registerFont(TTFont('Roboto-Bold', F + 'Roboto-Bold.ttf'))
pdfmetrics.registerFont(TTFont('Roboto-Italic', F + 'Roboto-Italic.ttf'))
pdfmetrics.registerFont(TTFont('Roboto-BoldItalic', F + 'Roboto-BoldItalic.ttf'))
pdfmetrics.registerFontFamily('Roboto', normal='Roboto', bold='Roboto-Bold', italic='Roboto-Italic', boldItalic='Roboto-BoldItalic')

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Roboto", 8)
        self.setFillColor(colors.HexColor("#475569"))
        
        # Üst bilgi (Header)
        self.drawString(45, 804, "TÜBİTAK 2204-C Kutup Araştırmaları Proje Yarışması | Proje Raporu")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(45, 798, 550, 798)
        
        # Alt bilgi (Footer)
        page_text = f"Sayfa {self._pageNumber} / {page_count}"
        self.drawRightString(550, 26, page_text)
        self.drawString(45, 26, "Marguerite Körfezi'nde Adélie Pengueni MaxEnt Ekolojik Niş Modellemesi ve CMIP6 İklim Projeksiyonu")
        self.line(45, 36, 550, 36)
        self.restoreState()

def build_report():
    out_dir = "/home/halil/adelie-maxent-2204c/rapor"
    raw_pdf = os.path.join(out_dir, "TUBITAK_2204C_PROJE_RAPORU_raw.pdf")
    final_pdf = os.path.join(out_dir, "TUBITAK_2204C_PROJE_RAPORU.pdf")
    out_md = os.path.join(out_dir, "TUBITAK_2204C_PROJE_RAPORU.md")

    doc = SimpleDocTemplate(
        raw_pdf,
        pagesize=A4,
        leftMargin=45,
        rightMargin=45,
        topMargin=52,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()

    # Özel renk paleti
    C_PRIMARY = colors.HexColor("#0F172A")    # Çok koyu lacivert
    C_SECONDARY = colors.HexColor("#1E3A8A")  # Derin mavi
    C_TEXT = colors.HexColor("#1E293B")       # Okunabilir gövde metni
    C_MUTED = colors.HexColor("#475569")      # Açıklama gri
    C_BORDER = colors.HexColor("#CBD5E1")     # Çerçeve
    C_HEADER_BG = colors.HexColor("#F1F5F9")  # Tablo başlık

    title_style = ParagraphStyle('RepTitle', fontName='Roboto-Bold', fontSize=13, leading=17, textColor=C_PRIMARY, alignment=TA_CENTER)
    sec_head = ParagraphStyle('SecHead', fontName='Roboto-Bold', fontSize=12, leading=16, textColor=C_PRIMARY, spaceBefore=12, spaceAfter=5)
    subsec_head = ParagraphStyle('SubSecHead', fontName='Roboto-Bold', fontSize=10.5, leading=14.5, textColor=C_SECONDARY, spaceBefore=9, spaceAfter=4)
    subsubsec_head = ParagraphStyle('SubSubSecHead', fontName='Roboto-Bold', fontSize=9.5, leading=13.5, textColor=C_PRIMARY, spaceBefore=7, spaceAfter=3)
    body = ParagraphStyle('RepBody', fontName='Roboto', fontSize=9.5, leading=13.8, textColor=C_TEXT, spaceAfter=5, alignment=TA_JUSTIFY)
    body_bold = ParagraphStyle('RepBodyBold', fontName='Roboto-Bold', fontSize=9.5, leading=13.8, textColor=C_PRIMARY, spaceAfter=5, alignment=TA_JUSTIFY)
    bullet = ParagraphStyle('RepBullet', fontName='Roboto', fontSize=9.5, leading=13.8, textColor=C_TEXT, leftIndent=14, firstLineIndent=-9, spaceAfter=3.5, alignment=TA_JUSTIFY)
    caption = ParagraphStyle('RepCap', fontName='Roboto-Italic', fontSize=8, leading=11, textColor=C_MUTED, alignment=TA_CENTER, spaceBefore=4, spaceAfter=7)
    ref_style = ParagraphStyle('RepRef', fontName='Roboto', fontSize=7.2, leading=9.8, textColor=C_TEXT, leftIndent=14, firstLineIndent=-14, spaceAfter=2.5, alignment=TA_LEFT)

    table_cell = ParagraphStyle('TC', fontName='Roboto', fontSize=8, leading=10.5, textColor=C_TEXT)
    table_cell_c = ParagraphStyle('TCC', fontName='Roboto', fontSize=8, leading=10.5, textColor=C_TEXT, alignment=TA_CENTER)
    table_cell_b = ParagraphStyle('TCB', fontName='Roboto-Bold', fontSize=8, leading=10.5, textColor=C_PRIMARY)
    table_cell_cb = ParagraphStyle('TCCB', fontName='Roboto-Bold', fontSize=8, leading=10.5, textColor=C_PRIMARY, alignment=TA_CENTER)

    story = []
    md_content = []

    def add_p(text, style=body, md_prefix=""):
        story.append(Paragraph(text, style))
        clean_text = text.replace("<b>", "**").replace("</b>", "**").replace("<i>", "*").replace("</i>", "*")
        if style == title_style:
            md_content.append(f"# {clean_text}\n")
        elif style == sec_head:
            md_content.append(f"\n# {clean_text}\n")
        elif style == subsec_head:
            md_content.append(f"\n## {clean_text}\n")
        elif style == subsubsec_head:
            md_content.append(f"\n### {clean_text}\n")
        elif style == bullet:
            md_content.append(f"- {clean_text}\n")
        elif style == caption:
            md_content.append(f"\n*{clean_text}*\n")
        elif style == ref_style:
            md_content.append(f"{clean_text}\n")
        else:
            md_content.append(f"{clean_text}\n")

    # =========================================================================
    # SAYFA 1: BAŞLIK, ÖZET, ANAHTAR KELİMELER
    # =========================================================================
    meta_table_data = [
        [Paragraph("<b>Proje Ana Alanı</b>", table_cell_b), Paragraph(": Kutup Araştırmaları (Biyoloji ve Ekoloji)", table_cell)],
        [Paragraph("<b>Proje Tematik Alanı</b>", table_cell_b), Paragraph(": Kutup Biyoçeşitliliği ve Ekosistem Dinamikleri", table_cell)],
        [Paragraph("<b>Proje Adı (Başlığı)</b>", table_cell_b), Paragraph(": <b>MaxEnt Algoritması ve CMIP6 İklim Senaryoları Kullanılarak Marguerite Körfezi'nde (Batı Antarktika) Adélie Pengueni (<i>Pygoscelis adeliae</i>) Potansiyel Habitat Uygunluğunun ve İklim Sığınaklarının Modellenmesi</b>", table_cell)]
    ]
    t_meta = Table(meta_table_data, colWidths=[120, 385])
    t_meta.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=1, color=C_SECONDARY, spaceBefore=2, spaceAfter=5))

    md_content.append("# TÜBİTAK 2204-C KUTUP ARAŞTIRMALARI PROJE RAPORU\n\n")
    md_content.append("**Proje Ana Alanı:** Kutup Araştırmaları (Biyoloji ve Ekoloji)\n")
    md_content.append("**Proje Tematik Alanı:** Kutup Biyoçeşitliliği ve Ekosistem Dinamikleri\n")
    md_content.append("**Proje Adı:** MaxEnt Algoritması ve CMIP6 İklim Senaryoları Kullanılarak Marguerite Körfezi'nde (Batı Antarktika) Adélie Pengueni (*Pygoscelis adeliae*) Potansiyel Habitat Uygunluğunun ve İklim Sığınaklarının Modellenmesi\n\n---\n\n")

    add_p("Özet", sec_head)
    add_p("Antarktika Yarımadası, son elli yılda küresel ortalamanın üç katını aşan sıcaklık artışıyla gezegenin iklim değişikliğine en duyarlı denizel ve karasal ekosistemlerinden birine ev sahipliği yapmaktadır. Bu çalışmada, deniz buzu zorunlu (sea-ice obligate) tepe avcı ve iklim değişikliği biyo-indikatörü olan Adélie pengueninin (<i>Pygoscelis adeliae</i>), Batı Antarktika Yarımadası'ndaki (WAP) kritik üreme ve beslenme sahası Marguerite Körfezi'ndeki (66°–70°G, 65°–74°B) potansiyel habitat uygunluğu ve iklim sığınakları modellenmiştir. Çalışmada, GBIF ve SCAR biyo-çeşitlilik veri tabanlarından temin edilen 2000–2026 dönemine ait 67 adet bağımsız mekânsal koordinat verisi, 0.25° (~25 km) grid ölçeğinde mekânsal inceltme (spatial thinning) uygulanarak örnekleme yanlılığından arındırılmıştır. Çevresel katman olarak ECMWF ERA5 atmosferik/denizel yeniden analizlerinden elde edilen yıllık deniz buzu konsantrasyonu (<i>buz_yillik</i>), deniz yüzeyi sıcaklığı (<i>sst_yillik</i>), en sıcak çeyrek yağış miktarı (<i>bio18</i>) ve REMA yüksek çözünürlüklü sayısal yükseklik modelinden türetilen çıplak kaya yüzdesi (<i>kaya</i>) değişkenleri kullanılmıştır.")
    add_p("Ekolojik niş modellemesi, bağımsız makine öğrenimi tabanlı Maksimum Entropi (MaxEnt 3.4.4) algoritması ve 10 katlı çapraz doğrulama (10-fold cross-validation) tasarımıyla yürütülmüştür. Model, test verileri üzerinde <b>0.768 ± 0.111</b> Alıcı İşletim Karakteristiği (ROC) Eğri Altındaki Alan (AUC) değerine ve eğitim verilerinde <b>0.838</b> AUC değerine ulaşarak yüksek doğrulukta simülasyon başarısı sergilemiştir. Değişken katkı analizleri sonucunda modelin en baskın belirleyicisinin <b>%55.6</b> permütasyon önemi ile yıllık deniz buzu konsantrasyonu olduğu, bunu sırasıyla deniz yüzeyi sıcaklığı (<b>%18.3</b>), en sıcak çeyrek yağış miktarı (<b>%17.1</b>) ve çıplak kaya alanının (<b>%9.1</b>) izlediği saptanmıştır. Çevresel tepki eğrileri, türün en yüksek uygunluğa %40–%60 deniz buzu konsantrasyonunda, -1.8°C ile -1.2°C deniz yüzeyi sıcaklığında ve 100–250 mm aralığındaki düşük yaz yağışlarında ulaştığını; 300 mm üzerindeki sıvı yağışlarda ve -0.5°C üzerindeki deniz sıcaklıklarında habitat uygunluğunun sıfırlandığını kanıtlamıştır.")
    add_p("CMIP6 IPSL-CM6A-LR SSP2-4.5 (orta derece emisyon senaryosu, 2041–2060 dönemi) iklim projeksiyonu altında yapılan mekânsal değişim analizi, Marguerite Körfezi'ndeki 703 grid hücresinin <b>297 adedinde (%42.2 / 89.155 km²)</b> net çevresel uygunluk kaybı yaşanacağını, <b>163 adedinde (%23.2 / 45.066 km²)</b> habitatın kararlı kalacağını, <b>243 adedinde (%34.6 / 68.460 km²)</b> ise iklimsel sığınak (refugia) oluşacağını ortaya koymuştur. Uygunluk kayıplarının körfezin kuzey açıklarında ve Adelaide Adası kıyılarında yoğunlaştığı, potansiyel sığınakların ise daha korunaklı güney fiyortlarına ve George VI Boğazı girişine doğru kaydığı tespit edilmiştir. Roberts vd. (2017) protokolüne dayalı 4 enlem bandı mekânsal blok çapraz doğrulaması (Spatial Block CV), rastgele kat tasarımının AUC'yi +0.135 ila +0.288 puan aşırı iyimser tahmin ettiğini ortaya koyarak yerel kutup modellerinde mekânsal otokorelasyon denetiminin hayati zorunluluğunu belgelemiştir. Elde edilen bulgular, Türkiye'nin Ulusal Antarktika Bilim Seferleri (TAE) kapsamında yürütülecek koruma ve saha izleme stratejilerine doğrudan sayısal veri tabanı sunmaktadır.")
    add_p("<b>Anahtar Kelimeler:</b> Adélie Pengueni (<i>Pygoscelis adeliae</i>), MaxEnt Algoritması, Marguerite Körfezi, CMIP6 SSP2-4.5, İklim Değişikliği, Mekânsal Çapraz Doğrulama, İklim Sığınağı (Refugia).", body_bold)

    story.append(PageBreak())

    # =========================================================================
    # SAYFA 2: AMAÇ VE GİRİŞ BAŞLANGICI
    # =========================================================================
    add_p("Amaç", sec_head)
    add_p("Bu projenin temel amacı; küresel iklim krizine bağlı olarak son elli yılda gezegenin en şiddetli atmosferik ve oşinografik ısınma süreçlerinden birine maruz kalan Batı Antarktika Yarımadası'ndaki (WAP) Marguerite Körfezi'nde, deniz buzu dinamiklerine sıkı sıkıya bağımlı tepe indikatör tür olan Adélie pengueninin (<i>Pygoscelis adeliae</i>) günümüz (2000–2026) potansiyel habitat uygunluğunu makine öğrenimi tabanlı Maksimum Entropi (MaxEnt 3.4.4) algoritmasıyla modellemek; CMIP6 IPSL-CM6A-LR SSP2-4.5 (2041–2060) iklim senaryosu altında türün coğrafi dağılımındaki daralma, kararlılık ve genişleme eğilimlerini niceliksel olarak tespit etmek; iklim sığınağı (refugia) potansiyeli taşıyan denizel ve kıyısal koridorları haritalandırmak ve model aktarılabilirliğini mekânsal blok çapraz doğrulama yöntemiyle test etmektir.")
    add_p("Bu genel amaç doğrultusunda şu özel hedefler gerçekleştirilmiştir:", body_bold)
    add_p("1. GBIF ve SCAR açık kaynak biyo-çeşitlilik veri tabanlarından Marguerite Körfezi'ne ait 2000–2026 dönemini kapsayan Adélie pengueni gözlem ve koloni koordinat verilerini derlemek; 0.25° grid ölçeğinde mekânsal inceltme (spatial thinning) uygulayarak örnekleme yanlılığı (sampling bias) barındırmayan 67 adet bağımsız varlık hücresi elde etmek.", bullet)
    add_p("2. ECMWF ERA5 atmosferik/denizel yeniden analizlerinden ve REMA sayısal yükseklik modellerinden türetilen oşinografik (deniz buzu konsantrasyonu, deniz yüzeyi sıcaklığı), atmosferik (en sıcak çeyrek yağış miktarı / kar-yağmur ayrımı) ve topografik (çıplak kaya yüzdesi) çevresel katmanları 0.25° mekânsal çözünürlükte ve EPSG:3031 Kutup Stereografik projeksiyonunda standartlaştırmak.", bullet)
    add_p("3. Çoklu eşdoğrusallık (multicollinearity) ve Varyans Şişme Faktörü (VIF) analizi uygulayarak Pearson korelasyon katsayısı |r| ≥ 0.70 olan değişkenleri elemek ve biyolojik olarak en anlamlı bağımsız 4 çevresel parametreyi seçmek.", bullet)
    add_p("4. 10 katlı çapraz doğrulama (10-fold cross-validation) ile eğitilen MaxEnt modelinde Alıcı İşletim Karakteristiği (ROC) Eğri Altındaki Alan (AUC), Jackknife tekil kazanç testleri ve yanıt eğrileri (response curves) üzerinden türün kritik biyolojik tolerans eşiklerini nicelendirmek.", bullet)
    add_p("5. Roberts vd. (2017) yöntemine dayalı 4 enlem bandı mekânsal blok çapraz doğrulama (Spatial Block CV) tasarımıyla modelin Tobler Coğrafya Kanunu çerçevesinde otokorelasyondan kaynaklanan aşırı öğrenme (overfitting) hassasiyetini denetlemek.", bullet)
    add_p("6. IPCC 6. Değerlendirme Raporu (AR6) kapsamında IPSL-CM6A-LR Yer Sistemi Modeli'nin SSP2-4.5 (2041–2060 dönemi / 2050 ufku) senaryosunu uygulayarak piksel bazında delta değişimi (Δ = Gelecek − Günümüz), Çok Değişkenli Çevresel Benzerlik Yüzeyi (MESS / Clamping) belirsizlik analizlerini gerçekleştirmek ve Türkiye'nin Ulusal Antarktika Bilim Seferleri (TAE) için bilimsel koruma stratejileri geliştirmek.", bullet)

    add_p("Giriş", sec_head)
    add_p("Antarktika kıtası ve onu çevreleyen Güney Okyanusu, küresel termohalin sirkülasyonu düzenleyen, gezegenin ısı bütçesini dengeleyen ve yüksek oranda endemik biyolojik çeşitliliğe ev sahipliği yapan hayati bir ekosistemdir (IPCC, 2021). Güney Okyanusu'nun en dinamik denizel bölgelerinden biri olan Batı Antarktika Yarımadası (WAP), 20. yüzyılın ikinci yarısından itibaren küresel ortalamanın neredeyse üç katına ulaşan (yaklaşık +3°C) olağanüstü bir atmosferik ısınma sürecine sahne olmuştur (Turner vd., 2014, 2016; Rignot vd., 2019). Bu hızlı ısınma rejimi; kış deniz buzu mevsimsel süresinin son kırk yılda 80 günden fazla kısalmasına, kıyı buz sahanlıklarının parçalanarak geri çekilmesine ve denizel birincil üretimin temelini oluşturan deniz buzu algleri ile Antarktika krili (<i>Euphausia superba</i>) biyokütlesinde ciddi düşüşlere yol açmıştır (Stammerjohn vd., 2008, 2012; Atkinson vd., 2004; Ducklow vd., 2007).")

    story.append(PageBreak())

    # =========================================================================
    # SAYFA 3: GİRİŞ DEVAMI VE LİTERATÜR SENTEZİ
    # =========================================================================
    add_p("Denizel besin ağının en üst basamaklarında yer alan ponpon kuyruklu kutup penguenleri (<i>Pygoscelis</i> cinsi), fiziksel çevre koşullarındaki değişimlere karşı son derece duyarlı tepe indikatör türlerdir (Ainley, 2002; Fraser & Hofmann, 2003). Bu cins içerisinde Adélie pengueni (<i>Pygoscelis adeliae</i>), morfolojik, fizyolojik ve davranışsal özellikleri bakımından tüm yaşam döngüsünü deniz buzuna endekslemiş gerçek bir 'deniz buzu zorunlu' (sea-ice obligate) penguen türüdür (Ainley, 2002). Adélie penguenleri; kış aylarında açık denizdeki paket buz (pack-ice) üzerinde dinlenmekte ve tüy dökmekte, ilkbahar ve yaz aylarında ise kıyı şeridindeki çıplak kaya zeminlerde koloni kurarak çakıl taşlarından inşa ettikleri yuvalarda kuluçkaya yatmaktadır (Ainley, 2002; Fretwell vd., 2014; Lyver vd., 2014). Beslenme rejiminin %80'den fazlasını oluşturan Antarktika krili, larva ve jüvenil evrelerini kış deniz buzunun alt yüzeyindeki mikroalgleri otlayarak geçirdiğinden, deniz buzu örtüsündeki en ufak bir zamansal veya alansal daralma, penguenlerin kuluçka dönemindeki dalış menzilini ve besin teminini doğrudan felce uğratmaktadır (Fraser & Hofmann, 2003; Atkinson vd., 2004; Trivelpiece vd., 2011).")
    add_p("İklim krizinin Batı Antarktika Yarımadası'ndaki etkileri yalnızca deniz buzu erimesiyle sınırlı kalmamaktadır. Isınan atmosferin nem taşıma kapasitesinin artması neticesinde, tarihsel olarak kuru ve dondurucu olan kutup ortamında aşırı yağış anomalileri, sıvı yağmur fırtınaları ve ıslak kar birikintileri gözlenmeye başlanmıştır (IPCC, 2021; Massom vd., 2006). Kuluçkadan yeni çıkan Adélie yavruları, henüz su geçirmez yetişkin tüylerine sahip olmayıp yalnızca ısı yalıtımı sağlayan narin hav tüyleri (down feathers) ile kaplıdır. Sıvı yağmur veya ıslak kar birikintileri altında kalan yavruların tüyleri ıslandığında yalıtım özelliğini tamamen yitirmekte; dondurucu rüzgar altında şiddetli hipotermiye girerek kitleler halinde telef olmaktadır (Chapman vd., 2011). Ayrıca yuvaların çamur ve eriyik kar sularıyla dolması yumurtaların boğulmasına yol açmaktadır (Chapman vd., 2011).")
    add_p("Türlerin coğrafi dağılım sınırlarını ve iklim değişikliği karşısındaki kırılganlıklarını anlamak amacıyla Ekolojik Niş Modelleri (ENM) ve Tür Dağılım Modelleri (SDM) yaygın olarak kullanılmaktadır (Elith vd., 2011; Phillips vd., 2006). Makine öğrenimi tabanlı Maksimum Entropi (MaxEnt) algoritması; yalnızca varlık (presence-only) verileriyle çalışabilmesi, arka plan (background) çevresel rastgeleliği başarıyla modellemesi, doğrusal olmayan karmaşık ilişkileri ve etkileşimleri yakalayabilmesi sayesinde ekoloji literatüründe altın standart olarak kabul görmektedir (Phillips vd., 2006; Elith vd., 2011).")
    add_p("Uluslararası saygın literatür incelendiğinde; <b>Wang, Hu ve Yang (Mart 2026, PMID: 42209243 - <i>Ying Yong Sheng Tai Xue Bao / The Journal of Applied Ecology</i>)</b> tarafından yayınlanan en güncel çalışmada, MaxEnt ve CMIP6 iklim modelleri kullanılarak tüm Antarktika kıtası ölçeğinde Adélie pengueninin potansiyel dağılımı modellenmiştir. Yazarlar, deniz buzu ve deniz yüzeyi sıcaklığının türün dağılımını belirleyen en kritik faktörler olduğunu, gelecekte alt-Antarktika ve Kuzey Yarımada kolonilerinde şiddetli daralmalar yaşanırken Doğu Antarktika'daki sığınakların korunacağını bildirmişlerdir (Wang vd., 2026). Benzer şekilde, <b>Cimino, Lynch, Saba ve Oliver (2016 - <i>Scientific Reports</i>)</b>, Antarktika Yarımadası'ndaki Adélie pengueni kolonilerinin yaklaşık %60'ının yüzyıl sonuna kadar iklim ısınması nedeniyle yok olma riskiyle karşı karşıya kalacağını matematiksel modellerle öngörmüşlerdir.")
    add_p("Ancak, kıtasal veya yarımada ölçeğindeki bu makro araştırmalar (Wang vd., 2026; Cimino vd., 2016); fiyort morfolojileri, ada topoğrafyaları, yerel polinya (açık su alanı) dinamikleri ve mikroklimatik çıplak kaya dağılımı gibi yerel ekolojik parametreleri kaba grid hücreleri nedeniyle yakalayamamaktadır. Dahası, ekolojik modelleme literatüründe sıkça göz ardı edilen mekânsal otokorelasyon sorunu (Tobler'in Coğrafya Kanunu), eğitim ve test verilerinin birbirine coğrafi olarak çok yakın seçilmesi durumunda model performans metriklerinin (AUC) yapay olarak şişmesine (overfitting) yol açmaktadır (Roberts vd., 2017; Dormann vd., 2013).")
    add_p("Bu araştırma; Batı Antarktika Yarımadası'nın en kritik biyolojik geçiş eşiği olan Marguerite Körfezi'ne odaklanarak literatürdeki bu temel bilimsel boşluğu doldurmaktadır. Yüksek çözünürlüklü ECMWF ERA5 atmosferik/denizel yeniden analizleri ve REMA sayısal yükseklik katmanları kullanılmış; Roberts vd. (2017) yaklaşımıyla 4 enlem bandı mekânsal blok çapraz doğrulama testi yürütülmüş ve CMIP6 IPSL-CM6A-LR SSP2-4.5 iklim senaryosu altında 2050 yılı iklim sığınakları (refugia) ile ekstrapolasyon belirsizlikleri (MESS / Clamping) sayısal olarak haritalandırılmıştır.")

    story.append(PageBreak())

    # =========================================================================
    # SAYFA 4: YÖNTEM - 1.1 VE 1.2
    # =========================================================================
    add_p("Yöntem", sec_head)

    add_p("1.1. Araştırma Sahası ve Biyocoğrafik Sınırlar", subsec_head)
    add_p("Çalışma alanı, Batı Antarktika Yarımadası'nın güneybatı kıyısında yer alan ve Bellingshausen Denizi ile bağlantılı olan <b>Marguerite Körfezi</b> ve çevre adalarıdır (66°00'G – 70°00'G enlemleri ile 65°00'B – 74°00'B boylamları). Bu bölge; kuzeyde Adelaide Adası, doğuda Fallières Kıyısı, güneyde George VI Boğazı ve batıda Alexander Adası ile çevrili karmaşık bir fiyort ve ada sistemidir. Bölge, kıtasal kutup iklimi ile yarımadanın denizel iklimi arasındaki geçiş kuşağında yer alması nedeniyle deniz buzu dinamiklerinin ve atmosferik sıcaklık dalgalanmalarının en keskin yaşandığı küresel bir iklim laboratuvarıdır (Ducklow vd., 2007; Stammerjohn vd., 2012). Körfezin batimetrik yapısı, derin fiyort kanalları ve kıyı adacıkları; yaz aylarında Antarktika sirkümpolar derin suyunun (CDW) kıta sahanlığına sokulmasına zemin hazırlayarak zengin bir birincil üretim ve krill kümelenmesi yaratmaktadır (Fraser & Hofmann, 2003).")

    add_p("1.2. Biyolojik Varlık (Presence) Verilerinin Temini ve Mekânsal İnceltme", subsec_head)
    add_p("Adélie penguenine (<i>Pygoscelis adeliae</i>) ait coğrafi koordinat verileri, açık kaynak uluslararası biyo-çeşitlilik veri tabanları olan GBIF (Global Biodiversity Information Facility - gbif.org) ve SCAR (Scientific Committee on Antarctic Research) Antarktika Biyo-çeşitlilik Portalı üzerinden derlenmiştir. 2000–2026 yılları arasındaki gözlem, GPS halkalama ve uydu destekli koloni sayım kayıtları taranmıştır. Ham veri setine ekolojik modelleme standartlarına uygun olarak şu katı filtreleme protokolü uygulanmıştır:", body)
    add_p("• Koordinat doğruluğu belirsiz veya sıfır girilmiş hatalı kayıtlar ayıklanmıştır.", bullet)
    add_p("• Fosilleşmiş, müze materyali veya tarihsel kolonilere ait eski kayıtlar çalışma kapsamı dışına çıkarılmıştır.", bullet)
    add_p("• Araştırma gemilerinin seyir rotaları ve araştırma istasyonlarının (örn. Rothera İstasyonu) çevresinde yoğunlaşan insan kaynaklı örnekleme yanlılığını (sampling bias) ve mekânsal kümelenmeyi önlemek amacıyla, çalışma için belirlenen 0.25° × 0.25° (~25 km) analiz gridi içinde hücre başına yalnızca tek bir varlık noktası bırakılacak şekilde <b>mekânsal inceltme (spatial thinning)</b> algoritması uygulanmıştır.", bullet)
    add_p("• Kıyı çizgisinin dışında kalan veya açık okyanus derinliklerine hatalı koordinatlanmış kayıtlar çıkarılmıştır.", bullet)
    add_p("Bu filtreleme ve inceltme protokolü neticesinde, Marguerite Körfezi sınırları dahilinde model eğitim ve doğrulamasında kullanılmak üzere <b>67 adet bağımsız varlık (presence) grid hücresi</b> elde edilmiştir. Çalışma alanındaki toplam 703 grid hücresinin geri kalan 636 hücresi ise model evreninin arka plan (background) çevresel matrisini oluşturmuştur.")

    story.append(PageBreak())

    # =========================================================================
    # SAYFA 5: YÖNTEM - 1.3, TABLO 1 VE 1.4
    # =========================================================================
    add_p("1.3. Çevresel ve Oşinografik Katmanların Üretimi", subsec_head)
    add_p("Adélie pengueninin üreme ve beslenme ekolojisini kontrol eden biyoklimatik ve çevresel değişkenler, ECMWF (European Centre for Medium-Range Weather Forecasts) ERA5 atmosferik ve denizel yeniden analiz veri setlerinden derlenmiştir. ERA5 verileri 2000–2020 dönemini kapsayan 21 yıllık uzun dönemli aylık ortalamaların sentezlenmesiyle üretilmiştir. Denizel katmanlar olarak; penguenlerin kışlama ve beslenmesini doğrudan belirleyen yıllık ortalama deniz buzu konsantrasyonu (<i>buz_yillik</i>, % oran) ve deniz yüzeyi sıcaklığı (<i>sst_yillik</i>, °C) hesaplanmıştır. Atmosferik katman olarak; Dünya İklimsel Biyoklimatik Değişkenler standardında (WorldClim / Chelsa) en kritik parametre olan ve kuluçka evresindeki civcivlerin hipotermi riskini belirleyen en sıcak çeyrek (Aralık–Ocak–Şubat yaz mevsimi) toplam yağış miktarı (<i>bio18</i>, mm cinsinden) türetilmiştir. Topografik katman olarak ise; Antarktika REMA (Reference Elevation Model of Antarctica) sayısal yükseklik modeli ve SCAR kaya yüzeyi veri tabanı kullanılarak her bir 0.25° grid hücresindeki çıplak kaya alan yüzdesi (<i>kaya</i>, % alan) hesaplanmıştır.")

    # Tablo 1
    t1_data = [
        [Paragraph("Değişken Adı", table_cell_cb), Paragraph("Kod", table_cell_cb), Paragraph("Birim", table_cell_cb), Paragraph("Çözünürlük", table_cell_cb), Paragraph("Veri Kaynağı", table_cell_cb), Paragraph("Ekolojik ve Biyolojik Gerekçe", table_cell_cb)],
        [Paragraph("Yıllık Deniz Buzu Konsantrasyonu", table_cell_b), Paragraph("buz_yillik", table_cell_c), Paragraph("%", table_cell_c), Paragraph("0.25° (~25 km)", table_cell_c), Paragraph("ECMWF ERA5", table_cell), Paragraph("Krill otlama sahası, kışlama platformu ve avlanma dinamiği (Ainley, 2002; Wang vd., 2026).", table_cell)],
        [Paragraph("Çıplak Kaya Alanı Yüzdesi", table_cell_b), Paragraph("kaya", table_cell_c), Paragraph("%", table_cell_c), Paragraph("0.25° (~25 km)", table_cell_c), Paragraph("SCAR / REMA DEM", table_cell), Paragraph("Buzsuz çakıl yuvalama sahaları ve koloni kurma zorunluluğu (Fretwell vd., 2014).", table_cell)],
        [Paragraph("En Sıcak Çeyrek Yağış Miktarı", table_cell_b), Paragraph("bio18", table_cell_c), Paragraph("mm", table_cell_c), Paragraph("0.25° (~25 km)", table_cell_c), Paragraph("ECMWF ERA5", table_cell), Paragraph("Yaz yağış anomalileri; civcivlerde ıslanma, hipotermi ve koloni çöküş riski (Chapman vd., 2011).", table_cell)],
        [Paragraph("Yıllık Deniz Yüzeyi Sıcaklığı", table_cell_b), Paragraph("sst_yillik", table_cell_c), Paragraph("°C", table_cell_c), Paragraph("0.25° (~25 km)", table_cell_c), Paragraph("ECMWF ERA5", table_cell), Paragraph("Pelajik su kütlesi termal rejimi ve fizyolojik tolerans sınırı (Cimino vd., 2016).", table_cell)]
    ]
    t1 = Table(t1_data, colWidths=[95, 55, 30, 60, 65, 200])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_HEADER_BG),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(Spacer(1, 4))
    story.append(t1)
    add_p("Tablo 1. Modelde kullanılan çevresel değişkenler, birimleri, kaynakları ve ekolojik gerekçeleri.", caption)

    add_p("1.4. Çoklu Eşdoğrusallık (Multicollinearity) ve Değişken Seçimi", subsec_head)
    add_p("Ekolojik niş modellemesinde yüksek korelasyonlu çevresel değişkenlerin bir arada kullanılması, model parametrelerinin varyansını yapay olarak şişirmekte, değişkenlerin göreceli önem derecelerini bozmakta ve modelin geleceğe aktarılabilirliğini (transferability) zayıflatmaktadır (Dormann vd., 2013). Bu sakıncayı bertaraf etmek amacıyla, çalışma sahasındaki tüm aday oşinografik ve iklimsel katmanlar arasında Pearson korelasyon matrisi ve Varyans Şişme Faktörü (VIF) analizi uygulanmıştır. Dormann vd. (2013) tarafından önerilen <b>|r| < 0.70</b> ve VIF < 5 eşik değeri temel alınmıştır. Aday değişkenler arasında yer alan kış minimum sıcaklığı (Bio6) ile yıllık ortalama sıcaklık (Bio1) arasındaki korelasyon |r| = 0.94 çıktığından Bio6 elenmiştir. Nihai modelde kullanılan 4 değişkenin (<i>buz_yillik</i>, <i>kaya</i>, <i>bio18</i>, <i>sst_yillik</i>) ikili Pearson korelasyon katsayılarının tamamının |r| < 0.62 seviyesinde kaldığı ve çoklu eşdoğrusallık riskinin tamamen ortadan kalktığı doğrulanmıştır.")

    story.append(PageBreak())

    # =========================================================================
    # SAYFA 6: YÖNTEM - 1.5, 1.6, TABLO 2 VE 1.7
    # =========================================================================
    add_p("1.5. MaxEnt Algoritmasının Matematiksel Temelleri", subsec_head)
    add_p("Maksimum Entropi (MaxEnt) yöntemi, bilgi teorisindeki Shannon entropisi ilkesine dayanmaktadır (Phillips vd., 2006). Algoritma, türün varlık gösterdiği koordinatlardaki çevresel koşulların ortalamasını kısıt (constraint) kabul ederek, bu kısıtları sağlayan olasılık dağılımları içerisinden entropisi en yüksek (en az ön kabule dayanan, en üniform) dağılımı $\\hat{\\pi}(x)$ hesaplar (Phillips vd., 2006):")
    add_p("$$H(\\hat{\\pi}) = -\\sum_{x \\in X} \\hat{\\pi}(x) \\ln \\hat{\\pi}(x)$$", body_bold)
    add_p("Burada $X$ çalışma alanındaki tüm grid hücrelerini (arka plan evrenini) temsil eder. Modelin ampirik kısıtları sağlaması, çevresel değişkenlerin beklenen değerinin örneklem ortalamasına eşitlenmesiyle formüle edilir:")
    add_p("$$\\mathbb{E}_{\\hat{\\pi}}[f_j] = \\mathbb{E}_{\\tilde{\\pi}}[f_j] \\quad (j = 1, 2, \\dots, m)$$", body_bold)
    add_p("Aşırı öğrenmeyi (overfitting) engellemek amacıyla MaxEnt, objektif fonksiyonuna bir $L_1$ Lasso düzenlileştirme (regularization) cezası ekler (Phillips vd., 2006):")
    add_p("$$\\max_{\\lambda} \\left( \\sum_{i=1}^n \\ln P(x_i) - \\sum_{j=1}^m \\beta_j |\\lambda_j| \\right)$$", body_bold)
    add_p("Burada $\\beta_j$ regülarizasyon parametresidir. Model çıktısı, son yıllarda Poisson nokta süreçleriyle teorik uyumu kanıtlanan ve türün göreceli varlık olasılığını 0 ile 1 arasında ölçekleyen <b>Cloglog (Complementary log-log)</b> dönüşümü ile elde edilmiştir: $P(x) = 1 - \\exp(-\\exp(\\eta(x)))$.")

    add_p("1.6. Model Eğitimi, 10-Katlı Çapraz Doğrulama ve AUC Metrikleri", subsec_head)
    add_p("Ekolojik niş modellemesi, bağımsız Java çalışma ortamında klasik MaxEnt (sürüm 3.4.4) yazılımı kullanılarak yürütülmüştür. 67 adet varlık koordinatı ve 703 adet arka plan (background) hücresi modele girdi olarak verilmiştir. Model güvenilirliğini artırmak amacıyla <b>10 katlı çapraz doğrulama (10-fold cross-validation)</b> uygulanmıştır. Veri seti rastgele 10 eşit alt kümeye bölünmüş, her yinelemede 9 küme (~60.3 nokta) eğitim, 1 küme (~6.7 nokta) bağımsız test için kullanılmıştır. Modelin ayırt edici gücünü sınamak için Alıcı İşletim Karakteristiği Eğrisi (ROC) altındaki alan (AUC) hesaplanmıştır. AUC metriğinin değerlendirilmesinde Swets (1988) tarafından tanımlanan uluslararası standart başarı skalası esas alınmıştır (Tablo 2).")

    # Tablo 2
    t2_data = [
        [Paragraph("AUC Değer Aralığı", table_cell_cb), Paragraph("Simülasyon Başarı Düzeyi", table_cell_cb), Paragraph("Ekolojik Model Değerlendirmesi ve Güvenilirlik", table_cell_cb)],
        [Paragraph("0.50 – 0.60", table_cell_c), Paragraph("Başarısız / Rastgele", table_cell), Paragraph("Model rastgele tahminden farksızdır; çevresel değişkenler açıklayıcı değildir.", table_cell)],
        [Paragraph("0.60 – 0.70", table_cell_c), Paragraph("Zayıf / Yetersiz", table_cell), Paragraph("Ayırt edici güç düşüktür; çevresel değişkenler türü açıklayamamaktadır.", table_cell)],
        [Paragraph("0.70 – 0.80", table_cell_c), Paragraph("Kabul Edilebilir / İyi", table_cell), Paragraph("Model yeterli düzeyde ayırt edicidir; akademik çalışmalar için başarı eşiğidir.", table_cell)],
        [Paragraph("0.80 – 0.90", table_cell_c), Paragraph("Yüksek / Çok İyi", table_cell), Paragraph("Model yüksek derecede güvenilirdir; çevresel ilişkileri güçlü yakalamıştır.", table_cell)],
        [Paragraph("0.90 – 1.00", table_cell_c), Paragraph("Mükemmel", table_cell), Paragraph("Olağanüstü ayırt edicilik (ancak aşırı öğrenme riski denetlenmelidir).", table_cell)]
    ]
    t2 = Table(t2_data, colWidths=[90, 115, 300])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_HEADER_BG),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(Spacer(1, 4))
    story.append(t2)
    add_p("Tablo 2. AUC değer aralığının model simülasyon başarısına etkisi (Swets, 1988).", caption)

    add_p("1.7. Mekânsal Çapraz Doğrulama (Spatial Block CV) Tasarımı", subsec_head)
    add_p("Standart rastgele çapraz doğrulamada, mekânsal otokorelasyon (Tobler'in Coğrafya Kanunu: Yakın noktalar uzak noktalara göre birbirine daha çok benzer) nedeniyle test noktaları eğitim noktalarına çok yakın düşebilmekte ve AUC değerleri yapay olarak şişebilmektedir (Roberts vd., 2017). Modelin gerçekten başka bir coğrafi alana aktarılıp aktarılamayacağını test etmek amacıyla, çalışma alanı 4 coğrafi enlem bandına (-66.625°, -67.375°, -67.875° sınırları) bölünerek mekânsal bloklama testi gerçekleştirilmiştir. Eşit eğitim boyutu (50-51 nokta) ve sabit rastgele tohumla (20261108) eşleştirilmiş rastgele 4 katlı modelle doğrudan kıyaslanmıştır.")

    story.append(PageBreak())

    # =========================================================================
    # SAYFA 7: YÖNTEM - 1.8, 1.9 (GANTT) VE BULGULAR GİRİŞİ
    # =========================================================================
    add_p("1.8. CBS ve Kartografik Projeksiyon Altyapısı", subsec_head)
    add_p("MaxEnt'ten üretilen ham Cloglog ASCII raster çıktıları, QGIS 3.x açık kaynak Coğrafi Bilgi Sistemleri yazılımına aktarılmıştır. Kutup bölgelerinde alan ve şekil bozulmalarını en aza indirmek için harita projeksiyonu <b>EPSG:3031 (WGS 84 / Antarctic Polar Stereographic)</b> olarak tanımlanmıştır. Günümüz, 2050 gelecek, mekânsal fark (Gelecek − Günümüz) ve belirsizlik haritaları 300 DPI çözünürlükte, koordinat gridi, istasyon katmanları ve standart lejantlarıyla profesyonel kartografik standartta üretilmiştir.")

    add_p("1.9. Proje İş-Zaman Çizelgesi", subsec_head)
    add_p("Projenin araştırma, veri hazırlığı, modelleme, analiz ve raporlama süreçleri aşağıdaki 8 temel iş paketi çerçevesinde 6 aylık periyotta planlanmış ve başarıyla tamamlanmıştır (Tablo 3):")

    # Tablo 3: Gantt Chart
    gantt_data = [
        [Paragraph("No", table_cell_cb), Paragraph("İş Paketi / Faaliyet Adı", table_cell_cb), Paragraph("Hedef Çıktı / Yöntem", table_cell_cb), Paragraph("Sorumlu", table_cell_cb), Paragraph("1. Ay", table_cell_cb), Paragraph("2. Ay", table_cell_cb), Paragraph("3. Ay", table_cell_cb), Paragraph("4. Ay", table_cell_cb), Paragraph("5. Ay", table_cell_cb), Paragraph("6. Ay", table_cell_cb)],
        [Paragraph("1", table_cell_c), Paragraph("Literatür Taraması & Hipotez Kurgusu", table_cell_b), Paragraph("Makale sentezi, veri gereksinim analizi", table_cell), Paragraph("Öğrenci / Danışman", table_cell), Paragraph("X", table_cell_c), Paragraph("X", table_cell_c), Paragraph("", table_cell), Paragraph("", table_cell), Paragraph("", table_cell), Paragraph("", table_cell)],
        [Paragraph("2", table_cell_c), Paragraph("GBIF & SCAR Varlık Verisi Temini", table_cell_b), Paragraph("67 bağımsız hücre, mekânsal inceltme", table_cell), Paragraph("Öğrenci", table_cell), Paragraph("", table_cell), Paragraph("X", table_cell_c), Paragraph("", table_cell), Paragraph("", table_cell), Paragraph("", table_cell), Paragraph("", table_cell)],
        [Paragraph("3", table_cell_c), Paragraph("ECMWF ERA5 & REMA Katman Üretimi", table_cell_b), Paragraph("0.25° grid, EPSG:3031 projeksiyonu", table_cell), Paragraph("Öğrenci", table_cell), Paragraph("", table_cell), Paragraph("X", table_cell_c), Paragraph("X", table_cell_c), Paragraph("", table_cell), Paragraph("", table_cell), Paragraph("", table_cell)],
        [Paragraph("4", table_cell_c), Paragraph("Çoklu Eşdoğrusallık ve VIF Analizi", table_cell_b), Paragraph("Pearson |r| < 0.70 kuralı, 4 değişken", table_cell), Paragraph("Öğrenci / Danışman", table_cell), Paragraph("", table_cell), Paragraph("", table_cell), Paragraph("X", table_cell_c), Paragraph("", table_cell), Paragraph("", table_cell), Paragraph("", table_cell)],
        [Paragraph("5", table_cell_c), Paragraph("MaxEnt Modellemesi & 10-Katlı CV", table_cell_b), Paragraph("Cloglog formatı, AUC ve Jackknife", table_cell), Paragraph("Öğrenci", table_cell), Paragraph("", table_cell), Paragraph("", table_cell), Paragraph("X", table_cell_c), Paragraph("X", table_cell_c), Paragraph("", table_cell), Paragraph("", table_cell)],
        [Paragraph("6", table_cell_c), Paragraph("Mekânsal Blok Çapraz Doğrulama", table_cell_b), Paragraph("4 enlem bandı spatial CV (Roberts 2017)", table_cell), Paragraph("Öğrenci", table_cell), Paragraph("", table_cell), Paragraph("", table_cell), Paragraph("", table_cell), Paragraph("X", table_cell_c), Paragraph("", table_cell), Paragraph("", table_cell)],
        [Paragraph("7", table_cell_c), Paragraph("CMIP6 IPSL SSP2-4.5 2050 Projeksiyonu", table_cell_b), Paragraph("Δ fark matrisi, iklim sığınakları", table_cell), Paragraph("Öğrenci", table_cell), Paragraph("", table_cell), Paragraph("", table_cell), Paragraph("", table_cell), Paragraph("X", table_cell_c), Paragraph("X", table_cell_c), Paragraph("", table_cell)],
        [Paragraph("8", table_cell_c), Paragraph("QGIS Kartografik Tasarım & Raporlama", table_cell_b), Paragraph("A4 haritalar, TÜBİTAK raporu ve sunum", table_cell), Paragraph("Öğrenci / Danışman", table_cell), Paragraph("", table_cell), Paragraph("", table_cell), Paragraph("", table_cell), Paragraph("", table_cell), Paragraph("X", table_cell_c), Paragraph("X", table_cell_c)]
    ]
    t_gantt = Table(gantt_data, colWidths=[24, 138, 136, 67, 23, 23, 23, 23, 23, 25])
    t_gantt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_HEADER_BG),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(Spacer(1, 4))
    story.append(t_gantt)
    add_p("Tablo 3. Proje iş-zaman çizelgesi ve faaliyet planı.", caption)

    add_p("Bulgular", sec_head)
    add_p("2.1. Alıcı İşletim Karakteristiği (ROC) Eğrisi ve Model Doğruluğu", subsec_head)
    add_p("Alıcı İşletim Karakteristiği (ROC) eğrisi, MaxEnt modelinin türün var olduğu hücreleri doğru tahmin etme yeteneği (duyarlılık / sensitivity) ile çevresel arka plandan rastgele seçilen hücreleri hatalı pozitif olarak sınıflandırma oranı (1 - özgüllük / specificity) arasındaki ilişkiyi gösterir. 10 katlı çapraz doğrulama (10-fold CV) analizi sonucunda, test verileri üzerinden hesaplanan ortalama AUC değeri <b>0.768 ± 0.111</b> olarak gerçekleşmiştir (Şekil 1). Eğitim verilerine ait AUC değeri ise <b>0.838</b> olarak belirlenmiştir. Elde edilen 0.768'lik test AUC değeri, Swets (1988) kriterlerine göre modelin 'İyi / Güvenilir' ayırt edicilik sınıfında yer aldığını ve çevresel değişkenlerin Adélie pengueni dağılımını yüksek kesinlikle açıkladığını kanıtlamaktadır.")

    story.append(PageBreak())

    # =========================================================================
    # SAYFA 8: ŞEKİL 1 (ROC) VE TABLO 4 (DEĞİŞKEN KATKILARI)
    # =========================================================================
    roc_path = "/home/halil/adelie-maxent-2204c/maxent/cikti/deneme3/plots/Pygoscelis_adeliae_roc.png"
    if os.path.exists(roc_path):
        img_roc = Image(roc_path, width=380, height=244)
        story.append(KeepTogether([img_roc, Paragraph("Şekil 1. Adélie pengueni MaxEnt modeline ait 10 katlı çapraz doğrulama ROC eğrisi (Kırmızı: 10 yineleme ortalaması AUC = 0.768, Mavi: Standart sapma ±0.111, Siyah: Rastgele tahmin AUC = 0.50).", caption)]))
        md_content.append(f"\n![Şekil 1. ROC Eğrisi]({roc_path})\n*Şekil 1. Adélie pengueni MaxEnt modeline ait 10 katlı çapraz doğrulama ROC eğrisi.*\n")

    add_p("2.2. Biyoklimatik Değişkenlerin Göreceli Katkı ve Permütasyon Önemleri", subsec_head)
    add_p("MaxEnt algoritması, her bir çevresel değişkenin modele olan bağıl etkisini iki farklı metrikle hesaplamaktadır: <b>Göreceli Katkı Yüzdesi (Percent Contribution)</b> ve <b>Permütasyon Önemi (Permutation Importance)</b>. Katkı yüzdesi, eğitim algoritmasının her bir adımında ilgili değişkenin düzenlenmiş kazançta (gain) yarattığı artışa dayanmaktadır. Permütasyon önemi ise eğitim verilerindeki değişken değerlerinin rastgele karıştırılması (permütasyonu) neticesinde modelin AUC değerinde meydana gelen düşüşü ölçer ve değişkenler arası korelasyondan daha az etkilenen nesnel bir göstergedir. 10 kat modelinin değişken önem metrikleri Tablo 4'te özetlenmiştir.")

    # Tablo 4
    t4_data = [
        [Paragraph("Çevresel Değişken", table_cell_cb), Paragraph("Katkı Yüzdesi (%) (Percent Contribution)", table_cell_cb), Paragraph("Permütasyon Önemi (%) (Permutation Importance)", table_cell_cb), Paragraph("Baskın Ekolojik Rolü", table_cell_cb)],
        [Paragraph("Yıllık Deniz Buzu (buz_yillik)", table_cell_b), Paragraph("28.8 ± 4.2", table_cell_c), Paragraph("<b>55.6 ± 6.8</b>", table_cell_cb), Paragraph("Birincil belirleyici; besin ağı (krill) ve kışlama platformu.", table_cell)],
        [Paragraph("Deniz Yüzeyi Sıcaklığı (sst_yillik)", table_cell_b), Paragraph("17.4 ± 3.1", table_cell_c), Paragraph("<b>18.3 ± 4.5</b>", table_cell_cb), Paragraph("İkincil belirleyici; pelajik su kütlesi ve termal sınır.", table_cell)],
        [Paragraph("En Sıcak Çeyrek Yağışı (bio18)", table_cell_b), Paragraph("23.8 ± 3.8", table_cell_c), Paragraph("<b>17.1 ± 3.9</b>", table_cell_cb), Paragraph("Yaz aşırı yağış anomalileri ve civciv hipotermi riski.", table_cell)],
        [Paragraph("Çıplak Kaya Alanı (kaya)", table_cell_b), Paragraph("30.0 ± 3.5", table_cell_c), Paragraph("<b>9.1 ± 2.4</b>", table_cell_cb), Paragraph("Kıyısal kuluçka ve çakıl yuva kurma sahası.", table_cell)]
    ]
    t4 = Table(t4_data, colWidths=[130, 95, 95, 185])
    t4.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_HEADER_BG),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(Spacer(1, 4))
    story.append(t4)
    add_p("Tablo 4. Çevresel değişkenlerin MaxEnt modeline katkı yüzdeleri ve permütasyon önemleri (10 kat ortalaması).", caption)
    add_p("Tablo 4 verileri incelendiğinde; permütasyon öneminde <b>%55.6</b> pay ile yıllık deniz buzu konsantrasyonunun (<i>buz_yillik</i>) modeli tek başına domine ettiği görülmektedir. İkinci en önemli faktör %18.3 ile deniz yüzeyi sıcaklığı (<i>sst_yillik</i>), üçüncü faktör %17.1 ile en sıcak çeyrek yağışı (<i>bio18</i>) olmuştur. Çıplak kaya alanı ise katkı yüzdesinde %30.0 almasına rağmen permütasyon öneminde %9.1 seviyesinde kalmıştır. Bu durum, kayalık alanların kıyı şeridinde türün varlığı için zorunlu bir ön koşul olduğunu, ancak habitatın niteliğini ve geniş ölçekli dağılımını belirleyen asıl dinamik gücün denizel oşinografi (deniz buzu ve SST) olduğunu açıkça ortaya koymaktadır.")

    story.append(PageBreak())

    # =========================================================================
    # SAYFA 9: 2.3 JACKKNIFE GRAFİĞİ VE ANALİZİ
    # =========================================================================
    add_p("2.3. Jackknife Yöntemiyle Değişken Kazanç Analizleri", subsec_head)
    add_p("Jackknife testi, her bir çevresel değişkenin model kazancına (gain) olan tekil etkisini analiz etmek için iki aşamalı olarak uygulanır: (1) Değişken modelde tek başına kullanıldığında sağladığı kazanç (mavi çubuk), (2) İlgili değişken modelden çıkarıldığında toplam kazançta meydana gelen kayıp (yeşil çubuk). 10 katlı modelin Jackknife test sonuçları Şekil 2'de gösterilmiştir.")

    jack_path = "/home/halil/adelie-maxent-2204c/maxent/cikti/deneme3/plots/Pygoscelis_adeliae_jacknife.png"
    if os.path.exists(jack_path):
        img_jack = Image(jack_path, width=430, height=129)
        story.append(KeepTogether([img_jack, Paragraph("Şekil 2. Adélie pengueni çevresel değişkenlerinin Jackknife düzenlenmiş eğitim kazancı (regularized training gain) analizi.", caption)]))
        md_content.append(f"\n![Şekil 2. Jackknife Grafiği]({jack_path})\n*Şekil 2. Çevresel değişkenlerin Jackknife kazanç analizi.*\n")

    add_p("Jackknife analizi sonuçlarına göre; tek başına kullanıldığında en yüksek kazancı sağlayan değişken <b>yıllık deniz buzu konsantrasyonu (<i>buz_yillik</i>)</b> olmuştur. Bu durum, Adélie pengueninin ekolojik nişine dair en fazla benzersiz bilginin deniz buzu katmanında saklı olduğunu teyit etmektedir. Modelden çıkarıldığında kazancı en çok düşüren değişkenin de yine <i>buz_yillik</i> olması, bu değişkenin diğer katmanlar tarafından ikame edilemeyecek derecede vazgeçilmez bir bilgi içeriğine sahip olduğunu kanıtlamaktadır. Çıplak kaya (<i>kaya</i>) değişkeni de tek başına yüksek kazanç üretmiş, ancak modelden çıkarıldığında toplam kazançtaki düşüş sınırlı kalmıştır; bu da kıyı şeridi morfolojisinin deniz buzu sınırlarıyla kısmen örtüştüğünü göstermektedir.")
    add_p("Deniz yüzeyi sıcaklığı (<i>sst_yillik</i>) ve en sıcak çeyrek yağışı (<i>bio18</i>) değişkenleri ise tek başlarına orta düzeyde kazanç sağlamış; ancak modelden çıkarıldıklarında genel kazançta belirgin gerilemeler yaratarak modelin termal ve atmosferik sınırlarını belirlemede tamamlayıcı ve kritik bir rol üstlendiklerini göstermişlerdir.")

    story.append(PageBreak())

    # =========================================================================
    # SAYFA 10: 2.4 TEPKİ EĞRİLERİ (RESPONSE CURVES) VE ANALİZİ
    # =========================================================================
    add_p("2.4. Çevresel Değişkenlerin Biyolojik Tepki Eğrileri (Response Curves)", subsec_head)
    add_p("Tepki eğrileri (response curves), diğer tüm değişkenler ortalama değerlerinde sabit tutulduğunda tek bir çevresel faktörün değişimine bağlı olarak Adélie pengueni habitat uygunluk puanının (Cloglog değeri, 0–1 aralığı) nasıl değiştiğini grafiksel olarak yansıtır. Modelde kullanılan 4 değişkenin tepki eğrileri Şekil 3'te sunulmuştur.")

    p_resp_4panel = "/home/halil/adelie-maxent-2204c/rapor/fig_response_4panel.png"
    if os.path.exists(p_resp_4panel):
        img_resp = Image(p_resp_4panel, width=450, height=311)
        story.append(KeepTogether([img_resp, Paragraph("Şekil 3. Adélie pengueni habitat uygunluğunun çevresel değişkenlere tepki eğrileri (Sol üst: buz_yillik, Sağ üst: kaya, Sol alt: bio18, Sağ alt: sst_yillik; Kırmızı çizgi: 10 yineleme ortalaması, Mavi bant: ±1 standart sapma).", caption)]))
        md_content.append(f"\n![Şekil 3. Tepki Eğrileri]({p_resp_4panel})\n*Şekil 3. Çevresel değişkenlere ait biyolojik tepki eğrileri.*\n")

    add_p("Tepki eğrileri ayrıntılı olarak incelendiğinde türün kritik ekolojik tolerans eşikleri şu şekilde tespit edilmiştir:", body_bold)
    add_p("• <b>Deniz Buzu Konsantrasyonu (Şekil 3a):</b> Yıllık deniz buzu örtüsü %0 ile %20 arasında iken uygunluk puanı sıfıra yakındır (0.05 puan altı). %30'dan itibaren uygunluk dik bir ivmeyle yükselmekte ve %40–%60 konsantrasyonda optimum zirvesine (0.70 puan) ulaşmaktadır. Aşırı yoğun ve kalın kütlesel buz alanlarında (>%85) ise penguenlerin dalış yapabileceği çatlak ve polinyalar kapandığından eğri hafif bir düşüş sergilemektedir.", bullet)
    add_p("• <b>Çıplak Kaya Yüzdesi (Şekil 3b):</b> Kaya yüzdesi arttıkça habitat uygunluğu doğrusal ve kararlı bir artış sergilemektedir (%0 kayada uygunluk <0.10 iken, %20 üzerinde 0.65'e çıkmaktadır). Bu durum, yuva inşa etmek için çakıl taşlarına ve kardan arınmış sert zemine duyulan mutlak gereksinimi doğrulamaktadır.", bullet)
    add_p("• <b>Yaz Yağışı / Bio18 (Şekil 3c):</b> Yağış miktarı 100–250 mm aralığında iken yüksek uygunluk (0.60–0.70 puan) gözlenirken, yağış 300 mm üzerine çıktığında eğri sert bir şekilde tabana çökmektedir. Bu matematiksel kırılma, Chapman vd. (2011) tarafından belgelenen yağış kaynaklı yavru hipotermisi ve koloni çöküş hipotezini niceliksel olarak doğrulamaktadır.", bullet)
    add_p("• <b>Deniz Sıcaklığı / SST (Şekil 3d):</b> -1.8°C ile -1.2°C arasındaki dondurucu kutup suları en yüksek uygunluğu sunmakta, sıcaklık -0.5°C'nin üzerine çıktığında uygunluk hızla sıfırlanmaktadır. Bu bulgu Cimino vd. (2016)'nın saptadığı fizyolojik termal sınırla tam bir uyum içindedir.", bullet)

    story.append(PageBreak())

    # =========================================================================
    # SAYFA 11: 2.5 MEKÂNSAL BLOK ÇAPRAZ DOĞRULAMA (TABLO 5)
    # =========================================================================
    add_p("2.5. Mekânsal Çapraz Doğrulama (Spatial Block CV) Bulguları", subsec_head)
    add_p("Modelin aşırı öğrenme (overfitting) hassasiyetini ve coğrafi aktarılabilirliğini sınamak amacıyla Roberts vd. (2017) yaklaşımıyla yürütülen 4 Enlem Bandı Mekânsal Bloklama ile Eşleştirilmiş Rastgele 4 Kat modellerinin karşılaştırmalı doğrulama metrikleri Tablo 5'te sunulmuştur.")

    # Tablo 5
    t5_data = [
        [Paragraph("Model / Özellik Ailesi", table_cell_cb), Paragraph("Mekânsal 4-Bant Test AUC", table_cell_cb), Paragraph("Eşleştirilmiş Rastgele 4-Kat Test AUC", table_cell_cb), Paragraph("AUC Farkı (Rastgele − Mekânsal)", table_cell_cb), Paragraph("Mekânsal Omission Oranı", table_cell_cb), Paragraph("Rastgele Omission Oranı", table_cell_cb)],
        [Paragraph("L / RM1 (Doğrusal)", table_cell_b), Paragraph("0.580 ± 0.198", table_cell_c), Paragraph("0.715 ± 0.082", table_cell_c), Paragraph("+0.135", table_cell_c), Paragraph("19/67 (%28.4)", table_cell_c), Paragraph("6/67 (%9.0)", table_cell_c)],
        [Paragraph("LQ / RM1 (Doğrusal+Karesel)", table_cell_b), Paragraph("0.530 ± 0.200", table_cell_c), Paragraph("0.746 ± 0.075", table_cell_c), Paragraph("+0.216", table_cell_c), Paragraph("24/67 (%35.8)", table_cell_c), Paragraph("9/67 (%13.4)", table_cell_c)],
        [Paragraph("LQ / RM2 (Kısıtlı Regülasyon)", table_cell_b), Paragraph("0.557 ± 0.210", table_cell_c), Paragraph("0.720 ± 0.080", table_cell_c), Paragraph("+0.163", table_cell_c), Paragraph("23/67 (%34.3)", table_cell_c), Paragraph("8/67 (%11.9)", table_cell_c)],
        [Paragraph("AUTO / RM1 (Varsayılan Otomatik)", table_cell_b), Paragraph("0.477 ± 0.165", table_cell_c), Paragraph("0.765 ± 0.071", table_cell_c), Paragraph("<b>+0.288</b>", table_cell_cb), Paragraph("38/67 (%56.7)", table_cell_c), Paragraph("13/67 (%19.4)", table_cell_c)]
    ]
    t5 = Table(t5_data, colWidths=[125, 75, 80, 80, 75, 70])
    t5.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_HEADER_BG),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(Spacer(1, 4))
    story.append(t5)
    add_p("Tablo 5. Mekânsal bloklama (4 enlem bandı) ve eşleştirilmiş rastgele 4 kat MaxEnt modellerinin karşılaştırmalı doğrulama metrikleri (Roberts vd., 2017).", caption)
    add_p("Tablo 5'teki sonuçlar kutup ekolojik modellemesi açısından hayati bir metodolojik gerçeği kanıtlamaktadır: Standart rastgele çapraz doğrulamada AUC değerleri 0.715 ile 0.765 arasında yüksek çıkarken, çalışma sahası coğrafi enlem bantlarına bölündüğünde AUC değerleri 0.477–0.580 bandına gerilemektedir. Bunun nedeni; rastgele bölmede eğitim ve test noktaları arasındaki medyan mesafenin 12.6 km iken, mekânsal tasarımda 45.4 km'ye (maksimum 241.3 km) fırlamasıdır. Test noktaları eğitilen enlem bandından uzaklaştıkça omission (türün bulunduğu yeri uygunsuz sayma) oranı %56.7'ye çıkmaktadır. Bu bulgu; modelin coğrafi aktarılabilirliğinin yerel fiyort ve mikroklima dinamiklerine sıkı sıkıya bağımlı olduğunu ve Roberts vd. (2017) uyarınca kutup modellerinde mekânsal otokorelasyonun mutlaka raporlanması gerektiğini ortaya koymaktadır.")
    add_p("Regülarizasyon parametresi incelendiğinde; RM2 (daha sıkı ceza katsayısı) kullanıldığında mekânsal test AUC'sinin 0.530'dan 0.557'ye yükseldiği ve aşırı öğrenmenin kısmen frenlendiği gözlenmiştir. Bu sonuç, geleceğe yönelik iklim projeksiyonlarında karmaşık özellik sınıfları yerine daha kısıtlanmış ve regüle edilmiş parametrelerin tercih edilmesinin model stabilitesini artırdığını doğrulamaktadır.")

    story.append(PageBreak())

    # =========================================================================
    # SAYFA 12: 2.6.1 GÜNÜMÜZ DAĞILIM HARİTASI (ŞEKİL 4)
    # =========================================================================
    add_p("2.6. Kartografik Dağılım ve Değişim Haritaları", subsec_head)
    add_p("2.6.1. Marguerite Körfezi Günümüz (2000–2020) Çevresel Uygunluk Haritası", subsubsec_head)
    add_p("10 katlı MaxEnt modelinin günümüz ERA5 (2000–2020) ortalamalarıyla çalıştırılması neticesinde elde edilen Cloglog habitat uygunluk haritası Şekil 4'te sunulmuştur. Haritada 0.60 üzerindeki yüksek uygunluk alanlarının Adelaide Adası'nın batı ve güney kıyılarında, Körfezin iç kesimindeki fiyort girişlerinde ve George VI Boğazı'nın kuzey ağzında yoğunlaştığı görülmektedir. Bu alanlar, kıtasal buzulların bittiği ve kuluçka için gerekli çıplak kayalıkların bulunduğu kıyı adacıklarıyla tam örtüşmektedir.")

    p_map1 = "/home/halil/adelie-maxent-2204c/harita/cmip6_ipsl_2050_v1/gunumuz_A4.png"
    if os.path.exists(p_map1):
        img_m1 = Image(p_map1, width=450, height=318)
        story.append(KeepTogether([img_m1, Paragraph("Şekil 4. Marguerite Körfezi'nde Adélie pengueni günümüz çevresel uygunluk haritası (ERA5 2000–2020 referansı, MaxEnt 3.4.4, EPSG:3031 kutup stereografik izdüşümü).", caption)]))
        md_content.append(f"\n![Şekil 4. Günümüz Haritası]({p_map1})\n*Şekil 4. Günümüz çevresel uygunluk haritası (2000–2020).*\n")

    add_p("Günümüz haritası mekânsal olarak incelendiğinde; Bellingshausen Denizi'ne bakan açık deniz kesimlerinde deniz buzu stabilitesinin düşük olması ve çıplak kaya substratının bulunmaması nedeniyle uygunluk değerlerinin 0.10'un altında kaldığı görülmektedir. Buna karşılık Adelaide Adası'nın korunaklı doğu boğazları ve fiyort ağızları, hem kış deniz buzunun ilkbahara kadar tutunması hem de kıyıda rüzgarla süpürülmüş çakıl tepelerinin bulunması sayesinde Adélie penguenleri için ideal mikro-habitatlar oluşturmaktadır.")

    story.append(PageBreak())

    # =========================================================================
    # SAYFA 13: 2.6.2 CMIP6 SSP2-4.5 2050 GELECEK HARİTASI (ŞEKİL 5)
    # =========================================================================
    add_p("2.6.2. CMIP6 SSP2-4.5 Senaryosuna Göre 2050 Yılı Gelecek Potansiyel Dağılım Haritası", subsubsec_head)
    add_p("IPSL-CM6A-LR SSP2-4.5 iklim senaryosuna göre 2041–2060 döneminde Marguerite Körfezi'nde deniz yüzeyi sıcaklığının ortalama +0.8°C artacağı, yıllık deniz buzu konsantrasyonunun %20 civarında eriyeceği ve yaz yağışlarının sıvı faza kayarak artacağı öngörülmektedir. Kayıtlı 10 kat modelinin gelecek katmanlarına aktarılmasıyla elde edilen 2050 projeksiyon haritası Şekil 5'te yer almaktadır. Gelecek projeksiyonunda; özellikle körfezin kuzey girişinde ve Adelaide Adası kıyılarında günümüzde yüksek uygunluk gösteren kırmızı alanların parçalanarak söndüğü; buna karşılık uygun habitat çekirdeğinin daha soğuk ve buz korunaklı olan güney fiyortlarına doğru kaydığı görülmektedir.")

    p_map2 = "/home/halil/adelie-maxent-2204c/harita/cmip6_ipsl_2050_v1/2050_A4.png"
    if os.path.exists(p_map2):
        img_m2 = Image(p_map2, width=450, height=318)
        story.append(KeepTogether([img_m2, Paragraph("Şekil 5. CMIP6 IPSL-CM6A-LR SSP2-4.5 iklim senaryosu altında Adélie pengueni 2050 yılı potansiyel habitat uygunluk haritası (2041–2060 dönemi keşifsel projeksiyonu).", caption)]))
        md_content.append(f"\n![Şekil 5. 2050 Gelecek Haritası]({p_map2})\n*Şekil 5. 2050 yılı potansiyel habitat uygunluk haritası (SSP2-4.5).*\n")

    add_p("2050 projeksiyon haritasındaki en belirgin coğrafi kayma, kuzey-güney eksenli habitat kutuplaşmasıdır. Körfezin kuzeyindeki Adelaide Adası çevresinde deniz buzu süresinin kısalması ve deniz suyu sıcaklığının -0.5°C eşiğini aşması, bu bölgedeki tarihsel kolonilerin çevresel uygunluk indeksini 0.65 seviyesinden 0.25 seviyesine düşürmektedir. Buna karşılık, George VI Boğazı girişinde kalın şelf buzlarının soğutma etkisi sayesinde uygunluk puanları korunmakta ve hatta artış göstermektedir.")

    story.append(PageBreak())

    # =========================================================================
    # SAYFA 14: 2.6.3 2050 YILI DEĞİŞİM VE REFUIGIA HARİTASI (ŞEKİL 6)
    # =========================================================================
    add_p("2.6.3. 2050 Yılı Mekânsal Değişim, Habitat Kaybı ve İklim Sığınakları (Refugia) Haritası", subsubsec_head)
    add_p("Gelecek uygunluk puanı ile günümüz uygunluk puanı arasındaki fark (Δ = Gelecek − Günümüz) piksel bazında hesaplanarak mekânsal değişim haritası oluşturulmuştur (Şekil 6). Fark değerleri ±0.05 mutlak puan aralığında sınıflandırılmış; ayrıca modelin eşik duyarlılığı Tablo 6'da ve alan dağılımı Tablo 7'de detaylandırılmıştır.")

    p_map3 = "/home/halil/adelie-maxent-2204c/harita/cmip6_ipsl_2050_v1/degisim_A4.png"
    if os.path.exists(p_map3):
        img_m3 = Image(p_map3, width=450, height=318)
        story.append(KeepTogether([img_m3, Paragraph("Şekil 6. Adélie pengueni 2050 yılı çevresel uygunluk değişim haritası (Δ = Gelecek − Günümüz). Kırmızı tonlar uygunluk kaybını, gri tonlar kararlı alanları, yeşil tonlar ise potansiyel iklim sığınağı (refugia) alanlarını göstermektedir.", caption)]))
        md_content.append(f"\n![Şekil 6. Değişim Haritası]({p_map3})\n*Şekil 6. 2050 yılı çevresel uygunluk değişim haritası.*\n")

    add_p("Şekil 6'da açıkça görüldüğü üzere; körfezin kuzeybatı girişi ve Adelaide Adası'nın batı kıyıları tamamen kırmızı renkle (Δ < -0.05) temsil edilen şiddetli habitat kaybı kuşağına girmiştir. Buna karşılık iç fiyortlar ve George VI Boğazı'nın ağzı yeşil renkle (Δ > +0.05) gösterilen belirgin bir iklim sığınağı (refugia) özelliği kazanmıştır. Gri alanlar ise iklimsel değişimden istatistiksel olarak etkilenmeyen nötr kararlı bölgeleri temsil etmektedir.")

    story.append(PageBreak())

    # =========================================================================
    # SAYFA 15: TABLO 6, TABLO 7 VE ŞEKİL 7 (BELİRSİZLİK HARİTASI)
    # =========================================================================
    # Tablo 6
    t6_data = [
        [Paragraph("Uygunluk Değişim Eşiği", table_cell_cb), Paragraph("Değişim Sınıfı", table_cell_cb), Paragraph("Hücre Sayısı (703 Hücre)", table_cell_cb), Paragraph("Hücre Oranı (%)", table_cell_cb), Paragraph("Model Alanı Yüzölçümü (km²)", table_cell_cb), Paragraph("Model Alan Payı (%)", table_cell_cb)],
        [Paragraph("±0.025 Puan", table_cell), Paragraph("Azalma / Kararlı / Artış", table_cell), Paragraph("318 / 102 / 283", table_cell_c), Paragraph("%45.2 / %14.5 / %40.3", table_cell_c), Paragraph("95.323 / 27.818 / 79.539", table_cell_c), Paragraph("%47.0 / %13.7 / %39.2", table_cell_c)],
        [Paragraph("<b>±0.05 Puan (Referans)</b>", table_cell_b), Paragraph("<b>Azalma<br/>Kararlı<br/>Artış (Refugia)</b>", table_cell_b), Paragraph("<b>297<br/>163<br/>243</b>", table_cell_cb), Paragraph("<b>%42.2<br/>%23.2<br/>%34.6</b>", table_cell_cb), Paragraph("<b>89.155<br/>45.066<br/>68.460</b>", table_cell_cb), Paragraph("<b>%44.0<br/>%22.2<br/>%33.8</b>", table_cell_cb)],
        [Paragraph("±0.10 Puan", table_cell), Paragraph("Azalma / Kararlı / Artış", table_cell), Paragraph("220 / 290 / 193", table_cell_c), Paragraph("%31.3 / %41.3 / %27.5", table_cell_c), Paragraph("65.777 / 82.600 / 54.303", table_cell_c), Paragraph("%32.5 / %40.8 / %26.8", table_cell_c)],
        [Paragraph("±0.25 Puan (Şiddetli)", table_cell), Paragraph("Azalma / Kararlı / Artış", table_cell), Paragraph("102 / 531 / 70", table_cell_c), Paragraph("%14.5 / %75.5 / %10.0", table_cell_c), Paragraph("30.628 / 151.660 / 20.392", table_cell_c), Paragraph("%15.1 / %74.8 / %10.1", table_cell_c)]
    ]
    t6 = Table(t6_data, colWidths=[90, 85, 80, 80, 100, 70])
    t6.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_HEADER_BG),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t6)
    add_p("Tablo 6. Farklı lojistik değişim eşiklerine göre 2050 yılı habitat değişim sınıflarının duyarlılık dağılımı.", caption)

    # Tablo 7
    t7_data = [
        [Paragraph("Habitat Değişim Sınıfı (±0.05 Eşiği)", table_cell_cb), Paragraph("Hücre Sayısı", table_cell_cb), Paragraph("Yüzde Payı (%)", table_cell_cb), Paragraph("Toplam Yüzölçümü (km²)", table_cell_cb), Paragraph("Baskın Coğrafi Bölge", table_cell_cb)],
        [Paragraph("<b>Habitat Daralması / Kaybı (Δ < -0.05)</b>", table_cell_b), Paragraph("297", table_cell_c), Paragraph("%42.2", table_cell_c), Paragraph("89.155 km²", table_cell_c), Paragraph("Körfez girişi, Adelaide Adası batı/kuzey kıyıları.", table_cell)],
        [Paragraph("<b>Kararlı Alanlar (-0.05 ≤ Δ ≤ +0.05)</b>", table_cell_b), Paragraph("163", table_cell_c), Paragraph("%23.2", table_cell_c), Paragraph("45.066 km²", table_cell_c), Paragraph("Körfezin orta kesimleri ve iç kanal geçişleri.", table_cell)],
        [Paragraph("<b>İklim Sığınağı / Refugia (Δ > +0.05)</b>", table_cell_b), Paragraph("243", table_cell_c), Paragraph("%34.6", table_cell_c), Paragraph("68.460 km²", table_cell_c), Paragraph("George VI Boğazı kuzey ağzı ve güney iç fiyortlar.", table_cell)],
        [Paragraph("<b>TOPLAM MODEL EVRENİ</b>", table_cell_cb), Paragraph("<b>703</b>", table_cell_cb), Paragraph("<b>%100.0</b>", table_cell_cb), Paragraph("<b>202.681 km²</b>", table_cell_cb), Paragraph("Marguerite Körfezi çalışma alanı tamamı.", table_cell)]
    ]
    t7 = Table(t7_data, colWidths=[140, 55, 65, 85, 160])
    t7.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_HEADER_BG),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(Spacer(1, 3))
    story.append(t7)
    add_p("Tablo 7. CMIP6 SSP2-4.5 2050 projeksiyonunda Marguerite Körfezi habitat sınıflarının alan dökümü.", caption)

    add_p("2.6.4. Ekstrapolasyon, Novel Climate ve Clamping Belirsizlik Haritası", subsubsec_head)
    add_p("İklim projeksiyonlarında, gelecekteki çevresel değişkenlerin eğitim verisinde hiç karşılaşılmamış aşırı değerler (novel conditions) üretmesi durumunda modeller güvenilirliğini yitirebilmektedir. MaxEnt, bu tür durumlarda aşırı tahminleri engellemek için değerleri eğitim setinin minimum ve maksimum sınırlarında kırpar (clamping) (Phillips vd., 2006; Elith vd., 2011). Çalışma alanındaki 703 grid hücresinin <b>357 adedinde (%50.8 / 102.500 km²)</b> gelecekte clamping uygulanmıştır (Şekil 7). Clamping işlemlerinin tamamı, artan deniz yüzeyi sıcaklığı (SST) ve sıvı yağış (Bio18) değişkenlerinin üst sınırları aşmasından kaynaklanmıştır. Bu bulgu; gelecekteki habitat değişim tahminlerinin körfezin iç korunaklı alanlarında yüksek kesinliğe sahip olduğunu, ancak körfezin kuzeybatısındaki açık deniz alanlarında oşinografik ekstrapolasyon belirsizliğinin arttığını göstermektedir.")

    p_map4 = "/home/halil/adelie-maxent-2204c/harita/cmip6_ipsl_2050_v1/belirsizlik_A4.png"
    if os.path.exists(p_map4):
        img_m4 = Image(p_map4, width=380, height=220)
        story.append(KeepTogether([img_m4, Paragraph("Şekil 7. 2050 CMIP6 projeksiyonu için Çok Değişkenli Çevresel Benzerlik Yüzeyi (MESS), ekstrapolasyon ve Clamping belirsizlik haritası (Kırmızı pikseller: Eğitim sınırını aşan novel climate hücreleri).", caption)]))
        md_content.append(f"\n![Şekil 7. Belirsizlik Haritası]({p_map4})\n*Şekil 7. Ekstrapolasyon ve Clamping belirsizlik haritası.*\n")

    story.append(PageBreak())

    # =========================================================================
    # SAYFA 16: SONUÇ VE TARTIŞMA
    # =========================================================================
    add_p("Sonuç ve Tartışma", sec_head)
    add_p("Bu araştırmada, Batı Antarktika Yarımadası'nın en hassas denizel ekosistemlerinden biri olan Marguerite Körfezi'nde Adélie pengueninin (<i>Pygoscelis adeliae</i>) günümüz ve 2050 yılı potansiyel habitat uygunluğu ilk kez yüksek çözünürlüklü ERA5 yeniden analizleri, REMA topoğrafyası ve CMIP6 IPSL-CM6A-LR iklim projeksiyonları ile modellenmiştir. Elde edilen bulgular, kutup ekolojisi literatüründeki temel teorik hipotezleri doğrulamakta ve küresel iklim krizinin bölgesel etkilerine dair çarpıcı sayısal kanıtlar sunmaktadır.")
    add_p("Model sonuçlarında yıllık deniz buzu konsantrasyonunun %55.6 permütasyon önemi ile birincil belirleyici çıkması, Adélie pengueninin tam anlamıyla deniz buzuna bağımlı (sea-ice obligate) bir tepe avcı olduğunu ortaya koyan temel ekolojik literatürle (Ainley, 2002; Fraser & Hofmann, 2003) tam uyum içerisindedir. Tepki eğrilerinde görülen %40–%60 optimum deniz buzu aralığı; penguenlerin avlandığı kril (<i>Euphausia superba</i>) sürülerinin buz altı algleriyle beslenmesi için yeterli buz örtüsüne ihtiyaç duymasını, ancak aynı zamanda dalış yapabilmek ve nefes alabilmek için açık su çatlaklarına (lead) ve polinyalara gereksinim duymasını yansıtmaktadır. Aşırı buz örtüsünde (>%85) avlanma veriminin düşmesi, açık suda (<%20) ise avın tamamen kaybolması bu biyo-oşinografik dengenin hassasiyetini kanıtlamaktadır.")
    add_p("Giriş bölümünde incelenen en güncel uluslararası çalışma olan <b>Wang, Hu ve Yang'ın (2026, PMID: 42209243 - <i>Ying Yong Sheng Tai Xue Bao</i>)</b> tüm Antarktika ölçeğindeki MaxEnt ve CMIP6 bulgularıyla karşılaştırıldığında; Wang vd. (2026), alt-Antarktika adaları ile Kuzey Antarktika Yarımadası'ndaki kolonilerin yüzyılın ortasına kadar çökeceğini ve türün çekirdek popülasyonlarının Ross Denizi ve Doğu Antarktika kıyılarına çekileceğini öngörmüşlerdir. Bizim mikro-ölçekli çalışmamız, bu makro tezi doğrulamakla birlikte, Marguerite Körfezi ölçeğinde çok kritik bir bölgesel ayrıntıyı aydınlatmıştır: Körfez genelinde %42.2 oranında (89.155 km²) şiddetli bir habitat daralması yaşanacak olmasına rağmen, körfezin güneyindeki derin fiyortların ve George VI Boğazı girişinin <b>%34.6 oranında (68.460 km²) potansiyel bir iklim sığınağı (refugia)</b> işlevi göreceği tespit edilmiştir. Bu durum; kalın ana kara buzullarının soğutucu etkisiyle yerel mikroklimasını koruyan güney kıyılarının, türün Batı Antarktika Yarımadası'ndaki son kalelerinden biri olabileceğini kanıtlamaktadır.")
    add_p("Çalışmamızın ortaya koyduğu bir diğer kritik sonuç, kuluçka dönemi yaz yağışlarının (<i>bio18</i>) %17.1'lik önem derecesidir. Chapman vd. (2011) ve Massom vd. (2006) tarafından teorik olarak vurgulanan sıvı yağmur ve ıslak karın civciv ölümlerine yol açma riski, modelimizde 300 mm yağış eşiğinden sonra habitat uygunluğunun dikey bir düşüşle sıfırlanmasıyla matematiksel olarak teyit edilmiştir. CMIP6 projeksiyonunda atmosferik ısınmayla birlikte kar yağışlarının sıvı yağmura dönüşmesi, körfezin kuzey adalarındaki kolonilerin üreme başarısını fiziksel olarak imkansız hale getirecektir.")
    add_p("Roberts vd. (2017) yaklaşımıyla gerçekleştirdiğimiz 4 enlem bandı mekânsal blok çapraz doğrulama (Spatial Block CV) testleri ise ekolojik modelleme metodolojisi açısından evrensel bir uyarı niteliğindedir. Standart rastgele kat bölmelerinde 0.715–0.765 bandında yüksek çıkan AUC değerleri, coğrafi enlemler ayrıştırıldığında 0.477–0.580 bandına kadar gerilemiştir. Rastgele katlarda eğitim ve test noktaları arasındaki ortalama mesafe 12.6 km iken mekânsal tasarımda 45.4 km'ye fırlamakta ve omission oranı %56.7'ye tırmanmaktadır. Bu sonuç; yerel fiyort ve ada topografyasının yarattığı mikroklimanın genel modeller tarafından kolayca genellenemeyeceğini ve geleceğe yönelik iklim projeksiyonlarında mekânsal otokorelasyon denetlenmeden üretilen haritaların yanıltıcı olabileceğini göstermektedir.")

    story.append(PageBreak())

    # =========================================================================
    # SAYFA 17: SONUÇ TARTIŞMA SONU VE ÖNERİLER
    # =========================================================================
    add_p("Son olarak, 2050 iklim projeksiyonunda 357 hücrede (%50.8) karşılaşılan Clamping (ekstrapolasyon) olgusu; IPCC AR6 SSP2-4.5 senaryosunda öngörülen deniz suyu ısınması ve yağış artışının, günümüz ekolojik sınırlarını tamamen aşan 'yeni iklim koşulları' (novel climate) yaratacağını belgelemektedir. Bu nedenle, iklim koruma politikaları geliştirilirken bu belirsizlik alanları dikkate alınmalıdır. Sonuç olarak, Marguerite Körfezi Adélie penguenleri için gelecekte çift yönlü bir kader çizmektedir: Körfez girişindeki koloniler yok olma eşiğine gelirken, güney fiyortları türün genetik havuzunu koruyacak stratejik sığınaklar haline gelecektir.")

    add_p("Öneriler", sec_head)
    add_p("Bu araştırma kapsamında elde edilen bulgular doğrultusunda, ulusal ve uluslararası kutup araştırmaları ve çevre koruma politikaları için şu stratejik öneriler geliştirilmiştir:", body_bold)
    add_p("1. <b>TÜBİTAK MAM Kutup Araştırmaları Enstitüsü (KARE) ve Ulusal Seferler (TAE):</b> Türkiye'nin düzenlediği Ulusal Antarktika Bilim Seferleri (TAE) kapsamında, Marguerite Körfezi'nin güneyinde model tarafından iklim sığınağı (refugia) olarak belirlenen George VI Boğazı ve iç fiyort bölgelerine yönelik denizel biyo-çeşitlilik ve penguen koloni izleme seferleri planlanmalıdır.", bullet)
    add_p("2. <b>GPS Telemetri ve Uydu Vericileri ile İzleme:</b> Modelin mekânsal aktarılabilirlik kısıtlarını gidermek ve fiyort içi göç koridorlarını doğrulamak amacıyla, Marguerite Körfezi'ndeki Adélie pengueni kolonilerine uydu bağlantılı GPS telemetri cihazları takılarak bireylerin gerçek zamanlı kışlama ve avlanma rotaları haritalandırılmalıdır.", bullet)
    add_p("3. <b>Deniz Koruma Alanları (MPA) ve CCAMLR Düzenlemeleri:</b> Antarktika Deniz Yaşamı Kaynaklarının Korunması Komisyonu (CCAMLR) nezdinde, 2050 yılına kadar habitat kaybı yaşanacağı öngörülen körfez girişinde endüstriyel kril (<i>Euphausia superba</i>) avcılığına katı kotalar getirilmeli; iklim sığınağı olan güney fiyortları ise 'Özel Korunan Antarktika Alanı' (ASPA) statüsüne alınmalıdır.", bullet)
    add_p("4. <b>İHA / Drone ve Yüksek Çözünürlüklü Optik Uydu Görüntüleri ile Koloni Büyüklüğü Takibi:</b> Ulaşımı son derece güç olan fiyort adacıklarındaki koloni popülasyonlarının tespiti için Sentinel-2, WorldView uyduları ve insansız hava araçları (İHA) ile guano (dışkı) lekesi analizi ve otomatik sayım algoritmaları devreye sokulmalıdır.", bullet)
    add_p("5. <b>Otomatik Meteoroloji İstasyonları (AWS) ile Yerel Yağış İzleme:</b> Kuluçka döneminde civciv ölümlerine yol açan aşırı sıvı yağış ve ıslak kar olaylarının erken tespiti için körfez kıyısındaki üreme kolonilerine gerçek zamanlı mikroklimatik otomatik meteoroloji istasyonları (AWS) kurulmalıdır.", bullet)

    story.append(PageBreak())

    # =========================================================================
    # SAYFA 18: KAYNAKLAR
    # =========================================================================
    add_p("Kaynaklar", sec_head)

    refs = [
        "Ainley, D. G. (2002). <i>The Adélie Penguin: Bellwether of Climate Change</i>. Columbia University Press, New York. https://doi.org/10.7312/ainl12304",
        "Atkinson, A., Siegel, V., Pakhomov, E., & Rothery, P. (2004). Long-term serious decline in Antarctic krill stock and increase in salps in Southern Ocean. <i>Nature</i>, 432(7013), 100–103. https://doi.org/10.1038/nature02996",
        "Chapman, E. W., Hofmann, E. E., Patterson, D. L., & Fraser, W. R. (2011). The effects of climate change on normal and anomalous weather conditions in the Western Antarctic Peninsula: Consequences for Adélie penguin populations. <i>Marine Ecology Progress Series</i>, 429, 247–260. https://doi.org/10.3354/meps09108",
        "Cimino, M. A., Lynch, H. J., Saba, V. S., & Oliver, M. J. (2016). Projected asymmetric response of Adélie penguins to Antarctic climate change. <i>Scientific Reports</i>, 6, 28785. https://doi.org/10.1038/srep28785",
        "Dormann, C. F., Elith, J., Bacher, S., Buchmann, C., Carl, G., Carré, G., Marquéz, J. R. G., Gruber, B., Lafourcade, B., Leitão, P. J., Münkemüller, T., McClean, C., Osborne, P. E., Reineking, B., Schröder, B., Skidmore, A. K., Zurell, D., & Lautenbach, S. (2013). Collinearity: A review of methods to deal with it and a simulation study evaluating their performance. <i>Ecography</i>, 36(1), 27–46. https://doi.org/10.1111/j.1600-0587.2012.07348.x",
        "Ducklow, H. W., Baker, K., Martinson, D. G., Quetin, L. B., Ross, R. M., Smith, R. C., Stammerjohn, S. E., Vernet, M., & Fraser, W. (2007). Marine ecosystems: The West Antarctic Peninsula. <i>Philosophical Transactions of the Royal Society B: Biological Sciences</i>, 362(1477), 67–94. https://doi.org/10.1098/rstb.2006.1955",
        "Elith, J., Phillips, S. J., Hastie, T., Dudík, M., Chee, Y. E., & Yates, C. J. (2011). A statistical explanation of MaxEnt for ecologists. <i>Diversity and Distributions</i>, 17(1), 43–57. https://doi.org/10.1111/j.1472-4642.2010.00725.x",
        "Fielding, A. H., & Bell, J. F. (1997). A review of methods for the assessment of prediction errors in conservation presence/absence models. <i>Environmental Conservation</i>, 24(1), 38–49. https://doi.org/10.1017/S0376892997000088",
        "Fraser, W. R., & Hofmann, E. E. (2003). A predator's perspective on causal links between climate change, physical forcing and ecosystem response. <i>Marine Ecology Progress Series</i>, 265, 1–15. https://doi.org/10.3354/meps265001",
        "Fretwell, P. T., Trathan, P. N., Wienecke, B., & Kooyman, G. L. (2014). Emperor penguin colonies: Population and distribution in Antarctica using satellite imagery. <i>Polar Biology</i>, 37(5), 699–711. https://doi.org/10.1007/s00300-014-1471-4",
        "IPCC. (2021). <i>Climate Change 2021: The Physical Science Basis. Contribution of Working Group I to the Sixth Assessment Report of the Intergovernmental Panel on Climate Change</i>. Cambridge University Press, Cambridge, United Kingdom and New York, NY, USA. https://doi.org/10.1017/9781009157896",
        "Jenouvrier, S., Che-Castaldo, J., Brierley, A. S., Ainley, D. G., & Trathan, P. N. (2021). The call of the emperor penguin: Legal responses to species threatened by climate change. <i>Global Change Biology</i>, 27(19), 5008–5022. https://doi.org/10.1111/gcb.15806",
        "Liu, C., Berry, P. M., Dawson, T. P., & Pearson, R. G. (2005). Selecting thresholds of occurrence in the prediction of species distributions. <i>Journal of Biogeography</i>, 32(1), 51–63. https://doi.org/10.1111/j.1365-2699.2004.01149.x",
        "Lyver, P. O. B., Barron, M., Barton, K. J., Ainley, D. G., Pollard, A., Gordon, S., McNeill, S., & Ballard, G. (2014). Trends in the breeding population of Adélie penguins in the Ross Sea, 1981–2012: A review. <i>PLOS ONE</i>, 9(10), e111244. https://doi.org/10.1371/journal.pone.0111244",
        "Massom, R. A., Stammerjohn, S. E., Smith, R. C., Pook, M. J., Iannuzzi, R. A., Adams, N., & Fraser, W. R. (2006). Extreme anomalous atmospheric circulation in the West Antarctic Peninsula region in Austral spring and summer 2001/02, and its ecological consequences. <i>Antarctic Science</i>, 18(3), 403–418. https://doi.org/10.1017/S0954102006000454",
        "Phillips, S. J., Anderson, R. P., & Schapire, R. E. (2006). Maximum entropy modeling of species geographic distributions. <i>Ecological Modelling</i>, 190(3–4), 231–259. https://doi.org/10.1016/j.ecolmodel.2005.03.026",
        "Rignot, E., Mouginot, J., Scheuchl, B., van den Broeke, M., van Wessem, M. J., & Morlighem, M. (2019). Four decades of Antarctic Ice Sheet mass balance from 1979–2017. <i>Proceedings of the National Academy of Sciences</i>, 116(4), 1095–1103. https://doi.org/10.1073/pnas.1812883116",
        "Roberts, D. R., Bahn, V., Ciuti, S., Boyce, M. S., Elith, J., Guillera-Arroita, G., Hauenstein, S., Lahoz-Monfort, J. J., Schröder, B., Thuiller, W., Warton, D. I., Wintle, B. A., Hartig, F., & Dormann, C. F. (2017). Cross-validation strategies for data with spatial, temporal, or phylogenetic structure. <i>Ecography</i>, 40(8), 913–929. https://doi.org/10.1111/ecog.02881",
        "Southwell, C., Emmerson, L., McKinlay, J., Newbery, K., Takahashi, A., Kato, A., & Trathan, P. (2015). Spatially extensive standardized surveys reveal widespread, stable abundance of an Antarctic top predator. <i>Diversity and Distributions</i>, 21(1), 23–33. https://doi.org/10.1111/ddi.12260",
        "Stammerjohn, S. E., Martinson, D. G., Smith, R. C., & Iannuzzi, R. A. (2008). Sea ice in the western Antarctic Peninsula region: Spatio-temporal variability from ecological and climatological perspectives. <i>Deep Sea Research Part II: Topical Studies in Oceanography</i>, 55(18–19), 2041–2058. https://doi.org/10.1016/j.dsr2.2008.04.026",
        "Stammerjohn, S., Massom, R., Rind, D., & Martinson, D. (2012). Regions of rapid sea ice change: An inter-hemispheric seasonal comparison. <i>Geophysical Research Letters</i>, 39(6), L06501. https://doi.org/10.1029/2012GL050874",
        "Swets, J. A. (1988). Measuring the accuracy of diagnostic systems. <i>Science</i>, 240(4857), 1285–1293. https://doi.org/10.1126/science.3287615",
        "Trivelpiece, W. Z., Hinke, J. T., Miller, A. K., Reiss, C. S., Trivelpiece, S. G., & Watters, G. M. (2011). Variability in krill biomass links harvesting and climate warming to penguin population declines in Antarctica. <i>Proceedings of the National Academy of Sciences</i>, 108(18), 7625–7628. https://doi.org/10.1073/pnas.1016560108",
        "Turner, J., Barrand, N. E., Bradbury, W. M., Chelliah, M., Garabato, A. C. N., & Phillips, T. (2014). Antarctic climate change and the environment: An update. <i>Polar Record</i>, 50(3), 237–259. https://doi.org/10.1017/S0032247413000296",
        "Turner, J., Lu, H., White, I., King, J. C., Phillips, T., Hosking, J. S., Bracegirdle, T. J., Marshall, G. J., Mulvaney, R., & Deb, P. (2016). Absence of 21st century warming on Antarctic Peninsula consistent with natural variability. <i>Nature</i>, 535(7612), 411–415. https://doi.org/10.1038/nature18645",
        "Wang, J., Hu, M., & Yang, J. (2026). Predicting the potential distribution of Pygoscelis adeliae in Antarctica based on MaxEnt and CMIP6 models. <i>Ying Yong Sheng Tai Xue Bao (The Journal of Applied Ecology)</i>, 37(3), 839–848. https://doi.org/10.13287/j.1001-9332.202603.028 [PMID: 42209243]"
    ]

    for ref in refs:
        add_p(ref, ref_style)

    # Markdown dosyasını kaydet
    with open(out_md, 'w', encoding='utf-8') as f:
        f.writelines(md_content)
    print(f"Markdown report generated: {out_md}")

    # PDF oluştur
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Raw PDF built: {raw_pdf}")

    # Cairo ile sanitize et (CUPS filtresi ve baskı uyumu için şart)
    cairo_cmd = f"pdftocairo -pdf {raw_pdf} {final_pdf}"
    res = subprocess.run(cairo_cmd, shell=True, capture_output=True, text=True)
    if res.returncode == 0:
        print(f"Sanitized PDF generated successfully: {final_pdf}")
        if os.path.exists(raw_pdf):
            os.remove(raw_pdf)
    else:
        print(f"Cairo error: {res.stderr}")

if __name__ == '__main__':
    build_report()
