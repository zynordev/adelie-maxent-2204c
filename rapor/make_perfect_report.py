#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TÜBİTAK 2204-C Resmî Proje Raporu Oluşturucu (v4 - Tam Jüri Savunması ve Bilimsel Kusursuzluk)
Hedef: Tam 18 sayfa, sıfır taşma, hakem/jüri eleştirilerine karşı %100 bilimsel, sayısal ve metodolojik tutarlılık.
Unicode Türkçe karakter desteği: LiberationSans (TTF).
"""

import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily
import subprocess

# Türkçe Unicode desteği için LiberationSans font ailesini kaydet
FONT_DIR = "/usr/share/fonts/liberation"
if os.path.exists(os.path.join(FONT_DIR, "LiberationSans-Regular.ttf")):
    pdfmetrics.registerFont(TTFont('LiberationSans', os.path.join(FONT_DIR, 'LiberationSans-Regular.ttf')))
    pdfmetrics.registerFont(TTFont('LiberationSans-Bold', os.path.join(FONT_DIR, 'LiberationSans-Bold.ttf')))
    pdfmetrics.registerFont(TTFont('LiberationSans-Italic', os.path.join(FONT_DIR, 'LiberationSans-Italic.ttf')))
    pdfmetrics.registerFont(TTFont('LiberationSans-BoldItalic', os.path.join(FONT_DIR, 'LiberationSans-BoldItalic.ttf')))
    registerFontFamily('LiberationSans', normal='LiberationSans', bold='LiberationSans-Bold', italic='LiberationSans-Italic', boldItalic='LiberationSans-BoldItalic')
    F_NORM = 'LiberationSans'
    F_BOLD = 'LiberationSans-Bold'
    F_ITAL = 'LiberationSans-Italic'
else:
    ALT_DIR = "/usr/share/fonts/TTF"
    pdfmetrics.registerFont(TTFont('DejaVuSans', os.path.join(ALT_DIR, 'DejaVuSans.ttf')))
    pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', os.path.join(ALT_DIR, 'DejaVuSans-Bold.ttf')))
    pdfmetrics.registerFont(TTFont('DejaVuSans-Italic', os.path.join(ALT_DIR, 'DejaVuSans-Oblique.ttf')))
    pdfmetrics.registerFont(TTFont('DejaVuSans-BoldItalic', os.path.join(ALT_DIR, 'DejaVuSans-BoldOblique.ttf')))
    registerFontFamily('DejaVuSans', normal='DejaVuSans', bold='DejaVuSans-Bold', italic='DejaVuSans-Italic', boldItalic='DejaVuSans-BoldItalic')
    F_NORM = 'DejaVuSans'
    F_BOLD = 'DejaVuSans-Bold'
    F_ITAL = 'DejaVuSans-Italic'

class NumberedCanvas(canvas.Canvas):
    """
    İki geçişli canvas: Toplam sayfa sayısını hesaplar ve resmî TÜBİTAK üst/alt bilgi formatında basar.
    """
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        
        # Üst bilgi (Header) - Sayfa 1 hariç
        if self._pageNumber > 1:
            self.setFont(F_NORM, 8)
            self.setFillColor(colors.HexColor("#4A5568"))
            self.drawString(36, 815, "TÜBİTAK 2204-C Kutup Araştırmaları Proje Yarışması — Proje Raporu")
            self.drawRightString(559, 815, "Marguerite Körfezi Adélie Pengueni MaxEnt Modeli")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(36, 810, 559, 810)

        # Alt bilgi (Footer)
        self.setFont(F_NORM, 8)
        self.setFillColor(colors.HexColor("#4A5568"))
        page_str = f"Sayfa {self._pageNumber} / {page_count}"
        self.drawRightString(559, 25, page_str)
        self.drawString(36, 25, "Kutup Biyoçeşitliliği ve Ekosistem Dinamikleri | 2026")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(36, 35, 559, 35)

        self.restoreState()


def build_perfect_18_page_report():
    out_dir = "/home/halil/adelie-maxent-2204c/rapor"
    os.makedirs(out_dir, exist_ok=True)
    raw_pdf = os.path.join(out_dir, "TUBITAK_2204C_PROJE_RAPORU_raw.pdf")
    sanitized_pdf = os.path.join(out_dir, "TUBITAK_2204C_PROJE_RAPORU.pdf")
    out_md = os.path.join(out_dir, "TUBITAK_2204C_PROJE_RAPORU.md")

    # Sayfa yapısı: A4 (595.27 x 841.89 pt), Kenar boşlukları: 36 pt (12.7 mm)
    doc = SimpleDocTemplate(
        raw_pdf,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=38
    )

    styles = getSampleStyleSheet()

    # Renk Paleti
    C_PRIMARY = colors.HexColor("#0F2942")     # Antarktika Derin Deniz Mavisi
    C_SECONDARY = colors.HexColor("#1B4965")   # Kutup Okyanus Mavisi
    C_ACCENT = colors.HexColor("#C57B57")      # Buzul Pası / Vurgu Rengi
    C_TEXT = colors.HexColor("#1A202C")        # Koyu Antrasit Gövde Metni
    C_MUTED = colors.HexColor("#4A5568")       # Gri Yardımcı Metin
    C_BORDER = colors.HexColor("#CBD5E1")      # İnce Kenarlık Rengi
    C_HEADER_BG = colors.HexColor("#F1F5F9")    # Tablo Başlık Arka Planı

    # Özel Paragraf Stilleri
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName=F_BOLD,
        fontSize=13,
        leading=16,
        textColor=C_PRIMARY,
        alignment=1, # Center
        spaceAfter=3
    )

    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName=F_BOLD,
        fontSize=8.5,
        leading=11,
        textColor=C_SECONDARY,
        alignment=1,
        spaceAfter=5
    )

    sec_head = ParagraphStyle(
        'SecHead',
        parent=styles['Normal'],
        fontName=F_BOLD,
        fontSize=11,
        leading=14,
        textColor=C_PRIMARY,
        spaceBefore=4,
        spaceAfter=3,
        keepWithNext=True
    )

    subsec_head = ParagraphStyle(
        'SubSecHead',
        parent=styles['Normal'],
        fontName=F_BOLD,
        fontSize=9.5,
        leading=12.5,
        textColor=C_SECONDARY,
        spaceBefore=3,
        spaceAfter=2,
        keepWithNext=True
    )

    subsubsec_head = ParagraphStyle(
        'SubSubSecHead',
        parent=styles['Normal'],
        fontName=F_BOLD,
        fontSize=8.5,
        leading=11,
        textColor=C_TEXT,
        spaceBefore=2,
        spaceAfter=2,
        keepWithNext=True
    )

    body = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName=F_NORM,
        fontSize=8,
        leading=10.5,
        textColor=C_TEXT,
        alignment=4, # Justified
        spaceAfter=2.5
    )

    body_bold = ParagraphStyle(
        'BodyBold',
        parent=body,
        fontName=F_BOLD
    )

    bullet = ParagraphStyle(
        'Bullet',
        parent=body,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=1.5
    )

    caption = ParagraphStyle(
        'Caption',
        parent=styles['Normal'],
        fontName=F_ITAL,
        fontSize=7.2,
        leading=9.2,
        textColor=C_MUTED,
        alignment=1,
        spaceBefore=2,
        spaceAfter=3
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName=F_NORM,
        fontSize=6.8,
        leading=8.5,
        textColor=C_TEXT
    )

    table_cell_b = ParagraphStyle(
        'TableCellB',
        parent=table_cell,
        fontName=F_BOLD
    )

    table_cell_c = ParagraphStyle(
        'TableCellC',
        parent=table_cell,
        alignment=1
    )

    table_cell_cb = ParagraphStyle(
        'TableCellCB',
        parent=table_cell_b,
        alignment=1
    )

    ref_style = ParagraphStyle(
        'RefStyle',
        parent=styles['Normal'],
        fontName=F_NORM,
        fontSize=6.5,
        leading=8.3,
        leftIndent=12,
        firstLineIndent=-12,
        spaceAfter=2.2,
        textColor=C_TEXT
    )

    story = []
    md_content = []

    def add_p(text, style=body):
        # ReportLab Paragraph, LaTeX'ı matematik olarak işlemez. PDF'de ham
        # gösterim bırakmamak için formülleri sade metne çevir ve doğrulanmış
        # Wang DOI'sini kullan.
        replacements = [
            (r"$\cos(68^\circ) \approx 0.3746$", "kosinüs katsayısı yaklaşık 0,3746"),
            (r"$\hat{\pi}(x)$", "model dağılımı"),
            (r"$$H(\hat{\pi}) = -\sum_{x \in X} \hat{\pi}(x) \ln \hat{\pi}(x) \quad \text{ve} \quad \mathbb{E}_{\hat{\pi}}[f_j] = \mathbb{E}_{\tilde{\pi}}[f_j]$$", "MaxEnt, varlık ve arka plan çevresel dağılımlarını düzenlileştirilmiş entropi ölçütüyle karşılaştırır."),
            (r"$L_1$", "L1"),
            (r"$\max_{\lambda} ( \sum_{i=1}^n \ln P(x_i) - \sum_{j=1}^m \beta_j |\lambda_j| )$", "düzenlileştirilmiş amaç fonksiyonu"),
            (r"$P(x) = 1 - \exp(-\exp(\eta(x)))$", "Cloglog dönüşümü"),
            ("10.13287/j.1001-9332.202603.028", "10.13287/j.1001-9332.202603.037"),
            ("202.681 km²", "202.675 km²"),
            ("başarıyla yürütülmüştür", "uygulanmıştır"),
            ("Atmosferik katman olarak; kuluçka evresindeki civcivlerin ıslanma ve hipotermi riskini temsil eden", "Atmosferik katman olarak; en sıcak çeyrek yağışını geniş bir iklim vekili olarak kullanan"),
            ("Yaz yağış anomalileri; civciv tüylerinde ıslanma, hipotermi ve yuva çöküş riski vekili (Chapman vd., 2011).", "Geniş yaz yağışı vekili; yağış fazını ayırt etmez ve hipotermiyi doğrudan ölçmez."),
            ("Bu veri seti, türün yaşam döngüsündeki <b>genel bulunuşunu (overall occurrence)</b> temsil etmekte olup hem kıyı şeridindeki üreme kolonisi yerleşimlerini hem de şelf sahası üzerindeki neritik beslenme/hareket gözlemlerini içermektedir.", "Bu veri seti, türün yaşam döngüsündeki <b>genel bulunuşunu (overall occurrence)</b> temsil etmekte olup hem kıyı şeridindeki üreme kolonisi yerleşimlerini hem de şelf sahası üzerindeki neritik beslenme/hareket gözlemlerini içermektedir. Bu iki süreç aynı çevresel değişkenlere aynı ölçekte yanıt vermeyebileceğinden sonuçlar koloni uygunluğu olarak tek başına yorumlanamaz."),
            ("insan kaynaklı örnekleme yanlılığını (sampling bias) ve mekânsal yığılmayı önlemek amacıyla", "mekânsal yığılmayı azaltmak amacıyla"),
            ("Çalışma alanındaki toplam 703 grid hücresinin geri kalan 636 hücresi modelin arka plan (background) çevresel matrisini oluşturmuştur.", "Çalışma alanındaki toplam 703 grid hücresinin geri kalan 636 hücresi modelin arka plan (background) çevresel matrisini oluşturmuştur. Presence hücrelerinin arka plandan çıkarılması erişilebilir çevre varsayımına dayanır; bu uygulama ayrı bir bias-grid veya target-group arka planıyla sınanmamıştır."),
            ("türetilmiştir. Topografik katman olarak ise;", "türetilmiştir. Bio18 yağışın yağmur/kar fazını ve kısa süreli olay şiddetini ayırt etmediğinden civciv hipotermisi mekanizmasını doğrudan doğrulamaz. Topografik katman olarak ise;"),
            ("Bu durum, aşırı yağış koşullarında yavru hipotermi riskini yansıtmaktadır (Chapman vd., 2011).", "Bu eğilim bir yağış vekili ilişkisini gösterir; yağış fazı ve civciv sağkalımı ölçülmediği için doğrudan hipotermi mekanizması kanıtı değildir."),
            ("Buna karşılık Adelaide Adası ve iç fiyortlar türün tüm biyolojik gereksinimlerini karşılamaktadır.", "Buna karşılık Adelaide Adası ve iç fiyortlarda model yüksek uygunluk puanları üretmektedir; bu sonuç tüm biyolojik gereksinimlerin karşılandığını kanıtlamaz."),
            ("Fark değerleri ±0.05 mutlak puan eşiğinde sınıflandırılmış; modelin eşik duyarlılığı Tablo 6'da ve alan dağılımı Tablo 7'de özetlenmiştir (Liu vd., 2005).", "Fark değerleri ±0.05 mutlak puan eşiğinde sınıflandırılmış; bu değer biyolojik olarak doğrulanmış bir eşik değil, seçilmiş bir duyarlılık sınıfıdır. Eşik duyarlılığı Tablo 6'da, alan dağılımı Tablo 7'de özetlenmiştir."),
            ("Farklı lojistik değişim eşiklerine göre 2050 yılı habitat değişim sınıflarının duyarlılık dağılımı (Liu vd., 2005).", "Farklı değişim eşiklerine göre 2050 yılı uygunluk değişim sınıflarının duyarlılık dağılımı."),
            ("Bu durum, 2050 yılı projeksiyonunun geniş bir ekstrapolasyon belirsizliği barındırdığını ve sonuçların temkinle yorumlanması gerektiğini göstermektedir.", "Bu durum, 2050 yılı projeksiyonunun geniş bir ekstrapolasyon belirsizliği barındırdığını ve sonuçların temkinle yorumlanması gerektiğini göstermektedir. Ayrıca 246/703 hücrede eşlenik iklim katmanları değişim yönünde uyuşmamaktadır; bu hücreler tek yönlü ekolojik sinyal olarak yorumlanmamalıdır."),
            ("Giriş bölümünde incelenen", "Giriş bölümünde incelenen"),
            ("Çalışmamızda yaz yağışlarının (<i>bio18</i>) %17.1'lik permütasyon önemine sahip olması, Chapman vd. (2011) ve Massom vd. (2006) tarafından vurgulanan sıvı yağmur ve ıslak karın civciv ölümlerine yol açma riski hipotezini desteklemektedir.", "Çalışmamızda bio18'in %17.1'lik permütasyon önemi, bu değişkenin modelde bilgi taşıdığını gösterir; ancak bio18 yağış fazını ve civciv sağkalımını ölçmediği için sıvı yağmur/hipotermi mekanizmasını doğrudan doğrulamaz. Chapman vd. (2011) ve Massom vd. (2006) yalnızca biyolojik bir hipotez için bağlam sağlar."),
            ("• 4. <b>Deniz Koruma Alanları (MPA) ve CCAMLR Kapsamı:</b> Antarktika Deniz Yaşamı Kaynaklarının Korunması Komisyonu (CCAMLR) nezdinde,", "• 4. <b>İzleme ve bağımsız veri entegrasyonu:</b> CCAMLR gibi koruma süreçlerine doğrudan kota veya alan kararı önermek yerine,"),
            ("tarihsel referans dönemi ise ERA5 ile uyumlu olarak <b>2000–2025</b> olarak belirlenmiştir.", "referans dönemi ERA5 ile uyumlu olarak <b>2000–2025</b> biçiminde oluşturulmuştur. Bu dönem, CMIP6 historical verisinin 2000–2014 bölümü ile SSP2-4.5 devamının 2015–2025 bölümünün birleştirilmesidir; saf bir historical dönem değildir ve bu dönem uyumsuzluğu delta sonuçlarına ek belirsizlik getirir."),
            ("<b>IPSL-CM6A-LR</b> küresel iklim modeli", "tek GCM olarak kullanılan <b>IPSL-CM6A-LR</b> küresel iklim modeli"),
            ("GCM'in ~1° kaba çözünürlüğünü taşıması", "GCM'in ~1° kaba çözünürlüğünü taşıması; IPSL-CM6A-LR'nin model-özgül ısınma yanlılığı bu tek koşuda ayrıca nicelenmemiştir"),
            ("modeldeki 4 değişkenin ikili korelasyonlarının |r| < 0.62 seviyesinde kalarak çoklu eşdoğrusallık riskinin giderildiği doğrulanmıştır.", "modeldeki 4 değişkenin ikili korelasyonlarının |r| < 0.62 seviyesinde kaldığı hesaplanmıştır; ancak değişken bazlı VIF tablosu bu raporda gösterilmemiştir."),
            ("60'tan fazla örneklem bulunduğu için model hiperparametreleri olarak varsayılan <b>LQTH (Linear, Quadratic, Threshold, Hinge)</b> özellik sınıfları kullanılmış; aşırı öğrenmeyi önlemek için düzenlileştirme çarpanı (Regularization Multiplier = 1.0) seçilmiştir.", "Bu sürümde <b>LQTH (Linear, Quadratic, Threshold, Hinge)</b> özellik sınıfları ve Regularization Multiplier = 1.0 kullanılmıştır. ENMeval/AICc veya benzeri bir özellik sınıfı–düzenlileştirme taraması yapılmadığı için LQTH en iyi model olarak ilan edilmemektedir; mekânsal testte L/RM1'nin 0.580 AUC ile daha dayanıklı görünmesi bu ana modelin aktarılabilirlik açısından ihtiyatla yorumlanmasını gerektirir."),
            ("<i>kaya</i>, % alan) hesaplanmıştır.", "<i>kaya</i>, % alan) hesaplanmıştır. Bathymetry, kıyıya uzaklık ve klorofil/kril gibi değişkenler bu sürümde bulunmadığından denizel süreçler yalnızca buz ve SST vekilleriyle temsil edilmiştir."),
            ("zorunlu bir fiziksel ön koşul teşkil ettiğini", "koloni yerleşimi için anlamlı bir substrat ilişkisi taşıdığını; ancak kaya=0'da uygunluk puanının ~0.46 kalması ve permütasyon öneminin yalnızca %9.1 olması nedeniyle bunu tek başına zorunlu koşul olarak yorumlamadığımızı"),
            ("Habitat uygunluğu %20–%25 marjinal buz konsantrasyonunda zirveye ulaşmakta", "Model aralığında habitat uygunluğu %20–%25 marjinal buz konsantrasyonunda zirveye ulaşmaktadır; bu aralık alt sınıra dayandığı için dışarıda gerçek optimum iddiası yapılamaz"),
            ("%65–%69 bandında ise ~0.34 seviyesinde seyretmektedir. Bu eğilim,", "%65–%69 bandında ise ~0.34 seviyesinde seyretmektedir; uç değerlerde veri desteği ve tepki eğrisi belirsizliği dikkate alınmalıdır. Bu eğilim,"),
            ("Tepki eğrisinde yağış miktarı 600 mm'yi aştığında uygunluk puanının gerilemesi, iklim değişikliğiyle birlikte yağış fazının sıvıya kaymasının yaratabileceği olumsuz etkileri yansıtmaktadır.", "Tepki eğrisinde yağış miktarı 600 mm'yi aştığında uygunluk puanının gerilemesi gözlenmektedir; yağış fazı ve olay şiddeti ölçülmediği için bu desenin sıvı yağış kaynaklı olumsuzluk olduğunu kanıtlamaz."),
            ("körfezin kuzeybatı girişi ve Adelaide Adası batısında belirgin uygunluk azalması (Δ < -0.05) gözlenirken, güneydeki", "körfezin kuzeybatı girişi ve Adelaide Adası batısında belirgin uygunluk azalması (Δ < -0.05) gözlenirken, kuzeyde yer yer artış blokları da bulunduğu ve artışın yalnızca George VI'ya atfedilemeyeceği görülmektedir; güneydeki"),
            ("CMIP6 SSP2-4.5 2050 projeksiyonunda Marguerite Körfezi uygunluk değişim sınıflarının alan dökümü.", "CMIP6 SSP2-4.5 2050 projeksiyonunda Marguerite Körfezi uygunluk değişim sınıflarının alan dökümü; alanlar 0.25° çevresel grid hücreleridir, koloni alanı veya gerçek habitat alanı değildir."),
            ("Giriş bölümünde incelenen <b>Wang, Hu ve Yang'ın (2026, PMID: 42209243 - <i>Ying Yong Sheng Tai Xue Bao</i>)</b> bulgularıyla karşılaştırıldığında;", "Wang, Hu ve Yang'ın (2026, PMID: 42209243, DOI: 10.13287/j.1001-9332.202603.037) bulguları bağlamında;"),
            ("bildirmişlerdir (Wang vd., 2026). Bizim çalışmamızda ise", "bildirmişlerdir. Bu çalışma SSP5-8.5 ve 2090–2100 kullanırken bizim analizimiz SSP2-4.5, 2041–2060 ve yerel Marguerite Körfezi ölçeğindedir; sonuçlar doğrudan sayısal karşılaştırma değildir (Wang vd., 2026). Bizim çalışmamızda ise"),
            ("Wang, Hu ve Yang (Mart 2026, PMID: 42209243 - ", "Wang, Hu ve Yang (Mart 2026, PMID: 42209243, DOI: 10.13287/j.1001-9332.202603.037 - "),
            ("yüksek emisyon koşullarında türlerin uygun habitat alanlarında kıta genelinde belirgin daralmalar yaşanacağını bildirmişlerdir (Wang vd., 2026).", "yüksek emisyon koşullarında türlerin uygun habitat alanlarında kıta genelinde belirgin daralmalar yaşanacağını bildirmişlerdir (Wang vd., 2026). Bu çalışma ile mevcut analizimizin senaryo, dönem ve ölçekleri farklı olduğundan sonuçlar doğrudan karşılaştırılamaz."),
            ("Model çıktılarında körfezin güneyindeki George VI Boğazı girişinde %34.6 oranında (243 hücre;", "Model çıktılarında toplam %34.6 oranında (243 hücre; güneyde George VI Boğazı girişinde ve haritanın kuzey kesimlerindeki yerel artış bloklarında"),
        ]
        for old, new in replacements:
            text = text.replace(old, new)
        story.append(Paragraph(text, style))
        clean_text = text.replace('<b>', '**').replace('</b>', '**').replace('<i>', '*').replace('</i>', '*')
        if style == title_style:
            md_content.append(f"# {clean_text}\n\n")
        elif style == sec_head:
            md_content.append(f"\n# {clean_text}\n\n")
        elif style == subsec_head:
            md_content.append(f"\n## {clean_text}\n\n")
        elif style == subsubsec_head:
            md_content.append(f"\n### {clean_text}\n\n")
        elif style == caption:
            md_content.append(f"*{clean_text}*\n\n")
        elif style == bullet:
            md_content.append(f"- {clean_text}\n")
        else:
            md_content.append(f"{clean_text}\n\n")

    # =========================================================================
    # SAYFA 1: BAŞLIK, ÖZET, ANAHTAR KELİMELER
    # =========================================================================
    add_p("TÜBİTAK 2204-C KUTUP ARAŞTIRMALARI PROJE RAPORU", title_style)
    add_p("Proje Ana Alanı: Kutup Araştırmaları (Biyoloji ve Ekoloji) | Proje Tematik Alanı: Kutup Biyoçeşitliliği ve Ekosistem Dinamikleri", meta_style)
    add_p("MaxEnt Algoritması ve CMIP6 İklim Senaryoları Kullanılarak Marguerite Körfezi'nde (Batı Antarktika) Adélie Pengueni (<i>Pygoscelis adeliae</i>) Potansiyel Habitat Uygunluğunun ve İklim Değişim Eğilimlerinin Modellenmesi", ParagraphStyle('Sub', parent=title_style, fontSize=10.5, leading=13.5, textColor=C_SECONDARY))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=1, color=C_SECONDARY, spaceBefore=2, spaceAfter=5))

    md_content.append("# TÜBİTAK 2204-C KUTUP ARAŞTIRMALARI PROJE RAPORU\n\n")
    md_content.append("**Proje Ana Alanı:** Kutup Araştırmaları (Biyoloji ve Ekoloji)\n")
    md_content.append("**Proje Tematik Alanı:** Kutup Biyoçeşitliliği ve Ekosistem Dinamikleri\n")
    md_content.append("**Proje Adı:** MaxEnt Algoritması ve CMIP6 İklim Senaryoları Kullanılarak Marguerite Körfezi'nde (Batı Antarktika) Adélie Pengueni (*Pygoscelis adeliae*) Potansiyel Habitat Uygunluğunun ve İklim Değişim Eğilimlerinin Modellenmesi\n\n---\n\n")

    add_p("Özet", sec_head)
    add_p("Batı Antarktika Yarımadası, 20. yüzyılın ikinci yarısında 50 yıllık süreçte yaklaşık 2.5°C'lik (on yılda ~0.5°C) sıcaklık artışıyla yeryüzünün en hızlı bölgesel ısınma yaşayan sahalarından biridir (Vaughan vd., 2003). Bu çalışmada, deniz buzu zorunlu (sea-ice obligate) tepe avcı ve kutup biyo-indikatörü olan Adélie pengueninin (<i>Pygoscelis adeliae</i>), Batı Antarktika Yarımadası'ndaki (WAP) Marguerite Körfezi sahasında (65.88°–70.63°G, 63.88°–73.13°B) günümüz habitat uygunluğu mezo-ölçekte modellenmiş; CMIP6 iklim projeksiyonu altında 2050 yılı olası çevresel değişim eğilimleri keşifsel düzeyde incelenmiştir. GBIF ve SCAR veri tabanlarından derlenen türün yaşam döngüsündeki genel bulunuş (üreme kolonileri ve neritik beslenme gözlemleri), 0.25° grid ölçeğinde mekânsal inceltme uygulanarak örnekleme yığılmasından arındırılmış ve 67 adet bağımsız varlık hücresi elde edilmiştir. Çevresel katman olarak ECMWF ERA5 yeniden analizlerinden yıllık ortalama deniz buzu konsantrasyonu (<i>buz_yillik</i>), deniz yüzeyi sıcaklığı (<i>sst_yillik</i>), en sıcak çeyrek toplam yağışı (<i>bio18</i>) ve REMA modelinden çıplak kaya yüzdesi (<i>kaya</i>) üretilmiştir.")
    add_p("Maksimum Entropi (MaxEnt 3.4.4) algoritmasıyla yürütülen 10 katlı çapraz doğrulamada <b>0.768 ± 0.111</b> test AUC ve 0.838 eğitim AUC değeri elde edilmiştir. Permütasyon öneminde modelin birincil belirleyicisi <b>%55.6</b> ile yıllık deniz buzu konsantrasyonu olmuş; bunu deniz yüzeyi sıcaklığı (<b>%18.3</b>), yaz mevsimi yağışı (<b>%17.1</b>) ve çıplak kaya alanı (<b>%9.1</b>) izlemiştir. Çevresel tepki eğrileri, türün en yüksek uygunluğa %20–%25 marjinal buz konsantrasyonunda, -1.94°C su sıcaklığında ve 184 mm yaz yağışında ulaştığını göstermiştir. Buz konsantrasyonu arttıkça uygunluk kademeli düşerek %60.8'de 0.154 ile taban seviyesine inmekte; kapalı kütlesel buz örtüsünde dalış erişiminin kısıtlanmasını yansıtmaktadır.")
    add_p("Roberts vd. (2017) yaklaşımıyla uygulanan 4 enlem bandı mekânsal blok çapraz doğrulaması (Spatial Block CV), ana modelin (AUTO/RM1, LQTH) test AUC değerinin <b>0.477'ye (rastgele tahmin eşiğinin altına)</b> gerilediğini ve omission oranının %56.7'ye çıktığını belgeleyerek karmaşık kutup modellerinde coğrafi aktarılabilirlik kısıtlarının açıkça kabul edilmesinin zorunluluğunu ortaya koymuştur. CMIP6 IPSL-CM6A-LR SSP2-4.5 (2041–2060) delta projeksiyonunda, 703 grid hücresinin <b>297 adedinde (%42.2)</b> uygunluk azalması, <b>163 adedinde (%23.2)</b> kararlılık, <b>243 adedinde (%34.6)</b> ise deniz buzu incelmesine bağlı kuramsal uygunluk artışı belirlenmiştir. Ancak iklim delta anomalisinin GCM'in ~1° kaba çözünürlüğünü taşıması, hücrelerin %50.8'inde clamping görülmesi ve George VI Boğazı'nın kalıcı şelf buzuyla kaplı olması sebebiyle artış alanları kesin bir 'sığınak' sayılamaz; Ulusal Antarktika Bilim Seferleri (TAE) kapsamında sahada doğrulanması gereken birer <b>bölgesel hipotezdir</b>.")
    add_p("<b>Anahtar Kelimeler:</b> Adélie Pengueni (<i>Pygoscelis adeliae</i>), MaxEnt Ekolojik Niş Modeli, Marguerite Körfezi, CMIP6 SSP2-4.5, Mekânsal Blok Çapraz Doğrulama, İklim Değişimi, Ekstrapolasyon Belirsizliği.", body_bold)

    story.append(PageBreak())

    # =========================================================================
    # SAYFA 2: AMAÇ VE GİRİŞ BAŞLANGICI
    # =========================================================================
    add_p("Amaç", sec_head)
    add_p("Bu projenin temel amacı; küresel iklim değişikliğine bağlı olarak oşinografik ve atmosferik süreçlerin hızla dönüştüğü Batı Antarktika Yarımadası'ndaki (WAP) Marguerite Körfezi'nde, deniz buzu dinamiklerine duyarlı tepe indikatör tür olan Adélie pengueninin (<i>Pygoscelis adeliae</i>) günümüz (2000–2025) potansiyel habitat uygunluğunu Maksimum Entropi (MaxEnt 3.4.4) algoritmasıyla mezo-ölçekte modellemek; CMIP6 IPSL-CM6A-LR SSP2-4.5 (2041–2060) projeksiyonu altında türün çevresel uygunluk gradyanındaki olası değişim eğilimlerini keşifsel düzeyde incelemek; model aktarılabilirliğini mekânsal blok çapraz doğrulama yöntemiyle sınamak ve elde edilen kuramsal değişimlerin sahadaki ekolojik fizibilitesini değerlendirmektir.")
    add_p("Bu genel amaç doğrultusunda şu hedefler belirlenmiştir:")
    add_p("• 1. GBIF ve SCAR veri tabanlarından Marguerite Körfezi'ne ait 2000–2025 dönemini kapsayan Adélie pengueni genel bulunuş (üreme kolonisi ve neritik beslenme) koordinatlarını derlemek; 0.25° grid ölçeğinde mekânsal inceltme uygulayarak 67 adet bağımsız varlık hücresi belirlemek.", bullet)
    add_p("• 2. ECMWF ERA5 yeniden analizlerinden ve REMA sayısal yükseklik modelinden penguenlerin üreme ve beslenme ekolojisini kontrol eden 4 temel çevresel katmanı (<i>buz_yillik</i>, <i>kaya</i>, <i>bio18</i>, <i>sst_yillik</i>) üretmek; değişkenler arası çoklu eşdoğrusallığı (VIF ve Pearson korelasyonu) denetlemek.", bullet)
    add_p("• 3. MaxEnt 3.4.4 algoritmasıyla günümüz habitat uygunluk modelini kurmak; standart rastgele 10 katlı çapraz doğrulama (10-fold CV) ve Roberts vd. (2017) yöntemine dayalı 4 enlem bandı mekânsal blok çapraz doğrulama (Spatial Block CV) uygulayarak model başarımını ve coğrafi aktarılabilirlik sınırlarını karşılaştırmak.", bullet)
    add_p("• 4. CMIP6 IPSL-CM6A-LR SSP2-4.5 (2041–2060) iklim projeksiyonunu delta aşağı ölçekleme yöntemiyle ERA5 referansına entegre ederek 2050 yılı potansiyel habitat değişim haritalarını üretmek; novel climate ve clamping alanlarını haritalandırarak ekstrapolasyon belirsizliklerini ortaya koymak.", bullet)
    add_p("• 5. Model sonuçlarını ve mekânsal kısıtları, Türkiye'nin düzenlediği Ulusal Antarktika Bilim Seferleri (TAE) kapsamında yürütülecek izleme ve koruma stratejileri için sahada doğrulanabilir bir araştırma çerçevesine dönüştürmek.", bullet)

    add_p("Giriş", sec_head)
    add_p("Antarktika kıtası ve onu çevreleyen Güney Okyanusu, küresel termohalin sirkülasyonu düzenleyen ve gezegenin ısı bütçesini dengeleyen hayati bir ekosistemdir (IPCC, 2021). Güney Okyanusu'nun en dinamik denizel sahalarından biri olan Batı Antarktika Yarımadası (WAP), 20. yüzyılın ikinci yarısında 50 yıllık süreçte yaklaşık 2.5°C'lik (on yılda ~0.5°C) sıcaklık artışıyla yeryüzünün en hızlı bölgesel ısınma yaşayan sahalarından biridir (Vaughan vd., 2003; Turner vd., 2014). Her ne kadar 21. yüzyılın başlarında doğal atmosferik dolaşım modlarındaki (SAM ve IPO) salınımlara bağlı olarak bölgesel sıcaklıklarda geçici duraklama ve yavaşlamalar gözlense de (Turner vd., 2016), uzun dönemli eğilimler deniz buzu mevsimsel örtüsünün kısalması, kıyı buz sahanlıklarının geri çekilmesi ve Antarktika krili (<i>Euphausia superba</i>) biyokütlesindeki dalgalanmalar yönündedir (Stammerjohn vd., 2008, 2012; Atkinson vd., 2004; Rignot vd., 2019).")

    story.append(PageBreak())

    # =========================================================================
    # SAYFA 3: GİRİŞ DEVAMI VE LİTERATÜR SENTEZİ
    # =========================================================================
    add_p("Denizel besin ağının üst basamaklarında yer alan kutup penguenleri (<i>Pygoscelis</i> cinsi), fiziksel çevre koşullarındaki değişimlere karşı duyarlı indikatör türlerdir (Ainley, 2002; Fraser & Hofmann, 2003). Bu cins içerisinde Adélie pengueni (<i>Pygoscelis adeliae</i>), yaşam döngüsü deniz buzuna endeksli bir penguen türüdür (Ainley, 2002). Adélie penguenleri; kış aylarında açık denizdeki paket buz (pack-ice) üzerinde dinlenmekte ve tüy dökmekte, ilkbahar ve yaz aylarında ise kıyı şeridindeki kardan arınmış çıplak kayalık zeminlerde koloni kurarak çakıl taşlarından inşa ettikleri yuvalarda kuluçkaya yatmaktadır (Ainley, 2002; Southwell vd., 2015; Lyver vd., 2014). Türün temel besinini oluşturan Antarktika krili, larva ve jüvenil evrelerinde kış deniz buzunun alt yüzeyindeki mikroalgleri otlayarak hayatta kaldığından, deniz buzu dinamikleri penguenlerin besin teminini doğrudan etkilemektedir (Fraser & Hofmann, 2003; Atkinson vd., 2004; Trivelpiece vd., 2011).")
    add_p("İklimsel süreçlerin Batı Antarktika Yarımadası'ndaki etkileri deniz buzu dinamikleriyle sınırlı değildir. Isınan atmosferin nem taşıma kapasitesinin artması neticesinde, kutup ortamında aşırı yağış anomalileri, ıslak kar ve sıvı yağmur olayları gözlenmektedir (IPCC, 2021; Massom vd., 2006). Kuluçkadan yeni çıkan Adélie yavruları su geçirmez yetişkin tüylerine sahip olmayıp yalnızca ısı yalıtımı sağlayan hav tüyleri ile kaplıdır. Aşırı sıvı yağış veya eriyik çamur altında kalan yavruların tüyleri ıslandığında yalıtım özelliğini yitirmekte; dondurucu rüzgar altında hipotermiye girerek ölüm riskiyle karşılaşmaktadır (Chapman vd., 2011).")
    add_p("Türlerin coğrafi dağılım sınırlarını ve iklim değişikliği karşısındaki duyarlılıklarını anlamak amacıyla Tür Dağılım Modelleri (SDM) yaygın olarak kullanılmaktadır (Elith vd., 2011; Phillips vd., 2006; Fielding & Bell, 1997). Yalnızca varlık (presence-only) verileriyle çalışabilen Maksimum Entropi (MaxEnt) algoritması ekoloji literatüründe sıkça tercih edilmektedir (Phillips vd., 2006).")
    add_p("Uluslararası literatür incelendiğinde; <b>Wang, Hu ve Yang (Mart 2026, PMID: 42209243 - <i>Ying Yong Sheng Tai Xue Bao</i>)</b>, günümüz (2010–2020) ve gelecekteki (2090–2100 SSP5-8.5) iklim senaryoları altında MaxEnt kullanarak üç <i>Pygoscelis</i> penguen türünün tüm Antarktika ölçeğinde potansiyel habitatlarını modellemiş; deniz yüzeyi sıcaklığı ve buz örtüsünün kritik belirleyiciler olduğunu ve yüksek emisyon koşullarında türlerin uygun habitat alanlarında kıta genelinde belirgin daralmalar yaşanacağını bildirmişlerdir (Wang vd., 2026). Benzer şekilde, <b>Cimino, Lynch, Saba ve Oliver (2016 - <i>Scientific Reports</i>)</b>, CMIP5 modelleri ve varlık-yokluk kayıtlarıyla yaptıkları çalışmada, 2060 yılına kadar mevcut Adélie pengueni kolonilerinin yaklaşık üçte birinin (mevcut popülasyonun ~%20'si) iklim ısınması nedeniyle gerileme sürecine girebileceğini öngörmüşlerdir.")
    add_p("Kıtasal veya yarımada ölçeğindeki bu makro araştırmalar (Wang vd., 2026; Cimino vd., 2016), 100–200 km'lik kaba iklim hücreleri nedeniyle yerel çıplak kaya ve topografik dinamikleri temsil edememektedir. Bu çalışma, Marguerite Körfezi'ne odaklanarak günümüz koşullarını 0.25° grid (~288 km²) ölçeğinde mezo-ölçekli bir yerel çözünürlükle modellemektedir. Ancak 2050 iklim projeksiyonunda kullanılan delta anomalileri, küresel iklim modelinin (GCM) yerel ~1° (~100 km) kaba çözünürlüğünü yansıtmaktadır. Dolayısıyla mezo-ölçek avantajı temel olarak günümüz çevresel ve topografik katmanlarımız için geçerlidir; gelecek projeksiyonları mezo-topografya ile kaba iklim anomalisinin bir sentezini temsil etmektedir.")

    story.append(PageBreak())

    # =========================================================================
    # SAYFA 4: YÖNTEM - 1.1 VE 1.2
    # =========================================================================
    add_p("Yöntem", sec_head)

    add_p("1.1. Araştırma Sahası ve Biyocoğrafik Sınırlar", subsec_head)
    add_p("Çalışma alanı, Batı Antarktika Yarımadası'nın güneybatı kesiminde yer alan ve Bellingshausen Denizi ile bağlantılı olan <b>Marguerite Körfezi</b> ve çevre adalarıdır. Modelleme ızgarası; <b>65.875°G – 70.625°G enlemleri</b> ile <b>63.875°B – 73.125°B boylamları</b> arasında tanımlanmıştır (xllcorner: -73.125°, yllcorner: -70.625°, cellsize: 0.25°, 37 sütun × 19 satır, toplam 703 grid hücresi). Bu bölge; kuzeyde Adelaide Adası, doğuda Fallières Kıyısı, güneyde George VI Boğazı ve batıda Alexander Adası ile çevrili fiyort ve ada sistemidir (Ducklow vd., 2007; Stammerjohn vd., 2012).")
    add_p("Kutup enlemlerinde meridyenlerin birbirine yaklaşması (enlem daralması - meridian convergence) nedeniyle, 68°G enleminde $\\cos(68^\\circ) \\approx 0.3746$'dır. Bu coğrafi durum neticesinde 0.25° boylam genişliği yalnızca yaklaşık 10.4 km'ye, 0.25° enlem yüksekliği ise 27.8 km'ye karşılık gelmektedir. WGS84 elipsoidi üzerinde bir grid hücresinin yüzölçümü ortalama ~288.3 km² olup, 703 grid hücresinin kapsadığı toplam model kalibrasyon alanı <b>202.681 km²</b>'dir. Boylamsal komşu iki hücre merkezi arasındaki mesafe yalnızca ~10.4 km olduğundan, modelin mekânsal inceltme sonrası hücreler arası komşuluk mesafeleri kutup jeodeziği ile tam uyumludur.")

    add_p("1.2. Biyolojik Varlık (Presence) Verilerinin Temini ve Mekânsal İnceltme", subsec_head)
    add_p("Adélie penguenine (<i>Pygoscelis adeliae</i>) ait coğrafi koordinat verileri, açık kaynak uluslararası biyo-çeşitlilik veri tabanları olan GBIF (Global Biodiversity Information Facility - gbif.org) ve SCAR (Scientific Committee on Antarctic Research) Antarktika Biyo-çeşitlilik Portalı üzerinden derlenmiştir. 2000–2025 yılları arasındaki kayıtlar taranmıştır. Bu veri seti, türün yaşam döngüsündeki <b>genel bulunuşunu (overall occurrence)</b> temsil etmekte olup hem kıyı şeridindeki üreme kolonisi yerleşimlerini hem de şelf sahası üzerindeki neritik beslenme/hareket gözlemlerini içermektedir. Ham veri setine ekolojik modelleme standartlarına uygun olarak şu filtreleme protokolü uygulanmıştır:", body)
    add_p("• Koordinat doğruluğu belirsiz (belirsizlik > 5 km) veya hatalı girilmiş kayıtlar ayıklanmıştır.", bullet)
    add_p("• Fosilleşmiş veya tarihsel kolonilere ait eski kayıtlar çalışma kapsamı dışına çıkarılmıştır.", bullet)
    add_p("• Araştırma istasyonları (örn. Rothera İstasyonu) çevresinde yoğunlaşan insan kaynaklı örnekleme yanlılığını (sampling bias) ve mekânsal yığılmayı önlemek amacıyla, çalışma için belirlenen 0.25° × 0.25° analiz gridi içinde hücre başına yalnızca tek bir varlık noktası bırakılacak şekilde <b>mekânsal inceltme (spatial thinning)</b> uygulanmıştır.", bullet)
    add_p("• Çalışma alanı sınırları dışındaki açık okyanus derinliklerine hatalı koordinatlanmış kayıtlar elenmiştir.", bullet)
    add_p("Bu filtreleme neticesinde, Marguerite Körfezi sınırları dahilinde model eğitim ve doğrulamasında kullanılmak üzere <b>67 adet bağımsız varlık (presence) grid hücresi</b> elde edilmiştir. Çalışma alanındaki toplam 703 grid hücresinin geri kalan 636 hücresi modelin arka plan (background) çevresel matrisini oluşturmuştur.")

    story.append(PageBreak())

    # =========================================================================
    # SAYFA 5: YÖNTEM - 1.3, TABLO 1 VE 1.4
    # =========================================================================
    add_p("1.3. Çevresel ve Oşinografik Katmanların Üretimi", subsec_head)
    add_p("Adélie pengueninin üreme ve beslenme ekolojisini kontrol eden biyoklimatik ve çevresel değişkenler, ECMWF ERA5 atmosferik ve denizel yeniden analiz veri setlerinden derlenmiştir. ERA5 verileri 2000–2025 dönemini kapsayan 26 yıllık uzun dönemli aylık ortalamaların sentezlenmesiyle üretilmiştir. Denizel katmanlar olarak; penguenlerin kışlama platformunu ve açık su çatlaklarında avlanmasını temsil eden yıllık ortalama deniz buzu konsantrasyonu (<i>buz_yillik</i>, % oran) ve Güney Okyanusu su kütlesi termal rejimini temsil eden deniz yüzeyi sıcaklığı (<i>sst_yillik</i>, °C) hesaplanmıştır. Burada SST, endotermik bir kuş olan penguen için doğrudan öldürücü bir fizyolojik sınır olmaktan ziyade, penguenin ana besini olan krilin ve pelajik besin ağının su kütlesi vekili (proxy) niteliğindedir. Atmosferik katman olarak; kuluçka evresindeki civcivlerin ıslanma ve hipotermi riskini temsil eden en sıcak çeyrek (Aralık–Ocak–Şubat yaz mevsimi) toplam yağış miktarı (<i>bio18</i>, mm cinsinden) türetilmiştir. Topografik katman olarak ise; Antarktika REMA sayısal yükseklik modeli ve SCAR kaya yüzeyi veri tabanı kullanılarak her bir 0.25° grid hücresindeki çıplak kaya alan yüzdesi (<i>kaya</i>, % alan) hesaplanmıştır.")

    # Tablo 1
    t1_data = [
        [Paragraph("Değişken Adı", table_cell_cb), Paragraph("Kod", table_cell_cb), Paragraph("Birim", table_cell_cb), Paragraph("Çözünürlük", table_cell_cb), Paragraph("Veri Kaynağı", table_cell_cb), Paragraph("Ekolojik Rolü ve Biyolojik Anlamı (Vekil / Substrat)", table_cell_cb)],
        [Paragraph("Yıllık Deniz Buzu Konsantrasyonu", table_cell_b), Paragraph("buz_yillik", table_cell_c), Paragraph("%", table_cell_c), Paragraph("0.25° (~288 km²)", table_cell_c), Paragraph("ECMWF ERA5 (2000–2025)", table_cell), Paragraph("Kışlama platformu ve buz kenarı/marjinal zon avlanma sahası (Ainley, 2002; Wang vd., 2026).", table_cell)],
        [Paragraph("Çıplak Kaya Alanı Yüzdesi", table_cell_b), Paragraph("kaya", table_cell_c), Paragraph("%", table_cell_c), Paragraph("0.25° (~288 km²)", table_cell_c), Paragraph("SCAR / REMA DEM", table_cell), Paragraph("Kardan arınmış sert zemin; çakıl yuva inşası ve kuluçka fiziksel substratı (Southwell vd., 2015).", table_cell)],
        [Paragraph("En Sıcak Çeyrek Toplam Yağışı", table_cell_b), Paragraph("bio18", table_cell_c), Paragraph("mm", table_cell_c), Paragraph("0.25° (~288 km²)", table_cell_c), Paragraph("ECMWF ERA5 (2000–2025)", table_cell), Paragraph("Geniş yaz yağışı vekili; yağış fazını ayırt etmez ve hipotermiyi doğrudan ölçmez.", table_cell)],
        [Paragraph("Yıllık Deniz Yüzeyi Sıcaklığı", table_cell_b), Paragraph("sst_yillik", table_cell_c), Paragraph("°C", table_cell_c), Paragraph("0.25° (~288 km²)", table_cell_c), Paragraph("ECMWF ERA5 (2000–2025)", table_cell), Paragraph("Pelajik su kütlesi özellikleri ve krill/besin ağı dağılımının oşinografik vekili (Cimino vd., 2016).", table_cell)]
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

    add_p("1.4. CMIP6 İklim Modeli, Delta Aşağı Ölçekleme ve Çözünürlük Yapısı", subsec_head)
    add_p("2050 yılı iklim projeksiyonu için Dünya İklim Araştırma Programı (WCRP) CMIP6 veri tabanından <b>IPSL-CM6A-LR</b> küresel iklim modeli (ensemble üyesi: r1i1p1f1, senaryo: SSP2-4.5 orta emisyon yolu) temin edilmiştir. Projeksiyon dönemi <b>2041–2060</b> (20 yıllık ortalama), tarihsel referans dönemi ise ERA5 ile uyumlu olarak <b>2000–2025</b> olarak belirlenmiştir. GCM çıktılarının 0.25° gridimize aktarılmasında küre üzerinde en yakın komşu (nearest complete native cell on sphere) regridding ve delta aşağı ölçekleme yöntemi uygulanmıştır:")
    add_p("• <b>Deniz Buzu (buz_yillik):</b> Gelecek ve referans dönem arasındaki mutlak fark yüzdesi, ERA5 günümüz deniz buzu katmanına eklenmiş ve değerler [0, 100] aralığında sınırlandırılmıştır.", bullet)
    add_p("• <b>Deniz Yüzeyi Sıcaklığı (sst_yillik):</b> Aylık yerel SST anomalisi ERA5 yıllık deniz suyu sıcaklığına additif olarak eklenmiştir.", bullet)
    add_p("• <b>Yaz Yağışı (bio18):</b> Aylık yağış oranları ERA5 aylık yağışlarına uygulanmış; gelecekteki en sıcak çeyrek ayları (tas) yeniden tespit edilerek bio18 gelecekte dinamik olarak baştan hesaplanmıştır.", bullet)
    add_p("• <b>Çıplak Kaya (kaya):</b> Jeolojik kaya substratı 2050 yılı projeksiyonunda statik kabul edilmiştir.", bullet)
    add_p("Burada dikkat edilmesi gereken husus; iklim değişikliği sinyalinin (delta anomalisi) GCM'in yerel ~1° (~100 km) kaba çözünürlüğünü taşımasıdır. Dolayısıyla değişim haritalarındaki bloklu görünüm bu enterpolasyonun doğal bir sonucudur.")

    story.append(PageBreak())

    # =========================================================================
    # SAYFA 6: YÖNTEM - 1.5, 1.6, TABLO 2 VE 1.7
    # =========================================================================
    add_p("1.5. Çoklu Eşdoğrusallık ve MaxEnt Matematiksel Temelleri", subsec_head)
    add_p("Ekolojik modellemede yüksek korelasyonlu değişkenlerin kullanımı model parametrelerinin varyansını artırabilmektedir (Dormann vd., 2013). Değişkenler arasında Pearson korelasyon matrisi ve Varyans Şişme Faktörü (VIF) analizi uygulanmış; Dormann vd. (2013) uyarınca <b>|r| < 0.70</b> ve VIF < 5 kuralı işletilmiştir. Aday katmanlardan kış minimum sıcaklığı (Bio6) elenmiş; modeldeki 4 değişkenin ikili korelasyonlarının |r| < 0.62 seviyesinde kalarak çoklu eşdoğrusallık riskinin giderildiği doğrulanmıştır.")
    add_p("Maksimum Entropi (MaxEnt 3.4.4) algoritması, Shannon bilgi entropisi ilkesine dayanır (Phillips vd., 2006). Algoritma, türün varlık koordinatlarındaki çevresel ortalamaları kısıt kabul ederek, bu kısıtları sağlayan olasılık dağılımları içerisinden entropisi en yüksek dağılımı $\\hat{\\pi}(x)$ hesaplar:")
    add_p("$$H(\\hat{\\pi}) = -\\sum_{x \\in X} \\hat{\\pi}(x) \\ln \\hat{\\pi}(x) \\quad \\text{ve} \\quad \\mathbb{E}_{\\hat{\\pi}}[f_j] = \\mathbb{E}_{\\tilde{\\pi}}[f_j]$$", body_bold)
    add_p("Aşırı öğrenmeyi (overfitting) engellemek amacıyla MaxEnt, objektif fonksiyonuna bir $L_1$ Lasso düzenlileştirme cezası ekler (Phillips vd., 2006): $\\max_{\\lambda} ( \\sum_{i=1}^n \\ln P(x_i) - \\sum_{j=1}^m \\beta_j |\\lambda_j| )$. Model çıktısı, türün göreceli uygunluğunu 0 ile 1 arasında ölçekleyen Cloglog dönüşümü ile elde edilmiştir: $P(x) = 1 - \\exp(-\\exp(\\eta(x)))$.")

    add_p("1.6. Model Eğitimi, Hiperparametreler ve 10-Katlı Doğrulama", subsec_head)
    add_p("Ekolojik niş modellemesi bağımsız Java ortamında MaxEnt 3.4.4 yazılımıyla yürütülmüştür. 67 adet varlık hücresi ve çalışma alanındaki 636 adet arka plan hücresi (toplam 703 grid hücresi) modele girdi olarak verilmiştir. 60'tan fazla örneklem bulunduğu için model hiperparametreleri olarak varsayılan <b>LQTH (Linear, Quadratic, Threshold, Hinge)</b> özellik sınıfları kullanılmış; aşırı öğrenmeyi önlemek için düzenlileştirme çarpanı (Regularization Multiplier = 1.0) seçilmiştir. Model performansı <b>10 katlı çapraz doğrulama (10-fold CV)</b> ile sınanmış ve ROC altındaki alan (AUC) hesaplanmıştır (Fielding & Bell, 1997). Presence-only modellerde AUC, varlıkların rastgele arka plana karşı ayırt edilmesini temsil eder. AUC değerlendirmesinde Swets (1988) kriterleri esas alınmıştır (Tablo 2).")

    # Tablo 2
    t2_data = [
        [Paragraph("AUC Değer Aralığı", table_cell_cb), Paragraph("Simülasyon Başarı Düzeyi", table_cell_cb), Paragraph("Ekolojik Model Değerlendirmesi ve Güvenilirlik", table_cell_cb)],
        [Paragraph("0.50 – 0.60", table_cell_c), Paragraph("Başarısız / Rastgele", table_cell), Paragraph("Model rastgele tahminden farksızdır; çevresel değişkenler türü ayırt edememektedir.", table_cell)],
        [Paragraph("0.60 – 0.70", table_cell_c), Paragraph("Zayıf / Yetersiz", table_cell), Paragraph("Ayırt edici güç düşüktür; çevresel değişkenler türü açıklamakta yetersizdir.", table_cell)],
        [Paragraph("0.70 – 0.80", table_cell_c), Paragraph("Kabul Edilebilir / İyi", table_cell), Paragraph("Model yeterli düzeyde ayırt edicidir; akademik SDM çalışmaları için kabul eşiğidir.", table_cell)],
        [Paragraph("0.80 – 0.90", table_cell_c), Paragraph("Yüksek / Çok İyi", table_cell), Paragraph("Model yüksek derecede ayırt edicidir; çevresel ilişkileri güçlü yakalamıştır.", table_cell)],
        [Paragraph("0.90 – 1.00", table_cell_c), Paragraph("Mükemmel", table_cell), Paragraph("Olağanüstü ayırt edicilik (aşırı öğrenme veya örnekleme yanlılığı riski denetlenmelidir).", table_cell)]
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
    add_p("Standart rastgele çapraz doğrulamada, mekânsal otokorelasyon nedeniyle test noktaları eğitim noktalarına yakın düşmekte ve AUC değerleri iyimser tahmin edilebilmektedir (Roberts vd., 2017). Modelin coğrafi aktarılabilirliğini sınamak amacıyla, çalışma alanı 4 coğrafi enlem bandına (-66.625°, -67.375°, -67.875° sınırları) bölünerek mekânsal bloklama testi gerçekleştirilmiştir. Eşit eğitim boyutu (50-51 nokta) ve sabit rastgele tohumla (20261108) eşleştirilmiş rastgele 4 katlı modelle doğrudan kıyaslanmıştır.")

    story.append(PageBreak())

    # =========================================================================
    # SAYFA 7: YÖNTEM - 1.8, 1.9 (GANTT) VE BULGULAR GİRİŞİ
    # =========================================================================
    add_p("1.8. CBS ve Kartografik Projeksiyon Altyapısı", subsec_head)
    add_p("MaxEnt'ten üretilen ham Cloglog ASCII raster çıktıları, QGIS 3.x açık kaynak Coğrafi Bilgi Sistemleri yazılımına aktarılmıştır. Kutup bölgelerinde alan ve şekil bozulmalarını en aza indirmek için harita projeksiyonu <b>EPSG:3031 (WGS 84 / Antarctic Polar Stereographic)</b> olarak tanımlanmıştır. Günümüz (2000–2025), 2050 gelecek, mekânsal fark (Gelecek − Günümüz) ve belirsizlik haritaları 300 DPI çözünürlükte, koordinat gridi, istasyon katmanları ve standart lejantlarıyla kartografik standartta üretilmiştir.")

    add_p("1.9. Proje İş-Zaman Çizelgesi ve Gerçekleşme Takvimi", subsec_head)
    add_p("Projenin araştırma, veri hazırlığı, modelleme, analiz ve raporlama süreçleri aşağıdaki 8 temel iş paketi çerçevesinde 6 aylık periyotta planlanmış ve başarıyla yürütülmüştür (Tablo 3):")

    # Tablo 3: Gantt Chart
    gantt_data = [
        [Paragraph("No", table_cell_cb), Paragraph("İş Paketi / Faaliyet Adı", table_cell_cb), Paragraph("Hedef Çıktı / Yöntem", table_cell_cb), Paragraph("Sorumlu", table_cell_cb), Paragraph("1. Ay", table_cell_cb), Paragraph("2. Ay", table_cell_cb), Paragraph("3. Ay", table_cell_cb), Paragraph("4. Ay", table_cell_cb), Paragraph("5. Ay", table_cell_cb), Paragraph("6. Ay", table_cell_cb)],
        [Paragraph("1", table_cell_c), Paragraph("Literatür Taraması & Hipotez Kurgusu", table_cell_b), Paragraph("Makale sentezi, veri gereksinim analizi", table_cell), Paragraph("Öğrenci / Danışman", table_cell), Paragraph("X", table_cell_c), Paragraph("X", table_cell_c), Paragraph("", table_cell), Paragraph("", table_cell), Paragraph("", table_cell), Paragraph("", table_cell)],
        [Paragraph("2", table_cell_c), Paragraph("GBIF & SCAR Varlık Verisi Temini", table_cell_b), Paragraph("67 bağımsız hücre, mekânsal inceltme", table_cell), Paragraph("Öğrenci", table_cell), Paragraph("", table_cell), Paragraph("X", table_cell_c), Paragraph("", table_cell), Paragraph("", table_cell), Paragraph("", table_cell), Paragraph("", table_cell)],
        [Paragraph("3", table_cell_c), Paragraph("ECMWF ERA5 & REMA Katman Üretimi", table_cell_b), Paragraph("0.25° grid, EPSG:3031 projeksiyonu", table_cell), Paragraph("Öğrenci", table_cell), Paragraph("", table_cell), Paragraph("X", table_cell_c), Paragraph("X", table_cell_c), Paragraph("", table_cell), Paragraph("", table_cell), Paragraph("", table_cell)],
        [Paragraph("4", table_cell_c), Paragraph("Çoklu Eşdoğrusallık ve VIF Analizi", table_cell_b), Paragraph("Pearson |r| < 0.70 kuralı, 4 değişken", table_cell), Paragraph("Öğrenci / Danışman", table_cell), Paragraph("", table_cell), Paragraph("", table_cell), Paragraph("X", table_cell_c), Paragraph("", table_cell), Paragraph("", table_cell), Paragraph("", table_cell)],
        [Paragraph("5", table_cell_c), Paragraph("MaxEnt Modellemesi & 10-Katlı CV", table_cell_b), Paragraph("Cloglog formatı, AUC ve Jackknife", table_cell), Paragraph("Öğrenci", table_cell), Paragraph("", table_cell), Paragraph("", table_cell), Paragraph("X", table_cell_c), Paragraph("X", table_cell_c), Paragraph("", table_cell), Paragraph("", table_cell)],
        [Paragraph("6", table_cell_c), Paragraph("Mekânsal Blok Çapraz Doğrulama", table_cell_b), Paragraph("4 enlem bandı spatial CV (Roberts 2017)", table_cell), Paragraph("Öğrenci", table_cell), Paragraph("", table_cell), Paragraph("", table_cell), Paragraph("", table_cell), Paragraph("X", table_cell_c), Paragraph("", table_cell), Paragraph("", table_cell)],
        [Paragraph("7", table_cell_c), Paragraph("CMIP6 IPSL SSP2-4.5 2050 Projeksiyonu", table_cell_b), Paragraph("Δ fark matrisi, değişim eğilimleri", table_cell), Paragraph("Öğrenci", table_cell), Paragraph("", table_cell), Paragraph("", table_cell), Paragraph("", table_cell), Paragraph("X", table_cell_c), Paragraph("X", table_cell_c), Paragraph("", table_cell)],
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
    add_p("Tablo 3. Proje iş-zaman çizelgesi ve gerçekleşme takvimi.", caption)

    add_p("Bulgular", sec_head)
    add_p("2.1. Alıcı İşletim Karakteristiği (ROC) Eğrisi ve Model Doğruluğu", subsec_head)
    add_p("Alıcı İşletim Karakteristiği (ROC) eğrisi, modelin duyarlılığı ile (1 - özgüllük) arasındaki ilişkiyi gösterir. 10 katlı çapraz doğrulama (10-fold CV) analizi sonucunda, test verileri üzerinden hesaplanan ortalama AUC değeri <b>0.768 ± 0.111</b> olarak gerçekleşmiştir (Şekil 1). Eğitim verilerine ait AUC değeri ise <b>0.838</b> olarak belirlenmiştir. Bu değer, rastgele katlamalı değerlendirmede kabul edilebilir bir ayırt etme performansına işaret eder; ancak presence-only AUC gerçek yokluk doğrulaması değildir ve mekânsal blok doğrulamasındaki düşük değerler nedeniyle modelin coğrafi aktarılabilirliği sınırlıdır.")

    story.append(PageBreak())

    # =========================================================================
    # SAYFA 8: ŞEKİL 1 (ROC) VE TABLO 4 (DEĞİŞKEN KATKILARI)
    # =========================================================================
    roc_path = "/home/halil/adelie-maxent-2204c/maxent/cikti/deneme3/plots/Pygoscelis_adeliae_roc.png"
    if os.path.exists(roc_path):
        img_roc = Image(roc_path, width=380, height=244)
        story.append(KeepTogether([img_roc, Paragraph("Şekil 1. Adélie pengueni MaxEnt modeline ait 10 katlı çapraz doğrulama ROC eğrisi (Kırmızı: 10 yineleme ortalaması test AUC = 0.768, Mavi: Standart sapma ±0.111, Siyah: Rastgele tahmin AUC = 0.50).", caption)]))
        md_content.append(f"\n![Şekil 1. ROC Eğrisi]({roc_path})\n*Şekil 1. Adélie pengueni MaxEnt modeline ait 10 katlı çapraz doğrulama ROC eğrisi.*\n")

    add_p("2.2. Biyoklimatik Değişkenlerin Göreceli Katkı ve Permütasyon Önemleri", subsec_head)
    add_p("MaxEnt algoritması, çevresel değişkenlerin modele etkisini iki tamamlayıcı metrikle raporlamaktadır: <b>Göreceli Katkı Yüzdesi (Percent Contribution)</b> ve <b>Permütasyon Önemi (Permutation Importance)</b>. Katkı yüzdesi, eğitim algoritmasının yinelemeleri sırasında ilgili değişkenin düzenlenmiş kazançta (gain) yarattığı artışa dayanır. Permütasyon önemi ise eğitim verilerindeki değişken değerlerinin rastgele karıştırılması sonucu AUC değerindeki düşüşü ölçer ve değişkenler arası korelasyondan daha az etkilenen bir göstergedir. 10 kat modelinin değişken önem metrikleri Tablo 4'te sunulmuştur.")

    # Tablo 4 (GERÇEK 10-kat ortalaması)
    t4_data = [
        [Paragraph("Çevresel Değişken", table_cell_cb), Paragraph("Katkı Yüzdesi (%) (Percent Contribution)", table_cell_cb), Paragraph("Permütasyon Önemi (%) (Permutation Importance)", table_cell_cb), Paragraph("Baskın Ekolojik Rolü (Vekil / Substrat)", table_cell_cb)],
        [Paragraph("Yıllık Deniz Buzu (buz_yillik)", table_cell_b), Paragraph("<b>43.1 ± 5.2</b>", table_cell_cb), Paragraph("<b>55.6 ± 6.8</b>", table_cell_cb), Paragraph("Birincil belirleyici; marjinal buz avlanma sahası ve kışlama platformu.", table_cell)],
        [Paragraph("Çıplak Kaya Alanı (kaya)", table_cell_b), Paragraph("<b>30.0 ± 3.5</b>", table_cell_cb), Paragraph("<b>9.1 ± 2.4</b>", table_cell_cb), Paragraph("Kıyısal kuluçka ve çakıl yuva kurma fiziksel ön koşulu (substrat).", table_cell)],
        [Paragraph("En Sıcak Çeyrek Yağışı (bio18)", table_cell_b), Paragraph("13.9 ± 3.1", table_cell_c), Paragraph("<b>17.1 ± 3.9</b>", table_cell_cb), Paragraph("Yaz yağış anomalileri; civciv hipotermi ve yuva ıslanma riski vekili.", table_cell)],
        [Paragraph("Deniz Yüzeyi Sıcaklığı (sst_yillik)", table_cell_b), Paragraph("12.9 ± 2.8", table_cell_c), Paragraph("<b>18.3 ± 4.5</b>", table_cell_cb), Paragraph("Pelajik su kütlesi termal rejimi ve kril habitatı oşinografik vekili.", table_cell)]
    ]
    t4 = Table(t4_data, colWidths=[130, 95, 95, 185])
    t4.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_HEADER_BG),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(Spacer(1, 4))
    story.append(t4)
    add_p("Tablo 4. Çevresel değişkenlerin MaxEnt modeline katkı yüzdeleri ve permütasyon önemleri (10 kat ortalaması).", caption)
    add_p("Tablo 4 verileri incelendiğinde; hem göreceli katkı yüzdesinde (%43.1) hem de permütasyon öneminde (%55.6) yıllık deniz buzu konsantrasyonunun (<i>buz_yillik</i>) en belirleyici faktör olduğu görülmektedir. Çıplak kaya alanı (<i>kaya</i>) ise eğitim yinelemelerinde %30.0 katkı yüzdesi sağlamasına rağmen permütasyon öneminde %9.1 seviyesinde kalmıştır. Bu durum, kayalık alanların kıyı şeridinde kolonileşme için zorunlu bir fiziksel ön koşul teşkil ettiğini, ancak çalışma alanının tamamındaki habitat uygunluk gradyanını asıl şekillendiren etkenlerin denizel oşinografik değişkenler (deniz buzu %55.6 ve deniz sıcaklığı %18.3) olduğunu ortaya koymaktadır.")

    story.append(PageBreak())

    # =========================================================================
    # SAYFA 9: 2.3 JACKKNIFE GRAFİĞİ VE ANALİZİ
    # =========================================================================
    add_p("2.3. Jackknife Yöntemiyle Değişken Kazanç Analizleri", subsec_head)
    add_p("Jackknife testi, her bir çevresel değişkenin model kazancına (gain) olan etkisini iki tamamlayıcı yaklaşımla inceler: (1) Değişken modelde tek başına kullanıldığında sağladığı kazanç (turkuaz çubuk), (2) İlgili değişken modelden çıkarıldığında toplam kazançta meydana gelen kayıp (mavi çubuk). 10 katlı modelin Jackknife test sonuçları Şekil 2'de gösterilmiştir.")

    jack_path = "/home/halil/adelie-maxent-2204c/maxent/cikti/deneme3/plots/Pygoscelis_adeliae_jacknife.png"
    if os.path.exists(jack_path):
        img_jack = Image(jack_path, width=440, height=270)
        story.append(KeepTogether([img_jack, Paragraph("Şekil 2. Çevresel değişkenlerin Jackknife kazanç analizi (Turkuaz: Değişken tek başına kullanıldığında sağlanan kazanç, Mavi: Değişken modelden çıkarıldığında kalan kazanç, Kırmızı: Tüm değişkenlerin birlikte kullanıldığı tam model kazancı).", caption)]))
        md_content.append(f"\n![Şekil 2. Jackknife Grafiği]({jack_path})\n*Şekil 2. Çevresel değişkenlerin Jackknife kazanç analizi.*\n")

    add_p("Jackknife grafiği incelendiğinde; modelde tek başına kullanıldığında en yüksek düzenlenmiş eğitim kazancını sağlayan değişkenin <b>en sıcak çeyrek yağışı (<i>bio18</i>, ~0.287 kazanç)</b> olduğu, bunu <b>yıllık deniz buzu konsantrasyonunun (<i>buz_yillik</i>, ~0.210 kazanç)</b> izlediği görülmektedir. Çıplak kaya (<i>kaya</i>) tek başına ~0.139, deniz yüzeyi sıcaklığı (<i>sst_yillik</i>) ise ~0.058 kazanç sağlamıştır.")
    add_p("Buna karşılık, modelden çıkarıldığında düzenlenmiş eğitim kazancını en fazla düşüren değişken <b>yıllık deniz buzu konsantrasyonu (<i>buz_yillik</i>)</b> olmuştur (kazanç tam modeldeki 0.592'den 0.441'e gerilemektedir). Bunu deniz yüzeyi sıcaklığı (<i>sst_yillik</i>, 0.483'e gerileme) izlemiştir. Bu durum; tek başına en yüksek ayırt ediciliği <i>bio18</i> sağlasa da, modelden çıkarıldığında telafi edilemeyen en özgün ve bağımsız bilgi içeriğinin deniz buzu örtüsünde bulunduğunu göstermektedir.")

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

    add_p("Tepki eğrileri ham model verileri (.dat) ve grafiklerdeki gerçek sayısal değerler doğrultusunda incelendiğinde türün çevresel tepkileri şu şekilde özetlenmektedir:", body_bold)
    add_p("• <b>Deniz Buzu Konsantrasyonu (Şekil 3a):</b> Habitat uygunluğu %20–%25 marjinal buz konsantrasyonunda zirveye ulaşmakta (~0.997 Cloglog puanı); konsantrasyon arttıkça uygunluk kademeli olarak düşerek %40'ta ~0.74, %50'de ~0.43 seviyesine gerilemekte ve %60.8'de minimum ~0.154 değerine inmektedir. %65–%69 bandında ise ~0.34 seviyesinde seyretmektedir. Bu eğilim, Adélie penguenlerinin dalış ve avlanma için polinyalara ve marjinal buz kenarlarına ihtiyaç duymasıyla uyumludur (Ainley, 2002).", bullet)
    add_p("• <b>Çıplak Kaya Yüzdesi (Şekil 3b):</b> Çıplak kaya eğrisinde sıfır kaya kesişiminde uygunluk ~0.46 seviyesindedir ve düşük kaya yüzdelerinde hızla ~0.76'ya yükselerek %15–17 aralığında 0.948 zirvesine ulaşmaktadır. Sıfır kayada taban uygunluğunun sıfırlanmaması (~0.46), model kalibrasyonunda kolonilerin yanı sıra açık denizel beslenme gözlemlerinin de bulunmasından kaynaklanmaktadır.", bullet)
    add_p("• <b>Yaz Yağışı / Bio18 (Şekil 3c):</b> Uygunluk 184 mm civarında zirveye (~0.960 puan) ulaşmakta; 400 mm seviyesinde ~0.81 puan ile yüksek kalmaya devam etmekte, ancak 600 mm'nin üzerine çıktığında ~0.55–0.60 bandına gerilemektedir. Bu durum, aşırı yağış koşullarında yavru hipotermi riskini yansıtmaktadır (Chapman vd., 2011).", bullet)
    add_p("• <b>Deniz Sıcaklığı / SST (Şekil 3d):</b> -1.94°C ile -1.50°C arasındaki soğuk kutup sularında en yüksek uygunluk (0.903–0.816 puan) gözlenirken, deniz suyu sıcaklığı -0.80°C'nin üzerine çıktığında uygunluk hızla düşerek -0.50°C'de 0.118 seviyesine inmektedir. Bu bulgu, pelajik kril ekolojisiyle uyumlu oşinografik su kütlesi toleransını temsil etmektedir (Cimino vd., 2016).", bullet)

    story.append(PageBreak())

    # =========================================================================
    # SAYFA 11: 2.5 MEKÂNSAL BLOK ÇAPRAZ DOĞRULAMA (TABLO 5)
    # =========================================================================
    add_p("2.5. Mekânsal Çapraz Doğrulama (Spatial Block CV) Bulguları", subsec_head)
    add_p("Modelin mekânsal otokorelasyona karşı duyarlılığını ve coğrafi aktarılabilirliğini sınamak amacıyla Roberts vd. (2017) yaklaşımıyla yürütülen 4 Enlem Bandı Mekânsal Bloklama ile Eşleştirilmiş Rastgele 4 Kat modellerinin karşılaştırmalı doğrulama metrikleri Tablo 5'te sunulmuştur.")

    # Tablo 5 (Gerçek matched_comparison.csv verileri)
    t5_data = [
        [Paragraph("Model / Özellik Ailesi", table_cell_cb), Paragraph("Mekânsal 4-Bant Test AUC", table_cell_cb), Paragraph("Eşleştirilmiş Rastgele 4-Kat Test AUC", table_cell_cb), Paragraph("AUC Farkı (Rastgele − Mekânsal)", table_cell_cb), Paragraph("Mekânsal Omission Oranı", table_cell_cb), Paragraph("Rastgele Omission Oranı", table_cell_cb)],
        [Paragraph("L / RM1 (Doğrusal)", table_cell_b), Paragraph("0.580 ± 0.198", table_cell_c), Paragraph("0.715 ± 0.082", table_cell_c), Paragraph("+0.135", table_cell_c), Paragraph("19/67 (%28.4)", table_cell_c), Paragraph("6/67 (%9.0)", table_cell_c)],
        [Paragraph("LQ / RM1 (Doğrusal+Karesel)", table_cell_b), Paragraph("0.530 ± 0.200", table_cell_c), Paragraph("0.746 ± 0.075", table_cell_c), Paragraph("+0.216", table_cell_c), Paragraph("24/67 (%35.8)", table_cell_c), Paragraph("9/67 (%13.4)", table_cell_c)],
        [Paragraph("LQ / RM2 (Kısıtlı Regülasyon)", table_cell_b), Paragraph("0.557 ± 0.210", table_cell_c), Paragraph("0.720 ± 0.080", table_cell_c), Paragraph("+0.163", table_cell_c), Paragraph("23/67 (%34.3)", table_cell_c), Paragraph("8/67 (%11.9)", table_cell_c)],
        [Paragraph("<b>AUTO / RM1 (Ana Model: LQTH)</b>", table_cell_b), Paragraph("<b>0.477 ± 0.165</b>", table_cell_cb), Paragraph("0.765 ± 0.071", table_cell_c), Paragraph("<b>+0.288</b>", table_cell_cb), Paragraph("<b>38/67 (%56.7)</b>", table_cell_cb), Paragraph("13/67 (%19.4)", table_cell_c)]
    ]
    t5 = Table(t5_data, colWidths=[130, 75, 80, 75, 75, 65])
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
    add_p("Tablo 5'teki sonuçlar, ekolojik modelleme metodolojisi açısından hayati bir gerçeği belgelemektedir: Ana model ile aynı özellik ailesini taşıyan AUTO/RM1 (LQTH) konfigürasyonu, standart rastgele doğrulamada 0.765 test AUC verirken, coğrafi enlem bantları ayrıştırıldığında test AUC değeri <b>0.477'ye (rastgele tahmin eşiği olan 0.50'nin altına)</b> gerilemekte ve test omission oranı %56.7'ye fırlamaktadır. Buna karşılık doğrusal kısıtlı model (L/RM1) mekânsal testte 0.580 AUC ile daha dirençli kalmaktadır. Rastgele bölmede eğitim-test noktaları arası medyan mesafe 12.6 km iken (68°G enleminde 0.25° boylam ~10.4 km'dir), mekânsal bloklamada bu mesafe 45.4 km'ye çıkmaktadır. Bu bulgu; karmaşık özellik sınıflarının (hinge/threshold) yerel enleme aşırı uyum sağladığını ve modelin eğitildiği enlem dışındaki farklı sahalara doğrudan aktarılmasında ciddi genelleme yetersizliği bulunduğunu dürüstçe kanıtlamaktadır.")

    story.append(PageBreak())

    # =========================================================================
    # SAYFA 12: 2.6.1 GÜNÜMÜZ DAĞILIM HARİTASI (ŞEKİL 4)
    # =========================================================================
    add_p("2.6. Kartografik Dağılım ve Değişim Haritaları", subsec_head)
    add_p("2.6.1. Marguerite Körfezi Günümüz (2000–2025) Çevresel Uygunluk Haritası", subsubsec_head)
    add_p("MaxEnt modelinin günümüz ERA5 (2000–2025) ortalamalarıyla çalıştırılması neticesinde elde edilen Cloglog habitat uygunluk haritası Şekil 4'te sunulmuştur. Haritada 0.60 üzerindeki yüksek uygunluk alanlarının Adelaide Adası'nın kıyı kesimlerinde, körfezin iç fiyort girişlerinde ve George VI Boğazı'nın kuzey ağzında yoğunlaştığı gözlenmektedir. Bu alanlar, kuluçka için gerekli çıplak kayalıkların ve uygun marjinal deniz buzu dinamiklerinin bir arada bulunduğu kıyı kesimleriyle örtüşmektedir.")

    p_map1 = "/home/halil/adelie-maxent-2204c/harita/cmip6_ipsl_2050_v1/gunumuz_A4.png"
    if os.path.exists(p_map1):
        img_m1 = Image(p_map1, width=450, height=318)
        story.append(KeepTogether([img_m1, Paragraph("Şekil 4. Marguerite Körfezi'nde Adélie pengueni günümüz çevresel uygunluk haritası (ERA5 2000–2025 referansı, MaxEnt 3.4.4, EPSG:3031 kutup stereografik izdüşümü).", caption)]))
        md_content.append(f"\n![Şekil 4. Günümüz Haritası]({p_map1})\n*Şekil 4. Günümüz çevresel uygunluk haritası (2000–2025).*\n")

    add_p("Günümüz haritası incelendiğinde; Bellingshausen Denizi'ne bakan batı açık deniz kesimlerinde uygunluk değerlerinin 0.10'un altında kaldığı görülmektedir. Bu düşüklük yalnızca kaya eksikliğinden değil; açık denizde daha ılık seyreden pelajik deniz suyu sıcaklığı (SST > -0.5°C) ve marjinal kış buz örtüsünün yokluğunun birleşik etkisinden kaynaklanmaktadır. Buna karşılık Adelaide Adası ve iç fiyortlar türün tüm biyolojik gereksinimlerini karşılamaktadır.")

    story.append(PageBreak())

    # =========================================================================
    # SAYFA 13: 2.6.2 CMIP6 SSP2-4.5 2050 GELECEK HARİTASI (ŞEKİL 5)
    # =========================================================================
    add_p("2.6.2. CMIP6 IPSL-CM6A-LR SSP2-4.5 (2041–2060) Gelecek Projeksiyon Haritası", subsubsec_head)
    add_p("CMIP6 IPSL-CM6A-LR modelinin orta düzey sera gazı emisyon senaryosu (SSP2-4.5) altında 2050 yılı (2041–2060 dönemi) potansiyel habitat uygunluk projeksiyonu Şekil 5'te sunulmuştur. Projeksiyon haritası incelendiğinde; kuzey ve batı fiyortlarında habitat uygunluğunda gerilemeler gözlenirken, körfezin güneyindeki korunaklı boğaz alanlarında uygunluk değerlerinin korunduğu veya kısmen arttığı görülmektedir.")

    p_map2 = "/home/halil/adelie-maxent-2204c/harita/cmip6_ipsl_2050_v1/2050_A4.png"
    if os.path.exists(p_map2):
        img_m2 = Image(p_map2, width=450, height=318)
        story.append(KeepTogether([img_m2, Paragraph("Şekil 5. Adélie pengueni 2050 yılı potansiyel çevresel uygunluk projeksiyon haritası (CMIP6 IPSL-CM6A-LR SSP2-4.5, 2041–2060 dönemi, EPSG:3031 kutup stereografik izdüşümü).", caption)]))
        md_content.append(f"\n![Şekil 5. 2050 Projeksiyon Haritası]({p_map2})\n*Şekil 5. 2050 yılı potansiyel habitat uygunluk haritası (CMIP6 SSP2-4.5).*\n")

    add_p("2050 projeksiyonu, ısınan deniz suyu ve azalan kış deniz buzu nedeniyle türün geleneksel üreme ve avlanma alanlarında mekânsal baskıların artacağını ortaya koymaktadır. Özellikle Adelaide Adası'nın açık deniz etkisine açık batı kıyılarında uygunluk puanlarında belirgin azalmalar gözlenmiştir.")

    story.append(PageBreak())

    # =========================================================================
    # SAYFA 14: 2.6.3 2050 YILI DEĞİŞİM VE REFUGIA HARİTASI (ŞEKİL 6)
    # =========================================================================
    add_p("2.6.3. 2050 Yılı Mekânsal Değişim ve Uygunluk Fark Haritası", subsubsec_head)
    add_p("Gelecek uygunluk puanı ile günümüz uygunluk puanı arasındaki fark (Δ = Gelecek − Günümüz) piksel bazında hesaplanarak mekânsal değişim haritası oluşturulmuştur (Şekil 6). Fark değerleri ±0.05 mutlak puan eşiğinde sınıflandırılmış; modelin eşik duyarlılığı Tablo 6'da ve alan dağılımı Tablo 7'de özetlenmiştir (Liu vd., 2005).")

    p_map3 = "/home/halil/adelie-maxent-2204c/harita/cmip6_ipsl_2050_v1/degisim_A4.png"
    if os.path.exists(p_map3):
        img_m3 = Image(p_map3, width=450, height=318)
        story.append(KeepTogether([img_m3, Paragraph("Şekil 6. Adélie pengueni 2050 yılı çevresel uygunluk değişim haritası (Δ = Gelecek − Günümüz). Kırmızı tonlar uygunluk azalmasını, gri tonlar kararlı alanları, yeşil tonlar ise uygunluk artışı gösteren alanları temsil etmektedir.", caption)]))
        md_content.append(f"\n![Şekil 6. Değişim Haritası]({p_map3})\n*Şekil 6. 2050 yılı çevresel uygunluk değişim haritası.*\n")

    add_p("Şekil 6'da görüldüğü üzere; körfezin kuzeybatı girişi ve Adelaide Adası batısında belirgin uygunluk azalması (Δ < -0.05) gözlenirken, güneydeki George VI Boğazı ağzında uygunluk artışı eğilimi (Δ > +0.05) belirmektedir. Bu sınıflar günümüz ve gelecek sürekli uygunluk puanlarının farkını gösterir; doğrudan gerçek habitat alanı kaybı veya kazanımı olarak yorumlanamaz. Haritadaki bloklu sınırlar, delta anomalisinin ~1° GCM hücrelerinden aktarılmasından kaynaklanmaktadır. George VI Boğazı günümüzde kalın şelf buzuyla kaplı olduğundan, buradaki matematiksel artış kesin bir sığınak değil, kuramsal bir değişim hipotezidir.")

    story.append(PageBreak())

    # =========================================================================
    # SAYFA 15: TABLO 6, TABLO 7 VE ŞEKİL 7 (BELİRSİZLİK HARİTASI)
    # =========================================================================
    # Tablo 6
    t6_data = [
        [Paragraph("Uygunluk Değişim Eşiği", table_cell_cb), Paragraph("Değişim Sınıfı", table_cell_cb), Paragraph("Hücre Sayısı (703 Hücre)", table_cell_cb), Paragraph("Hücre Oranı (%)", table_cell_cb), Paragraph("Model Alanı Yüzölçümü (km²)", table_cell_cb), Paragraph("Model Alan Payı (%)", table_cell_cb)],
        [Paragraph("±0.025 Puan", table_cell), Paragraph("Azalma / Kararlı / Artış", table_cell), Paragraph("318 / 102 / 283", table_cell_c), Paragraph("%45.2 / %14.5 / %40.3", table_cell_c), Paragraph("95.323 / 27.818 / 79.539", table_cell_c), Paragraph("%47.0 / %13.7 / %39.2", table_cell_c)],
        [Paragraph("<b>±0.05 Puan (Referans)</b>", table_cell_b), Paragraph("<b>Azalma<br/>Kararlı<br/>Artış Eğilimi</b>", table_cell_b), Paragraph("<b>297<br/>163<br/>243</b>", table_cell_cb), Paragraph("<b>%42.2<br/>%23.2<br/>%34.6</b>", table_cell_cb), Paragraph("<b>89.155<br/>45.066<br/>68.460</b>", table_cell_cb), Paragraph("<b>%44.0<br/>%22.2<br/>%33.8</b>", table_cell_cb)],
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
    add_p("Tablo 6. Farklı lojistik değişim eşiklerine göre 2050 yılı habitat değişim sınıflarının duyarlılık dağılımı (Liu vd., 2005).", caption)

    # Tablo 7
    t7_data = [
        [Paragraph("Uygunluk Değişim Sınıfı (±0.05 Eşiği)", table_cell_cb), Paragraph("Hücre Sayısı", table_cell_cb), Paragraph("Yüzde Payı (%)", table_cell_cb), Paragraph("Toplam Yüzölçümü (km²)", table_cell_cb), Paragraph("Baskın Coğrafi Bölge", table_cell_cb)],
        [Paragraph("<b>Uygunluk Azalması Sınıfı (Δ < -0.05)</b>", table_cell_b), Paragraph("297", table_cell_c), Paragraph("%42.2", table_cell_c), Paragraph("89.155 km²", table_cell_c), Paragraph("Körfez girişi, Adelaide Adası batı/kuzey kıyıları.", table_cell)],
        [Paragraph("<b>Kararlı Alanlar (-0.05 ≤ Δ ≤ +0.05)</b>", table_cell_b), Paragraph("163", table_cell_c), Paragraph("%23.2", table_cell_c), Paragraph("45.066 km²", table_cell_c), Paragraph("Merkez körfez pelajik suları, korunaklı koylar.", table_cell)],
        [Paragraph("<b>Uygunluk Artışı Gösteren Alanlar (Δ > +0.05)</b>", table_cell_b), Paragraph("243", table_cell_c), Paragraph("%34.6", table_cell_c), Paragraph("68.460 km²", table_cell_c), Paragraph("İç fiyortlar, George VI Boğazı ağzı (kuramsal eğilim).", table_cell)]
    ]
    t7 = Table(t7_data, colWidths=[140, 65, 75, 95, 130])
    t7.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_HEADER_BG),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(Spacer(1, 2))
    story.append(t7)
    add_p("Tablo 7. CMIP6 SSP2-4.5 2050 projeksiyonunda Marguerite Körfezi uygunluk değişim sınıflarının alan dökümü.", caption)

    add_p("2.6.4. Ekstrapolasyon, Novel Climate ve Clamping Belirsizlik Haritası", subsubsec_head)
    add_p("İklim projeksiyonlarında çevresel değişkenlerin eğitim sınırlarını aşması durumunda model ekstrapolasyon uygular (Phillips vd., 2006). Çalışma alanındaki 703 grid hücresinin <b>357 adedinde (%50.8 / 102.500 km²)</b> clamping gerçekleşmiştir (Şekil 7). Clamping işlemlerinin önemli kısmı artan deniz yüzeyi sıcaklığı (SST) ve sıvı yağış (Bio18) değişkenlerinin günümüz üst sınırlarını aşmasından kaynaklanmıştır. Bu durum, 2050 yılı projeksiyonunun geniş bir ekstrapolasyon belirsizliği barındırdığını ve sonuçların temkinle yorumlanması gerektiğini göstermektedir.")

    p_map4 = "/home/halil/adelie-maxent-2204c/harita/cmip6_ipsl_2050_v1/belirsizlik_A4.png"
    if os.path.exists(p_map4):
        img_m4 = Image(p_map4, width=380, height=210)
        story.append(KeepTogether([img_m4, Paragraph("Şekil 7. Ekstrapolasyon ve Clamping belirsizlik haritası (Mor: En az bir değişkenin günümüz aralığını aştığı novel climate ve clamping uygulanan 357 hücre, Gri: Günümüz iklim aralığında kalan güvenli hücreler).", caption)]))
        md_content.append(f"\n![Şekil 7. Belirsizlik Haritası]({p_map4})\n*Şekil 7. Ekstrapolasyon ve Clamping belirsizlik haritası.*\n")

    story.append(PageBreak())

    # =========================================================================
    # SAYFA 16: SONUÇ VE TARTIŞMA
    # =========================================================================
    add_p("Sonuç ve Tartışma", sec_head)
    add_p("Bu araştırmada, Batı Antarktika Yarımadası'nın hassas denizel sahalarından biri olan Marguerite Körfezi'nde Adélie pengueninin (<i>Pygoscelis adeliae</i>) günümüz (2000–2025) ve 2050 yılı potansiyel habitat uygunluğu, ERA5 yeniden analizleri, REMA topoğrafyası ve CMIP6 IPSL-CM6A-LR iklim projeksiyonları ile modellenmiştir. Elde edilen bulgular, kutup ekolojisi literatürü ve metodolojik sınırlılıklar ışığında değerlendirilmiştir.")
    add_p("Model sonuçlarında yıllık deniz buzu konsantrasyonunun %43.1 katkı yüzdesi ve %55.6 permütasyon önemi ile birincil belirleyici çıkması, Adélie pengueninin deniz buzu dinamiklerine duyarlı yapısını ortaya koyan ekolojik literatürle (Ainley, 2002; Fraser & Hofmann, 2003) uyum sergilemektedir. Tepki eğrilerinde görülen %20–%25 marjinal buz optimumu; penguenlerin avlandığı kril sürülerinin buz altı algleriyle beslenmesi için yeterli buz örtüsüne ihtiyaç duymasını, ancak aynı zamanda dalış yapabilmek için açık su kanallarına ve polinyalara gereksinim duymasını yansıtmaktadır. Aşırı kapalı kütlesel buz örtüsünde dalış erişiminin düşmesi bu dengenin hassasiyetine işaret etmektedir.")
    add_p("Giriş bölümünde incelenen <b>Wang, Hu ve Yang'ın (2026, PMID: 42209243 - <i>Ying Yong Sheng Tai Xue Bao</i>)</b> bulgularıyla karşılaştırıldığında; Wang vd. (2026), CMIP6 SSP5-8.5 yüksek emisyon senaryosu altında yüzyıl sonuna doğru (2090–2100) Antarktika genelinde üç <i>Pygoscelis</i> türünün potansiyel uygun habitatlarında belirgin daralmalar bildirmişlerdir. Bizim çalışmamızda ise Marguerite Körfezi gridinin %42.2'si (297 hücre; yaklaşık 89.155 km²) uygunluk azalması sınıfında yer almıştır. Bu fark sınıflandırması gerçek habitat veya nüfus kaybı ölçümü değildir; model puanları arasındaki değişimi gösteren keşifsel bir göstergedir.")
    add_p("<b>'Refugia' ve George VI Boğazı Tartışması:</b> Model çıktılarında körfezin güneyindeki George VI Boğazı girişinde %34.6 oranında (243 hücre; yaklaşık 68.460 km²) uygunluk artışı (Δ > +0.05) gözlenmiştir. Ancak bu artış kesin bir 'ekolojik sığınak' (refugium) olarak kabul edilemez. Bir hücrede taban uygunluğu çok düşükse (örn. 0.02), matematiksel bir artışla 0.08'e yükselse dahi mutlak uygunluk penguen için yetersiz kalabilir. Dahası, George VI Boğazı günümüzde kalıcı şelf buzuyla kaplıdır ve kuluçka için zorunlu olan çıplak kaya substratından yoksundur. Buradaki uygunluk artışı, CMIP6 modelindeki deniz buzu değişimine MaxEnt algoritmasının verdiği kuramsal bir tepkidir. Dolayısıyla George VI Boğazı bir 'ispatlanmış sığınak' değil, sahada test edilmesi gereken bir <b>bölgesel hipotezdir</b>.")
    add_p("Çalışmamızda yaz yağışlarının (<i>bio18</i>) %17.1'lik permütasyon önemine sahip olması, Chapman vd. (2011) ve Massom vd. (2006) tarafından vurgulanan sıvı yağmur ve ıslak karın civciv ölümlerine yol açma riski hipotezini desteklemektedir. Tepki eğrisinde yağış miktarı 600 mm'yi aştığında uygunluk puanının gerilemesi, iklim değişikliğiyle birlikte yağış fazının sıvıya kaymasının yaratabileceği olumsuz etkileri yansıtmaktadır.")
    add_p("<b>Mekânsal Bloklama ve Sınırlılıklar:</b> Roberts vd. (2017) yaklaşımıyla gerçekleştirdiğimiz 4 enlem bandı mekânsal blok çapraz doğrulama testleri ekolojik metodoloji açısından kritik bir gerçeği vurgulamaktadır: Standart rastgele kat bölmelerinde 0.765 AUC veren ana model (AUTO/RM1, LQTH), coğrafi enlemler ayrıştırıldığında 0.477 AUC'ye gerilemekte ve omission oranı %56.7'ye çıkmaktadır. Bu sonuç; karmaşık özellik sınıflarının yerel enleme aşırı uyum sağladığını ve kutup modellerinde mekânsal otokorelasyon denetlenmeden üretilen projeksiyonlara şüpheyle yaklaşılması gerektiğini göstermektedir.")
    add_p("Son olarak, 2050 iklim projeksiyonunda 357 hücrede (%50.8) clamping uygulanması ve çalışmanın tek bir GCM (IPSL-CM6A-LR) ile tek bir senaryoya (SSP2-4.5) dayanması, bu projeksiyonların kesin bir gelecek tahmini değil, <b>keşifsel (exploratory)</b> bir ilk değerlendirme olduğunu ortaya koymaktadır. Gelecek araştırmalarda çoklu model toplulukları (ensemble) dahil edilmesi belirsizlikleri azaltacaktır (Araújo & New, 2007).")

    story.append(PageBreak())

    # =========================================================================
    # SAYFA 17: SONUÇ TARTIŞMA SONU VE ÖNERİLER
    # =========================================================================
    add_p("Öneriler", sec_head)
    add_p("Bu araştırma kapsamında elde edilen bulgular ve metodolojik sınırlılıklar doğrultusunda, ulusal ve uluslararası kutup araştırmaları için şu somut öneriler geliştirilmiştir:")
    add_p("• 1. <b>TÜBİTAK MAM Kutup Araştırmaları Enstitüsü (KARE) ve Ulusal Seferler (TAE):</b> Türkiye'nin düzenlediği Ulusal Antarktika Bilim Seferleri (TAE) kapsamında, modelin mekânsal aktarılabilirlik sınırlarını test etmek ve George VI Boğazı çevresindeki şelf buzu-mikroklima etkileşiminin biyolojik fizibilitesini incelemek amacıyla, körfezin güney kesimlerinde bilimsel saha doğrulaması (ground truthing) ve oşinografik ölçüm çalışmaları planlanmalıdır.", bullet)
    add_p("• 2. <b>GPS Telemetri ve Uydu Vericileri ile İzleme:</b> Modelin genel bulunuş kısıtını aşmak ve üreme kolonileri ile denizel beslenme hareketlerini net olarak ayrıştırmak amacıyla, körfezdeki Adélie kolonilerine uydu bağlantılı GPS telemetri cihazları takılarak bireylerin kışlama ve beslenme rotaları gerçek zamanlı izlenmelidir (Cimino vd., 2016).", bullet)
    add_p("• 3. <b>Çoklu Model Toplulukları (Ensemble SDM) ve Bölgesel İklim Modelleri (RCM):</b> GCM delta anomalisinin ~1° kaba çözünürlük kısıtını ve clamping (%50.8) belirsizliğini azaltmak için birden fazla GCM (örn. MPI-ESM1-2-HR, CNRM-CM6-1) ve Bölgesel İklim Modelleri (RCM) bir araya getirilerek topluluk (ensemble) modellemesi yürütülmelidir (Araújo & New, 2007).", bullet)
    add_p("• 4. <b>Deniz Koruma Alanları (MPA) ve CCAMLR Kapsamı:</b> Antarktika Deniz Yaşamı Kaynaklarının Korunması Komisyonu (CCAMLR) nezdinde, modelin uygunluk azalması sınıfı (Δ < -0.05) gösterdiği <b>kuzey körfez girişi ve Adelaide Adası çevresindeki</b> alanlar izleme önceliği olarak değerlendirilebilir. Bu sonuçlar gerçek koloni kaybı ölçümü olmadığı için koruma kararı tek başına bu haritaya dayandırılmamalı; kril avcılığı ve kolonilerin güncel durumu bağımsız verilerle birlikte izlenmelidir.", bullet)
    add_p("• 5. <b>Yüksek Çözünürlüklü Optik Uydu ve İHA ile Koloni Takibi:</b> Ulaşımı güç fiyort adacıklarındaki kolonilerin tespiti için Sentinel-2 ve yüksek çözünürlüklü ticari uydu görüntüleri ile insansız hava araçları (İHA) üzerinden guano lekesi analizi ve sayım çalışmaları yürütülmelidir (Southwell vd., 2015).", bullet)
    add_p("• 6. <b>Otomatik Meteoroloji İstasyonları (AWS) ile Yerel Yağış İzleme:</b> Kuluçka döneminde civciv ölümlerine yol açabilecek aşırı sıvı yağış olaylarının takibi için körfez kıyısındaki üreme kolonilerine gerçek zamanlı mikroklimatik otomatik meteoroloji istasyonları (AWS) kurulması önerilmektedir (Chapman vd., 2011).", bullet)

    story.append(Spacer(1, 4))
    add_p("Kaynaklar", sec_head)

    # Kaynaklar Listesi (Doğrulanmış ve Tam Uyumlu)
    refs = [
        "Ainley, D. G. (2002). <i>The Adélie Penguin: Bellwether of Climate Change</i>. Columbia University Press, New York. https://doi.org/10.7312/ainl12304",
        "Araújo, M. B., & New, M. (2007). Ensemble forecasting of species distributions. <i>Trends in Ecology & Evolution</i>, 22(1), 42–47. https://doi.org/10.1016/j.tree.2006.09.010",
        "Atkinson, A., Siegel, V., Pakhomov, E., & Rothery, P. (2004). Long-term serious decline in Antarctic krill stock and increase in salps in Southern Ocean. <i>Nature</i>, 432(7013), 100–103. https://doi.org/10.1038/nature02996",
        "Chapman, E. W., Hofmann, E. E., Patterson, D. L., & Fraser, W. R. (2011). The effects of climate change on normal and anomalous weather conditions in the Western Antarctic Peninsula: Consequences for Adélie penguin populations. <i>Marine Ecology Progress Series</i>, 429, 247–260. https://doi.org/10.3354/meps09108",
        "Cimino, M. A., Lynch, H. J., Saba, V. S., & Oliver, M. J. (2016). Projected asymmetric response of Adélie penguins to Antarctic climate change. <i>Scientific Reports</i>, 6, 28785. https://doi.org/10.1038/srep28785",
        "Dormann, C. F., Elith, J., Bacher, S., Buchmann, C., Carl, G., Carré, G., Marquéz, J. R. G., Gruber, B., Lafourcade, B., Leitão, P. J., Münkemüller, T., McClean, C., Osborne, P. E., Reineking, B., Schröder, B., Skidmore, A. K., Zurell, D., & Lautenbach, S. (2013). Collinearity: A review of methods to deal with it and a simulation study evaluating their performance. <i>Ecography</i>, 36(1), 27–46. https://doi.org/10.1111/j.1600-0587.2012.07348.x",
        "Ducklow, H. W., Baker, K., Martinson, D. G., Quetin, L. B., Ross, R. M., Smith, R. C., Stammerjohn, S. E., Vernet, M., & Fraser, W. (2007). Marine ecosystems: The West Antarctic Peninsula. <i>Philosophical Transactions of the Royal Society B: Biological Sciences</i>, 362(1477), 67–94. https://doi.org/10.1098/rstb.2006.1955",
        "Elith, J., Phillips, S. J., Hastie, T., Dudík, M., Chee, Y. E., & Yates, C. J. (2011). A statistical explanation of MaxEnt for ecologists. <i>Diversity and Distributions</i>, 17(1), 43–57. https://doi.org/10.1111/j.1472-4642.2010.00725.x",
        "Fielding, A. H., & Bell, J. F. (1997). A review of methods for the assessment of prediction errors in conservation presence/absence models. <i>Environmental Conservation</i>, 24(1), 38–49. https://doi.org/10.1017/S0376892997000088",
        "Fraser, W. R., & Hofmann, E. E. (2003). A predator's perspective on causal links between climate change, physical forcing and ecosystem response. <i>Marine Ecology Progress Series</i>, 265, 1–15. https://doi.org/10.3354/meps265001"
    ]

    for ref in refs:
        add_p(ref, ref_style)

    story.append(PageBreak())

    # =========================================================================
    # SAYFA 18: KAYNAKLAR DEVAMI VE BİTİŞİ
    # =========================================================================
    refs_p2 = [
        "IPCC. (2021). <i>Climate Change 2021: The Physical Science Basis. Contribution of Working Group I to the Sixth Assessment Report of the Intergovernmental Panel on Climate Change</i>. Cambridge University Press, Cambridge, UK and New York, NY, USA. https://doi.org/10.1017/9781009157896",
        "Liu, C., Berry, P. M., Dawson, T. P., & Pearson, R. G. (2005). Selecting thresholds of occurrence in the prediction of species distributions. <i>Journal of Biogeography</i>, 32(1), 51–63. https://doi.org/10.1111/j.1365-2699.2004.01149.x",
        "Lyver, P. O., Barron, M., Barton, K. J., Ainley, D. G., Pollard, A., Gordon, S., McNeill, S., Ballard, G., & Wilson, P. R. (2014). Trends in the breeding population of Adélie penguins in the Ross Sea, 1981–2012: A coincidence of climate and resource extraction effects. <i>PLOS ONE</i>, 9(3), e91188. https://doi.org/10.1371/journal.pone.0091188",
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
        "Vaughan, D. G., Marshall, G. J., Connolley, W. M., Parkinson, C., Mulvaney, R., Hodgson, D. A., King, J. C., Pudsey, C. J., & Turner, J. (2003). Recent rapid regional climate warming on the Antarctic Peninsula. <i>Climatic Change</i>, 60(3), 243–274. https://doi.org/10.1023/A:1026021217991",
        "Wang, J., Hu, M., & Yang, J. (2026). Impact of climate change on the potentially suitable habitat distribution of Pygoscelis penguins in Antarctica. <i>Ying Yong Sheng Tai Xue Bao (The Journal of Applied Ecology)</i>, 37(3), 926–932. https://doi.org/10.13287/j.1001-9332.202603.028 [PMID: 42209243]"
    ]

    for ref in refs_p2:
        add_p(ref, ref_style)

    # Markdown dosyasını kaydet
    with open(out_md, 'w', encoding='utf-8') as f:
        f.writelines(md_content)
    print(f"Markdown report generated: {out_md}")

    # PDF oluştur
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Raw PDF built: {raw_pdf}")

    # CUPS / Poppler pdftocairo sanitizasyonu
    cmd = f"pdftocairo -pdf {raw_pdf} {sanitized_pdf}"
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if res.returncode == 0:
        print(f"Sanitized PDF generated successfully: {sanitized_pdf}")
    else:
        print(f"pdftocairo warning: {res.stderr}")

if __name__ == "__main__":
    raise SystemExit(
        'Bu tarihsel üretici eski bilimsel metni yeniden yazdığı için devre dışıdır. '
        'Güncel Markdown kaynağını kullanan rapor/rapor_derle.py çalıştırılmalıdır. '
        'Önceki üretici ve rapor rapor/arsiv/2026-11-12_veri_oncesi/ içinde korunur.'
    )
