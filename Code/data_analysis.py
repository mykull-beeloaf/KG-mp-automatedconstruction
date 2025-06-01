from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
import tikzplotlib

if __name__ == "__main__":

    gemma3_mp_results = [5/13, 12/35, 5/17, 8/22, 20/41, 14/35, 12/27]
    gemma3_nomp_results = [12/29, 8/27, 14/28, 12/24, 22/43, 19/36, 11/29]
    llama3_2_mp_results = [6/19, 11/27, 8/24, 11/30, 14/35, 11/21, 7/23]
    llama3_2_nomp_results = [8/27, 7/34, 7/23, 8/22, 9/23, 14/45, 11/30]
    llama3_3_mp_results = [5/9, 13/26, 12/20, 12/19, 21/34, 23/36, 15/24]
    llama3_3_nomp_results = [7/13, 16/30, 15/25, 12/18, 24/36, 25/54, 18/28]
    res = [gemma3_mp_results, gemma3_nomp_results, llama3_2_mp_results, llama3_2_nomp_results, llama3_3_mp_results, llama3_3_nomp_results]

    mp_res = np.concatenate([gemma3_mp_results, llama3_2_mp_results, llama3_3_mp_results])
    nomp_res = np.concatenate([gemma3_nomp_results, llama3_2_nomp_results, llama3_3_nomp_results])

    differences = mp_res - nomp_res
    mean_diff = np.mean(differences)
    std_diff = np.std(differences, ddof=1)
    t_statistic, two_sided_pvalue = stats.ttest_rel(mp_res, nomp_res)
    # If mean_diff > 0, the one-sided p-value is simply two_sided_pvalue / 2
    one_sided_pvalue = two_sided_pvalue / 2 if mean_diff > 0 else 1 - two_sided_pvalue / 2

    print(one_sided_pvalue)

    papers = np.arange(1, 8)

    # gemma3
    plt.figure()
    plt.plot(papers, gemma3_mp_results, marker='o', label='gemma3_mp')
    plt.plot(papers, gemma3_nomp_results, marker='s', label='gemma3_nomp')
    plt.xlabel('Paper Index')
    plt.ylabel('Accuracy')
    plt.title('Accuracy Comparison: gemma3 mp vs nomp')
    plt.legend()
    plt.grid(True)
    #plt.show()

    tikzplotlib.save("plotsg3.tex")

    # llama3_2
    plt.figure()
    plt.plot(papers, llama3_2_mp_results, marker='o', label='llama3_2_mp')
    plt.plot(papers, llama3_2_nomp_results, marker='s', label='llama3_2_nomp')
    plt.xlabel('Paper Index')
    plt.ylabel('Accuracy')
    plt.title('Accuracy Comparison: llama3_2 mp vs nomp')
    plt.legend()
    plt.grid(True)
    #plt.show()

    tikzplotlib.save("plotsll32.tex")

    # llama3_3
    plt.figure()
    plt.plot(papers, llama3_3_mp_results, marker='o', label='llama3_3_mp')
    plt.plot(papers, llama3_3_nomp_results, marker='s', label='llama3_3_nomp')
    plt.xlabel('Paper Index')
    plt.ylabel('Accuracy')
    plt.title('Accuracy Comparison: llama3_3 mp vs nomp')
    plt.legend()
    plt.grid(True)
    #plt.show()

    tikzplotlib.save("plotsll33.tex")

    # Histogram of paired differences
    plt.figure()
    plt.hist(differences, bins=8, edgecolor='black')
    plt.axvline(0, color='red', linestyle='--', label='Zero Difference')
    plt.xlabel('mp - nomp')
    plt.ylabel('Frequency')
    plt.title(f'Histogram of Paired Differences\nOne-sided p-value = {one_sided_pvalue:.3f}')
    plt.legend()
    plt.grid(True)
    #plt.show()

    tikzplotlib.save("plotshist.tex")

    # Boxplot of mp vs nomp accuracies
    plt.figure()
    plt.boxplot([mp_res, nomp_res], tick_labels=['mp', 'nomp'])
    plt.ylabel('Accuracy')
    plt.title(f'Boxplot of mp vs nomp\nOne-sided p-value = {one_sided_pvalue:.3f}')
    plt.grid(True)
    #plt.show()

    tikzplotlib.save("plots.tex")