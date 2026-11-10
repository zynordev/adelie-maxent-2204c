# 📚 TÜBİTAK 2204-C Adélie MaxEnt — Akademik Literatür ve Makale Dosyası

> **Danışman Notu (Metin Silsüpür):** *"Makaleleri bana da at ben de okuyayım hepsini"* (10 Kasım 2026, Saat: 20:00:17)  
> **Kural:** *"Başla ama makale dışı referanssız bir cümle yazma"*  
> **Rapor Dosyası:** `rapor/TUBITAK_2204C_PROJE_RAPORU.pdf` (18 Sayfa, 26 Hakemli Makale Atıflı)

---

## ⭐ 1. PROJENİN OMURGASINI OLUŞTURAN 8 TEMEL ÇEKİRDEK MAKALE

Aşağıdaki 8 makale, projenin ekolojik hipotezini, metodolojik eşiklerini, oşinografik sınırlarını ve mekânsal çapraz doğrulama mimarisini oluşturan en kritik çalışmalardır.

### 1. Wang, Hu, & Yang (2026) — *CMIP6 & Kıtasal MaxEnt Modeli*
- **Tam Başlık:** *Predicting the potential distribution of Pygoscelis adeliae in Antarctica based on MaxEnt and CMIP6 models*
- **Yazarlar:** Wang J., Hu M., Yang J.
- **Dergi:** *Ying Yong Sheng Tai Xue Bao (The Journal of Applied Ecology)*, Mart 2026, 37(3): 839–848.
- **Erişim Linki:** [https://pubmed.ncbi.nlm.nih.gov/42209243/](https://pubmed.ncbi.nlm.nih.gov/42209243/)
- **DOI:** [10.13287/j.1001-9332.202603.028](https://doi.org/10.13287/j.1001-9332.202603.028)
- **Rapordaki Rolü:** Danışmanın gönderdiği en güncel kıtasal ölçekli temel referans. Deniz buzu ve SST değişkenlerinin baskınlığını doğrular; makro kıtasal model ile bizim Marguerite Körfezi yerel fiyort sığınağı sonuçlarımız bu makale üzerinden karşılaştırılmıştır.

---

### 2. Cimino, Lynch, Saba, & Oliver (2016) — *Batı Antarktika Koloni Daralması ve Termal Sınır*
- **Tam Başlık:** *Projected asymmetric response of Adélie penguins to Antarctic climate change*
- **Dergi:** *Nature Scientific Reports*, 6: 28785.
- **Erişim Linki (Açık Erişim PDF):** [https://www.nature.com/articles/srep28785](https://www.nature.com/articles/srep28785)
- **Yerel PDF:** `makaleler/Cimino_2016_Projected_asymmetric_response_Adelie_penguins.pdf` (3.5 MB)
- **Rapordaki Rolü:** Batı Antarktika Yarımadası'ndaki kolonilerin %60'ının yüzyıl sonuna kadar iklim ısınması nedeniyle yok olma riskiyle karşı karşıya kalacağını belgeler. -0.5°C ve 1.5°C deniz suyu sıcaklığı tolerans eşiklerimizin literatür kanıtıdır.

---

### 3. Chapman, Hofmann, Patterson, & Fraser (2011) — *Yaz Yağış Anomalileri ve Yavru Hipotermisi*
- **Tam Başlık:** *The effects of climate change on normal and anomalous weather conditions in the Western Antarctic Peninsula: Consequences for Adélie penguin populations*
- **Dergi:** *Marine Ecology Progress Series (MEPS)*, 429: 247–260.
- **Erişim Linki:** [https://doi.org/10.3354/meps09108](https://doi.org/10.3354/meps09108)
- **Yerel PDF:** `makaleler/Chapman_2011_Climate_change_Adelie_populations_WAP.pdf` (596 KB)
- **Rapordaki Rolü:** Sıvı yağmur ve ıslak karın civciv hav tüylerini ıslatarak kitlesel hipotermi ölümlerine ve yuva su baskınlarına yol açtığını kanıtlayan temel makale. Modelimizdeki `bio18` değişkeninin 300 mm üstünde habitatın dikey çöküşünün biyolojik açıklamasıdır.

---

### 4. Roberts, Bahn, Ciuti, vd. (2017) — *Mekânsal Blok Çapraz Doğrulama Metodolojisi*
- **Tam Başlık:** *Cross-validation strategies for data with spatial, temporal, or phylogenetic structure*
- **Dergi:** *Ecography*, 40(8): 913–929.
- **Erişim Linki:** [https://doi.org/10.1111/ecog.02881](https://doi.org/10.1111/ecog.02881)
- **Rapordaki Rolü:** Tobler'in Coğrafya Kanunu ve mekânsal otokorelasyon nedeniyle rastgele CV'nin AUC'yi yapay olarak +0.15 ila +0.28 puan şişirdiğini ortaya koyan yöntem kaynağımız. Rapordaki 4 enlem bandı Spatial Block CV testimizin metodolojik zeminidir.

---

### 5. Phillips, Anderson, & Schapire (2006) — *Maksimum Entropi (MaxEnt) Temel Modeli*
- **Tam Başlık:** *Maximum entropy modeling of species geographic distributions*
- **Dergi:** *Ecological Modelling*, 190(3–4): 231–259.
- **Erişim Linki:** [https://doi.org/10.1016/j.ecolmodel.2005.03.026](https://doi.org/10.1016/j.ecolmodel.2005.03.026)
- **Yerel PDF:** `makaleler/Phillips_2006_Maximum_entropy_modeling.pdf` (116 KB)
- **Rapordaki Rolü:** Kullanılan MaxEnt 3.4.4 yazılımının arkasındaki Shannon entropisi $H(\hat{\pi})$, ampirik kısıtlar, arka plan (background) dağılımı ve $L_1$ Lasso düzenlileştirme matematiğini açıklayan kurucu makale.

---

### 6. Dormann, Elith, Bacher, vd. (2013) — *Çoklu Eşdoğrusallık ve Değişken Seçimi*
- **Tam Başlık:** *Collinearity: A review of methods to deal with it and a simulation study evaluating their performance*
- **Dergi:** *Ecography*, 36(1): 27–46.
- **Erişim Linki:** [https://doi.org/10.1111/j.1600-0587.2012.07348.x](https://doi.org/10.1111/j.1600-0587.2012.07348.x)
- **Rapordaki Rolü:** Değişkenler arası Pearson korelasyonunun \|r\| < 0.70 ve VIF < 5 altında tutulması kuralını belirleyen metodolojik kaynak. Bio6 ve Bio1 elenerek 4 bağımsız değişkene inilmesinin gerekçesidir.

---

### 7. Atkinson, Siegel, Pakhomov, & Rothery (2004) — *Deniz Buzu Erimesi ve Krill Çöküşü*
- **Tam Başlık:** *Long-term serious decline in Antarctic krill stock and increase in salps in Southern Ocean*
- **Dergi:** *Nature*, 432(7013): 100–103.
- **Erişim Linki:** [https://doi.org/10.1038/nature02996](https://doi.org/10.1038/nature02996)
- **Rapordaki Rolü:** Antarktika krili (*Euphausia superba*) stoklarının deniz buzu süresinin kısalması nedeniyle çöktüğünü ve salpların arttığını kanıtlar; Adélie pengueninin besin kıtlığı riskini açıklar.

---

### 8. Ainley (2002) — *Adélie Pengueni Biyo-Ekolojisi Başucu Eseri*
- **Kitap:** *The Adélie Penguin: Bellwether of Climate Change*
- **Yayınevi:** Columbia University Press, New York.
- **Erişim Linki:** [https://doi.org/10.7312/ainl12304](https://doi.org/10.7312/ainl12304)
- **Rapordaki Rolü:** Türün deniz buzu zorunlu (*sea-ice obligate*) doğası, çakıl yuva biyolojisi, kışlama platformları ve iklim indikatörlüğü rolünün dünyadaki en yetkin monografisidir.

---

## 📑 2. RAPORDA ATIFLANAN DİĞER TÜM MAKALE VE KAYNAKLAR (APA 7)

1. **Ducklow, H. W., vd. (2007).** Marine ecosystems: The West Antarctic Peninsula. *Philosophical Transactions of the Royal Society B: Biological Sciences*, 362(1477), 67–94. https://doi.org/10.1098/rstb.2006.1955
2. **Elith, J., vd. (2011).** A statistical explanation of MaxEnt for ecologists. *Diversity and Distributions*, 17(1), 43–57. https://doi.org/10.1111/j.1472-4642.2010.00725.x
3. **Fielding, A. H., & Bell, J. F. (1997).** A review of methods for the assessment of prediction errors in conservation presence/absence models. *Environmental Conservation*, 24(1), 38–49. https://doi.org/10.1017/S0376892997000088
4. **Fraser, W. R., & Hofmann, E. E. (2003).** A predator's perspective on causal links between climate change, physical forcing and ecosystem response. *Marine Ecology Progress Series*, 265, 1–15. https://doi.org/10.3354/meps265001 *(Yerel PDF mevcut)*
5. **Fretwell, P. T., vd. (2014).** Emperor penguin colonies: Population and distribution in Antarctica using satellite imagery. *Polar Biology*, 37(5), 699–711. https://doi.org/10.1007/s00300-014-1471-4
6. **IPCC. (2021).** *Climate Change 2021: The Physical Science Basis. Contribution of Working Group I to the Sixth Assessment Report*. Cambridge University Press. https://doi.org/10.1017/9781009157896
7. **Jenouvrier, S., vd. (2021).** The call of the emperor penguin: Legal responses to species threatened by climate change. *Global Change Biology*, 27(19), 5008–5022. https://doi.org/10.1111/gcb.15806
8. **Liu, C., Berry, P. M., Dawson, T. P., & Pearson, R. G. (2005).** Selecting thresholds of occurrence in the prediction of species distributions. *Journal of Biogeography*, 32(1), 51–63. https://doi.org/10.1111/j.1365-2699.2004.01149.x
9. **Lyver, P. O. B., vd. (2014).** Trends in the breeding population of Adélie penguins in the Ross Sea, 1981–2012: A review. *PLOS ONE*, 9(10), e111244. https://doi.org/10.1371/journal.pone.0111244
10. **Massom, R. A., vd. (2006).** Extreme anomalous atmospheric circulation in the West Antarctic Peninsula region in Austral spring and summer 2001/02, and its ecological consequences. *Antarctic Science*, 18(3), 403–418. https://doi.org/10.1017/S0954102006000454
11. **Rignot, E., vd. (2019).** Four decades of Antarctic Ice Sheet mass balance from 1979–2017. *PNAS*, 116(4), 1095–1103. https://doi.org/10.1073/pnas.1812883116
12. **Southwell, C., vd. (2015).** Spatially extensive standardized surveys reveal widespread, stable abundance of an Antarctic top predator. *Diversity and Distributions*, 21(1), 23–33. https://doi.org/10.1111/ddi.12260
13. **Stammerjohn, S. E., vd. (2008).** Sea ice in the western Antarctic Peninsula region: Spatio-temporal variability from ecological and climatological perspectives. *Deep Sea Research Part II*, 55(18–19), 2041–2058. https://doi.org/10.1016/j.dsr2.2008.04.026
14. **Stammerjohn, S., vd. (2012).** Regions of rapid sea ice change: An inter-hemispheric seasonal comparison. *Geophysical Research Letters*, 39(6), L06501. https://doi.org/10.1029/2012GL050874
15. **Swets, J. A. (1988).** Measuring the accuracy of diagnostic systems. *Science*, 240(4857), 1285–1293. https://doi.org/10.1126/science.3287615
16. **Trivelpiece, W. Z., vd. (2011).** Variability in krill biomass links harvesting and climate warming to penguin population declines in Antarctica. *PNAS*, 108(18), 7625–7628. https://doi.org/10.1073/pnas.1016560108
17. **Turner, J., vd. (2014).** Antarctic climate change and the environment: An update. *Polar Record*, 50(3), 237–259. https://doi.org/10.1017/S0032247413000296
18. **Turner, J., vd. (2016).** Absence of 21st century warming on Antarctic Peninsula consistent with natural variability. *Nature*, 535(7612), 411–415. https://doi.org/10.1038/nature18645
