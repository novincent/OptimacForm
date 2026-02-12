import seaborn as sns
from statannotations.Annotator import Annotator
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu
from statsmodels.stats.multitest import multipletests


action_names = [["as_usual","monthly","weekly"],["monthly","notatall","weekly"]]
methods = ["optimac","random","roundrobin","highestrank"]
method_colors = {
    "optimac": "#1f77b4",
    "highestrank": "#ff7f0e",
    "random": "#2ca02c",
    "roundrobin": "#d62728"
}
hatch_before = ""
hatch_after = "/"


def plotting_ba_bars(scenario,stats_before,stats_after,title,ylabel):
    #Function generating before/after dropout simulation bar plots
    categories = action_names[scenario]
    x = np.arange(len(categories))
    total_width = 0.8
    n_methods = len(methods)
    bar_width = total_width / (2 * n_methods)  # Each method has 2 bars: before & after

    fig, ax = plt.subplots(figsize=(14, 7))

    for idx, method in enumerate(methods):
        mean_before, std_before = stats_before[method]
        mean_after, std_after = stats_after[method]

        offsets = x + (idx - n_methods / 2) * 2 * bar_width + bar_width / 2
        color = method_colors[method]

        # Before bars
        ax.bar(offsets - bar_width / 2, mean_before, bar_width, yerr=std_before,
            label=f'{method} - Before', capsize=4, color=color, hatch=hatch_before, alpha=0.8)

        # After bars
        ax.bar(offsets + bar_width / 2, mean_after, bar_width, yerr=std_after,
            label=f'{method} - After', capsize=4, color=color, hatch=hatch_after, alpha=0.8)

    # --- Formatting with larger fonts ---
    ax.set_xticks(x)
    ax.set_xticklabels(categories, rotation=30, fontsize=18)
    ax.set_ylabel(ylabel, fontsize=16)
    ax.set_title(title, fontsize=15)
    ax.tick_params(axis='y', labelsize=14)
    ax.grid(axis='y', linestyle='--', alpha=0.5)

    # Legend with bigger font
    ax.legend(loc='center left', bbox_to_anchor=(1.02, 0.5), fontsize=14)

    plt.tight_layout(rect=[0, 0.05, 1, 1])
    plt.show()



def plot_violins(xs,title,ylabel,ylim = (0,0.4)):
    data = []
    for name in methods:
        for r in xs[name]:
            data.append({'Algorithm': name, 'Data': r})


    df_ratios = pd.DataFrame(data)
    # --- Plot violin plots ---
    plt.figure(figsize=(16, 10))
    ax = sns.violinplot(data=df_ratios, x='Algorithm', y="Data", hue='Algorithm', inner='quart', palette=method_colors, legend=False)
    ax.tick_params(axis='y', labelsize=16)
    ax.set_xlabel("", fontsize=20)
    ax.set_xticklabels(methods, fontsize=18)
    ax.set_ylim(ylim)
    ax.set_ylabel(ylabel, fontsize=20)
    plt.ylim(ylim)  # Set y-axis limits
    #fig.legend(handles=legend_patches, title="Algorithm", loc='upper left', fontsize=20)

    # --- Define pairs for testing ---
    pairs = [(methods[i],methods[j]) for i in range(len(methods)) for j in range(i+1,len(methods))]

    # --- Compute p-values manually ---
    pvals = []
    for g1, g2 in pairs:
        x1 = df_ratios[df_ratios['Algorithm'] == g1]['Data']
        x2 = df_ratios[df_ratios['Algorithm'] == g2]['Data']
        stat, p = mannwhitneyu(x1, x2, alternative='two-sided')
        if np.isnan(p):
            p = 0
        print(p,type(p))
        pvals.append(p)

    # --- Apply Holm correction ---
    reject, pvals_corr, _, _ = multipletests(pvals, method='holm')

    # --- Annotate the plot ---
    annotator = Annotator(ax, pairs, data=df_ratios, x='Algorithm', y='Data')
    annotator.configure(fontsize=28)  # Set the size of the asterisks
    annotator.set_pvalues(pvals_corr).annotate()

    # --- Print results ---
    print("\nSignificant differences (Holm-corrected Mann-Whitney U-tests):")
    for (g1, g2), pval_corr, is_sig in zip(pairs, pvals_corr, reject):
        if is_sig:
            print(f" - {g1} vs {g2}: Significant (p = {pval_corr})")
        else:
            print(f" - {g1} vs {g2}: Not significant (p = {pval_corr})")

    # --- Final touches ---
    plt.title(title, fontsize=20)
    plt.tight_layout()
    plt.grid(True, axis='y', linestyle='-', alpha=0.5)
    plt.show()

