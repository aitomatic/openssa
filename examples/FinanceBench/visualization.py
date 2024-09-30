import numpy as np
import matplotlib.pyplot as plt


# Define the categories
categories = ['0-RETRIEVE', '1-COMPARE', '2-CALC-CHANGE',
              '3-CALC-COMPLEX', '4-CALC-AND-JUDGE', '5-EXPLAIN-FACTORS', '6-OTHER-ADVANCED']


# Create angles for the plot
N = len(categories)
angles = [n / float(N) * 2 * np.pi for n in range(N)]
# Calculate radii for each difficulty level with increased dynamic range
max_radius = 10
radii = [max_radius * (1 + i * 0.8) for i in range(N)]
# Define percentage zones and colors for background
percentages = [0.25, 0.5, 0.75, 1.0]
colors = ['#FFF3E0', '#FFE0B2', '#FFCC80', '#FFB74D']


# Accuracy Data
accuracy_llamaindex_rag = [71, 83, 78, 30, 14, 70, 43]
accuracy_langchain_react = [85, 90, 69, 88, 60, 70, 37]
accuracy_openai_assistant = [49, 46, 36, 40, 14, 50, 46]
accuracy_openssa_dana = [95, 90, 93, 100, 94, 100, 89]

# Consistency Data
consistency_llamaindex_rag = [96, 90, 100, 87, 88, 60, 100]
consistency_langchain_react = [86, 91, 78, 84, 68, 60, 66]
consistency_openai_assistant = [76, 65, 87, 73, 72, 100, 77]
consistency_openssa_dana = [96, 97, 87, 100, 92, 100, 94]


# Function to plot the data
def plot_data(ax, data, color, label=None):
    values = data
    r = [radius * value / 100 for radius, value in zip(radii, values)]
    ax.plot(angles + [angles[0]], r + [r[0]], 'o-', linewidth=2, label=label, color=color)
    ax.fill(angles + [angles[0]], r + [r[0]], color=color, alpha=0.25)


# Create the figure and two subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 10), subplot_kw={'projection': 'polar'})


# Function to set up the polar plot (background, grid, labels)
def setup_polar_plot(ax, title):
    # Remove grid and spines
    ax.grid(False)
    ax.spines['polar'].set_visible(False)
    # Plot radial lines (terminating at 100%)
    for angle, radius in zip(angles, radii):
        ax.plot([angle, angle], [0, radius], color='gray', linestyle='-', linewidth=0.5, alpha=0.5)
    # Plot percentage lines and fill background
    for i, percentage in enumerate(percentages):
        r = [radius * percentage for radius in radii]
        theta = np.linspace(0, angles[-1], 1000)
        spiral_r = np.interp(theta, angles, r)
        ax.plot(theta, spiral_r, color='gray', linestyle='--', linewidth=0.5, alpha=0.7)
        if i > 0:
            ax.fill(angles + [angles[0]], r + [r[0]], colors[i], alpha=0.1)
    # Add full category labels without rotation
    for i, category in enumerate(categories):
        angle = angles[i]
        r = radii[i] * 1.15
        ha = 'left' if -np.pi / 2 <= angle < np.pi / 2 else 'right'
        ax.text(angle, r, category, ha=ha, va='center', fontsize=10, fontweight='bold')
    # Remove radial labels and ticks
    ax.set_yticks([])
    ax.set_yticklabels([])
    ax.set_xticks([])
    ax.set_xticklabels([])
    # Set the ylim to ensure all labels are visible
    ax.set_ylim(0, max(radii) * 1.3)
    # Set title for the chart
    ax.set_title(title, y=0.75, fontsize=14, fontweight='bold')


# Set up both subplots
setup_polar_plot(ax1, "AGENT ACCURACY")
setup_polar_plot(ax2, "AGENT CONSISTENCY")

# Plot accuracy data on the first subplot with labels for the legend
plot_data(ax1, accuracy_llamaindex_rag, 'red', 'LlamaIndex RAG')
plot_data(ax1, accuracy_langchain_react, 'yellow', 'LangChain ReAct')
plot_data(ax1, accuracy_openai_assistant, 'blue', 'OpenAI Assistant')
plot_data(ax1, accuracy_openssa_dana, 'green', 'OpenSSA DANA-NK-NP')

# Plot consistency data on the second subplot without labels to avoid duplicate legend
plot_data(ax2, consistency_llamaindex_rag, 'red')
plot_data(ax2, consistency_langchain_react, 'yellow')
plot_data(ax2, consistency_openai_assistant, 'blue')
plot_data(ax2, consistency_openssa_dana, 'green')

# Adjust space between subplots
plt.subplots_adjust(wspace=-0.4)

# Add a single legend closer to the plots
fig.legend(loc='lower center', bbox_to_anchor=(0.5, 0), fontsize=12, ncol=4)
plt.tight_layout()
plt.savefig('agent_comparison.pdf', bbox_inches='tight')
