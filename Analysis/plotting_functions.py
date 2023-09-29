# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 14:00:57 2023

@author: Liad
"""


def plot_tf_resp(
    resp,
    ts,
    quiet,
    active,
    testedVar,
    tf,
    sf,
    contrast,
    ori,
    n,
    reqSf=[0.08],
    reqTf=[2],
    reqOri=[0, 90, 180, 270],
    reqContrast=[1],
):
    tvu = np.unique(testedVar)
    tfu = np.unique(tf)
    sfu = np.unique(sf)
    cu = np.unique(contrast)
    oriu = np.unique(ori)
    oriu = oriu[np.isin(oriu, reqOri)]

    # make sure tested item is not limited
    if np.array_equal(tf, testedVar):
        reqTf = tfu
    if np.array_equal(sf, testedVar):
        reqSf = sfu
    if np.array_equal(contrast, testedVar):
        reqContrast = cu

    f, ax = plt.subplots(len(tvu), len(oriu), sharex=True, sharey=True)
    ax = np.atleast_2d(ax)
    for tfi, tfl in enumerate(tvu):
        for orii, oril in enumerate(oriu):
            Inds = np.where(
                (testedVar == tfl)
                & (ori == oril)
                & (np.isin(sf, reqSf))
                & (np.isin(tf, reqTf))
                & (np.isin(ori, reqOri))
                & (np.isin(contrast, reqContrast))
            )[0]
            respQ = sp.ndimage.gaussian_filter1d(
                resp[:, np.intersect1d(Inds, quiet), n], 1.5, axis=0
            )
            respA = sp.ndimage.gaussian_filter1d(
                resp[:, np.intersect1d(Inds, active), n], 1.5, axis=0
            )

            ax[-1, orii].set_xlabel(f"time\nOri: {oril}")
            ax[tfi, 0].set_ylabel(f"var: {tfl}\ndf/f")
            m = np.nanmean(respQ, 1)
            sd = sp.stats.sem(respQ, 1)
            ax[tfi, orii].plot(
                ts,
                m,
                "b",
            )
            ax[tfi, orii].fill_between(
                ts, m - sd, m + sd, facecolor="b", alpha=0.2
            )
            m = np.nanmean(respA, 1)
            sd = sp.stats.sem(respA, 1)
            ax[tfi, orii].plot(
                ts,
                m,
                "r",
            )
            ax[tfi, orii].fill_between(
                ts, m - sd, m + sd, facecolor="r", alpha=0.2
            )
            ax[tfi, orii].spines["right"].set_visible(False)
            ax[tfi, orii].spines["top"].set_visible(False)
            f.set_size_inches(8, 8)
            # plt.tight_layout()
    return f, ax


def plot_summary_plot(
    df, x, y, hue=None, ax=None, line=False, palette=None, color=None
):

    if ax is None:
        f, ax = plt.subplots(1)
    else:
        f = None
    if len(df) == 0:
        return f, ax
    if line:
        sns.lineplot(
            data=df,
            x=x,
            y=y,
            hue=hue,
            ax=ax,
            err_style="bars",
            linestyle="none",
            marker="o",
            palette=palette,
            color=color,
            markerfacecolor=color,
        )
    else:

        sns.pointplot(
            data=df, x=x, y=y, hue=hue, ax=ax, palette=palette, color=color
        )
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    return f, ax


def print_fitting_data(
    gratingRes,
    quietI,
    activeI,
    data,
    paramsOri,
    paramsOriSplit,
    varsOri,
    pvalOri,
    paramsTf,
    paramsTfSplit,
    varsTf,
    pvalTf,
    paramsSf,
    paramsSfSplit,
    varsSf,
    pvalSf,
    n,
    sessionData=None,
    saveDir=None,
):

    save = not (saveDir is None)
    if (save) & (not (sessionData is None)):
        saveDir = os.path.join(
            saveDir, sessionData["Name"], sessionData["Date"]
        )
    if save:
        if not os.path.isdir(saveDir):
            os.makedirs(saveDir)

    dfAll = make_neuron_db(
        gratingRes,
        ts,
        quietI,
        activeI,
        data["gratingsTf"],
        data["gratingsSf"],
        data["gratingsContrast"],
        data["gratingsOri"],
        n,
    )
    ### ORI

    tunerBase = OriTuner("gauss")
    tunerBase.props = paramsOri[:, n]
    tunerSplit = OriTuner("gauss_split")
    tunerSplit.props = paramsOriSplit[:, n]

    df = dfAll[(dfAll.sf == 0.08) & (dfAll.tf == 2) & (dfAll.contrast == 1)]
    f, ax = plt.subplots(2)
    f.suptitle(f"Ori Tuning, Resp p: {np.round(respP[n],3)}")
    f.subplots_adjust(hspace=2)
    ax[0].set_title(
        f"One fit, VE flat: {np.round(varsOri[0,n],3)}, VE model: {np.round(varsOri[1,n],3)}"
    )
    ax[1].set_title(
        f"Separate fit, VE model: {np.round(varsOri[2,n],3)}, pVal dAUC: {np.round(pvalOri[n],3)}"
    )
    sns.lineplot(
        x=np.arange(0, 360, 0.01),
        y=tunerBase.func(np.arange(0, 360, 0.01), *paramsOri[:, n]),
        ax=ax[0],
        color="black",
    )
    plot_summary_plot(df, x="ori", y="avg", line=True, ax=ax[0], color="black")

    # divided
    sns.lineplot(
        x=np.arange(0, 360, 0.01),
        y=tunerSplit.predict_split(np.arange(0, 360, 0.01), 0),
        ax=ax[1],
        color="blue",
    )
    plot_summary_plot(
        df[df.movement == 0],
        x="ori",
        y="avg",
        line=True,
        ax=ax[1],
        color="blue",
    )

    sns.lineplot(
        x=np.arange(0, 360, 0.01),
        y=tunerSplit.predict_split(np.arange(0, 360, 0.01), 1),
        ax=ax[1],
        color="red",
    )
    plot_summary_plot(
        df[df.movement == 1],
        x="ori",
        y="avg",
        line=True,
        ax=ax[1],
        color="red",
    )

    mng = plt.get_current_fig_manager()
    mng.window.showMaximized()
    if save:
        plt.savefig(os.path.join(saveDir, f"{n}_Ori_fit.png"))
        plt.savefig(os.path.join(saveDir, f"{n}_Ori_fit.pdf"))
        plt.close(f)

    #### temporal
    tunerBase = FrequencyTuner("gauss")
    tunerBase.props = paramsTf[:, n]
    tunerSplit = FrequencyTuner("gauss_split")
    tunerSplit.props = paramsTfSplit[:, n]

    df = dfAll[
        (dfAll.sf == 0.08)
        & (dfAll.contrast == 1)
        & (np.isin(dfAll.ori, [0, 90, 180, 270]))
    ]

    df = filter_nonsig_orientations(df, criterion=0.05)

    fittingRange = np.arange(0.5, 16, 0.01)

    f, ax = plt.subplots(2)
    f.suptitle(f"Temporal frequency Tuning, Resp p: {np.round(respP[n],3)}")
    f.subplots_adjust(hspace=2)
    ax[0].set_title(
        f"One fit, VE flat: {np.round(varsTf[0,n],3)}, VE model: {np.round(varsTf[1,n],3)}"
    )
    ax[1].set_title(
        f"Separate fit, VE model: {np.round(varsTf[2,n],3)}, pVal dAUC: {np.round(pvalTf[n],3)}"
    )
    sns.lineplot(
        x=fittingRange,
        y=tunerBase.predict(fittingRange),
        ax=ax[0],
        color="black",
    )
    plot_summary_plot(df, x="tf", y="avg", line=True, ax=ax[0], color="black")

    # divided
    sns.lineplot(
        x=fittingRange,
        y=tunerSplit.predict_split(fittingRange, 0),
        ax=ax[1],
        color="blue",
    )
    plot_summary_plot(
        df[df.movement == 0],
        x="tf",
        y="avg",
        line=True,
        ax=ax[1],
        color="blue",
    )

    sns.lineplot(
        x=fittingRange,
        y=tunerSplit.predict_split(fittingRange, 1),
        ax=ax[1],
        color="red",
    )
    plot_summary_plot(
        df[df.movement == 1], x="tf", y="avg", line=True, ax=ax[1], color="red"
    )

    ax[0].set_xscale("log", base=2)
    ax[1].set_xscale("log", base=2)
    mng = plt.get_current_fig_manager()
    mng.window.showMaximized()
    if save:
        plt.savefig(os.path.join(saveDir, f"{n}_Tf_fit.png"))
        plt.savefig(os.path.join(saveDir, f"{n}_Tf_fit.pdf"))
        plt.close(f)

    ### spatial
    tunerBase = FrequencyTuner("gauss")
    tunerBase.props = paramsSf[:, n]
    tunerSplit = FrequencyTuner("gauss_split")
    tunerSplit.props = paramsSfSplit[:, n]

    df = dfAll[
        (dfAll.tf == 2)
        & (dfAll.contrast == 1)
        & (np.isin(dfAll.ori, [0, 90, 180, 270]))
    ]

    df = filter_nonsig_orientations(df, criterion=0.05)
    f, ax = plt.subplots(2)
    f.suptitle(f"Spatial frequency Tuning, Resp p: {np.round(respP[n],3)}")
    f.subplots_adjust(hspace=2)
    ax[0].set_title(
        f"One fit, VE flat: {np.round(varsSf[0,n],3)}, VE model: {np.round(varsSf[1,n],3)}"
    )
    ax[1].set_title(
        f"Separate fit, VE model: {np.round(varsSf[2,n],3)}, pVal dAUC: {np.round(pvalSf[n],3)}"
    )
    fittingRange = np.arange(0.01, 0.34, 0.01)
    sns.lineplot(
        x=fittingRange,
        y=tunerBase.predict(fittingRange),
        ax=ax[0],
        color="black",
    )
    plot_summary_plot(df, x="sf", y="avg", line=True, ax=ax[0], color="black")

    # divided
    sns.lineplot(
        x=fittingRange,
        y=tunerSplit.predict_split(fittingRange, 0),
        ax=ax[1],
        color="blue",
    )
    plot_summary_plot(
        df[df.movement == 0],
        x="sf",
        y="avg",
        line=True,
        ax=ax[1],
        color="blue",
    )

    sns.lineplot(
        x=fittingRange,
        y=tunerSplit.predict_split(fittingRange, 1),
        ax=ax[1],
        color="red",
    )
    plot_summary_plot(
        df[df.movement == 1], x="sf", y="avg", line=True, ax=ax[1], color="red"
    )

    mng = plt.get_current_fig_manager()
    mng.window.showMaximized()
    ax[0].set_xscale("log", base=2)
    ax[1].set_xscale("log", base=2)
    if save:
        plt.savefig(os.path.join(saveDir, f"{n}_Sf_fit.png"))
        plt.savefig(os.path.join(saveDir, f"{n}_Sf_fit.pdf"))
        plt.close(f)
