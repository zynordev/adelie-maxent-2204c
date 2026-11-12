"""Export scientific diagnostic figures from completed revision experiments."""
import csv
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]


def main():
    out=ROOT/'maxent/cikti/revizyon_20261112/figures'
    out.mkdir(exist_ok=True)
    rows=list(csv.DictReader((ROOT/'maxent/cikti/revizyon_20261112/comparison_v3/summary.csv').open()))
    candidates=['L_RM1','LQ_RM1','LQ_RM2','LQH_RM1','LQH_RM2','coordinates_reference','distance_null']
    schemes=list(dict.fromkeys(r['scheme'] for r in rows))
    fig,axs=plt.subplots(1,2,figsize=(13,5),layout='constrained')
    for ax,predictors in zip(axs,['annual','seasonal_no_sst']):
        values=np.array([[float(next(r['auc_mean'] for r in rows if r['predictors']==predictors and
                    r['scheme']==s and r['candidate']==c)) for s in schemes] for c in candidates])
        im=ax.imshow(values,vmin=.45,vmax=.9,cmap='viridis',aspect='auto')
        ax.set_xticks(range(len(schemes)),schemes,rotation=45,ha='right',fontsize=8)
        ax.set_yticks(range(len(candidates)),candidates,fontsize=9)
        ax.set_title('Yıllık değişkenler' if predictors=='annual' else 'Üreme dönemi buzu; SST çıkarılmış')
        for i in range(len(candidates)):
            for j in range(len(schemes)):ax.text(j,i,f'{values[i,j]:.2f}',ha='center',va='center',fontsize=8,
                                                color='black' if values[i,j]>.76 else 'white')
    fig.colorbar(im,ax=axs,label='Ayrılmış test bölgesinde varlık–arka plan AUC',shrink=.8)
    fig.suptitle('Coğrafi referansa karşı sınama | 61 bulunuş hücresi | Model seçilmedi')
    fig.savefig(out/'spatial_null_comparison.png',dpi=180)
    fig.savefig(out/'spatial_null_comparison.pdf')
    plt.close(fig)
    rows=list(csv.DictReader((ROOT/'maxent/cikti/revizyon_20261112/projection_IPSL/model_metrics.csv').open()))
    fig,ax=plt.subplots(figsize=(10,5),layout='constrained')
    x=np.arange(5);w=.22
    for j,(predictors,color) in enumerate([('annual','#255f85'),('seasonal_no_sst','#bd6c35')]):
        values=[float(next(r['delta_mean_presence_resubstitution'] for r in rows if r['predictors']==predictors and
                    r['candidate']==c)) for c in candidates[:5]]
        ax.bar(x+(j-.5)*w,values,width=w,color=color,label=predictors)
    ax.axhline(0,color='black',lw=.7);ax.set_xticks(x,candidates[:5]);ax.legend()
    ax.set_ylabel('Varlık hücrelerinde ortalama Δ uygunluk puanı')
    ax.set_title('IPSL tek-GCM denemesi: model yapısı değişim yönünü değiştirebiliyor')
    fig.supxlabel('Tam veriyle eğitilmiş genel bulunuş modelleri; bağımsız doğrulama veya nüfus değişimi değildir',fontsize=9)
    fig.savefig(out/'structural_delta_sensitivity.png',dpi=180)
    fig.savefig(out/'structural_delta_sensitivity.pdf')
    plt.close(fig)


if __name__=='__main__':main()
