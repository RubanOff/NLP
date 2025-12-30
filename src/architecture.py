import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch

def add_box(ax, xy, w, h, text, fontsize=9):
    rect = Rectangle(xy, w, h, fill=False, linewidth=1.4)
    ax.add_patch(rect)
    ax.text(
        xy[0] + w / 2,
        xy[1] + h / 2,
        text,
        ha="center",
        va="center",
        fontsize=fontsize,
        wrap=True,
    )

def arrow(ax, start, end):
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle="->",
            mutation_scale=12,
            linewidth=1.2,
        )
    )

fig, ax = plt.subplots(figsize=(11, 5))
ax.set_xlim(0, 12)
ax.set_ylim(0, 6)
ax.axis("off")

w_user, h_user = 2.3, 1.0
w_ctrl, h_ctrl = 2.6, 1.0
w_mem, h_mem = 2.4, 1.0
w_pr, h_pr = 1.7, 1.0
w_llm, h_llm = 1.7, 0.95
w_pii, h_pii = 2.6, 0.85

pos_user = (0.6, 2.6)
pos_ctrl = (3.2, 2.6)
pos_pii = (3.2, 1.2)
pos_prof = (6.2, 3.7)
pos_vec = (6.2, 1.8)
pos_pr = (9.0, 2.6)
pos_llm = (9.0, 4.15)

resp_w, resp_h = 2.0, 0.8
pos_resp = (0.6, 5.05)

add_box(ax, pos_user, w_user, h_user, "Пользователь\nсообщение $x_t$", fontsize=10)
add_box(ax, pos_ctrl, w_ctrl, h_ctrl, "Memory Controller\n(LLM-extractor)\n• profile Δ\n• facts", fontsize=9)
add_box(ax, pos_pii, w_pii, h_pii, "Фильтр PII\n(regex/Luhn)\nблокирует SENSITIVE", fontsize=8.5)
add_box(ax, pos_prof, w_mem, h_mem, "Структурированный\nпрофиль $M_{struct}$\n(JSON/Pydantic)", fontsize=9)
add_box(ax, pos_vec, w_mem, h_mem, "Векторная память\n$M_{vec}$\n(ChromaDB)", fontsize=9)
add_box(ax, pos_pr, w_pr, h_pr, "Сборка\nпромпта", fontsize=9.5)
add_box(ax, pos_llm, w_llm, h_llm, "LLM-агент\nгенерация $y_t$", fontsize=9.5)
add_box(ax, pos_resp, resp_w, resp_h, "Ответ $y_t$", fontsize=10)

def rc(pos, w, h):
    return (pos[0] + w, pos[1] + h / 2)

def lc(pos, w, h):
    return (pos[0], pos[1] + h / 2)

def tc(pos, w, h):
    return (pos[0] + w / 2, pos[1] + h)

def bc(pos, w, h):
    return (pos[0] + w / 2, pos[1])

arrow(ax, rc(pos_user, w_user, h_user), lc(pos_ctrl, w_ctrl, h_ctrl))
arrow(ax, rc(pos_ctrl, w_ctrl, h_ctrl), lc(pos_prof, w_mem, h_mem))
arrow(ax, rc(pos_ctrl, w_ctrl, h_ctrl), lc(pos_vec, w_mem, h_mem))

arrow(ax, bc(pos_ctrl, w_ctrl, h_ctrl), tc(pos_pii, w_pii, h_pii))
arrow(ax, rc(pos_pii, w_pii, h_pii), lc(pos_vec, w_mem, h_mem))

arrow(ax, rc(pos_prof, w_mem, h_mem), lc(pos_pr, w_pr, h_pr))
arrow(ax, rc(pos_vec, w_mem, h_mem), lc(pos_pr, w_pr, h_pr))

arrow(ax, tc(pos_pr, w_pr, h_pr), bc(pos_llm, w_llm, h_llm))

start = tc(pos_llm, w_llm, h_llm)
end = rc(pos_resp, resp_w, resp_h)

ax.add_patch(
    FancyArrowPatch(
        start,
        end,
        arrowstyle="->",
        mutation_scale=12,
        linewidth=1.2,
        connectionstyle="angle3,angleA=90,angleB=180",
    )
)

out_path = "profile_rag_architecture_final.png"
plt.tight_layout(pad=0.5)
plt.savefig(out_path, dpi=240)
plt.show()
plt.close(fig)
