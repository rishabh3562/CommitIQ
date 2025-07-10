import io
import matplotlib
matplotlib.use("Agg")
import networkx as nx
import matplotlib.pyplot as plt
def plot_influence_graph(commit_data: list):
    G = nx.DiGraph()

    # Build influence edges (naive file-time proximity)
    for i, c1 in enumerate(commit_data):
        a1, f1, t1 = c1["author"], set(c1["files"]), c1["timestamp"]
        for j in range(i + 1, len(commit_data)):
            a2, f2, t2 = commit_data[j]["author"], set(commit_data[j]["files"]), commit_data[j]["timestamp"]
            if a1 != a2 and f1 & f2 and (t2 - t1).total_seconds() < 3 * 24 * 3600:
                G.add_edge(a1, a2)

    pos = nx.spring_layout(G, seed=42)
    fig, ax = plt.subplots(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color="skyblue", edge_color="gray", node_size=2000, font_size=10)
    ax.set_title("Influence Graph")
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png")
    buf.seek(0)
    return {"influence_graph.png": buf}

def plot_stats(stats):
    authors = list(stats.keys())
    commits = [v["commits"] for v in stats.values()]
    lines   = [v.get("lines_added",0) for v in stats.values()]

    fig, axs = plt.subplots(2, 2, figsize=(12, 8))

    # 1) Influence map (horizontal bar)
    axs[0,0].barh(authors, commits)
    axs[0,0].set_title("Commits by Author")

    # 2) LOC contribution (pie)
    axs[0,1].pie(lines, labels=authors, autopct="%1.1f%%")
    axs[0,1].set_title("LOC Contribution")

    # 3) Commit trend (line)
    axs[1,0].plot(range(len(commits)), commits, marker="o")
    axs[1,0].set_title("Commit Trend")

    # 4) MTTR vs Lead Time (if passed via stats; else blank)
    axs[1,1].axis("off")

    fig.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    return buf.getvalue()

def plot_individual_graphs(stats: dict) -> dict:
    import io
    import warnings
    warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")
    import matplotlib.pyplot as plt
    authors = list(stats.keys())
    commits = [v["commits"] for v in stats.values()]
    lines = [v.get("lines_added", 0) for v in stats.values()]
    
    buffers = {}

    # 1. Commits by Author (barh)
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    ax1.barh(authors, commits)
    ax1.set_title("Commits by Author")
    fig1.tight_layout()
    buf1 = io.BytesIO()
    fig1.savefig(buf1, format="png")
    buf1.seek(0)
    buffers["commits_by_author.png"] = buf1

    # 2. LOC Contribution (improved pie chart)
    total_lines = sum(lines)
    data = sorted(zip(authors, lines), key=lambda x: x[1], reverse=True)
    main_labels, main_sizes = [], []
    other_total = 0
    threshold = 0.02 * total_lines  # 2%

    for author, size in data:
        if size >= threshold:
            main_labels.append(author)
            main_sizes.append(size)
        else:
            other_total += size

    if other_total > 0:
        main_labels.append("Others")
        main_sizes.append(other_total)

    fig2, ax2 = plt.subplots(figsize=(8, 8))
    ax2.pie(main_sizes, labels=main_labels, autopct="%1.1f%%", startangle=140, textprops={'fontsize': 9})
    ax2.set_title("Lines of Code Contribution (Grouped)")
    fig2.tight_layout()
    buf2 = io.BytesIO()
    fig2.savefig(buf2, format="png")
    buf2.seek(0)
    buffers["loc_contribution.png"] = buf2

    # 3. Commit Trend (line chart)
    fig3, ax3 = plt.subplots(figsize=(10, 5))
    ax3.plot(range(len(commits)), commits, marker="o")
    ax3.set_xticks(range(len(authors)))
    ax3.set_xticklabels(authors, rotation=45, ha="right")
    ax3.set_title("Commit Trend")
    fig3.tight_layout()
    buf3 = io.BytesIO()
    fig3.savefig(buf3, format="png")
    buf3.seek(0)
    buffers["commit_trend.png"] = buf3

    return buffers


def plot_commit_trends(daily_counts: dict[str, list[int]]) -> dict:
    """
    daily_counts: { author: [counts_per_day…] }
    """
    buffers = {}
    for author, counts in daily_counts.items():
        fig, ax = plt.subplots(figsize=(8,2))
        ax.plot(counts, marker="o")
        ax.set_title(f"{author} — Commits per Day")
        ax.set_xlabel("Day")
        ax.set_ylabel("Commits")
        ax.grid(True)
        fig.tight_layout()

        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        buf.seek(0)
        buffers[f"{author}_trend.png"] = buf
    return buffers